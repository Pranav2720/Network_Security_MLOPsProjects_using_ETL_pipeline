from pymongo import MongoClient
import certifi

MONGO_DB_URL = "mongodb+srv://pranavnichit20:GAqfz939MnoQnbHr@cluster0.kwuqf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = MongoClient(MONGO_DB_URL, tls=True, tlsCAFile=certifi.where())
    print("Connection Successful!")
    print(client.server_info())  # Fetch server details to verify connection
except Exception as e:
    print(f"Connection Failed: {e}")
