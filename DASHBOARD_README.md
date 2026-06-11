# Tunnel Exhaust System - Flask Dashboard

A comprehensive web-based dashboard for monitoring and analyzing tunnel exhaust system data in real-time.

## Features

### Page 1: Model Performance Metrics

- AQI Model accuracy, precision, recall, and F1 score
- Fan control model accuracy
- Detailed metrics comparison table
- Model information and specifications

### Page 2: Confusion Matrix

- Interactive heatmap visualization of the confusion matrix
- True Positives, False Positives, True Negatives, False Negatives
- Key metrics calculation (Sensitivity, Specificity, Precision, F1)
- Interpretation guide for confusion matrix results

### Page 3: Feature Importance

- Random Forest feature importance visualization
- Feature contribution percentages
- Detailed feature descriptions and analysis
- Model configuration details

### Page 4: Live Sensor Monitoring

- Real-time sensor data display (MQ2, MQ3, Temperature, Humidity)
- Multi-subplot visualization of all sensors
- Recent readings table
- Sensor specifications and information
- Data export functionality (CSV)
- Configurable refresh rates

## Project Structure

```
Tunnel_Exhaust_System/
├── app.py                      # Main Flask application
├── requirements_dashboard.txt   # Python dependencies
├── templates/
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Home page
│   ├── page1.html             # Model performance metrics
│   ├── page2.html             # Confusion matrix
│   ├── page3.html             # Feature importance
│   ├── page4.html             # Live sensor monitoring
│   ├── 404.html               # Error page
│   └── 500.html               # Error page
├── models/                     # Pre-trained ML models
├── results/                    # Model evaluation results
│   ├── real/
│   │   ├── classification_report.txt
│   │   └── feature_importance.csv
│   ├── synth/
│   │   ├── classification_report.txt
│   │   └── feature_importance.csv
│   └── classification_report.txt
├── data/                       # Sensor and training data
├── src/                        # Python source code
└── firmware/                   # ESP8266 firmware
```

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements_dashboard.txt
```

Or install individually:

```bash
pip install Flask==2.3.0
pip install pandas==2.0.0
pip install numpy==1.24.0
pip install plotly==5.14.0
pip install scikit-learn==1.2.0
pip install python-dotenv==1.0.0
```

### 2. Verify Directory Structure

Ensure you have the following directories in your project root:

```bash
mkdir -p templates
mkdir -p static
```

### 3. Prepare Data Files

Place your model evaluation results in the `results/` directory:

- `results/real/classification_report.txt` - Classification metrics for real data
- `results/real/feature_importance.csv` - Feature importance scores

## Running the Dashboard

### Start the Flask Server

```bash
python app.py
```

The dashboard will be available at: **http://localhost:5000**

### For Production Deployment

Use a production WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Configuration

### Sensor Data Sources

The dashboard can be configured to pull data from:

1. **MQTT Broker** - Real-time sensor data from ESP8266
2. **CSV Files** - Historical sensor data
3. **Database** - PostgreSQL, MongoDB, etc.

### Sample Data

By default, the dashboard generates sample sensor data. To integrate real data:

1. Modify `generate_live_sensor_data()` in `app.py` to read from MQTT/database
2. Update `load_model_metrics()` and `load_confusion_matrix()` to read actual model files

## API Endpoints

```
GET  /                           # Home page
GET  /page1                      # Model performance metrics
GET  /page2                      # Confusion matrix
GET  /page3                      # Feature importance
GET  /page4                      # Live sensor monitoring

API Endpoints:
GET  /api/page1/metrics          # Fetch model metrics as JSON
GET  /api/page2/confusion-matrix # Fetch confusion matrix visualization
GET  /api/page3/feature-importance # Fetch feature importance chart
GET  /api/page4/sensor-data      # Fetch live sensor data
GET  /api/page4/sensor-chart     # Fetch sensor chart visualization
```

## Features Explained

### Model Performance (Page 1)

- **Accuracy**: Percentage of correct predictions out of total predictions
- **Precision**: Of all positive predictions, how many were actually positive
- **Recall (Sensitivity)**: Of all actual positives, how many did we identify
- **F1 Score**: Harmonic mean of precision and recall

### Confusion Matrix (Page 2)

- **True Positives (TP)**: Correctly identified positive cases
- **False Positives (FP)**: Incorrectly identified as positive (false alarm)
- **True Negatives (TN)**: Correctly identified negative cases
- **False Negatives (FN)**: Incorrectly identified as negative (missed detection)

### Feature Importance (Page 3)

Shows how much each feature contributes to the Random Forest model's predictions:

- **MQ2_Raw**: Smoke and combustible gas sensor
- **MQ3_Raw**: Alcohol and vapor sensor
- **Temperature**: Environmental temperature
- **Humidity**: Environmental humidity

### Live Monitoring (Page 4)

Real-time visualization of all sensors with:

- Individual sensor graphs
- Data table with recent readings
- Customizable refresh rate
- CSV export functionality

## Sensor Information

### Gas Sensors (MQ Series)

- **MQ2**: Smoke and combustible gas detector (0-1023)
- **MQ3**: Alcohol and vapor detector (0-1023)
- Response time: ~30-60 seconds
- Both connect to ADC with 10-bit resolution

### Environmental Sensors

- **DHT11**: Temperature (-40 to 50°C) and Humidity (0-100%)
- Connected to GPIO2 (D4) on ESP8266
- Update rate: ~1 second

## Troubleshooting

### Dashboard not loading

1. Ensure Flask is running: `python app.py`
2. Check if port 5000 is available
3. Verify all template files are in the `templates/` directory

### Missing charts/data

1. Verify `results/` directory contains required CSV files
2. Check if `load_*` functions in `app.py` can access data files
3. Look at browser console for JavaScript errors (F12)

### MQTT connection issues

1. Ensure mosquitto broker is running
2. Check ESP8266 WiFi credentials and connection
3. Verify MQTT topic names match in firmware and Python code

## Browser Compatibility

- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Technologies Used

- **Backend**: Flask 2.3
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Visualization**: Plotly.js
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: scikit-learn
- **Microcontroller**: ESP8266 NodeMCU
- **Communication**: MQTT, WiFi

## Future Enhancements

- [ ] Real-time WebSocket updates
- [ ] Historical data database
- [ ] Alert/notification system
- [ ] Model retraining interface
- [ ] Data export (PDF reports)
- [ ] Multi-user authentication
- [ ] Dark mode theme
- [ ] Mobile-responsive improvements

## License

Your License Here

## Support

For issues or questions, please refer to the project documentation or contact the development team.
