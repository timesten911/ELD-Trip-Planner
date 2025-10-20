# ELD Trip Planner

A full-stack web application for planning truck trips with Hours of Service (HOS) compliance and Electronic Logging Device (ELD) log generation.

## 🚀 Features

- **Route Planning**: Calculate routes with pickup and dropoff locations
- **HOS Compliance**: Automatic calculation of rest breaks based on FMCSA regulations
- **ELD Log Generation**: Visual daily log sheets similar to paper logs
- **Interactive Map**: View your route with OpenStreetMap
- **Trip Summary**: Detailed breakdown of segments, fuel stops, and rest breaks
- **70hr/8-day Cycle**: Track and manage your cycle hours

## 📋 Requirements

### Backend
- Python 3.8+
- Django 4.2+
- pip

### Frontend
- Node.js 16+
- npm or yarn

## 🛠️ Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create environment file:
```bash
copy .env.example .env
```

6. Run migrations:
```bash
python manage.py migrate
```

7. Start the development server:
```bash
python manage.py runserver
```

The backend API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file:
```bash
copy .env.example .env
```

4. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## 🎯 Usage

1. **Enter Trip Details**:
   - Current location (e.g., "Los Angeles, CA")
   - Pickup location (e.g., "Phoenix, AZ")
   - Dropoff location (e.g., "Dallas, TX")
   - Current cycle hours used (0-70)

2. **View Results**:
   - **Map & Route**: Interactive map showing your complete route
   - **Trip Summary**: Detailed breakdown of segments and statistics
   - **ELD Logs**: Daily log sheets for each day of the trip

3. **Download Logs**: Click the download button on any log sheet to save as PNG

## 📊 HOS Rules Implemented

- **Property-Carrying Driver**: 70 hours/8 days cycle
- **Driving Limit**: 11 hours maximum driving per day
- **On-Duty Limit**: 14 hours maximum on-duty per day
- **Rest Break**: 10 hours minimum consecutive off-duty time
- **Fuel Stops**: Automatic fuel stop every 1,000 miles (30 min)
- **Pickup/Dropoff**: 1 hour allocated for each

## 🗺️ APIs Used

- **Routing**: OSRM (Open Source Routing Machine) - Free, no API key required
- **Geocoding**: Nominatim (OpenStreetMap) - Free, no API key required
- **Maps**: Leaflet with OpenStreetMap tiles - Free

## 🏗️ Architecture

### Backend (Django)
- `eld_service.py`: HOS compliance calculations
- `routing_service.py`: Route calculation and geocoding
- `log_generator.py`: ELD log sheet generation
- `views.py`: REST API endpoints

### Frontend (React)
- Modern UI with TailwindCSS
- shadcn/ui components
- Leaflet for maps
- Axios for API calls

## 📦 Deployment

### Backend (Django)
- Can be deployed to Heroku, Railway, or any Python hosting
- Uses Gunicorn as WSGI server
- WhiteNoise for static files

### Frontend (React)
- Can be deployed to Vercel, Netlify, or any static hosting
- Build with `npm run build`
- Set `REACT_APP_API_URL` environment variable to your backend URL

## 🔧 Configuration

### Backend Environment Variables
- `DJANGO_SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `ORS_API_KEY`: (Optional) OpenRouteService API key for enhanced routing

### Frontend Environment Variables
- `REACT_APP_API_URL`: Backend API URL

## 📝 API Endpoints

- `POST /api/calculate-trip/`: Calculate trip with route and ELD logs
- `POST /api/geocode/`: Convert address to coordinates
- `GET /api/health/`: Health check

## 🤝 Contributing

This is an assessment project. For production use, consider:
- Adding user authentication
- Database storage for trip history
- Real-time traffic data integration
- Mobile app version
- PDF export for logs

## ⚠️ Disclaimer

This application is for educational and planning purposes only. Always verify HOS compliance with official FMCSA regulations and use certified ELD devices for actual logging.

## 📄 License

MIT License - See LICENSE file for details

## 👨‍💻 Developer

Created as a Full Stack Developer Assessment Project

## 🎥 Demo Video

[Link to Loom video demonstration]
