from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import re
import secrets

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_master_admin = db.Column(db.Boolean, default=False)  # Super admin
    is_workplace_admin = db.Column(db.Boolean, default=False)  # Workplace admin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key for workplace association
    workplace_id = db.Column(db.Integer, db.ForeignKey('workplaces.id'), nullable=True)
    
    # Password reset
    reset_token = db.Column(db.String(100), unique=True)
    reset_token_expires = db.Column(db.DateTime)
    
    # Relationships - specify foreign_keys to avoid ambiguity
    bookings = db.relationship('Booking', backref='user', lazy=True)
    attendance_records = db.relationship('Attendance', backref='user', lazy=True)
    
    # Workplace relationship - specify foreign key explicitly
    workplace = db.relationship('Workplace', foreign_keys=[workplace_id], backref='users')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_reset_token(self):
        """Generate a password reset token"""
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()
        return self.reset_token
    
    def verify_reset_token(self, token):
        """Verify if the reset token is valid"""
        return (self.reset_token == token and 
                self.reset_token_expires and 
                datetime.utcnow() < self.reset_token_expires)
    
    def clear_reset_token(self):
        """Clear the reset token after use"""
        self.reset_token = None
        self.reset_token_expires = None
        db.session.commit()
    
    @staticmethod
    def validate_phone_number(phone):
        # Nigerian phone number validation
        pattern = r'^(\+234|0)[789][01]\d{8}$'
        return re.match(pattern, phone) is not None
    
    def __repr__(self):
        return f'<User {self.username}>'
