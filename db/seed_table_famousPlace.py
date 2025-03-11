import uuid
from sqlalchemy import create_engine, Column, String, Float, Boolean, MetaData, Table
from sqlalchemy.orm import declarative_base, sessionmaker

# Database setup
db_url = "postgresql://postgres:12345@localhost:5432/islapp"
engine = create_engine(db_url)
Base = declarative_base()
Session = sessionmaker(bind=engine)

def generate_uuid():
    return str(uuid.uuid4())

# Table definition
class FamousPlace(Base):
    __tablename__ = 'famous_places'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    image = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    video = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    most_popular = Column(Boolean, default=False, nullable=False)

# Insert data into table
def insert_famous_places():
    session = Session()
    try:
        places = [
            FamousPlace(
                image='https://winvinayafoundation.org/wp-content/uploads/2024/12/Santhome_Basilica.jpg',
                title='Santhome Cathedral Basilica',
                location='Chennai',
                latitude=13.0843,
                longitude=80.2705,
                video='https://winvinaya.com/wp-content/uploads/2024/11/Charminar_1_2.mp4',
                description='San Thome Church, officially known as St Thomas Cathedral Basilica and National Shrine of Saint Thomas, is a minor basilica of the Catholic Church in India, at the Santhome neighbourhood of Chennai, in Tamil Nadu.'
            ),
            FamousPlace(
                image='https://winvinayafoundation.org/wp-content/uploads/2024/12/lalbagh.jpg',
                title='Lalbagh Botanical Garden',
                location='Bengaluru',
                latitude=12.9716,
                longitude=77.5946,
                video='https://winvinaya.com/wp-content/uploads/2024/11/Charminar_1_2.mp4',
                description='It is a botanical garden in Bangalore, India, with an over 200-year history. First planned and laid out during the dalavaiship of King Hyder Ali, the garden was later managed under numerous British Superintendents before Indian Independence.'
            ),
            FamousPlace(
                image='https://winvinayafoundation.org/wp-content/uploads/2024/12/red_fort.jpg',
                title='Red Fort',
                location='Delhi',
                latitude=28.6139,
                longitude=77.2089,
                video='https://winvinaya.com/wp-content/uploads/2024/11/Charminar_1_2.mp4',
                description='A historic fort in the city of Delhi, known for its stunning Mughal architecture.'
            ),
            FamousPlace(
                image='https://winvinayafoundation.org/wp-content/uploads/2024/12/golden_temple.jpg',
                title='Golden Temple',
                location='Amritsar, Punjab',
                latitude=31.6200,
                longitude=74.8765,
                video='https://winvinaya.com/wp-content/uploads/2024/11/Charminar_1_2.mp4',
                description='The holiest Sikh gurdwara, known for its stunning gold-covered architecture and spiritual significance.'
            ),
            FamousPlace(
                image='https://winvinayafoundation.org/wp-content/uploads/2024/12/brihadeeshwara_temple.jpg',
                title='Brihadeeshwara Temple',
                location='Tanjavur, Tamil Nadu',
                latitude=10.7850,
                longitude=79.1320,
                video='https://winvinaya.com/wp-content/uploads/2024/11/Charminar_1_2.mp4',
                description='A UNESCO World Heritage site, known for its grand Dravidian architecture.'
            ),
            FamousPlace(
                image='https://winvinayafoundation.org/wp-content/uploads/2024/12/hawa_mahal.jpg',
                title='Hawa Mahal',
                location='Jaipur, Rajasthan',
                latitude=26.9238,
                longitude=75.8203,
                video='https://winvinaya.com/wp-content/uploads/2024/11/Charminar_1_2.mp4',
                description='A five-story palace in Jaipur, known for its intricate lattice work and history as a royal women’s palace.'
            ),
            FamousPlace(
                image='https://winvinayafoundation.org/wp-content/uploads/2024/12/sun_temple.jpg',
                title='Sun Temple',
                location='Konark, Odisha',
                latitude=20.2833,
                longitude=86.0920,
                video='https://winvinaya.com/wp-content/uploads/2024/11/Charminar_1_2.mp4',
                description='A UNESCO World Heritage site, famous for its stunning architectural design dedicated to the Sun God.'
            ),
            FamousPlace(
                image='https://winvinayafoundation.org/wp-content/uploads/2024/12/ajantha_caves.jpg',
                title='Ajanta Caves',
                location='Maharashtra',
                latitude=20.5984,
                longitude=75.7037,
                video='https://winvinaya.com/wp-content/uploads/2024/11/Charminar_1_2.mp4',
                description='Ancient Buddhist rock-cut caves, known for their exquisite paintings and sculptures.'
            ),
            FamousPlace(
                image='https://winvinayafoundation.org/wp-content/uploads/2024/12/india_gate.jpg',
                title='India Gate',
                location='Delhi',
                latitude=28.6129,
                longitude=77.2295,
                video='https://winvinaya.com/wp-content/uploads/2024/11/Charminar_1_2.mp4',
                description='A war memorial located in New Delhi, dedicated to the soldiers of India.'
            ),
            FamousPlace(
                image='https://winvinayafoundation.org/wp-content/uploads/2024/12/charminar.jpg',
                title='Charminar',
                location='Hyderabad, Telangana',
                latitude=17.3616,
                longitude=78.4747,
                video='https://winvinaya.com/wp-content/uploads/2024/11/Charminar_1_2.mp4',
                description='A historic mosque and monument, an iconic symbol of Hyderabad.'
            ),
            FamousPlace(
                image='https://winvinayafoundation.org/wp-content/uploads/2024/12/lotus_temple.jpg',
                title='Lotus Temple',
                location='Delhi',
                latitude=28.5535,
                longitude=77.2588,
                video='https://winvinaya.com/wp-content/uploads/2024/11/Charminar_1_2.mp4',
                description='A Baháʼí House of Worship, famous for its flowerlike architecture.'
            ),
            FamousPlace(
                image='https://winvinayafoundation.org/wp-content/uploads/2024/12/meenakshi_temple.jpg',
                title='Meenakshi Temple',
                location='Madurai, Tamil Nadu',
                latitude=9.9197,
                longitude=78.1194,
                video='https://winvinaya.com/wp-content/uploads/2024/11/Charminar_1_2.mp4',
                description='A historic Hindu temple dedicated to goddess Meenakshi, known for its gopurams and sculptures.'
            )
        ]
        session.bulk_save_objects(places)
        session.commit()
        print("Data inserted successfully.")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    insert_famous_places()
