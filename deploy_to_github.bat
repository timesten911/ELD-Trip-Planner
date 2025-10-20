@echo off
echo ========================================
echo Deploying ELD Trip Planner to GitHub
echo ========================================

REM Configure git user
git config user.name "ELD Developer"
git config user.email "developer@eld.com"

REM Commit all changes
git commit -m "Initial commit: ELD Trip Planner with route optimization and log generation"

REM Add remote repository
git remote add origin https://github.com/timesten911/ELD-Trip-Planner.git

REM Push to GitHub
git branch -M main
git push -u origin main

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Your code is now at:
echo https://github.com/timesten911/ELD-Trip-Planner
echo.
pause
