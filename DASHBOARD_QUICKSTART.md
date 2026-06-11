# Flask Dashboard - Quick Start Guide

## What Was Created

I've created a complete Flask-based dashboard for your Tunnel Exhaust System with 4 pages and full visualization support.

## Files Created

### Main Application

- **app.py** - Main Flask application with all routes and API endpoints
- **config.py** - Configuration management for different environments
- **.env.example** - Environment variables template

### Templates (HTML)

- **templates/base.html** - Base template with navigation bar and styling
- **templates/index.html** - Home/landing page
- **templates/page1.html** - Model Performance Metrics
- **templates/page2.html** - Confusion Matrix Visualization
- **templates/page3.html** - Feature Importance Analysis
- **templates/page4.html** - Live Sensor Monitoring
- **templates/404.html** - Error page (not found)
- **templates/500.html** - Error page (server error)

### Configuration & Scripts

- **requirements_dashboard.txt** - Python dependencies
- **run_dashboard.bat** - Windows launcher script
- **run_dashboard.sh** - Linux/Mac launcher script
- **DASHBOARD_README.md** - Complete documentation

## Quick Start

### Option 1: Windows

```bash
run_dashboard.bat
```

### Option 2: Linux/Mac

```bash
chmod +x run_dashboard.sh
./run_dashboard.sh
```

### Option 3: Manual

```bash
pip install -r requirements_dashboard.txt
python app.py
```

Then open: **http://localhost:5000**

## Page Descriptions

### Page 1: Model Performance Metrics

- AQI Model: Accuracy, Precision, Recall, F1 Score
- Fan Control Model: Accuracy
- Detailed metrics table
- Model information cards

### Page 2: Confusion Matrix

- Interactive heatmap visualization
- True Positives, False Positives, True Negatives, False Negatives
- Calculated metrics (Sensitivity, Specificity, Precision, F1)
- Comprehensive explanation of each metric

### Page 3: Feature Importance

- Horizontal bar chart showing feature contributions
- Feature descriptions and explanations
- Statistics table with importance scores
- Random Forest model details

### Page 4: Live Sensor Monitoring

- Real-time metric cards (MQ2, MQ3, Temperature, Humidity)
- 4-subplot visualization showing all sensors over time
- Data table with recent readings
- CSV export functionality
- Configurable refresh rate (1-60 seconds)
- Sensor specifications

## Features Included

✅ Responsive Bootstrap 5 design
✅ Interactive Plotly charts
✅ Real-time data visualization
✅ CSV data export
✅ Error handling (404, 500 pages)
✅ Navigation bar with page links
✅ Auto-refreshing metrics
✅ Professional styling with gradients
✅ Metric cards with hover effects
✅ Data tables with sorting
✅ Sensor specifications
✅ Model information

## Integration Points

To connect real data, modify these functions in `app.py`:

1. **load_model_metrics()** - Load from your trained models
2. **load_confusion_matrix()** - Load from evaluation results
3. **load_feature_importance()** - Read from `results/real/feature_importance.csv`
4. **generate_live_sensor_data()** - Connect to MQTT or database

## Environment Variables

Create a `.env` file based on `.env.example`:

```bash
FLASK_ENV=development
MQTT_SERVER=192.168.0.233
MQTT_PORT=1883
SENSOR_REFRESH_INTERVAL=5000
```

## Troubleshooting

### Port 5000 already in use

```bash
python app.py --port 5001
```

### Module not found error

```bash
pip install -r requirements_dashboard.txt
```

### Missing feature_importance.csv

- Ensure `results/real/` directory exists
- Run your training pipeline first
- Or modify `load_feature_importance()` to use sample data

## Next Steps

1. **Connect MQTT data** - Modify `generate_live_sensor_data()` to read from your ESP8266
2. **Load real model metrics** - Update `load_model_metrics()` from your trained models
3. **Database integration** - Optional: Store historical data in database
4. **Authentication** - Add Flask-Login for multi-user access
5. **Deployment** - Use Gunicorn for production deployment

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Tech Stack

- **Backend**: Flask 2.3
- **Frontend**: Bootstrap 5, Plotly.js, HTML5/CSS3
- **Data**: Pandas, NumPy
- **ML**: scikit-learn
- **Server**: Development (Flask), Production (Gunicorn)

## File Structure After Creation

```
Tunnel_Exhaust_System/
├── app.py
├── config.py
├── .env.example
├── requirements_dashboard.txt
├── run_dashboard.bat
├── run_dashboard.sh
├── DASHBOARD_README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── page1.html
│   ├── page2.html
│   ├── page3.html
│   ├── page4.html
│   ├── 404.html
│   └── 500.html
├── results/
│   ├── real/
│   │   ├── feature_importance.csv (needed)
│   │   └── classification_report.txt (needed)
│   └── synth/
├── models/
├── data/
└── src/
```

## Support & Documentation

- See **DASHBOARD_README.md** for detailed documentation
- Check inline code comments in **app.py** for implementation details
- Review Bootstrap documentation: https://getbootstrap.com/
- Plotly documentation: https://plotly.com/

Enjoy your dashboard! 🚀
