from app import db
from datetime import datetime

class Developer(db.Model):
    __tablename__ = 'developers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    github_url = db.Column(db.String(200))
    linkedin_url = db.Column(db.String(200))
    portfolio_url = db.Column(db.String(200))
    bio = db.Column(db.Text)
    skills = db.Column(db.Text)  # JSON string of skills
    profile_image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Developer {self.name}>'
