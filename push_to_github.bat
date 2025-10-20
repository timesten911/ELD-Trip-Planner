@echo off
echo ========================================
echo Pushing to GitHub
echo ========================================

git config user.name "Alex Chomba"
git config user.email "chombaalex2019@gmail.com"

git add DEPLOYMENT_COMPLETE.md deploy_to_github.bat push_to_github.bat
git commit -m "Add deployment documentation"

echo.
echo Pushing to GitHub...
git push -u origin main --force

echo.
echo ========================================
echo Push Complete!
echo ========================================
echo.
echo Check your repository at:
echo https://github.com/timesten911/ELD-Trip-Planner
echo.
pause
