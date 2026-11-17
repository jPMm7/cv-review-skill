#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="${SCRIPT_DIR}/.agents/skills/cv-review"
TARGET_BASE="${HOME}/.gemini/config/skills"
TARGET_DIR="${TARGET_BASE}/cv-review"

if [[ ! -d "${SOURCE_DIR}" ]]; then
  echo "Error: Skill source directory not found: ${SOURCE_DIR}" >&2
  exit 1
fi

mkdir -p "${TARGET_BASE}"
rm -rf "${TARGET_DIR}"
cp -R "${SOURCE_DIR}" "${TARGET_DIR}"

echo "Installed cv-review skill to: ${TARGET_DIR}"
echo "Start a new Antigravity chat and ask to review any CV (PDF, image, or Canva)."
