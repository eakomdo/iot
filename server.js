const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const WebSocket = require('ws');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Serve static files from frontend
app.use(express.static(path.join(__dirname, 'frontend/dist')));

// Initialize SQLite database
const db = new sqlite3.Database(':memory:', (err) => {
    if (err) {
        console.error('Error opening database:', err.message);
    } else {
        console.log('Connected to SQLite database.');
        initializeDatabase();
    }
});

// Create tables
function initializeDatabase() {
    const createTableQuery = `
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            sensor_type TEXT NOT NULL,
            value REAL,
            unit TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            raw_data TEXT
        )
    `;
    
    db.run(createTableQuery, (err) => {
        if (err) {
            console.error('Error creating table:', err.message);
        } else {
            console.log('Database table created successfully.');
        }
    });
}

// WebSocket server for real-time updates
const server = require('http').createServer(app);
const wss = new WebSocket.Server({ server });

wss.on('connection', (ws) => {
    console.log('New WebSocket connection established');
    
    ws.on('close', () => {
        console.log('WebSocket connection closed');
    });
});

// Broadcast data to all connected clients
function broadcastData(data) {
    wss.clients.forEach((client) => {
        if (client.readyState === WebSocket.OPEN) {
            client.send(JSON.stringify(data));
        }
    });
}

// API Routes

// Health check
app.get('/api/health', (req, res) => {
    res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// Get all sensor readings
app.get('/api/readings', (req, res) => {
    const query = `
        SELECT * FROM sensor_readings 
        ORDER BY timestamp DESC 
        LIMIT 100
    `;
    
    db.all(query, [], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json(rows);
    });
});

// Get readings by sensor type
app.get('/api/readings/:sensorType', (req, res) => {
    const { sensorType } = req.params;
    const query = `
        SELECT * FROM sensor_readings 
        WHERE sensor_type = ? 
        ORDER BY timestamp DESC 
        LIMIT 50
    `;
    
    db.all(query, [sensorType], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json(rows);
    });
});

// Post new sensor reading (for ESP32)
app.post('/api/readings', (req, res) => {
    const { device_id, sensor_type, value, unit, raw_data } = req.body;
    
    if (!device_id || !sensor_type || value === undefined) {
        return res.status(400).json({ 
            error: 'Missing required fields: device_id, sensor_type, value' 
        });
    }
    
    const query = `
        INSERT INTO sensor_readings (device_id, sensor_type, value, unit, raw_data)
        VALUES (?, ?, ?, ?, ?)
    `;
    
    db.run(query, [device_id, sensor_type, value, unit || '', raw_data || ''], function(err) {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        
        const newReading = {
            id: this.lastID,
            device_id,
            sensor_type,
            value,
            unit,
            raw_data,
            timestamp: new Date().toISOString()
        };
        
        // Broadcast to WebSocket clients
        broadcastData({
            type: 'new_reading',
            data: newReading
        });
        
        res.status(201).json(newReading);
    });
});

// Get latest readings for dashboard
app.get('/api/latest', (req, res) => {
    const query = `
        SELECT 
            sensor_type,
            value,
            unit,
            timestamp,
            device_id
        FROM sensor_readings 
        WHERE timestamp = (
            SELECT MAX(timestamp) 
            FROM sensor_readings sr2 
            WHERE sr2.sensor_type = sensor_readings.sensor_type
        )
        ORDER BY sensor_type
    `;
    
    db.all(query, [], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json(rows);
    });
});

// Delete all readings (for testing)
app.delete('/api/readings', (req, res) => {
    db.run('DELETE FROM sensor_readings', [], function(err) {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json({ message: `Deleted ${this.changes} readings` });
    });
});

// Catch-all handler for React app
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'frontend/dist/index.html'));
});

// Start server
server.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
    console.log(`WebSocket server also running on port ${PORT}`);
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\nShutting down server...');
    db.close((err) => {
        if (err) {
            console.error(err.message);
        }
        console.log('Database connection closed.');
        process.exit(0);
    });
});
