#!/usr/bin/env bash
set -euo pipefail
# Publish this project to the GitHub user's PUBLIC fork of IBM's starter repo.
# Requires: Git, GitHub CLI; run `gh auth login` first.
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_REPO="ibm-developer-skills-network/oaqjp-final-project-emb-ai"
TARGET_REPO="tdao7/oaqjp-final-project-emb-ai"
command -v gh >/dev/null || { echo 'Install GitHub CLI (gh) first'; exit 1; }
gh auth status >/dev/null
if ! gh repo view "$TARGET_REPO" >/dev/null 2>&1; then
    gh repo fork "$SOURCE_REPO" --clone=false
fi
visibility="$(gh repo view "$TARGET_REPO" --json visibility --jq .visibility)"
if [[ "$visibility" != PUBLIC ]]; then
    echo "ERROR: $TARGET_REPO is not public; make it public before submitting." >&2
    exit 1
fi
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT
git clone "https://github.com/${TARGET_REPO}.git" "$TEMP_DIR/repo"
tar -C "$SOURCE_DIR" --exclude=.git --exclude='*.zip' -cf - . | tar -C "$TEMP_DIR/repo" -xf -
cd "$TEMP_DIR/repo"
git add .
if ! git diff --cached --quiet; then
    git commit -m "Complete Watson emotion detection Flask final project"
    git push origin HEAD:main
fi
printf '
Ready for submission:
'
printf 'Question 1: https://github.com/%s/blob/main/README.md
' "$TARGET_REPO"
printf 'Question 6: https://github.com/%s/blob/main/EmotionDetection/__init__.py
' "$TARGET_REPO"
