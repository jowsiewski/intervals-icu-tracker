# Intervals.icu Activity Tracker - Deployment Guide

## 🚀 Quick Deployment Options

### Option 1: Railway.app (RECOMMENDED) ⭐

**Pros:**
- Free tier: 500 hours/month (enough for 24/7)
- Automatic HTTPS
- Easy database setup
- No credit card required for start

**Steps:**
1. Push your code to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

2. Go to [railway.app](https://railway.app)
3. Click "Start a New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Railway will auto-detect the Dockerfile and deploy!

**Environment Variables to set in Railway:**
```
INTERVALS_ICU_API_KEY=your_api_key
INTERVALS_ICU_ATHLETE_ID=your_athlete_id
DATABASE_URL=sqlite:///./data/activities.db
INTERVALS_ICU_BASE_URL=https://intervals.icu/api/v1
FETCH_INTERVAL_MINUTES=60
```

7. Get your public URL from Railway dashboard

---

### Option 2: Render.com

**Pros:**
- Free tier available
- Automatic SSL
- Easy deployment

**Cons:**
- Spins down after 15 minutes of inactivity (free tier)
- Takes ~30s to wake up

**Steps:**
1. Push code to GitHub (same as above)
2. Go to [render.com](https://render.com)
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: intervals-icu-tracker
   - **Environment**: Docker
   - **Instance Type**: Free
6. Add Environment Variables (same as Railway)
7. Click "Create Web Service"

---

### Option 3: Fly.io

**Pros:**
- 3 free apps
- Fast global deployment
- Good free tier

**Steps:**
1. Install Fly CLI:
```bash
brew install flyctl
```

2. Login and launch:
```bash
flyctl auth login
flyctl launch --no-deploy
```

3. Set secrets:
```bash
flyctl secrets set INTERVALS_ICU_API_KEY=your_api_key
flyctl secrets set INTERVALS_ICU_ATHLETE_ID=your_athlete_id
flyctl secrets set DATABASE_URL=sqlite:///./data/activities.db
```

4. Deploy:
```bash
flyctl deploy
```

---

### Option 4: DigitalOcean App Platform

**Pros:**
- $5/month tier (very stable)
- Professional infrastructure
- Good for production

**Steps:**
1. Push to GitHub
2. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
3. Create new app from GitHub
4. Select repository and branch
5. DigitalOcean auto-detects Dockerfile
6. Add environment variables
7. Choose $5/month plan
8. Deploy!

---

## 📝 Pre-Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] `.env` file in `.gitignore` (already done)
- [ ] Environment variables ready
- [ ] Test locally with Docker:
```bash
docker build -t intervals-tracker .
docker run -p 8000:8000 --env-file .env intervals-tracker
```

---

## 🔒 Security Notes

**Never commit these to Git:**
- ✅ Already in `.gitignore`:
  - `.env`
  - `activities.db`
  - `__pycache__`
  - `venv/`

**Set as environment variables in cloud:**
- `INTERVALS_ICU_API_KEY`
- `INTERVALS_ICU_ATHLETE_ID`

---

## 🗄️ Database Options

### SQLite (Current - Good for start)
- ✅ Simple, no setup needed
- ✅ Free
- ⚠️ File-based (needs persistent volume)

### PostgreSQL (For production)
Railway/Render offer free PostgreSQL. Update `config.py`:
```python
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./activities.db")
# Railway/Render provide DATABASE_URL automatically
```

Then update requirements.txt:
```txt
psycopg2-binary==2.9.9
```

---

## 🎯 Recommended: Railway.app

**Why?**
1. ✅ Easiest setup
2. ✅ True free tier
3. ✅ No sleep mode
4. ✅ Fast deployment
5. ✅ Great for hobby projects

**Expected URL:**
`https://intervals-icu-tracker-production.up.railway.app`

---

## 📊 Cost Comparison

| Platform | Free Tier | Paid Start | Best For |
|----------|-----------|------------|----------|
| Railway | 500h/month | $5/month | Hobby projects |
| Render | Unlimited* | $7/month | Side projects |
| Fly.io | 3 apps | $5/month | Multiple apps |
| DigitalOcean | Trial only | $5/month | Production |

*Spins down after 15min inactivity

---

## 🆘 Troubleshooting

**Issue: Database not persisting**
- Add volume in Railway: `/app/data`
- Or switch to PostgreSQL

**Issue: Port errors**
- Make sure app uses `$PORT` environment variable
- Already configured in our files!

**Issue: Build fails**
- Check Dockerfile syntax
- Verify all requirements in requirements.txt

---

## 📞 Next Steps

1. Choose your platform (I recommend Railway!)
2. Push to GitHub
3. Deploy in ~5 minutes
4. Share your public URL!

Need help with any step? Let me know! 🚀
