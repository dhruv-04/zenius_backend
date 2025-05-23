from models.database import users_collection
from utils.bcryptPassword import hash_password

def create_user(firstName: str, lastName: str, email: str, phone: str, username: str, password: str):
    try:
        # Check if the username or email already exists
        if users_collection.find_one({"username": username}):
            return {"success": False, "message": "Username already exists"}
        # if users_collection.find_one({"email": email}):
        #     return {"success": False, "message": "Email already exists"}

        # Hash the password
        hashed_password = hash_password(password)

        # Create the user document
        user_document = {
            "firstName": firstName,
            "lastName": lastName,
            "email": email,
            "phone": phone,
            "username": username,
            "password": hashed_password,
            "role": "free",
            "sessions": [],
            "memory": []
        }

        # Insert the user into the database
        users_collection.insert_one(user_document)

        return {"success": True, "message": "User created successfully"}
    except Exception as e:
        return {"success": False, "message": f"Error creating user: {str(e)}"}
