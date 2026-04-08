import os
import sys
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
load_dotenv()

def ping_mongodb():
    uri = os.getenv("MONGO_URI")
    
    if not uri:
        print("Error: MONGODB_URI environment variable not found.")
        sys.exit(1)

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Successfully pinged the MongoDB deployment. Cluster is awake!")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        client.close()

if __name__ == "__main__":
    ping_mongodb()