import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def insert_data_mongodb(self, records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            # Connect to MongoDB with SSL and certifi
            self.mongo_client = pymongo.MongoClient(
                MONGO_DB_URL,
                tls=True,  # Enable TLS/SSL
                tlsCAFile=ca,  # Use certifi to verify the server certificate
                serverSelectionTimeoutMS=50000  # Increase timeout to 50 seconds
            )

            # Access the database and collection
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]

            # Insert records into the collection
            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
if __name__ == '__main__':
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "Pranav"
    Collection = "NetworkData"

    # Instantiate the NetworkDataExtract class
    networkobj = NetworkDataExtract()

    # Convert CSV data to JSON
    records = networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    print(records)

    # Insert records into MongoDB
    no_of_records = networkobj.insert_data_mongodb(records, DATABASE, Collection)
    print(f"Number of records inserted: {no_of_records}")
