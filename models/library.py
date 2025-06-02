from app import db
from datetime import datetime

class LibraryItem(db.Model):
    __tablename__ = 'library_items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    item_type = db.Column(db.String(50))  # book, document, video, etc.
    file_url = db.Column(db.String(255))
    cover_image = db.Column(db.String(255))
    author = db.Column(db.String(100))
    workplace_id = db.Column(db.Integer, db.ForeignKey('workplaces.id'), nullable=False)
    hall_id = db.Column(db.Integer, db.ForeignKey('halls.id'), nullable=True)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_public = db.Column(db.Boolean, default=True)
    download_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    workplace = db.relationship('Workplace', backref='library_items')
    hall = db.relationship('Hall', backref='library_items')
    uploader = db.relationship('User', backref='uploaded_library_items')
