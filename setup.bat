@echo off
echo ========================================
echo ELD Trip Planner - Setup Script
echo ========================================
echo.

echo [1/4] Setting up Backend...
cd backend

echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

echo Installing backend dependencies...
pip install -r requirements.txt

echo Creating .env file...
if not exist .env (
    copy .env.example .env
    echo .env file created. Please edit it with your configuration.
)

echo Running migrations...
python manage.py migrate

echo Creating superuser (optional)...
set /p create_superuser="Create Django admin superuser? (y/n): "
if /i "%create_superuser%"=="y" (
    python manage.py createsuperuser
)

cd ..

echo.
echo [2/4] Setting up Frontend...
cd frontend

echo Installing frontend dependencies...
call npm install

echo Creating .env file...
if not exist .env (
    copy .env.example .env
    echo .env file created. Please edit it with your backend URL.
)

cd ..

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the application:
echo.
echo 1. Start Backend (in one terminal):
echo    cd backend
echo    venv\Scripts\activate
echo    python manage.py runserver
echo.
echo 2. Start Frontend (in another terminal):
echo    cd frontend
echo    npm start
echo.
echo The app will be available at:
echo - Frontend: http://localhost:3000
echo - Backend API: http://localhost:8000/api
echo.
echo For deployment instructions, see DEPLOYMENT.md
echo.
pause
