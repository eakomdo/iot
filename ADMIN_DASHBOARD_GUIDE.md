# 📊 Admin Dashboard Guide

## 🎯 **Your Admin Dashboard URL:**
**https://iot-khgd.onrender.com/admin/**

---

## 🔑 **What You'll See After Login:**

### **Main Sections:**
1. **SENSORS** section:
   - **Devices** - All your ESP32 and IoT devices
   - **ECG readings** - Heart rate data from ECG sensors  
   - **Pulse oximeter readings** - SpO2 and pulse data
   - **MAX30102 readings** - Heart rate and SpO2 from MAX30102 sensor
   - **Accelerometer readings** - X/Y/Z motion data
   - **Device statuses** - Battery, WiFi, temperature data

2. **AUTHENTICATION AND AUTHORIZATION**:
   - **Users** - Admin users (you can add more)
   - **Groups** - User permissions (advanced)

---

## 📱 **Viewing Your IoT Data:**

### **1. View All Devices:**
- Click **"Devices"** under SENSORS
- See all ESP32 devices that have connected
- Shows device ID, name, type, last seen time

### **2. View Sensor Readings:**
Click any of these to see data:
- **ECG readings** → Heart rate data
- **Pulse oximeter readings** → SpO2 percentage  
- **MAX30102 readings** → Heart rate + SpO2
- **Accelerometer readings** → Motion/orientation data
- **Device statuses** → Battery level, WiFi strength, etc.

### **3. Filter and Search:**
- Use the **filter panel** on the right to filter by device, date, etc.
- Use the **search box** to find specific readings
- Click **column headers** to sort data

---

## 🔍 **Monitoring Your Test Data:**

After running our tests, you should see:
- **1 Device**: "IoT Device TEST_ESP32_DEPLOYMENT"  
- **Multiple readings** from our test upload
- **Timestamps** showing when data was received

---

## 🚀 **Real ESP32 Data:**

Once you upload code to your actual ESP32:
- New device will appear automatically
- Real sensor data will flow in every 10 seconds
- You can track battery levels, WiFi strength, sensor values

---

## 💡 **Pro Tips:**

### **Add More Admin Users:**
- Go to **Users** → **Add User**
- Create accounts for team members
- Set permissions as needed

### **Export Data:**
- Select readings you want
- Choose **"Export selected..."** from Actions dropdown
- Get CSV files for analysis

### **Monitor in Real-Time:**
- Keep admin page open
- Refresh to see new data from ESP32
- Watch live sensor readings come in

---

## 🛠️ **Troubleshooting Admin Access:**

### **Can't Login?**
1. Make sure you created superuser in Render Shell
2. Check username/password spelling
3. Try password reset if needed

### **No Data Showing?**
1. Check if ESP32 is sending data
2. Verify WiFi connection on ESP32
3. Check Render logs for errors

### **Admin Page Won't Load?**
1. Check if your Render service is running
2. Try the direct URL: https://iot-khgd.onrender.com/admin/
3. Clear browser cache

---

## 🎯 **Your Admin Dashboard is Ready!**

**URL:** https://iot-khgd.onrender.com/admin/  
**Purpose:** Monitor all IoT sensor data in real-time  
**Features:** Filter, search, export, manage devices  

Once you create the superuser account, you'll have full access to monitor your IoT system! 🌟
