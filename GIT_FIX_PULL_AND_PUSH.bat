@echo off
REM ============================================
REM FINAL GIT FIX - PULL, MERGE, AND PUSH
REM ============================================

echo.
echo ============================================
echo GIT FIX - PULL AND PUSH
echo ============================================
echo.

echo The remote has changes you don't have.
echo Fixing by pulling first, then pushing...
echo.

REM Pull first to get remote changes
echo Step 1: Pull from remote...
git pull origin main

if %errorlevel% neq 0 (
    echo.
    echo If merge conflict occurs, you can:
    echo Option A: Accept all incoming changes
    echo   git checkout --theirs .
    echo   git add .
    echo   git commit -m "merge: resolve conflicts"
    echo   git push origin main
    echo.
    echo Option B: Keep local changes
    echo   git checkout --ours .
    echo   git add .
    echo   git commit -m "merge: keep local changes"
    echo   git push origin main
    echo.
    pause
    exit /b 1
)

echo.
echo Step 2: Push to remote...
git push origin main

if %errorlevel% equ 0 (
    echo.
    echo ============================================
    echo SUCCESS! Code pushed to GitHub
    echo ============================================
    echo.
    echo What happens next:
    echo 1. Railway detects push
    echo 2. Docker build starts
    echo 3. Deployment begins
    echo 4. All 3 environments will redeploy
    echo.
    echo Go check Railway dashboard in 2-3 minutes
    echo.
) else (
    echo ERROR: Push failed
)

pause
