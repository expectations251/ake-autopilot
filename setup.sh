#!/usr/bin/env bash
set -euo pipefail

echo "==> A.K.E. Setup"
if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI (gh) is required. Install from https://cli.github.com/ then re-run."
  exit 1
fi
if ! command -v git >/dev/null 2>&1; then
  echo "Git is required. Install Git then re-run."
  exit 1
fi

REPO_NAME="ake-autopilot"
if [ -n "${1-}" ]; then REPO_NAME="$1"; fi

echo "Logging into GitHub… (a browser window will open)"
gh auth login -p https -h github.com -w

echo "Creating repo $REPO_NAME (public)…"
gh repo create "$REPO_NAME" --public --confirm

echo "Pushing project…"
git init
git add -A
git commit -m "Initial commit: A.K.E."
git branch -M main
git remote add origin "https://github.com/$(gh api user --jq .login)/$REPO_NAME.git"
git push -u origin main

echo "Enabling GitHub Pages…"
gh api -X PUT repos/{owner}/$REPO_NAME/pages --input - <<'JSON'
{ "build_type": "workflow" }
JSON

echo "Done. Your site will deploy after the first workflow run."
echo "You can trigger it now from the Actions tab: 'AKE Daily Publish' -> Run workflow."
