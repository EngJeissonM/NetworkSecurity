import os #to get the enviroment variables
import sys #to get the exception details
import json #to convert the data into json format
import pandas as pd 
import numpy as np
import pymongo #to connect to mongodb
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from dotenv import load_dotenv #this allows us to call the enviroments variables, like URL in MongoDB
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL") #getting the URL from the env file
print("The URL is: /n")
print(MONGO_DB_URL)

import certifi 
#to avoid the ssl certificate error, we need add this package to requirements, 
# this allows us to get the certificates
ca=certifi.where()



class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
   
   
    #READING THE CSV FILE AND CONVERTING IT TO JSON
    # we will use pandas to read the csv file and then convert it to json   
    def csv_to_json_convertor(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True) #resetting the index, the fisrt row will be 0
            #every row will be converted to json format
            records=list(json.loads(data.T.to_json()).values()) 
            return records
        except Exception as e: #If the file is not found or any other exception
            raise NetworkSecurityException(e,sys)
    
    
    #INSERTING THE DATA INTO MONGODB
    # we will use pymongo to connect to mongodb and insert the data 
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database=database #the database name where we want to insert the data
            self.collection=collection #the collection name where we want to insert the data
            self.records=records #the data to be inserted

            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL) #connecting to mongodb
            self.database = self.mongo_client[self.database] #creating the database
            
            self.collection=self.database[self.collection] #creating the collection
            self.collection.insert_many(self.records) #inserting the data into the collection
            return(len(self.records)) #returning the number of records inserted
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
#testing the code
if __name__=='__main__':
    #specifying the file path, database name and collection name
    FILE_PATH="Network_Data\phisingData.csv"
    DATABASE="JEISSONENGINEERING"
    Collection="NetworkData"

    #then we will create an object of the class and call the methods
    networkobj=NetworkDataExtract()
    records=networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    print(f"these are the records: {records}")

    no_of_records=networkobj.insert_data_mongodb(records,DATABASE,Collection)
    print(f"the number of records to be inserted: {no_of_records}")

    print("\n\n\n Data inserted successfully")
        


