@echo off
echo Fixing linting errors...
git add .
git commit -m "Fix: Remove unused imports and linting warnings"
git push origin main
echo.
echo Done! Vercel will auto-deploy the fix.
echo Or go to Vercel and click Redeploy.
echo.
pause
