# 🚀 RAILWAY HOBBY PLAN: COMPLETE DEPLOYMENT GUIDE

## ✅ You Have: Railway Hobby Plan

Perfect! Your Hobby plan includes everything you need to deploy your Prompt-to-Prod platform.

**Hobby Plan Features:**
- ✅ 1 project
- ✅ $5 monthly credit
- ✅ Up to 500MB RAM per service
- ✅ PostgreSQL database included
- ✅ Public URLs
- ✅ HTTPS/SSL (free)
- ✅ Unlimited bandwidth
- ✅ Custom domains (optional)

---

## 🎯 STEP-BY-STEP DEPLOYMENT

### STEP 1: Log In to Railway Dashboard

**Action:**
1. Go to: https://railway.app
2. Click "Dashboard" (top right)
3. Log in with your GitHub account
4. You should see: "Projects" page

**Expected Result:**
- You're logged in
- Dashboard is open
- You can see projects area

---

### STEP 2: Create New Project

**Action:**
1. In Railway Dashboard, click: "+ New Project"
2. Select: "GitHub Repo"
3. Choose: "Public Repo" or "Private Repo"

**Expected Result:**
- Railway connects to GitHub
- Authorization dialog appears
- You can see your repositories

---

### STEP 3: Select Your Repository

**Action:**
1. Search or find: "prompt-to-prod" repository
2. Click on it to select
3. Confirm authorization

**Expected Result:**
- Your repository is selected
- Railway starts creating project
- Project appears in dashboard

---

### STEP 4: Configure Build Settings

**In Railway Dashboard:**

1. **Click** on your new project
2. **Click** on "Settings" (gear icon)
3. **Look for** "Build" section:
   - **Build Command**: Leave empty (Railway auto-detects Docker)
   - **Start Command**: Leave empty
   - **Dockerfile**: Should show: `./ai-agent/Dockerfile`
   - **Workdir**: Leave as default

**If not auto-detected:**
1. Click "Dockerfile" field
2. Enter: `./ai-agent/Dockerfile`
3. Click "Deploy" button

**Expected Result:**
- Build settings configured
- Dockerfile is recognized
- Ready to deploy

---

### STEP 5: Set Environment Variables

**CRITICAL STEP - This is required for the app to work!**

**In Railway Dashboard:**

1. **Click** on your project
2. **Click** on "Variables" (in left sidebar)
3. **Add these variables:**

```
OPENAI_API_KEY=sk-your-actual-key-here
LOG_LEVEL=INFO
AGENT_TIMEOUT=30
ENVIRONMENT=production
DB_PASSWORD=YourSecurePassword123!
```

**How to add each variable:**

1. Click "+ New Variable"
2. Enter **Name**: (e.g., OPENAI_API_KEY)
3. Enter **Value**: (your actual key)
4. Click "Add"
5. Repeat for each variable

**Important:**
- Replace `sk-your-actual-key-here` with your REAL OpenAI API key
- Use a STRONG password for DB_PASSWORD
- Don't use special characters that might break it

**Expected Result:**
- All 5 variables are showing
- Values are saved
- Green checkmarks next to each

---

### STEP 6: Configure Database (PostgreSQL)

**In Railway Dashboard:**

1. **Click** on your project
2. **In the services list**, look for "PostgreSQL"
3. **If you don't see it:**
   - Click "+ Add Service"
   - Search: "PostgreSQL"
   - Click it to add
4. **Click** on PostgreSQL service
5. **Copy these values:**
   - Host
   - Port
   - Database
   - Username
   - Password

**Add to Environment Variables:**
```
DATABASE_URL=postgresql://username:password@host:port/database
```

**Expected Result:**
- PostgreSQL service is added
- Database credentials visible
- DATABASE_URL variable set

---

### STEP 7: Deploy the Application

**In Railway Dashboard:**

1. **Click** on your project name
2. **Look** for the "Deploy" button
3. **Click**: "Deploy" or "Trigger Deploy"

**Alternative - Auto Deploy from GitHub:**
1. Your app auto-deploys when you push to GitHub
2. Check: "GitHub" section in Railway settings
3. Enable: "Auto-deploy from main branch" (if available)

**Expected Result:**
- Deployment starts
- You see building progress
- Status changes to "Building..."

---

### STEP 8: Wait for Build and Deployment

**What to expect:**

1. **Building Phase** (2-3 minutes):
   - Docker image is built
   - Dependencies installed
   - See: "Building..." status

2. **Deploying Phase** (1-2 minutes):
   - Container starts
   - See: "Deploying..." status
   - Health checks run

3. **Complete** (when ready):
   - Status: "✓ Running" (green)
   - You see: Public URL

**Monitor Progress:**

Click on your project to see:
- Build logs
- Deployment logs
- Errors (if any)

---

### STEP 9: Get Your Public URL

**In Railway Dashboard:**

1. **Click** on your project
2. **Look** for "Deployments" section
3. **Find** your latest deployment
4. **Look** for "Public URL" or "Domain"
5. **Copy** the URL

**It will look like:**
```
https://prompt-to-prod-prod-xxxx.railway.app
```

**Expected Result:**
- You have a public URL
- URL is showing in dashboard
- Status is "Running"

---

### STEP 10: Test Your Deployment

**Test in Browser:**

```
1. Open your public URL in browser:
   https://prompt-to-prod-prod-xxxx.railway.app

2. You should see the Railway "Welcome" page
   (or your app if configured)

3. Test API endpoints:
   - Health: /health
   - Docs: /docs
   - Chat: /api/chat
```

**Test with cURL (in PowerShell):**

```powershell
# Test health check
curl https://prompt-to-prod-prod-xxxx.railway.app/health

# Expected response:
# {"status":"healthy","service":"p2p-agent","version":"2.0.0"}

# Test API docs
curl https://prompt-to-prod-prod-xxxx.railway.app/docs
```

**Expected Result:**
- /health returns 200 OK
- /docs shows Swagger UI
- App is working correctly

---

## ⚠️ TROUBLESHOOTING

### Issue: Deployment Failed

**Check logs:**
1. Click on project
2. Click on "Deployments"
3. Click on failed deployment
4. Read the error message
5. Common issues:
   - Missing OPENAI_API_KEY
   - Wrong Dockerfile path
   - Database connection error

**Fix:**
1. Fix the issue
2. Click "Retry" in Railway
3. Or wait for auto-redeploy on next git push

### Issue: App Shows Error

**Steps:**
1. Click project
2. Click "View Logs"
3. Look for error messages
4. Common causes:
   - Missing environment variables
   - Database not connected
   - API key invalid

**Fix:**
1. Add missing variables
2. Restart deployment: Click "Redeploy"
3. Wait 2-3 minutes

### Issue: URL Not Working

**Steps:**
1. Verify deployment is "Running" (green)
2. Wait 5 minutes (DNS propagation)
3. Clear browser cache (Ctrl+Shift+Delete)
4. Try in incognito window

### Issue: Database Connection Error

**Steps:**
1. Check PostgreSQL service exists
2. Verify DATABASE_URL is correct
3. Test connection:
   ```powershell
   # Try to connect (requires psql installed)
   psql "postgresql://user:pass@host:port/db"
   ```
4. If fails, redeploy the database

---

## ✅ VERIFICATION CHECKLIST

Before sharing your URL, verify:

- [ ] Project created in Railway
- [ ] GitHub repo connected
- [ ] Environment variables set (5 total):
  - [ ] OPENAI_API_KEY
  - [ ] LOG_LEVEL
  - [ ] AGENT_TIMEOUT
  - [ ] ENVIRONMENT
  - [ ] DB_PASSWORD
- [ ] PostgreSQL service added
- [ ] DATABASE_URL configured
- [ ] Build successful (green checkmark)
- [ ] Deployment running (green status)
- [ ] Public URL generated
- [ ] Health check responds: `curl /health` = 200 OK
- [ ] API docs accessible: `/docs` loads

---

## 🎯 NEXT: SHARE YOUR APP

Once verified, your app is LIVE!

**Share this URL:**
```
https://prompt-to-prod-prod-xxxx.railway.app
```

**Tell people:**
```
Try my AI DevOps Platform!

🌐 https://prompt-to-prod-prod-xxxx.railway.app

Features:
✨ Chat with AI for infrastructure automation
🚀 Deploy Kubernetes apps with natural language
📊 Full infrastructure monitoring included
🔧 Infrastructure as Code included

Try these:
- API Docs: /docs
- Health: /health
- Chat: POST /chat with {"query":"What is Kubernetes?"}

Open source: github.com/yourusername/prompt-to-prod
```

---

## 📊 MANAGING YOUR HOBBY PLAN

### Monthly Usage

**Track your costs:**
1. Go to Railway Dashboard
2. Click "Billing" (bottom left)
3. You see: "Usage" and "Credits"
4. Your $5 credit covers ~1-2 months typical usage

### If You Exceed Credits

**Options:**
1. Upgrade to Pro: $20/month
2. Or wait for next month
3. Or optimize your app (reduce RAM usage, etc.)

### Estimated Costs

| Scenario | Monthly Cost |
|----------|--------------|
| Dev/demo | $0 (with credit) |
| Small (10 users) | $2-3 |
| Medium (100 users) | $5-10 |
| Large (1000 users) | $20-50 |

---

## 🔄 AUTO-DEPLOY FROM GITHUB

**Enable auto-deployment:**

1. In Railway, go to project settings
2. Look for "GitHub" integration
3. Enable: "Auto-deploy on push to main"
4. Now every `git push` redeploys automatically

**Workflow:**
```powershell
# Make changes locally
git add .
git commit -m "Feature: Add new AI capability"

# Push to GitHub
git push origin main

# Railway automatically redeploys!
# Check deployment in 2-3 minutes
```

---

## 📝 IMPORTANT REMINDERS

1. **Don't commit `.env` file**
   - Use environment variables in Railway instead
   - Never push API keys to GitHub

2. **Keep API key secure**
   - Only in Railway environment
   - Not in code
   - Not in git history

3. **Monitor your usage**
   - Check Railway billing monthly
   - Set alerts if budget concerned
   - Optimize if needed

4. **Update regularly**
   - Push improvements to GitHub
   - Railway auto-deploys
   - Keep app current

---

## 🎉 YOU'RE DONE!

Your Prompt-to-Prod platform is LIVE on the web!

✅ Public URL created
✅ Anyone can access
✅ AI agent is working
✅ Database connected
✅ Monitoring included
✅ Auto-deploys on code push
✅ 24/7 uptime

---

## 📖 NEXT DOCUMENTATION

- **Monitor Logs**: View deployment logs in Railway
- **Scale Up**: Increase RAM if needed
- **Custom Domain**: Add your own domain (optional, $10/year)
- **GitHub Collaboration**: Invite team members
- **Security**: Rotate API keys regularly

---

**Your app is live! Share the URL and celebrate! 🚀🎉**
