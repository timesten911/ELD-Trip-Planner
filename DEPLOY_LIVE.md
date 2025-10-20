# 🚀 Deploy ELD Trip Planner Live

## Step 1: Deploy Backend to Railway ✅

### A. In Railway Dashboard (railway.app)

1. **Click "New Project"**
2. **Select "Deploy from GitHub repo"**
3. **Choose:** `timesten911/ELD-Trip-Planner`
4. **Click "Deploy Now"**

### B. Configure Environment Variables

In Railway, go to your project → **Variables** tab and add:

```
DJANGO_SECRET_KEY=your-secret-key-here-make-it-long-and-random
DEBUG=False
ALLOWED_HOSTS=*
RAILWAY_ENVIRONMENT_NAME=production
```

### C. Set Root Directory

1. Go to **Settings** tab
2. Find **Root Directory**
3. Set to: `backend`
4. Click **Save**

### D. Get Your Backend URL

After deployment completes:
- Railway will give you a URL like: `https://eld-trip-planner-production.up.railway.app`
- **Copy this URL** - you'll need it for frontend!

---

## Step 2: Deploy Frontend to Vercel ✅

### A. In Vercel Dashboard (vercel.com)

1. **Click "Add New..." → Project**
2. **Import Git Repository**
3. **Select:** `timesten911/ELD-Trip-Planner`
4. **Click "Import"**

### B. Configure Build Settings

**Framework Preset:** Create React App

**Root Directory:** `frontend`

**Build Command:** `npm run build`

**Output Directory:** `build`

### C. Add Environment Variable

In **Environment Variables** section, add:

**Name:** `REACT_APP_API_URL`
**Value:** `https://your-railway-url.up.railway.app` (from Step 1D)

Example:
```
REACT_APP_API_URL=https://eld-trip-planner-production.up.railway.app
```

### D. Deploy

1. Click **Deploy**
2. Wait 2-3 minutes
3. Vercel will give you a URL like: `https://eld-trip-planner.vercel.app`

---

## Step 3: Update Backend CORS Settings

After getting your Vercel URL, update Railway environment variables:

Add this variable in Railway:
```
ALLOWED_HOSTS=your-vercel-url.vercel.app,*.railway.app
```

Example:
```
ALLOWED_HOSTS=eld-trip-planner.vercel.app,*.railway.app
```

Then **redeploy** the backend in Railway.

---

## 🎯 Quick Deploy Commands (Alternative)

### If you prefer command line:

**Railway CLI:**
```bash
cd backend
railway login
railway init
railway up
```

**Vercel CLI:**
```bash
cd frontend
npm install -g vercel
vercel login
vercel --prod
```

---

## ✅ Verification Checklist

After deployment:

### Backend (Railway)
- [ ] Visit: `https://your-railway-url.up.railway.app/api/health/`
- [ ] Should return: `{"status":"healthy",...}`

### Frontend (Vercel)
- [ ] Visit: `https://your-vercel-url.vercel.app`
- [ ] Should see the trip planner interface
- [ ] Try calculating a trip

### Full Test
- [ ] Enter trip details
- [ ] Click "Calculate Trip"
- [ ] See route on map
- [ ] View ELD logs
- [ ] Download log as PNG

---

## 🔧 Troubleshooting

### Backend Issues

**Problem:** 500 Error
**Solution:** Check Railway logs, ensure all environment variables are set

**Problem:** CORS Error
**Solution:** Update ALLOWED_HOSTS in Railway variables

### Frontend Issues

**Problem:** "Failed to calculate trip"
**Solution:** Check REACT_APP_API_URL is correct

**Problem:** Blank page
**Solution:** Check browser console for errors

---

## 📊 Your Live URLs

After deployment, you'll have:

**Backend API:** `https://eld-trip-planner-production.up.railway.app`
**Frontend App:** `https://eld-trip-planner.vercel.app`

**Share this URL with anyone:** Your Vercel frontend URL

---

## 🎥 Demo Video

After deployment:
1. Record a Loom video showing the live app
2. Update README.md with the video link
3. Add your live URLs to README.md

---

## 💡 Pro Tips

1. **Custom Domain:** Both Railway and Vercel support custom domains
2. **Monitoring:** Railway provides logs and metrics
3. **Auto-Deploy:** Both platforms auto-deploy when you push to GitHub
4. **Free Tier:** Both have generous free tiers for this project

---

## 🚨 Important Notes

1. **Railway Variables:** Make sure DEBUG=False in production
2. **Secret Key:** Use a strong, random secret key
3. **CORS:** Ensure frontend URL is in ALLOWED_HOSTS
4. **API URL:** Frontend must point to correct backend URL

---

## 📞 Need Help?

If deployment fails:
1. Check Railway logs (Railway dashboard → Deployments → View logs)
2. Check Vercel logs (Vercel dashboard → Deployments → View logs)
3. Verify all environment variables are set correctly
4. Ensure root directories are set correctly

---

**Ready to deploy? Follow Step 1 first (Railway), then Step 2 (Vercel)!** 🚀
