#!/usr/bin/env bash
set -euo pipefail

# Cross-agent installer for the cv-review Agent Skill.
# Supports: antigravity, claude, codex (and ~/.agents standard), gemini, cursor, openclaw, grok.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="${SCRIPT_DIR}/.agents/skills/cv-review"

if [[ ! -d "${SOURCE_DIR}" ]]; then
  echo "Error: Skill source directory not found: ${SOURCE_DIR}" >&2
  exit 1
fi

usage() {
  cat <<'EOF'
Usage: ./install.sh [OPTIONS]

Options:
  --all                   Install into all supported global agent directories
  --agent <name>          Install for a specific agent (repeatable or comma-separated):
                          antigravity, claude, codex, gemini, cursor, openclaw, grok
  --project <dir>         Install into a project's .agents/, .claude/, and .grok/ skills dirs
  -h, --help              Show this help message

Without flags, auto-detects installed agents in $HOME and installs cv-review into each.
EOF
}

install_to() {
  local target_dir="$1"
  local label="$2"
  mkdir -p "$(dirname "${target_dir}")"
  rm -rf "${target_dir}"
  cp -R "${SOURCE_DIR}" "${target_dir}"
  echo "  [OK] ${label} -> ${target_dir}"
}

target_for_agent() {
  case "$1" in
    antigravity) echo "${HOME}/.gemini/config/skills/cv-review|Antigravity" ;;
    claude)      echo "${HOME}/.claude/skills/cv-review|Claude Code" ;;
    codex|agents)echo "${HOME}/.agents/skills/cv-review|Codex / AgentSkills Standard (~/.agents)" ;;
    gemini)      echo "${HOME}/.gemini/skills/cv-review|Gemini CLI" ;;
    cursor)      echo "${HOME}/.cursor/skills/cv-review|Cursor" ;;
    openclaw)    echo "${HOME}/.openclaw/skills/cv-review|OpenClaw" ;;
    grok)        echo "${HOME}/.grok/skills/cv-review|Grok Build / Grok Bot" ;;
    *)
      echo "Unknown agent: $1" >&2
      exit 1
      ;;
  esac
}

ALL_AGENTS=(antigravity claude codex gemini cursor openclaw grok)
SELECTED=()
INSTALL_ALL=false
PROJECT_DIR=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --all)
      INSTALL_ALL=true
      shift
      ;;
    --agent|-a)
      IFS=',' read -ra PARTS <<< "${2:-}"
      for p in "${PARTS[@]}"; do
        SELECTED+=("$(echo "$p" | tr '[:upper:]' '[:lower:]' | xargs)")
      done
      shift 2
      ;;
    --project)
      PROJECT_DIR="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -n "${PROJECT_DIR}" ]]; then
  if [[ ! -d "${PROJECT_DIR}" ]]; then
    echo "Error: Project directory not found: ${PROJECT_DIR}" >&2
    exit 1
  fi
  echo "Installing cv-review into project: ${PROJECT_DIR}"
  install_to "${PROJECT_DIR}/.agents/skills/cv-review" "Universal (.agents)"
  install_to "${PROJECT_DIR}/.claude/skills/cv-review" "Claude Code (.claude)"
  install_to "${PROJECT_DIR}/.grok/skills/cv-review"   "Grok (.grok)"
  exit 0
fi

if [[ "${INSTALL_ALL}" == true ]]; then
  SELECTED=("${ALL_AGENTS[@]}")
elif [[ ${#SELECTED[@]} -eq 0 ]]; then
  [[ -d "${HOME}/.gemini/config" ]] && SELECTED+=(antigravity)
  [[ -d "${HOME}/.claude" ]]        && SELECTED+=(claude)
  { [[ -d "${HOME}/.codex" ]] || [[ -d "${HOME}/.agents" ]]; } && SELECTED+=(codex)
  [[ -d "${HOME}/.gemini" ]]        && SELECTED+=(gemini)
  [[ -d "${HOME}/.cursor" ]]        && SELECTED+=(cursor)
  [[ -d "${HOME}/.openclaw" ]]      && SELECTED+=(openclaw)
  [[ -d "${HOME}/.grok" ]]          && SELECTED+=(grok)
  if [[ ${#SELECTED[@]} -eq 0 ]]; then
    SELECTED=(antigravity codex)
  fi
fi

echo "Installing cv-review skill..."
declare -A SEEN=()
for agent in "${SELECTED[@]}"; do
  [[ -n "${SEEN[$agent]:-}" ]] && continue
  SEEN[$agent]=1
  IFS='|' read -r target label <<< "$(target_for_agent "$agent")"
  install_to "${target}" "${label}"
done

echo ""
echo "Done! Start a new session in your agent and ask to evaluate any CV."
