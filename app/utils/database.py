
from pymongo.mongo_client import MongoClient
from app.utils import config

uri = f"mongodb+srv://{config.DB_USERNAME}:{config.DB_PASSWORD}@{config.DB_URL}/?retryWrites=true&w=majority&appName=melody-mint"
client = MongoClient(uri)

db = client[config.DB_NAME]
user_collection = db["users"]

