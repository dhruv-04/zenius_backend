from utils.authentication import generate_token
from utils.bcryptPassword import verify_password
from models.database import users_collection

def loginUser(username: str, password: str):
    try:
        # Check if the user exists in the database
        user = users_collection.find_one({"username": username})
        if not user:
            return {"success": False, "message": "Invalid username or password"}

        # Verify the password
        if not verify_password(password, user["password"]):
            return {"success": False, "message": "Invalid username or password"}

        # Generate a token
        token = generate_token(username)
        return {"success": True, "token": token}
    except Exception as e:
        return {"success": False, "message": "Error logging in user: " + str(e)}