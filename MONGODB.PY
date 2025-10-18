from pymongo import MongoClient

try:
    client = MongoClient("mongodb+srv://jsmoraleshengineer_db_user:Test1234@jeisson.sxonfwo.mongodb.net/?retryWrites=true&w=majority&appName=Jeisson")
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB Atlas!")
except Exception as e:
    print("❌ Connection error:", e)