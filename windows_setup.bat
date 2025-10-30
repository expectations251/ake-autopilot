@echo off
setlocal ENABLEDELAYEDEXPANSION

echo ==^> A.K.E. Setup (Windows)
where gh >nul 2>nul
if errorlevel 1 (
  echo GitHub CLI (gh) is required. Install from https://cli.github.com/ then re-run.
  exit /b 1
)
where git >nul 2>nul
if errorlevel 1 (
  echo Git is required. Install Git then re-run.
  exit /b 1
)

set REPO_NAME=ake-autopilot
if not "%~1"=="" set REPO_NAME=%~1

echo Logging into GitHub… (a browser window will open)
gh auth login -p https -h github.com -w

echo Creating repo %REPO_NAME% (public)…
gh repo create "%REPO_NAME%" --public --confirm

echo Pushing project…
git init
git add -A
git commit -m "Initial commit: A.K.E."
for /f "tokens=2 delims=: " %%a in ('gh api user --jq .login') do set USER=%%a
git branch -M main
git remote add origin https://github.com/%USER%/%REPO_NAME%.git
git push -u origin main

echo Enabling GitHub Pages…
echo { "build_type": "workflow" } > tmp.json
gh api -X PUT repos/{owner}/%REPO_NAME%/pages --input tmp.json
del tmp.json

echo Done. Your site will deploy after the first workflow run.
echo You can trigger it now from the Actions tab: "AKE Daily Publish" -> Run workflow.
