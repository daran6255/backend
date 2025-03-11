from sqlalchemy import Column, String, DateTime, Boolean
from datetime import datetime
import uuid
from ..database import db
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = 'users'  # Maps the model to the 'users' table

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    differently_abled = db.Column(db.Boolean, nullable=False)
    avatar = db.Column(db.String(255), nullable=True)
    
    recents = relationship('Recent', back_populates='user')

