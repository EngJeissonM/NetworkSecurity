
from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri ="mongodb+srv://jsmoraleshengineer_db_user:Test1234@jeisson.sxonfwo.mongodb.net/?retryWrites=true&w=majority&appName=Jeisson"

#the uri is connection string to connect to the mongodb database

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("✅ Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)