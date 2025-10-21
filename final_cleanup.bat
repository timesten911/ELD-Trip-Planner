@echo off
echo Committing cleanup...
git add -A
git commit -m "Clean up: Remove unnecessary documentation and batch files, keep only README and LOOM_SCRIPT"
git push origin main
echo.
echo ========================================
echo Cleanup pushed to GitHub!
echo ========================================
echo.
echo Your repository now has:
echo - README.md (main documentation)
echo - LOOM_SCRIPT.md (demo script)
echo - Clean codebase
echo.
echo Live URLs:
echo Backend: https://eld-trip-planner-production.up.railway.app
echo Frontend: https://eld-trip-planner-live.vercel.app
echo.
pause
