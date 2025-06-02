from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import Config
import os
from werkzeug.utils import secure_filename

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

    # Create upload directories if they don't exist
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'workplace_logos'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'developer'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'library'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'chat_files'), exist_ok=True)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.user import user_bp
    from routes.booking import booking_bp
    from routes.workplace import workplace_bp
    from routes.developer import developer_bp
    from routes.premium import premium_bp
    from routes.password_reset import password_reset_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(booking_bp, url_prefix='/booking')
    app.register_blueprint(workplace_bp, url_prefix='/workplace')
    app.register_blueprint(developer_bp, url_prefix='/developer')
    app.register_blueprint(premium_bp, url_prefix='/premium')
    app.register_blueprint(password_reset_bp)
    
    # Main route
    from flask import redirect, url_for
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))
    
    # Workplace-specific registration route
    @app.route('/register/<workplace_url>')
    def workplace_registration(workplace_url):
        from models.workplace import Workplace
        workplace = Workplace.query.filter_by(unique_url=workplace_url).first_or_404()
        return redirect(url_for('auth.register', workplace_id=workplace.id))
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
