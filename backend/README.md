# ELD Trip Planner - Backend

Django REST API for calculating truck routes with HOS compliance and ELD log generation.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create .env file:
```bash
copy .env.example .env
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start server:
```bash
python manage.py runserver
```

## API Endpoints

### Calculate Trip
```
POST /api/calculate-trip/
Content-Type: application/json

{
  "current_location": "Los Angeles, CA",
  "pickup_location": "Phoenix, AZ",
  "dropoff_location": "Dallas, TX",
  "current_cycle_used": 25.5
}
```

### Geocode Address
```
POST /api/geocode/
Content-Type: application/json

{
  "address": "123 Main St, City, State"
}
```

### Health Check
```
GET /api/health/
```

## Project Structure

```
backend/
├── eld_backend/          # Django project settings
│   ├── settings.py       # Configuration
│   ├── urls.py          # URL routing
│   └── wsgi.py          # WSGI config
├── trip_planner/        # Main app
│   ├── eld_service.py   # HOS calculations
│   ├── routing_service.py # Route calculation
│   ├── log_generator.py # ELD log generation
│   ├── views.py         # API views
│   └── urls.py          # App URLs
├── requirements.txt     # Dependencies
└── manage.py           # Django management
```

## HOS Rules

- 70 hours/8 days cycle
- 11 hours max driving per day
- 14 hours max on-duty per day
- 10 hours minimum rest break
- Fuel stop every 1000 miles
- 1 hour for pickup/dropoff

## Dependencies

- Django 4.2.7
- djangorestframework 3.14.0
- django-cors-headers 4.3.1
- requests 2.31.0
- Pillow 10.1.0
- reportlab 4.0.7
