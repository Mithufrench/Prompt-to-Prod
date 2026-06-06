@echo off
REM Railway.app Deployment Script (Easiest Free Hosting)
REM Takes 5 minutes, completely free

setlocal enabledelayedexpansion

echo.
echo ====================================
echo Railway.app FREE Deployment
echo ====================================
echo.
echo This will deploy your app to Railway.app (free)
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found
    echo Install from: https://nodejs.org/
    exit /b 1
)

REM Check if Railway CLI is installed
railway --version >nul 2>&1
if errorlevel 1 (
    echo Installing Railway CLI...
    call npm install -g @railway/cli
)

echo.
echo ====================================
echo Step 1: Login to Railway
echo ====================================
echo.
echo Visit: https://railway.app
echo Sign up/login with GitHub
echo Then press Enter to continue...
pause

echo.
echo Attempting Railway login...
call railway login

if errorlevel 1 (
    echo ERROR: Login failed
    exit /b 1
)

echo ✓ Logged in successfully

echo.
echo ====================================
echo Step 2: Initialize Project
echo ====================================
echo.

cd /d C:\Projects\Prompt-to-Prod
call railway init

if errorlevel 1 (
    echo ERROR: Initialization failed
    exit /b 1
)

echo ✓ Project initialized

echo.
echo ====================================
echo Step 3: Set Environment Variables
echo ====================================
echo.

set /p OPENAI_KEY="Enter your OpenAI API key (sk-...): "
set /p DB_PASS="Enter database password: "

call railway variables set OPENAI_API_KEY=%OPENAI_KEY%
call railway variables set DB_PASSWORD=%DB_PASS%
call railway variables set LOG_LEVEL=INFO
call railway variables set ENVIRONMENT=production

echo ✓ Environment variables set

echo.
echo ====================================
echo Step 4: Deploy to Railway
echo ====================================
echo.

call railway up

if errorlevel 1 (
    echo ERROR: Deployment failed
    exit /b 1
)

echo ✓ Deployment started

echo.
echo ====================================
echo Step 5: Get Your Public URL
echo ====================================
echo.

call railway open

echo.
echo ====================================
echo DEPLOYMENT COMPLETE!
echo ====================================
echo.
echo Your app is now live on the internet!
echo.
echo To view your deployment:
echo   railway open
echo.
echo To view logs:
echo   railway logs
echo.
echo To stop/restart:
echo   railway stop
echo   railway restart
echo.
echo To scale:
echo   railway scale
echo.
echo ====================================
echo.
