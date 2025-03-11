import uuid
from datetime import datetime
from sqlalchemy import create_engine, Column, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Database setup
db_url = "postgresql://postgres:12345@localhost:5432/islapp"
engine = create_engine(db_url)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Utility function to generate UUID
def generate_uuid():
    return str(uuid.uuid4())

# Users table
class Users(Base):
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    recents = relationship('Recent', back_populates='user')

# FamousPlaces table
class FamousPlaces(Base):
    __tablename__ = 'famous_places'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    recents = relationship('Recent', back_populates='famous_place')

# Recent table
class Recent(Base):
    __tablename__ = 'recent'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    famous_place_id = Column(String(36), ForeignKey('famous_places.id'), nullable=False)
    searched_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('Users', back_populates='recents')
    famous_place = relationship('FamousPlaces', back_populates='recents')

# Insert records into the `recent` table
def insert_records_to_recent():
    session = Session()
    try:
        # Fetch user IDs from the users table
        user_ids = session.query(Users.id).all()
        famous_place_ids = session.query(FamousPlaces.id).all()

        # Flatten results to get a list of IDs
        user_ids = [u[0] for u in user_ids]
        famous_place_ids = [fp[0] for fp in famous_place_ids]

        if not user_ids or not famous_place_ids:
            print("No data found in users or famous_places table.")
            return

        # Insert records into recent table
        recents = []
        for user_id in user_ids:
            for famous_place_id in famous_place_ids:
                recents.append(
                    Recent(user_id=user_id, famous_place_id=famous_place_id)
                )

        session.bulk_save_objects(recents)
        session.commit()
        print(f"{len(recents)} records inserted into the `recent` table.")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    # Ensure the table is created before inserting records
    Base.metadata.create_all(engine)
    insert_records_to_recent()
