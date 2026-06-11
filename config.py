"""
Configuration file for Flask Dashboard
"""
import os

class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    JSON_SORT_KEYS = False
    
    # Flask settings
    FLASK_ENV = 'production'
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RESULTS_DIR = os.path.join(BASE_DIR, 'results')
    MODELS_DIR = os.path.join(BASE_DIR, 'models')
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    
    # MQTT Settings (if using real-time data)
    MQTT_SERVER = os.environ.get('MQTT_SERVER', '192.168.0.233')
    MQTT_PORT = int(os.environ.get('MQTT_PORT', 1883))
    MQTT_TOPIC = os.environ.get('MQTT_TOPIC', 'tunnel/sensors')
    
    # Database Settings (optional)
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///tunnel_data.db')
    
    # Sensor Settings
    SENSOR_REFRESH_INTERVAL = int(os.environ.get('SENSOR_REFRESH_INTERVAL', 5000))  # milliseconds
    SENSOR_HISTORY_SIZE = int(os.environ.get('SENSOR_HISTORY_SIZE', 60))  # number of readings
    
    # Model Settings
    MODEL_TYPE = os.environ.get('MODEL_TYPE', 'random_forest')
    AQI_THRESHOLD = float(os.environ.get('AQI_THRESHOLD', 0.5))
    FAN_MIN_SPEED = int(os.environ.get('FAN_MIN_SPEED', 0))
    FAN_MAX_SPEED = int(os.environ.get('FAN_MAX_SPEED', 255))
    
    # Thresholds for sensor alerts
    MQ2_WARNING_THRESHOLD = int(os.environ.get('MQ2_WARNING_THRESHOLD', 200))
    MQ2_CRITICAL_THRESHOLD = int(os.environ.get('MQ2_CRITICAL_THRESHOLD', 500))
    MQ3_WARNING_THRESHOLD = int(os.environ.get('MQ3_WARNING_THRESHOLD', 150))
    MQ3_CRITICAL_THRESHOLD = int(os.environ.get('MQ3_CRITICAL_THRESHOLD', 400))
    
    TEMP_MIN = int(os.environ.get('TEMP_MIN', 10))
    TEMP_MAX = int(os.environ.get('TEMP_MAX', 40))
    
    HUMIDITY_MIN = int(os.environ.get('HUMIDITY_MIN', 20))
    HUMIDITY_MAX = int(os.environ.get('HUMIDITY_MAX', 90))


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    """Get configuration object"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    return config.get(config_name, config['default'])
