from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from .config import Config
from flask_jwt_extended import JWTManager
from datetime import timedelta
from dotenv import load_dotenv
from flask_redis import FlaskRedis
from flask_wtf.csrf import CSRFProtect
import os
import logging
# from .limiter import rate_limit_middleware

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
jwt = JWTManager() 
# redis = FlaskRedis()
load_dotenv()
csrf = CSRFProtect()

logging.basicConfig(
    filename='agam_tube.log',  # Log file name
    level=logging.DEBUG,  # Log level
    format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s'  # Log format with filename and line number
)

def create_app():
    app = Flask(__name__)
    # app.debug = False
    app.config.from_object(Config)

    mail.init_app(app)
    jwt.init_app(app) 
    # csrf.init_app(app)
    # rate_limit_middleware(app)
    # app.config['REDIS_URL'] = os.getenv('REDIS_URL')

    # app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
    # app.config['SESSION_COOKIE_HTTPONLY'] = True  # Accessible only via HTTP(S)

    # redis.init_app(app,decode_responses=True)
    # app.config['SERVER_NAME'] = 'localhost:5000'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False #timedelta(minutes=180) 
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = False #timedelta(days=30)   
    # App Configuration for SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # @app.before_request
    # def detect_subdomain():
    #     host = request.host.split(':')[0]
    #     print("🧪 Host received:", host)
        
    #     subdomain = host.split('.')[0] if '.' in host else 'main'
        
    #     print("🔥 Subdomain detected:", subdomain)
    #     request.tenant = subdomain
    # Initialize database and migrations
    db.init_app(app)
    migrate.init_app(app, db)
    

    # Register Blueprints
    from app.blueprints import video_play
    app.register_blueprint(video_play.video_blueprint, url_prefix='/video')
   

    return app

