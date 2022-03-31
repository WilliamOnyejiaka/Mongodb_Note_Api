from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()

MONGODB_URI = os.environ.get('MONGODB_URI')
SECRET_KEY = os.environ.get('SECRET_KEY')
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
JWT_TOKEN_LOCATION = ["headers","query_string"]
JWT_QUERY_STRING_NAME = "token"
