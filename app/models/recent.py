from sqlalchemy import Column, String, ForeignKey, DateTime
from datetime import datetime
from ..database import db
from .user import User  
from .famous_place import FamousPlaces
import uuid

class Recent(db.Model):
    __tablename__ = 'recent'  
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)  
    famous_place_id = Column(String(36), ForeignKey('famous_places.id'), nullable=False)  
    searched_at = Column(DateTime, default=datetime.utcnow)  

    # Relationships
    user = db.relationship('User', back_populates='recents')
    famous_place = db.relationship('FamousPlaces', back_populates='recents')

    def __repr__(self):
        return f"<Recent user_id={self.user_id}, famous_place_id={self.famous_place_id}, searched_at={self.searched_at}>"

User.recents = db.relationship('Recent', back_populates='user', lazy=True)
FamousPlaces.recents = db.relationship('Recent', back_populates='famous_place', lazy=True)
