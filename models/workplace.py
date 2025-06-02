from app import db
from datetime import datetime
import secrets
import string

class Workplace(db.Model):
    __tablename__ = 'workplaces'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # Premium features
    logo_filename = db.Column(db.String(255))
    about = db.Column(db.Text)
    website = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    contact_email = db.Column(db.String(120))
    operating_hours = db.Column(db.String(100))
    
    # Multi-tenancy features
    unique_url = db.Column(db.String(50), unique=True)
    custom_domain = db.Column(db.String(100))
    email_sender = db.Column(db.String(120))  # Custom email sender
    email_password = db.Column(db.String(255))  # Encrypted email password
    
    # Admin management - separate foreign key for owner
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Relationships - specify foreign_keys to avoid ambiguity
    halls = db.relationship('Hall', backref='workplace', lazy=True, cascade='all, delete-orphan')
    
    # Owner relationship - specify foreign key explicitly to avoid ambiguity
    owner = db.relationship('User', foreign_keys=[owner_id], backref='owned_workplaces')
    
    def __init__(self, **kwargs):
        super(Workplace, self).__init__(**kwargs)
        if not self.unique_url:
            self.unique_url = self.generate_unique_url()
    
    def generate_unique_url(self):
        """Generate a unique URL for the workplace"""
        while True:
            url = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(8))
            if not Workplace.query.filter_by(unique_url=url).first():
                return url
    
    def get_registration_url(self):
        """Get the unique registration URL for this workplace"""
        return f"/register/{self.unique_url}"
    
    def has_premium_feature(self, feature):
        """Check if workplace has access to a premium feature"""
        # Import here to avoid circular imports
        from models.subscription import Subscription
        subscription = Subscription.query.filter_by(workplace_id=self.id, is_active=True).first()
        if subscription:
            return subscription.has_feature(feature)
        return False
    
    def __repr__(self):
        return f'<Workplace {self.name}>'
