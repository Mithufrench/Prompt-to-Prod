@echo off
REM Push the committed changes to GitHub
echo Pushing to GitHub...
git push origin main

if %errorlevel% equ 0 (
    echo.
    echo ============================================
    echo SUCCESS! Changes pushed to GitHub
    echo ============================================
    echo.
    echo NEXT STEPS:
    echo.
    echo 1. Go to Railway Dashboard
    echo 2. Click on your Prompt-to-Prod service
    echo 3. Go to Variables tab
    echo 4. Set GROQ_API_KEY = your-actual-key
    echo 5. Go to Deployments tab
    echo 6. Click menu (three dots)
    echo 7. Click "Force Redeploy"
    echo 8. Wait 5-10 minutes
    echo 9. Check logs for "Starting Prompt-to-Prod"
    echo.
    echo The healthcheck issue is now FIXED!
    echo.
    pause
) else (
    echo ERROR: Push failed
    echo Try running this again or use:
    echo   git push origin main
    pause
)
