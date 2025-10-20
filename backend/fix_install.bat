@echo off
echo Fixing installation issues...
echo.

echo Step 1: Uninstalling Django 5.2.7...
pip uninstall -y django

echo.
echo Step 2: Installing Django 4.2.7...
pip install Django==4.2.7

echo.
echo Step 3: Installing other dependencies...
pip install djangorestframework==3.14.0
pip install django-cors-headers==4.3.1
pip install requests==2.31.0
pip install python-dotenv==1.0.0
pip install gunicorn==21.2.0
pip install whitenoise==6.6.0

echo.
echo Step 4: Installing Pillow (may take a moment)...
pip install Pillow

echo.
echo Installation complete!
echo.
echo Now you can run: python manage.py migrate
pause
