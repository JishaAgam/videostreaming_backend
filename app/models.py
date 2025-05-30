from app import db 
from datetime import datetime


class vidoe_space(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_name = db.Column(db.String(100), nullable=False)
    thumbnail_img = db.Column(db.String(100), nullable=False)
    vidoe_title = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class continue_play(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Float, nullable=True)
    video_id = db.Column(db.Integer, db.ForeignKey('vidoe_space.id'), nullable=False)  # Foreign key
    video = db.relationship('vidoe_space', backref=db.backref('continue_video', cascade="all, delete-orphan", lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

