from app.database import db
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, Float, Boolean, ForeignKey

class FamousPlaces(db.Model):
    __tablename__ = 'famous_places'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # Use UUID for primary key
    image = db.Column(db.String(255), nullable=False)  
    title = db.Column(db.String(255), nullable=False)  
    location = db.Column(db.String(255), nullable=False) 
    latitude = db.Column(db.Float, nullable=False) 
    longitude = db.Column(db.Float, nullable=False)  
    video = db.Column(db.String(255), nullable=False)  
    description = db.Column(db.String(255), nullable=False)
    most_popular = db.Column(db.Boolean, default=False, nullable=False)  # Add a boolean column to mark most popular records
    
    recents = relationship('Recent', back_populates='famous_place')