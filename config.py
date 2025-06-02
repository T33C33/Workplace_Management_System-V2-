import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Database Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    
    # Database URL - SQLite for development, MySQL/PostgreSQL for production
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///workplace_management.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email Configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'teeceeiheukwumere@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'qkqt vffv ksfb gnqp'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME') or 'teeceeiheukwumere@gmail.com'
    
    # Payment Configuration
    PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY') or 'sk_test_your_key_here'
    PAYSTACK_PUBLIC_KEY = os.environ.get('PAYSTACK_PUBLIC_KEY') or 'pk_test_your_key_here'
    
    # AI Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') or 'your-openai-key-here'
    
    # Application Configuration
    BASE_URL = os.environ.get('BASE_URL') or 'http://localhost:5000'
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'static/uploads'
