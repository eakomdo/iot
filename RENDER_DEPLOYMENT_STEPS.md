# 🚀 Complete Render Deployment Guide

## Prerequisites Checklist ✅
- [ ] Render account created
- [ ] GitHub account created  
- [ ] Code pushed to GitHub repository
- [ ] All files are in the project directory

## Step 1: Prepare Your Code Repository

### Option A: Using GitHub Desktop (Easiest for beginners)
1. Download GitHub Desktop from: https://desktop.github.com/
2. Install and sign in with your GitHub account
3. Click "Add an Existing Repository from your Hard Drive"
4. Browse to `/home/eakomdo/Desktop/iot`
5. Click "Create Repository" → "Publish Repository"
6. Make sure "Keep this code private" is UNCHECKED (or you need paid GitHub)
7. Click "Publish Repository"

### Option B: Using Terminal Commands
```bash
# Navigate to your project
cd /home/eakomdo/Desktop/iot

# Initialize git repository
git init

# Add all files
git add .

# Make first commit
git commit -m "Initial IoT sensor system"

# Create GitHub repository (you'll need GitHub CLI or do this on GitHub.com)
# Go to github.com, click '+' → 'New repository'
# Name it: iot-sensor-system
# Don't initialize with README (you already have one)
# Copy the git remote add command they show you

# Add your GitHub repository as remote (replace with your actual repo URL)
git remote add origin https://github.com/YOUR_USERNAME/iot-sensor-system.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 2: Deploy on Render

### 2.1: Create New Web Service
1. Log into Render Dashboard
2. Click **"New +"** button
3. Select **"Web Service"**
4. Choose **"Build and deploy from a Git repository"**
5. Click **"Connect GitHub"** and authorize if needed

### 2.2: Connect Your Repository
1. Find your repository: `iot-sensor-system` (or whatever you named it)
2. Click **"Connect"**

### 2.3: Configure Web Service Settings
**Basic Settings:**
- **Name**: `iot-sensor-backend` (or any name you prefer)
- **Region**: Choose closest to your location
- **Branch**: `main`
- **Root Directory**: Leave empty (blank)

**Build & Deploy:**
- **Runtime**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn iot_backend.wsgi:application`

**Advanced Settings (Click "Advanced"):**
- **Auto-Deploy**: `Yes` (recommended)

### 2.4: Environment Variables
Click **"Add Environment Variable"** and add these one by one:

| Key | Value |
|-----|-------|
| `DJANGO_DEBUG` | `False` |
| `DJANGO_SECRET_KEY` | `your-super-secret-key-here-make-it-long-and-random` |
| `DATABASE_URL` | *(Leave empty - Render will auto-populate this)* |
| `DJANGO_ALLOWED_HOSTS` | `*` |

**To generate a secret key:**
1. Go to: https://djecrety.ir/
2. Copy the generated key
3. Use it for `DJANGO_SECRET_KEY`

### 2.5: Add PostgreSQL Database
1. Still in the service creation page, scroll down to **"Add Database"**
2. Click **"Add PostgreSQL"**
3. **Database Name**: `iot_sensor_db`
4. **Database User**: `iot_user`
5. Click **"Create Database"**

### 2.6: Deploy!
1. Click **"Create Web Service"**
2. Wait for deployment (usually 5-10 minutes)
3. Watch the logs - they should show:
   ```
   ==> Build successful 🎉
   ==> Starting service...
   ==> Your service is live 🎉
   ```

## Step 3: Verify Deployment

### 3.1: Check Your Live URL
1. In Render dashboard, you'll see your service URL like:
   `https://iot-sensor-backend-abc123.onrender.com`
2. Click on it to open your API

### 3.2: Test API Endpoints
Your API endpoints will be available at:
- **API Root**: `https://your-app-name.onrender.com/api/`
- **Devices**: `https://your-app-name.onrender.com/api/devices/`
- **Sensor Data**: `https://your-app-name.onrender.com/api/sensor-data/bulk/`
- **Admin Panel**: `https://your-app-name.onrender.com/admin/`

### 3.3: Create Admin User (Important!)
1. In Render Dashboard, go to your service
2. Click **"Shell"** tab
3. Run this command:
   ```bash
   python manage.py createsuperuser
   ```
4. Enter username, email, and password when prompted
5. Now you can access admin at: `https://your-app-name.onrender.com/admin/`

## Step 4: Update ESP32 Code

Update your ESP32 code to use the new Render URL:

```cpp
// Replace this line in your ESP32 code:
const char* serverURL = "http://localhost:8000/api/sensor-data/bulk/";

// With your actual Render URL:
const char* serverURL = "https://your-app-name.onrender.com/api/sensor-data/bulk/";
```

## Step 5: Monitor Your Application

### 5.1: View Logs
- In Render Dashboard → Your Service → **"Logs"** tab
- Watch for any errors or issues

### 5.2: Monitor Usage
- **"Metrics"** tab shows CPU, memory usage
- **"Events"** tab shows deployment history

### 5.3: Database Management
- Click on your PostgreSQL database
- Use **"Connect"** to get connection details
- Use tools like pgAdmin or DBeaver to manage data

## 🎉 You're Live!

Your IoT sensor system is now deployed and accessible worldwide!

**Your URLs:**
- **API**: `https://your-app-name.onrender.com/api/`
- **Admin**: `https://your-app-name.onrender.com/admin/`
- **Health Check**: `https://your-app-name.onrender.com/health/`

## Troubleshooting Common Issues

### Issue 1: Build Fails
- Check logs for error messages
- Ensure `build.sh` has execute permissions
- Verify `requirements.txt` is correct

### Issue 2: Database Connection Error
- Make sure PostgreSQL database is created
- Check that `DATABASE_URL` environment variable is set
- Verify database migrations ran successfully

### Issue 3: 500 Internal Server Error
- Check `DJANGO_SECRET_KEY` is set
- Ensure `DJANGO_DEBUG=False`
- Review application logs in Render dashboard

### Issue 4: ESP32 Can't Connect
- Verify the server URL in ESP32 code is correct
- Check if HTTPS is being used (Render uses HTTPS)
- Ensure your WiFi allows outbound HTTPS connections

## Need Help?
- Check Render's documentation: https://render.com/docs
- Review your application logs in Render dashboard
- Test API endpoints using tools like Postman
- Monitor the Health Check endpoint

## Free Tier Limitations
- 750 hours/month (about 30 days)
- Services sleep after 15 minutes of inactivity
- Database limited to 1GB storage
- Upgrade to paid plan for production use

---

**Congratulations! Your IoT sensor system is now live on the internet! 🌐**
