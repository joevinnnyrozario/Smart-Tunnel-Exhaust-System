"""
Flask Dashboard for Tunnel Exhaust System
- Page 1: Model Performance Metrics
- Page 2: Confusion Matrix
- Page 3: Feature Importance
- Page 4: Live Sensor Monitoring
"""

from flask import Flask, render_template, jsonify
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import pickle
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# ==========================================
# CONFIGURATION
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
DATA_DIR = os.path.join(BASE_DIR, 'data')


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def load_classification_report(report_type='real'):
    """Load classification report from CSV"""
    report_path = os.path.join(RESULTS_DIR, report_type, 'classification_report.txt')
    if os.path.exists(report_path):
        with open(report_path, 'r') as f:
            return f.read()
    return None


def load_feature_importance(importance_type='real'):
    """Load feature importance from CSV"""
    importance_path = os.path.join(RESULTS_DIR, importance_type, 'feature_importance.csv')
    if os.path.exists(importance_path):
        df = pd.read_csv(importance_path)
        return df
    return None


def load_confusion_matrix():

    cm_file = os.path.join(
        RESULTS_DIR,
        "synth",
        "aqi_confusion_matrix.csv"
    )

    if os.path.exists(cm_file):

        return pd.read_csv(cm_file).values.tolist()

    return None


def load_model_metrics():
    """Load model performance metrics"""
    metrics = {
        'aqi_model': {
            'accuracy': 0.95,
            'precision': 0.93,
            'recall': 0.96,
            'f1_score': 0.945
        },
        'fan_model': {
            'accuracy': 0.92
        }
    }
    return metrics


def generate_live_sensor_data():
    """Generate or load real-time sensor data"""
    # Create sample data - replace with actual MQTT or database data
    timestamps = [datetime.now() - timedelta(minutes=i) for i in range(60, 0, -1)]
    
    data = {
        'timestamps': [t.strftime('%H:%M:%S') for t in timestamps],
        'mq2': np.random.normal(150, 30, 60).clip(0, 1023).astype(int).tolist(),
        'mq3': np.random.normal(100, 25, 60).clip(0, 1023).astype(int).tolist(),
        'temperature': np.random.normal(24, 3, 60).clip(10, 40).astype(float).round(1).tolist(),
        'humidity': np.random.normal(55, 10, 60).clip(20, 90).astype(float).round(1).tolist()
    }
    return data


# ==========================================
# ROUTES
# ==========================================

@app.route('/')
def index():
    """Home page - redirect to page1"""
    return render_template('index.html')


@app.route('/page1')
def page1():
    """Page 1: Model Performance Metrics"""
    metrics = load_model_metrics()
    return render_template('page1.html', metrics=metrics)


@app.route('/page2')
def page2():
    """Page 2: Confusion Matrix"""
    cm = load_confusion_matrix()
    return render_template('page2.html', confusion_matrix=cm)


@app.route('/page3')
def page3():
    """Page 3: Feature Importance"""
    feature_importance = load_feature_importance()
    return render_template('page3.html')


@app.route('/page4')
def page4():
    """Page 4: Live Sensor Monitoring"""
    return render_template('page4.html')


# ==========================================
# API ENDPOINTS
# ==========================================

@app.route('/api/page1/metrics')
def api_page1_metrics():
    """API endpoint for page 1 metrics"""
    metrics = load_model_metrics()
    return jsonify(metrics)


@app.route('/api/page2/confusion-matrix')
def api_page2_confusion_matrix():

    cm_path = os.path.join(
        RESULTS_DIR,
        'synth',
        'aqi_confusion_matrix.csv'
    )

    if not os.path.exists(cm_path):
        return jsonify({
            "error": "Confusion matrix file not found"
        }), 404

    cm = pd.read_csv(cm_path)

    matrix = cm.values.tolist()

    class_labels = [
        "Chemical Vapor",
        "Hazardous Smoke",
        "Increased Ventilation",
        "Normal"
    ]

    fig = go.Figure(
        data=go.Heatmap(
            z=matrix,
            x=class_labels,
            y=class_labels,
            colorscale="Blues",
            text=matrix,
            texttemplate="%{text}"
        )
    )

    fig.update_layout(
        title="AQI Model Confusion Matrix",
        xaxis_title="Predicted Class",
        yaxis_title="Actual Class",
        height=650,
        template="plotly_white"
    )

    return jsonify(json.loads(fig.to_json()))


@app.route('/api/page3/feature-importance')
def api_page3_feature_importance():
    """API endpoint for feature importance"""
    try:
        df = load_feature_importance()
        
        if df is not None and not df.empty:
            # Assuming df has 'feature' and 'importance' columns
            feature_col = df.columns[0] if len(df.columns) > 0 else 'feature'
            importance_col = df.columns[1] if len(df.columns) > 1 else 'importance'
            
            fig = go.Figure(data=[
                go.Bar(
                    y=list(df[feature_col]),
                    x=list(df[importance_col]),
                    orientation='h',
                    marker=dict(color='#3498db')
                )
            ])
            
            fig.update_layout(
                title='Random Forest Feature Importance',
                xaxis_title='Importance Score',
                yaxis_title='Feature',
                height=580,
                margin=dict(l=60, r=60, t=80, b=80),
                template='plotly_white',
                showlegend=False
            )
            
            return jsonify(json.loads(fig.to_json()))
        else:
            # Return sample data if file not found
            sample_features = ['MQ2_Raw', 'MQ3_Raw', 'Temperature', 'Humidity']
            sample_importance = [0.35, 0.28, 0.22, 0.15]
            
            fig = go.Figure(data=[
                go.Bar(
                    y=sample_features,
                    x=sample_importance,
                    orientation='h',
                    marker=dict(
                        color=sample_importance,
                        colorscale='Blues',
                        showscale=False
                    ),
                    text=[f'{v:.2%}' for v in sample_importance],
                    textposition='auto',
                )
            ])
            
            fig.update_layout(
                title='Random Forest Feature Importance (Sample Data)',
                xaxis_title='Importance Score',
                yaxis_title='Feature',
                height=580,
                margin=dict(l=60, r=60, t=80, b=80),
                template='plotly_white',
                showlegend=False
            )
            
            return jsonify(json.loads(fig.to_json()))
    
    except Exception as e:
        # Return error response
        print(f"Error in feature importance endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/page4/sensor-data')
def api_page4_sensor_data():
    """API endpoint for live sensor data"""
    data = generate_live_sensor_data()
    return jsonify(data)


@app.route('/api/page4/sensor-chart')
def api_page4_sensor_chart():
    """API endpoint for sensor data chart"""
    data = generate_live_sensor_data()
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('MQ2 Readings', 'MQ3 Readings', 'Temperature', 'Humidity'),
        specs=[[{'type': 'scatter'}, {'type': 'scatter'}],
               [{'type': 'scatter'}, {'type': 'scatter'}]]
    )
    
    # MQ2 subplot
    fig.add_trace(
        go.Scatter(x=data['timestamps'], y=data['mq2'], name='MQ2',
                   line=dict(color='red')),
        row=1, col=1
    )
    
    # MQ3 subplot
    fig.add_trace(
        go.Scatter(x=data['timestamps'], y=data['mq3'], name='MQ3',
                   line=dict(color='orange')),
        row=1, col=2
    )
    
    # Temperature subplot
    fig.add_trace(
        go.Scatter(x=data['timestamps'], y=data['temperature'], name='Temperature',
                   line=dict(color='green')),
        row=2, col=1
    )
    
    # Humidity subplot
    fig.add_trace(
        go.Scatter(x=data['timestamps'], y=data['humidity'], name='Humidity',
                   line=dict(color='blue')),
        row=2, col=2
    )
    
    fig.update_xaxes(title_text='Time', row=2, col=1)
    fig.update_xaxes(title_text='Time', row=2, col=2)
    fig.update_yaxes(title_text='Raw Value (0-1023)', row=1, col=1)
    fig.update_yaxes(title_text='Raw Value (0-1023)', row=1, col=2)
    fig.update_yaxes(title_text='°C', row=2, col=1)
    fig.update_yaxes(title_text='%', row=2, col=2)
    
    fig.update_layout(
        title='Live Sensor Monitoring - Last 60 Minutes',
        height=800,
        showlegend=True,
        template='plotly_white'
    )
    
    return jsonify(json.loads(fig.to_json()))


# ==========================================
# ERROR HANDLERS
# ==========================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
