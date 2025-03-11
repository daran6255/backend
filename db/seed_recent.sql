CREATE TABLE recent (
    id SERIAL PRIMARY KEY,  
    user_id INTEGER NOT NULL,  
    image VARCHAR(255) NOT NULL,  
    title VARCHAR(100) NOT NULL,  
    location VARCHAR(100) NOT NULL,  
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,  
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
INSERT INTO recent (user_id, image, title, location, created_at)
VALUES
    (1, 'https://winvinayafoundation.org/wp-content/uploads/2024/12/charminar.jpg', 'Charminar', 'Hydrabad', NOW()),
    (1, 'https://winvinayafoundation.org/wp-content/uploads/2024/12/tajmahal.jpg', 'Taj Mahal', 'Agra', NOW()),
    (1, 'https://winvinayafoundation.org/wp-content/uploads/2024/12/waterpalace.jpg', 'Water Palace', 'Jaipur', NOW());

CREATE TABLE most_popular (
    id SERIAL PRIMARY KEY,  
    image VARCHAR(255) NOT NULL,  
    title VARCHAR(100) NOT NULL,  
    location VARCHAR(100) NOT NULL,  
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
);
INSERT INTO most_popular (image, title, location, created_at)
VALUES
    ('https://winvinayafoundation.org/wp-content/uploads/2024/12/red_fort.jpg', 'Red Fort', 'Delhi', NOW()),
    ('https://winvinayafoundation.org/wp-content/uploads/2024/12/golden_temple.jpg', 'Golden Temple', 'Amritsar, Punjab', NOW()),
    ('https://winvinayafoundation.org/wp-content/uploads/2024/12/brihadeeshwara_temple.jpg', 'Brihadeeshwara Temple', 'Tanjavur, Tamil Nadu', NOW());
    ('https://winvinayafoundation.org/wp-content/uploads/2024/12/hawa_mahal.jpg', 'Hawa Mahal', 'Jaipur, Rajasthan', NOW());
    ('https://winvinayafoundation.org/wp-content/uploads/2024/12/sun_temple.jpg', 'Sun Temple', 'Konark, Odisha', NOW());
    ('https://winvinayafoundation.org/wp-content/uploads/2024/12/ajantha_caves.jpg', 'Ajanta Cave', 'Maharashtra', NOW());

CREATE TABLE famous_places (
    id INT AUTO_INCREMENT PRIMARY KEY,
    image VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    video VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL
);
INSERT INTO famous_places (image, title, location, latitude, longitude, video, description)
VALUES
    ('https://winvinayafoundation.org/wp-content/uploads/2024/12/red_fort.jpg', 'Red Fort', 'Delhi', 28.6139, 77.2089, 'https://winvinaya.com/wp-content/uploads/2024/11/Charminar_1_2.mp4', 'A historic fort in the city of Delhi, known for its stunning Mughal architecture.'),
    ('https://winvinayafoundation.org/wp-content/uploads/2024/12/golden_temple.jpg', 'Golden Temple', 'Amritsar, Punjab', 31.6200, 74.8765, 'https://winvinaya.com/wp-content/uploads/2024/11/Charminar_1_2.mp4', 'The holiest Sikh gurdwara, known for its stunning gold-covered architecture and spiritual significance.'),
    ('https://winvinayafoundation.org/wp-content/uploads/2024/12/brihadeeshwara_temple.jpg', 'Brihadeeshwara Temple', 'Tanjavur, Tamil Nadu', 10.7850, 79.1320, 'https://winvinaya.com/wp-content/uploads/2024/11/Charminar_1_2.mp4', 'A UNESCO World Heritage site, known for its grand Dravidian architecture.'),
    ('https://winvinayafoundation.org/wp-content/uploads/2024/12/hawa_mahal.jpg', 'Hawa Mahal', 'Jaipur, Rajasthan', 26.9238, 75.8203, 'https://winvinaya.com/wp-content/uploads/2024/11/Charminar_1_2.mp4', 'A five-story palace in Jaipur, known for its intricate lattice work and history as a royal women’s palace.'),
    ('https://winvinayafoundation.org/wp-content/uploads/2024/12/sun_temple.jpg', 'Sun Temple', 'Konark, Odisha', 20.2833, 86.0920, 'https://winvinaya.com/wp-content/uploads/2024/11/Charminar_1_2.mp4', 'A UNESCO World Heritage site, famous for its stunning architectural design dedicated to the Sun God.'),
    ('https://winvinayafoundation.org/wp-content/uploads/2024/12/ajantha_caves.jpg', 'Ajanta Caves', 'Maharashtra', 20.5984, 75.7037, 'https://winvinaya.com/wp-content/uploads/2024/11/Charminar_1_2.mp4', 'Ancient Buddhist rock-cut caves, known for their exquisite paintings and sculptures.'),
    ('https://winvinayafoundation.org/wp-content/uploads/2024/12/india_gate.jpg', 'India Gate', 'Delhi', 28.6129, 77.2295, 'https://winvinaya.com/wp-content/uploads/2024/11/Charminar_1_2.mp4', 'A war memorial located in New Delhi, dedicated to the soldiers of India.'),
    ('https://winvinayafoundation.org/wp-content/uploads/2024/12/charminar.jpg', 'Charminar', 'Hyderabad, Telangana', 17.3616, 78.4747, 'https://winvinaya.com/wp-content/uploads/2024/11/Charminar_1_2.mp4', 'A historic mosque and monument, an iconic symbol of Hyderabad.'),
    ('https://winvinayafoundation.org/wp-content/uploads/2024/12/lotus_temple.jpg', 'Lotus Temple', 'Delhi', 28.5535, 77.2588, 'https://winvinaya.com/wp-content/uploads/2024/11/Charminar_1_2.mp4', 'A Baháʼí House of Worship, famous for its flowerlike architecture.'),
    ('https://winvinayafoundation.org/wp-content/uploads/2024/12/meenakshi_temple.jpg', 'Meenakshi Temple', 'Madurai, Tamil Nadu', 9.9197, 78.1194, 'https://winvinaya.com/wp-content/uploads/2024/11/Charminar_1_2.mp4', 'A historic Hindu temple dedicated to goddess Meenakshi, known for its gopurams and sculptures.');

-- for alter the record as most_popular - true
UPDATE famous_places
SET most_popular = TRUE
WHERE title IN ('Red Fort', 'Golden Temple', 'Brihadeeshwara Temple', 'Hawa Mahal', 'Sun Temple');

INSERT INTO famous_places (image, title, location, latitude, longitude, video, description, most_popular)
VALUES
    ('https://winvinayafoundation.org/wp-content/uploads/2024/12/Santhome_Basilica.jpg', 'Santhome Cathedral Basilica', 'Chennai', 13.0843, 80.2705, 'https://winvinaya.com/wp-content/uploads/2024/11/Charminar_1_2.mp4', 'San Thome Church, officially known as St Thomas Cathedral Basilica and National Shrine of Saint Thomas, is a minor basilica of the Catholic Church in India, at the Santhome neighbourhood of Chennai, in Tamil Nadu.','true'),
    ('https://winvinayafoundation.org/wp-content/uploads/2024/12/lalbagh.jpg', 'Lalbagh Botanical Garden', 'Bengaluru', 12.9716, 77.5946, 'https://winvinaya.com/wp-content/uploads/2024/11/Charminar_1_2.mp4', 'Lalbagh Botanical Garden or simply Lalbagh, is a botanical garden in Bangalore, India, with an over 200-year history. First planned and laid out during the dalavaiship of King Hyder Ali, the garden was later managed under numerous British Superintendents before Indian Independence.', 'true');

UPDATE famous_places
SET most_popular = TRUE
WHERE title IN ('Lalbagh Botanical Garden', 'Santhome Cathedral Basilica');
