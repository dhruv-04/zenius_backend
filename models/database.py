from pymongo import MongoClient
import os

# Replace the connection string with your actual MongoDB Atlas connection string
MONGO_CONNECTION_STRING = "mongodb+srv://dhruvkum04:r0cR5wuJcvwnYSkb@cluster0.sbx4w2z.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Initialize the MongoDB client
client = MongoClient(MONGO_CONNECTION_STRING)

# Access the database (replace 'your_database_name' with your actual database name)
db = client['zenius']

# Example: Access a collection (replace 'your_collection_name' with your actual collection name)
users_collection = db['users']

# You can now use `users_collection` to perform CRUD operations
