@echo off
echo Cleaning up unnecessary files...

REM Delete unnecessary markdown files
del CHECKLIST.md
del DEPLOYMENT.md
del DEPLOYMENT_COMPLETE.md
del DEPLOYMENT_STEPS.md
del DEPLOY_LIVE.md
del FEATURES.md
del GITHUB_VERIFICATION.md
del NEXT_STEPS.md
del PROJECT_STATUS.md
del PROJECT_SUMMARY.md
del QUICKSTART.md
del RAILWAY_FIX.md
del TESTING.md
del QUICK_DEPLOY.txt

REM Delete batch files
del commit_and_push.bat
del deploy_to_github.bat
del final_push.bat
del fix_lint.bat
del fix_vercel.bat
del push_fix.bat
del push_simple.bat
del push_to_github.bat

REM Delete test files
del backend\test_trip.py 2>nul

REM Delete old/backup files
del backend\trip_planner\log_generator_new.py 2>nul

echo.
echo Cleanup complete!
echo.
echo Remaining documentation:
echo - README.md
echo - LOOM_SCRIPT.md
echo.
pause
