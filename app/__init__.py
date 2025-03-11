from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from .database import db
from .models.user import User

from .api.signup import signup_api
from .api.login import login_api
from .api.recent import recent_api
from .api.most_popular import mostpopular_api
from .api.famous_place import geo_api
from .api.search_location import search_location_api
from .api.location import location_api
from .api.nearby import nearby_api
from .api.search import search_api
from .api.searchimage import searchimage_api

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    CORS(app)
    # Enable CORS for any origin (allowing mobile devices/emulators to connect)
    CORS(app, origins="*")  # Allow all origins (for development)

    # Initialize Database
    db.init_app(app)
    migrate = Migrate(app, db)

    # Register Blueprints
    app.register_blueprint(signup_api, url_prefix='/api')
    app.register_blueprint(login_api, url_prefix='/api')
    app.register_blueprint(recent_api, url_prefix='/api')
    app.register_blueprint(mostpopular_api, url_prefix='/api')
    app.register_blueprint(geo_api, url_prefix='/api')
    app.register_blueprint(search_location_api, url_prefix='/api')
    app.register_blueprint(location_api, url_prefix='/api')
    app.register_blueprint(nearby_api, url_prefix='/api')
    app.register_blueprint(search_api, url_prefix='/api')
    app.register_blueprint(searchimage_api, url_prefix='/api')
    
    return app
