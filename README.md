# IoT Sensor Data Collection System

A Django REST API backend for collecting and storing data from ESP32-based IoT devices with multiple health sensors.

## Supported Sensors

- **ECG (Electrocardiogram)** - Heart electrical activity monitoring
- **Pulse Oximeter** - Blood oxygen saturation and pulse rate
- **MAX30102** - Heart rate and SpO2 sensor
- **Accelerometer** - Motion and orientation detection
- **ESP32** - WiFi/Bluetooth enabled microcontroller

## Features

- RESTful API for sensor data collection
- Bulk data endpoint for efficient ESP32 communication
- Device management and monitoring
- Real-time sensor readings storage
- Device status tracking (battery, WiFi signal, etc.)
- Admin interface for data visualization
- PostgreSQL database support for production
- Ready for Render deployment

## API Endpoints

### Main Endpoints
- `GET /api/` - API overview and documentation
- `POST /api/sensors/bulk/` - Bulk sensor data submission (for ESP32)
- `GET /api/devices/{device_id}/readings/` - Get all readings for a device

### Device Management
- `GET /api/devices/` - List all devices
- `POST /api/devices/` - Create new device
- `GET /api/devices/{device_id}/` - Get device details

### Individual Sensor Endpoints
- `GET/POST /api/sensors/ecg/` - ECG readings
- `GET/POST /api/sensors/pulse-oximeter/` - Pulse oximeter readings
- `GET/POST /api/sensors/max30102/` - MAX30102 readings
- `GET/POST /api/sensors/accelerometer/` - Accelerometer readings
- `GET/POST /api/sensors/status/` - Device status readings

## Deployment on Render

### Method 1: Using render.yaml (Recommended)

1. **Fork or clone this repository**
2. **Connect to Render:**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file

3. **Configure Environment Variables** (if needed):
   - `SECRET_KEY` - Automatically generated
   - `DEBUG` - Set to `false` for production

### Method 2: Manual Setup

1. **Create PostgreSQL Database:**
   - In Render dashboard: New → PostgreSQL
   - Name: `iot-database`
   - Region: Choose closest to your location
   - Copy the database URL

2. **Create Web Service:**
   - New → Web Service
   - Connect your repository
   - Settings:
     - **Build Command:** `./build.sh`
     - **Start Command:** `gunicorn iot_backend.wsgi:application`
     - **Environment Variables:**
       - `DATABASE_URL`: [Your PostgreSQL URL]
       - `SECRET_KEY`: [Generate a secure key]
       - `DEBUG`: `false`

### Local Development

1. **Clone the repository:**
```bash
git clone [your-repo-url]
cd iot
```

2. **Create virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run migrations:**
```bash
python manage.py migrate
```

5. **Create superuser (optional):**
```bash
python manage.py createsuperuser
```

6. **Run development server:**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## ESP32 Setup

1. **Hardware Requirements:**
   - ESP32 development board
   - ECG sensor module (e.g., AD8232)
   - MAX30102 sensor
   - Pulse oximeter sensor
   - Accelerometer (e.g., MPU6050)
   - Breadboard and jumper wires

2. **Arduino IDE Setup:**
   - Install ESP32 board package
   - Install required libraries:
     - ArduinoJson
     - WiFi (built-in)
     - HTTPClient (built-in)
     - Wire (built-in)

3. **Upload Code:**
   - Open `esp32_sensor_code.ino` in Arduino IDE
   - Update WiFi credentials
   - Update API endpoint URL (your Render app URL)
   - Upload to ESP32

## Data Format

The ESP32 sends data to `/api/sensors/bulk/` endpoint with this JSON format:

```json
{
  "device_id": "ESP32_001",
  "ecg_heart_rate": 75.0,
  "ecg_value": 123.45,
  "ecg_signal_quality": "good",
  "spo2": 98.5,
  "pulse_heart_rate": 74.0,
  "pulse_signal_strength": 85,
  "max30102_heart_rate": 76.0,
  "max30102_spo2": 97.2,
  "red_value": 12345,
  "ir_value": 67890,
  "temperature": 36.8,
  "x_axis": 0.1,
  "y_axis": 0.2,
  "z_axis": 9.8,
  "magnitude": 9.82,
  "battery_level": 85.0,
  "wifi_signal_strength": -45,
  "memory_usage": 45.2,
  "cpu_temperature": 42.1,
  "uptime_seconds": 3600
}
```

## Database Models

- **Device** - IoT device information
- **ECGReading** - ECG sensor data
- **PulseOximeterReading** - Pulse oximeter data
- **MAX30102Reading** - MAX30102 sensor data
- **AccelerometerReading** - Accelerometer data
- **DeviceStatus** - Device health monitoring

## API Testing

Test the bulk endpoint with curl:

```bash
curl -X POST https://your-app.onrender.com/api/sensors/bulk/ \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "TEST_001",
    "ecg_heart_rate": 75.0,
    "spo2": 98.5,
    "x_axis": 0.1,
    "y_axis": 0.2,
    "z_axis": 9.8,
    "battery_level": 85.0
  }'
```

## Admin Interface

Access the Django admin at: `https://your-app.onrender.com/admin/`

Create a superuser to access the admin interface:
```bash
python manage.py createsuperuser
```

## Environment Variables

- `SECRET_KEY` - Django secret key (auto-generated on Render)
- `DEBUG` - Set to `false` in production
- `DATABASE_URL` - PostgreSQL database URL (auto-set by Render)
- `WEB_CONCURRENCY` - Number of gunicorn workers (default: 4)

## Security Features

- CORS enabled for IoT device communication
- HTTPS enforced in production
- Security headers configured
- Database connection encryption
- Secret key management

## Monitoring

- Device last seen timestamps
- Battery level monitoring
- WiFi signal strength tracking
- Memory and CPU usage monitoring
- Sensor data quality indicators

## Troubleshooting

### Common Issues:

1. **ESP32 can't connect to WiFi:**
   - Check WiFi credentials
   - Verify network compatibility (2.4GHz)

2. **HTTP requests failing:**
   - Verify API endpoint URL
   - Check HTTPS certificate
   - Ensure proper JSON format

3. **Database errors:**
   - Run migrations: `python manage.py migrate`
   - Check DATABASE_URL environment variable

4. **Render deployment issues:**
   - Check build logs in Render dashboard
   - Verify all environment variables are set
   - Ensure PostgreSQL database is connected

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## License

This project is open source and available under the [MIT License](LICENSE).
