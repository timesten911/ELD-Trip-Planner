# 🔧 Railway Deployment Fix

## The Error You're Seeing:
"Error creating build plan with Nixpacks"

## ✅ SOLUTION - Follow These Steps:

### Step 1: In Railway Dashboard

1. **Click on your service** (ELD-Trip-Planner)

2. **Go to Settings tab**

3. **Find "Build & Deploy" section**

4. **Set these values:**

   **Root Directory:** `backend`
   
   **Build Command:** 
   ```
   pip install -r requirements.txt && python manage.py collectstatic --noinput
   ```
   
   **Start Command:**
   ```
   gunicorn eld_backend.wsgi:application --bind 0.0.0.0:$PORT
   ```

5. **Click "Deploy" or "Redeploy"**

---

### Step 2: Add Environment Variables

Go to **Variables** tab and add:

```
DJANGO_SECRET_KEY=eld-trip-planner-production-secret-key-2024
DEBUG=False
ALLOWED_HOSTS=*
DISABLE_COLLECTSTATIC=1
```

---

### Step 3: Redeploy

1. Go to **Deployments** tab
2. Click the **"..."** menu on the latest deployment
3. Click **"Redeploy"**

---

## Alternative: Use Railway CLI

If the above doesn't work, try this:

```bash
cd backend
railway login
railway link
railway up
```

---

## ✅ Expected Result

After redeployment, you should see:
- ✓ Build successful
- ✓ Deploy successful
- ✓ Service running

Then visit: `https://your-railway-url.up.railway.app/api/health/`

You should see: `{"status":"healthy",...}`

---

## 🚨 If Still Not Working

Try this simpler approach:

1. **Delete the service** in Railway
2. **Create a new service**
3. **Select "Empty Service"**
4. **Go to Settings → Connect Repo**
5. **Select your GitHub repo**
6. **Set Root Directory to:** `backend`
7. **Add the environment variables above**
8. **Railway will auto-detect Python and deploy**

---

## 📞 Common Issues

**Issue:** "Module not found"
**Fix:** Make sure Root Directory is set to `backend`

**Issue:** "Port binding error"
**Fix:** Make sure start command uses `$PORT` variable

**Issue:** "Static files not found"
**Fix:** Add `DISABLE_COLLECTSTATIC=1` to variables

---

## ✅ Once Working

Your Railway URL will be like:
`https://eld-trip-planner-production.up.railway.app`

Test it: `https://your-url.up.railway.app/api/health/`

Then use this URL in Vercel for `REACT_APP_API_URL`
