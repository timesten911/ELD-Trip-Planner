#!/bin/bash

echo "========================================"
echo "ELD Trip Planner - Setup Script"
echo "========================================"
echo ""

echo "[1/4] Setting up Backend..."
cd backend

echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing backend dependencies..."
pip install -r requirements.txt

echo "Creating .env file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo ".env file created. Please edit it with your configuration."
fi

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser (optional)..."
read -p "Create Django admin superuser? (y/n): " create_superuser
if [ "$create_superuser" = "y" ]; then
    python manage.py createsuperuser
fi

cd ..

echo ""
echo "[2/4] Setting up Frontend..."
cd frontend

echo "Installing frontend dependencies..."
npm install

echo "Creating .env file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo ".env file created. Please edit it with your backend URL."
fi

cd ..

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To start the application:"
echo ""
echo "1. Start Backend (in one terminal):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "2. Start Frontend (in another terminal):"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "The app will be available at:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:8000/api"
echo ""
echo "For deployment instructions, see DEPLOYMENT.md"
echo ""
