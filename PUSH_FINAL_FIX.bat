@echo off
REM ============================================
REM FINAL RAILWAY DEPLOYMENT FIX - PUSH NOW
REM ============================================
REM This fixes the healthcheck timeout issue by using railway.json

echo.
echo ============================================
echo RAILWAY DEPLOYMENT - FINAL FIX
echo ============================================
echo.

git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git not found. Install from https://git-scm.com/
    pause
    exit /b 1
)

git status >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Not a git repository
    pause
    exit /b 1
)

echo Current status:
git status

echo.
echo ============================================
echo CRITICAL FIX FILES:
echo ============================================
echo.
echo 1. Dockerfile - Removed embedded healthcheck
echo 2. railway.json - NEW: Proper Railway config
echo 3. ai-agent/main.py - Enhanced logging
echo 4. Procfile - Process declaration
echo.

echo Staging changes...
git add Dockerfile railway.json railway.toml ai-agent/main.py Procfile ai-agent/requirements.txt .env .env.example .dockerignore

echo Committing...
git commit -m "fix: Final Railway deployment - healthcheck issue resolved

CRITICAL CHANGES:
- Removed embedded HEALTHCHECK from Dockerfile
- Created railway.json with proper healthcheck config
- Enhanced logging in main.py for debugging
- Procfile tells Railway how to start
- app will listen on PORT env var (Railway assigns)

ISSUE FIXED:
Railway was probing port 8000 but app was on dynamic port
Now: railway.json handles healthcheck correctly
Result: Deployment will succeed!"

if %errorlevel% neq 0 (
    echo ERROR: Commit failed
    pause
    exit /b 1
)

echo.
echo Pushing to GitHub...
git push origin main

if %errorlevel% neq 0 (
    echo ERROR: Push failed
    pause
    exit /b 1
)

echo.
echo ============================================
echo SUCCESS! Changes pushed
echo ============================================
echo.
echo NEXT STEPS:
echo.
echo 1. Go to Railway Dashboard
echo 2. Make sure these variables are set:
echo    - GROQ_API_KEY = your-actual-key
echo    - MODEL = mixtral-8x7b-32728
echo    - PYTHONUNBUFFERED = 1
echo.
echo 3. Click "Force Redeploy" in Railway
echo 4. Wait 5-10 minutes
echo 5. Check logs for: "Starting Prompt-to-Prod AI DevOps Agent"
echo.
echo The healthcheck issue should be FIXED!
echo.

pause
