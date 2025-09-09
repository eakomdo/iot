from fastapi import FastAPI, Response
import uvicorn

app = FastAPI()

@app.get("/get_device_values")
async def get_device_values():
    """Get current IoT device sensor values"""
    # This will return the latest sensor readings
    return {"status": "waiting_for_sensors"}

@app.post("/post_sensor_data") 
async def post_sensor_data(sensor_data: dict):
    """Receive sensor data from IoT devices"""
    
    # Extract sensor values
    ecg = sensor_data.get("ecg_heart_rate", 0)
    spo2 = sensor_data.get("spo2", 0) 
    pulse = sensor_data.get("pulse_heart_rate", 0)
    max30102 = sensor_data.get("max30102_heart_rate", 0)
    x_axis = sensor_data.get("x_axis", 0)
    y_axis = sensor_data.get("y_axis", 0)
    z_axis = sensor_data.get("z_axis", 0)
    
    # Process the sensor data
    print(f"ECG: {ecg}, SpO2: {spo2}, Pulse: {pulse}")
    print(f"MAX30102: {max30102}")
    print(f"Accelerometer: X={x_axis}, Y={y_axis}, Z={z_axis}")
    
    # Return just the values (like your blood values example)
    if ecg > 0 or spo2 > 0 or max30102 > 0:
        return f"{ecg}\n{spo2}\n{pulse}\n{max30102}\n{x_axis}\n{y_axis}\n{z_axis}"
    else:
        return "WAITING_FOR_SENSORS"

@app.get("/ecg")
async def get_ecg():
    """Get ECG heart rate value"""
    # Return current ECG reading
    return {"ecg_heart_rate": 0}  # Will be filled by real sensor

@app.get("/spo2") 
async def get_spo2():
    """Get SpO2 oxygen saturation value"""
    # Return current SpO2 reading
    return {"spo2": 0}  # Will be filled by real sensor

@app.get("/accelerometer")
async def get_accelerometer():
    """Get accelerometer values"""
    # Return current accelerometer readings
    return {"x_axis": 0, "y_axis": 0, "z_axis": 0}  # Will be filled by real sensor

@app.get("/all_sensors")
async def get_all_sensors():
    """Get all sensor values at once"""
    return {
        "ecg_heart_rate": 0,
        "spo2": 0,
        "pulse_heart_rate": 0, 
        "max30102_heart_rate": 0,
        "x_axis": 0,
        "y_axis": 0,
        "z_axis": 0
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3443)
