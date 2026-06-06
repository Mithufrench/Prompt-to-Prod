@echo off
REM Complete Git Setup and Push Script
REM Run this in PowerShell or Command Prompt in the project directory

echo.
echo ========================================
echo INITIALIZING GIT AND PUSHING TO GITHUB
echo ========================================
echo.

REM Initialize git repository
echo Step 1: Initializing Git repository...
git init
if errorlevel 1 (
    echo ERROR: Failed to initialize git
    pause
    exit /b 1
)
echo. & echo ✓ Git initialized

REM Set user config
echo.
echo Step 2: Setting Git configuration...
git config user.name "Mithufrench"
git config user.email "msikst@hotmail.com"
echo ✓ Git configuration set

REM Add remote origin
echo.
echo Step 3: Adding GitHub remote...
git remote add origin https://github.com/yourusername/prompt-to-prod.git
if errorlevel 1 (
    echo WARNING: Remote might already exist, trying to update...
    git remote set-url origin https://github.com/yourusername/prompt-to-prod.git
)
echo ✓ Remote added

REM Add all files
echo.
echo Step 4: Adding all files...
git add .
echo ✓ Files staged

REM Commit
echo.
echo Step 5: Committing files...
git commit -m "feat: Add complete Prompt-to-Prod AI DevOps platform

- AI Agent (LangChain + FastAPI)
- Web UI (React)
- Kubernetes manifests
- Terraform infrastructure
- Ansible playbooks
- Docker Compose setup
- Complete documentation
- Ready for Railway deployment"
if errorlevel 1 (
    echo ERROR: Commit failed
    pause
    exit /b 1
)
echo ✓ Files committed

REM Set main branch
echo.
echo Step 6: Setting main as default branch...
git branch -M main
echo ✓ Main branch set

REM Push to GitHub
echo.
echo Step 7: Pushing to GitHub...
echo (You may be asked to authenticate with GitHub token)
echo.
git push -u origin main
if errorlevel 1 (
    echo ERROR: Push failed
    echo.
    echo If authentication failed:
    echo 1. Go to: https://github.com/settings/tokens
    echo 2. Click "Generate new token (classic)"
    echo 3. Select "repo" scope
    echo 4. Generate and copy the token
    echo 5. Try again: git push -u origin main
    echo 6. Use your username, paste token as password
    pause
    exit /b 1
)
echo ✓ Files pushed to GitHub!

echo.
echo ========================================
echo SUCCESS! 
echo ========================================
echo.
echo Your files are now on GitHub!
echo Railway will auto-detect and redeploy.
echo.
echo Next steps:
echo 1. Go to Railway Dashboard: https://railway.app/dashboard
echo 2. Click Prompt-to-Prod project
echo 3. Watch the Deployments tab
echo 4. Status will change: Building → Deploying → Running
echo 5. Wait ~5 minutes for green checkmark
echo 6. Copy public URL when ready
echo.
echo Done!
echo.
pause
