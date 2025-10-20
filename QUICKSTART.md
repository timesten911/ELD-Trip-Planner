# Quick Start Guide

Get the ELD Trip Planner running in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- Node.js 16+ installed
- Git installed

## Step 1: Clone/Download Project

If you haven't already, navigate to the project directory:
```bash
cd c:\Spotter
```

## Step 2: Backend Setup (2 minutes)

### Windows
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py runserver
```

### Mac/Linux
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

**Keep this terminal open!** Backend is now running at `http://localhost:8000`

## Step 3: Frontend Setup (2 minutes)

Open a **NEW terminal** window:

```bash
cd c:\Spotter\frontend
npm install
copy .env.example .env    # Windows
# or
cp .env.example .env      # Mac/Linux
npm start
```

**Frontend will open automatically** at `http://localhost:3000`

## Step 4: Test the App (1 minute)

1. In your browser at `http://localhost:3000`, enter:
   - **Current Location**: Los Angeles, CA
   - **Pickup Location**: Phoenix, AZ
   - **Dropoff Location**: Dallas, TX
   - **Current Cycle Used**: 0

2. Click **Calculate Trip**

3. Wait 5-10 seconds for results

4. Explore the three tabs:
   - **Map & Route**: See your route on the map
   - **Trip Summary**: View detailed breakdown
   - **ELD Logs**: See daily log sheets

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (should be 3.8+)
- Make sure port 8000 is not in use
- Check for error messages in terminal

### Frontend won't start
- Check Node version: `node --version` (should be 16+)
- Delete `node_modules` and run `npm install` again
- Make sure port 3000 is not in use

### "Failed to calculate trip" error
- Make sure backend is running (check terminal)
- Check backend URL in `frontend/.env` is `http://localhost:8000/api`
- Try refreshing the page

### Map not showing
- Check browser console for errors (F12)
- Make sure you have internet connection (for map tiles)
- Try a different browser

### Geocoding fails
- Check your internet connection
- Try more specific addresses (include city and state)
- Wait a few seconds and try again (rate limiting)

## Next Steps

- Read [README.md](README.md) for detailed documentation
- See [DEPLOYMENT.md](DEPLOYMENT.md) for hosting instructions
- Check [TESTING.md](TESTING.md) for testing guidelines

## Common Test Addresses

### Short Trips (1 day)
- Los Angeles, CA → San Diego, CA → Las Vegas, NV

### Medium Trips (2-3 days)
- Los Angeles, CA → Phoenix, AZ → Dallas, TX
- New York, NY → Chicago, IL → Denver, CO

### Long Trips (4+ days)
- Seattle, WA → Portland, OR → Miami, FL
- Los Angeles, CA → New York, NY

## Features to Try

1. **Different cycle hours**: Try entering 30, 50, or 65 hours
2. **Download logs**: Click download button on ELD logs
3. **View segments**: Scroll through trip segments in summary
4. **Map interaction**: Zoom and pan the map, click markers

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review error messages in browser console (F12)
3. Check terminal output for backend errors
4. See [TESTING.md](TESTING.md) for known issues

## Stopping the Application

### Stop Backend
- Press `Ctrl+C` in the backend terminal
- Type `deactivate` to exit virtual environment

### Stop Frontend
- Press `Ctrl+C` in the frontend terminal

## Restarting

### Backend
```bash
cd backend
venv\Scripts\activate    # Windows
# or
source venv/bin/activate # Mac/Linux
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm start
```

---

**Congratulations!** 🎉 You now have a fully functional ELD Trip Planner running locally!
