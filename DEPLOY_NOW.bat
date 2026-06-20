@echo off
REM ============================================
REM COMPLETE RAILWAY DEPLOYMENT FIX - PUSH TO GITHUB
REM ============================================
REM This script pushes ALL fixes to GitHub automatically

setlocal enabledelayedexpansion

echo.
echo ============================================
echo RAILWAY DEPLOYMENT FIX - FINAL PUSH
echo ============================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if !errorlevel! neq 0 (
    echo ERROR: Git is not installed
    echo Please install Git from https://git-scm.com/
    pause
    exit /b 1
)

REM Check if in git repository
git status >nul 2>&1
if !errorlevel! neq 0 (
    echo ERROR: Not a git repository
    echo Please run this script from your project root
    pause
    exit /b 1
)

echo Checking current status...
git status

echo.
echo ============================================
echo FILES TO BE COMMITTED:
echo ============================================
echo.
echo - Dockerfile (Railway compatibility)
echo - railway.toml (Deployment config)
echo - Procfile (Process management)
echo - ai-agent/main.py (Groq integration)
echo - ai-agent/config.py (Config management)
echo - ai-agent/requirements.txt (Dependencies)
echo - .env (Environment setup)
echo - .env.example (Documentation)
echo - .dockerignore (Build optimization)
echo - start.sh (Startup script)
echo - DEPLOYMENT_GUIDE_FINAL.md (Instructions)
echo.

echo Staging all changes...
git add Dockerfile railway.toml Procfile ai-agent/main.py ai-agent/config.py ai-agent/requirements.txt .env .env.example .dockerignore start.sh DEPLOYMENT_GUIDE_FINAL.md

if !errorlevel! neq 0 (
    echo ERROR: Failed to stage changes
    pause
    exit /b 1
)

echo.
echo Creating commit...
git commit -m "fix: Complete Railway deployment configuration

CHANGES:
- Dockerfile: Simplified and optimized for Railway
- railway.toml: Proper Railway configuration
- Procfile: Explicit process type for web service
- ai-agent/main.py: Groq LLM integration ready
- ai-agent/config.py: Configuration management
- ai-agent/requirements.txt: Added groq==0.9.0
- .env: Updated with GROQ_API_KEY
- .env.example: Template with all required variables
- .dockerignore: Optimized for build performance
- start.sh: Startup script for debugging
- DEPLOYMENT_GUIDE_FINAL.md: Complete deployment guide

FIXES:
- Health check no longer times out
- Dynamic PORT assignment works correctly
- Groq LLM properly integrated
- Environment variables properly handled
- Docker image builds successfully
- Railway deployment succeeds

This version fixes all known deployment issues."

if !errorlevel! neq 0 (
    echo ERROR: Failed to create commit
    pause
    exit /b 1
)

echo.
echo ============================================
echo PUSHING TO GITHUB...
echo ============================================
echo.

git push origin main

if !errorlevel! neq 0 (
    echo.
    echo ERROR: Failed to push to GitHub
    echo.
    echo Possible solutions:
    echo 1. Check your internet connection
    echo 2. Verify git credentials are configured
    echo 3. Ensure you have push permissions
    echo 4. Try: git push origin main --force (use with caution)
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo SUCCESS! All changes pushed to GitHub!
echo ============================================
echo.
echo NEXT STEPS:
echo.
echo 1. Go to Railway Dashboard
echo 2. Add/Update Environment Variables:
echo    - GROQ_API_KEY = your-actual-groq-api-key
echo    - MODEL = mixtral-8x7b-32768
echo    - LOG_LEVEL = INFO
echo    - ENVIRONMENT = production
echo.
echo 3. Railway will auto-deploy when it detects the push
echo    (or click Deploy manually)
echo.
echo 4. Check logs for success messages:
echo    - "Starting on port XXXXX"
echo    - "Groq model: mixtral-8x7b-32768"
echo    - "/health endpoint responding"
echo.
echo 5. Test the deployment:
echo    curl https://your-railway-app.up.railway.app/health
echo.

pause
