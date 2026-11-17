<#
.SYNOPSIS
    Cross-agent installer for the cv-review Agent Skill.
.DESCRIPTION
    Installs cv-review into one or more AI coding agents that support the
    Agent Skills specification (SKILL.md): Antigravity, Claude Code, Codex CLI,
    Gemini CLI, Cursor, OpenClaw, and Grok Build/Bot.
.EXAMPLE
    .\install.ps1
    Auto-detects installed agent directories in $HOME and installs cv-review.
.EXAMPLE
    .\install.ps1 -Agents claude,codex,grok
    Installs specifically for Claude Code, Codex/Agents, and Grok.
.EXAMPLE
    .\install.ps1 -All
    Installs into every supported global agent skill directory.
#>
[CmdletBinding()]
param(
    [string[]]$Agents = @(),
    [switch]$All,
    [string]$ProjectPath = ""
)

$ErrorActionPreference = "Stop"

$SourceDir = Join-Path $PSScriptRoot ".agents\skills\cv-review"
if (-not (Test-Path $SourceDir)) {
    Write-Error "Skill source directory not found: $SourceDir"
}

$AgentMap = [ordered]@{
    antigravity = @{ Probe = (Join-Path $HOME ".gemini\config"); Target = (Join-Path $HOME ".gemini\config\skills\cv-review"); Label = "Antigravity" }
    claude      = @{ Probe = (Join-Path $HOME ".claude");        Target = (Join-Path $HOME ".claude\skills\cv-review");        Label = "Claude Code" }
    codex       = @{ Probe = (Join-Path $HOME ".codex");         Target = (Join-Path $HOME ".agents\skills\cv-review");        Label = "Codex / AgentSkills Standard (~/.agents)" }
    gemini      = @{ Probe = (Join-Path $HOME ".gemini");        Target = (Join-Path $HOME ".gemini\skills\cv-review");        Label = "Gemini CLI" }
    cursor      = @{ Probe = (Join-Path $HOME ".cursor");        Target = (Join-Path $HOME ".cursor\skills\cv-review");        Label = "Cursor" }
    openclaw    = @{ Probe = (Join-Path $HOME ".openclaw");      Target = (Join-Path $HOME ".openclaw\skills\cv-review");      Label = "OpenClaw" }
    grok        = @{ Probe = (Join-Path $HOME ".grok");          Target = (Join-Path $HOME ".grok\skills\cv-review");          Label = "Grok Build / Grok Bot" }
}

function Install-SkillTo([string]$TargetDir, [string]$Label) {
    $Parent = Split-Path -Parent $TargetDir
    New-Item -ItemType Directory -Force -Path $Parent | Out-Null
    if (Test-Path $TargetDir) {
        Remove-Item -Recurse -Force $TargetDir
    }
    Copy-Item -Recurse -Force -Path $SourceDir -Destination $TargetDir
    Write-Host "  [OK] $Label -> $TargetDir" -ForegroundColor Green
}

if ($ProjectPath -ne "") {
    if (-not (Test-Path $ProjectPath)) {
        Write-Error "Project path not found: $ProjectPath"
    }
    Write-Host "Installing cv-review into project: $ProjectPath" -ForegroundColor Cyan
    Install-SkillTo (Join-Path $ProjectPath ".agents\skills\cv-review") "Universal (.agents)"
    Install-SkillTo (Join-Path $ProjectPath ".claude\skills\cv-review") "Claude Code (.claude)"
    Install-SkillTo (Join-Path $ProjectPath ".grok\skills\cv-review")   "Grok (.grok)"
    exit 0
}

$Selected = @()
if ($All) {
    $Selected = @($AgentMap.Keys)
} elseif ($Agents.Count -gt 0) {
    foreach ($item in $Agents) {
        foreach ($token in ($item -split ",")) {
            $key = $token.Trim().ToLowerInvariant()
            if ($key -eq "agents") { $key = "codex" }
            if (-not $AgentMap.Contains($key)) {
                Write-Error "Unknown agent '$token'. Valid options: $($AgentMap.Keys -join ', ')"
            }
            if ($Selected -notcontains $key) { $Selected += $key }
        }
    }
} else {
    foreach ($key in $AgentMap.Keys) {
        if (Test-Path $AgentMap[$key].Probe) {
            $Selected += $key
        }
    }
    if ((Test-Path (Join-Path $HOME ".agents")) -and ($Selected -notcontains "codex")) {
        $Selected += "codex"
    }
    if ($Selected.Count -eq 0) {
        $Selected = @("antigravity", "codex")
    }
}

Write-Host "Installing cv-review skill..." -ForegroundColor Cyan
foreach ($key in $Selected) {
    Install-SkillTo $AgentMap[$key].Target $AgentMap[$key].Label
}
Write-Host "`nDone! Start a new session in your agent and ask to evaluate any CV." -ForegroundColor Cyan
