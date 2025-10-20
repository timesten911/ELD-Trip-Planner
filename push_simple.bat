@echo off
git add .
git commit -m "Simplify Railway config"
git push origin main
echo.
echo Now in Railway:
echo 1. Go to Settings
echo 2. Set Root Directory to: backend
echo 3. Click Redeploy
echo.
pause
