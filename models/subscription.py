from app import db
from datetime import datetime, timedelta
from enum import Enum

class SubscriptionTier(Enum):
    BASIC = "basic"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    ULTIMATE = "ultimate"

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    workplace_id = db.Column(db.Integer, db.ForeignKey('workplaces.id'), nullable=False)
    tier = db.Column(db.Enum(SubscriptionTier), default=SubscriptionTier.BASIC)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    payment_reference = db.Column(db.String(100))
    amount_paid = db.Column(db.Float)
    currency = db.Column(db.String(3), default='NGN')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    workplace = db.relationship('Workplace', backref=db.backref('subscription', uselist=False))
    
    def is_expired(self):
        return datetime.utcnow() > self.end_date if self.end_date else False
    
    def days_remaining(self):
        if self.end_date:
            delta = self.end_date - datetime.utcnow()
            return max(0, delta.days)
        return 0
    
    def has_feature(self, feature):
        """Check if subscription tier has access to a feature"""
        features = {
            SubscriptionTier.BASIC: [
                'seat_booking', 'basic_attendance', 'limited_emails'
            ],
            SubscriptionTier.PROFESSIONAL: [
                'seat_booking', 'attendance_management', 'unlimited_emails',
                'basic_reporting', 'task_scheduling'
            ],
            SubscriptionTier.ENTERPRISE: [
                'seat_booking', 'attendance_management', 'unlimited_emails',
                'advanced_reporting', 'analytics', 'task_management',
                'workplace_chat', 'hall_chat', 'notifications'
            ],
            SubscriptionTier.ULTIMATE: [
                'seat_booking', 'attendance_management', 'unlimited_emails',
                'advanced_reporting', 'analytics', 'task_management',
                'workplace_chat', 'hall_chat', 'group_chat', 'chat_rooms',
                'library_management', 'advanced_notifications', 'ai_chatbot'
            ]
        }
        return feature in features.get(self.tier, [])

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    workplace_id = db.Column(db.Integer, db.ForeignKey('workplaces.id'), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.id'), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='NGN')
    payment_method = db.Column(db.String(50))  # paystack, flutterwave, etc.
    reference = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(20), default='pending')  # pending, success, failed
    gateway_response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workplace = db.relationship('Workplace', backref='payments')
    subscription = db.relationship('Subscription', backref='payments')

class MasterAccess(db.Model):
    __tablename__ = 'master_access'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(120))  # Master admin who granted access
