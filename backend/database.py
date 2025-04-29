# backend/database.py

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")  # Change if your MongoDB server is elsewhere
db = client["LungCancerDB"]

users_collection = db["users"]
actions_collection = db["actions"]
