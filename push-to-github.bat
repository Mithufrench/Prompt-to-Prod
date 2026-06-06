@echo off
REM Push Prompt-to-Prod to GitHub

echo.
echo ========================================
echo GitHub Push Script
echo ========================================
echo.

cd /d C:\Projects\Prompt-to-Prod

echo Checking git status...
git status

echo.
echo Adding all files...
git add .

echo.
echo Checking what will be committed...
git status

echo.
echo Committing changes...
git commit -m "feat: Add complete Prompt-to-Prod application

- AI Agent (LangChain + FastAPI)
- Web UI (React)
- Kubernetes manifests
- Terraform infrastructure
- Ansible playbooks
- Docker Compose setup
- Complete documentation
- Ready for Railway deployment"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo SUCCESS! 
echo ========================================
echo.
echo Files pushed to GitHub!
echo Railway will auto-deploy in a few moments.
echo.
echo Check Railway Dashboard:
echo https://railway.app/dashboard
echo.
echo Watch the status change from FAILED to BUILDING to RUNNING
echo.
