from app import create_app
from app.config import Config  # If config.py is in app/

# print(Config.SECRET_KEY)

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
