from app.config import MONGODB_URI
from pymongo import MongoClient

client = MongoClient(MONGODB_URI)
db = client["mydatabase"]

contracts_collection = db["contracts"]
analysis_collection = db["analysis"]

def init_db():
    # Create indexes for the collections if they don't exist
    contracts_collection.create_index("filename", unique=True)
    analysis_collection.create_index("contract_id")

