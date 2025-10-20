# Deployment Guide

## Backend Deployment (Railway/Render/Heroku)

### Railway (Recommended)

1. **Create Railway Account**: Sign up at [railway.app](https://railway.app)

2. **Deploy Backend**:
   ```bash
   cd backend
   railway login
   railway init
   railway up
   ```

3. **Set Environment Variables**:
   - Go to your Railway project
   - Add variables:
     - `DJANGO_SECRET_KEY`: Generate a secure key
     - `DEBUG`: Set to `False`
     - `ALLOWED_HOSTS`: Add your Railway domain

4. **Get Backend URL**: Copy your Railway backend URL (e.g., `https://your-app.railway.app`)

### Alternative: Render

1. Create account at [render.com](https://render.com)
2. New Web Service → Connect your GitHub repo
3. Build Command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
4. Start Command: `gunicorn eld_backend.wsgi`
5. Add environment variables (same as Railway)

### Alternative: Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Push: `git push heroku main`
5. Set environment variables: `heroku config:set KEY=VALUE`

## Frontend Deployment (Vercel)

### Vercel (Recommended)

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Deploy Frontend**:
   ```bash
   cd frontend
   vercel
   ```

3. **Set Environment Variables**:
   - In Vercel dashboard, go to your project
   - Settings → Environment Variables
   - Add: `REACT_APP_API_URL` = Your backend URL (e.g., `https://your-app.railway.app/api`)

4. **Redeploy**: After setting env vars, trigger a new deployment

### Alternative: Netlify

1. **Build the app**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy**:
   - Drag and drop `build` folder to [netlify.com](https://netlify.com)
   - Or use Netlify CLI:
     ```bash
     npm install -g netlify-cli
     netlify deploy --prod
     ```

3. **Environment Variables**:
   - Site settings → Environment variables
   - Add: `REACT_APP_API_URL`

## Quick Deploy Steps

### 1. Backend First
```bash
cd backend
# Deploy to Railway/Render/Heroku
# Get your backend URL
```

### 2. Update Frontend Config
```bash
cd frontend
# Create .env file
echo REACT_APP_API_URL=https://your-backend-url.com/api > .env
```

### 3. Deploy Frontend
```bash
# Still in frontend directory
vercel
# Or netlify deploy --prod
```

## Environment Variables Summary

### Backend
- `DJANGO_SECRET_KEY`: Django secret (generate with `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`)
- `DEBUG`: `False` for production
- `ALLOWED_HOSTS`: Your domain (e.g., `your-app.railway.app`)
- `ORS_API_KEY`: (Optional) OpenRouteService API key

### Frontend
- `REACT_APP_API_URL`: Full backend API URL including `/api` (e.g., `https://your-app.railway.app/api`)

## Testing Deployment

1. Visit your frontend URL
2. Enter test trip:
   - Current: "Los Angeles, CA"
   - Pickup: "Phoenix, AZ"
   - Dropoff: "Dallas, TX"
   - Cycle: 0
3. Verify:
   - Map loads correctly
   - Route is displayed
   - ELD logs are generated
   - No console errors

## Troubleshooting

### CORS Issues
- Ensure backend `ALLOWED_HOSTS` includes frontend domain
- Check `CORS_ALLOW_ALL_ORIGINS` in settings.py

### API Connection Failed
- Verify `REACT_APP_API_URL` is correct
- Check backend is running: visit `https://your-backend-url/api/health/`
- Ensure no trailing slashes mismatch

### Static Files Not Loading
- Run `python manage.py collectstatic` on backend
- Check WhiteNoise is installed and configured

### Map Not Displaying
- Check browser console for errors
- Verify Leaflet CSS is loaded
- Check network tab for tile loading

## Monitoring

- **Backend Logs**: Check Railway/Render/Heroku logs
- **Frontend Logs**: Check Vercel/Netlify deployment logs
- **API Health**: Monitor `/api/health/` endpoint

## Cost Estimates

- **Railway**: Free tier available, $5/month for hobby
- **Render**: Free tier available
- **Vercel**: Free for personal projects
- **Netlify**: Free for personal projects

All services offer free tiers suitable for this assessment project.
