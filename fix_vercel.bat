@echo off
echo Adding utils.js file...
git add .
git commit -m "Fix: Add utils.js for shadcn components"
git push origin main
echo.
echo Done! Now go to Vercel and click "Redeploy"
echo.
pause
