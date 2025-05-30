import os
from dotenv import load_dotenv

# import secrets
# secret_key = secrets.token_hex(24)
# jwt_secret_key = secrets.token_urlsafe(32)
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('FLASK_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

    #smtp
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT') 
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')  
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    # S3 bucket
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET')
    AWS_S3_REGION = os.getenv('AWS_S3_REGION')




    
