@echo off
REM Railway Deployment Fix - GitHub Push Script
REM This script commits and pushes all the fixes to your GitHub repository

echo.
echo ========================================
echo Railway Deployment Fix - GitHub Push
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com/
    exit /b 1
)

REM Check if we're in a git repository
git status >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Not a git repository. Initialize with: git init
    exit /b 1
)

REM Display what will be pushed
echo Checking git status...
git status

echo.
echo ========================================
echo Files to be committed:
echo ========================================
echo.
echo 1. Dockerfile - Railway PORT compatibility
echo 2. railway.toml - startCommand and env vars
echo 3. Procfile - Process type declaration
echo 4. ai-agent/requirements.txt - Groq package
echo 5. ai-agent/config.py - Groq API key config
echo 6. ai-agent/main.py - Groq LLM integration
echo 7. .env - Updated credentials
echo 8. .env.example - Updated template
echo.

REM Stage all changes
echo Adding files to git...
git add Dockerfile railway.toml Procfile ai-agent/requirements.txt ai-agent/config.py ai-agent/main.py .env .env.example

REM Commit changes
echo.
echo Committing changes...
git commit -m "fix: Railway PORT compatibility and Groq LLM integration

- Update Dockerfile to use dynamic PORT variable for healthchecks
- Add railway.toml with startCommand and env config
- Create Procfile for explicit Railway process type
- Add groq package to requirements.txt
- Update config.py to use GROQ_API_KEY
- Update main.py to use Groq API instead of hardcoded responses
- Update .env and .env.example with Groq credentials

Fixes: Deployment failures caused by healthcheck probing wrong port
This ensures healthchecks probe the correct dynamically-assigned PORT"

if %errorlevel% neq 0 (
    echo ERROR: Failed to commit changes
    exit /b 1
)

REM Push changes
echo.
echo ========================================
echo Pushing to GitHub...
echo ========================================
echo.

git push origin main

if %errorlevel% neq 0 (
    echo ERROR: Failed to push to GitHub
    echo Make sure you have:
    echo 1. Configured git credentials: git config --global user.name/email
    echo 2. Set up SSH keys or personal access token
    echo 3. Have push permissions on the repository
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! Changes pushed to GitHub
echo ========================================
echo.
echo Next steps:
echo 1. Go to Railway Dashboard
echo 2. Set environment variables:
echo    - GROQ_API_KEY=your-actual-groq-key
echo    - MODEL=mixtral-8x7b-32768
echo    - LOG_LEVEL=INFO
echo 3. Trigger redeploy or wait for auto-deploy
echo 4. Check logs: "Starting on port XXXX" confirms PORT is dynamic
echo.

pause
