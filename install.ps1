$ErrorActionPreference = "Stop"

$SourceDir = Join-Path $PSScriptRoot ".agents\skills\cv-review"
$TargetBase = Join-Path $HOME ".gemini\config\skills"
$TargetDir = Join-Path $TargetBase "cv-review"

if (-not (Test-Path $SourceDir)) {
    Write-Error "Skill source directory not found: $SourceDir"
}

New-Item -ItemType Directory -Force -Path $TargetBase | Out-Null
if (Test-Path $TargetDir) {
    Remove-Item -Recurse -Force $TargetDir
}
Copy-Item -Recurse -Force -Path $SourceDir -Destination $TargetDir

Write-Host "Installed cv-review skill to: $TargetDir" -ForegroundColor Green
Write-Host "Restart or start a new Antigravity chat and ask to evaluate any CV (PDF, image, or Canva)." -ForegroundColor Cyan
