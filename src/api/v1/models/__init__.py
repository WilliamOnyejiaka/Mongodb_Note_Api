from pymongo import MongoClient
from src.config.config import MONGODB_URI

mongo = MongoClient(MONGODB_URI)
db = mongo.note_db