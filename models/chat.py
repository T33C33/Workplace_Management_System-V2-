from app import db
from datetime import datetime
from enum import Enum

class ChatType(Enum):
    WORKPLACE = "workplace"
    HALL = "hall"
    GROUP = "group"
    PRIVATE = "private"
    ROOM = "room"

class ChatGroup(db.Model):
    __tablename__ = 'chat_groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    chat_type = db.Column(db.Enum(ChatType), nullable=False)
    workplace_id = db.Column(db.Integer, db.ForeignKey('workplaces.id'), nullable=False)
    hall_id = db.Column(db.Integer, db.ForeignKey('halls.id'), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    workplace = db.relationship('Workplace', backref='chat_groups')
    hall = db.relationship('Hall', backref='chat_groups')
    creator = db.relationship('User', backref='created_chat_groups')
    messages = db.relationship('ChatMessage', backref='chat_group', lazy=True)
    members = db.relationship('ChatMember', backref='chat_group', lazy=True)

class ChatMember(db.Model):
    __tablename__ = 'chat_members'
    
    id = db.Column(db.Integer, primary_key=True)
    chat_group_id = db.Column(db.Integer, db.ForeignKey('chat_groups.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='chat_memberships')

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    chat_group_id = db.Column(db.Integer, db.ForeignKey('chat_groups.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(20), default='text')  # text, image, file, system
    file_url = db.Column(db.String(255))
    reply_to_id = db.Column(db.Integer, db.ForeignKey('chat_messages.id'), nullable=True)
    is_edited = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='chat_messages')
    reply_to = db.relationship('ChatMessage', remote_side=[id], backref='replies')
