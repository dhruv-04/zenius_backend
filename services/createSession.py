from tinydb import TinyDB, Query
from models.updateSessionDB import update_session_on_creation
import datetime

def create_session_id(username: str) -> str:
    """Generate a unique session ID"""
    current_time = datetime.datetime.now().strftime("%H%M%S")
    return f"{username}{current_time}"

# print(create_session_id("dhruv"))

def create_session(username: str) -> dict:
    """Create a new session for the user"""
    session_id = create_session_id(username)
    userInfo_db = update_session_on_creation(session_id, username)
    if userInfo_db:
        return {
            "session_id": session_id,
            "message": f"Session {session_id} created successfully."
        }
    else:
        return {
            "session_id": None,
            "message": "Failed to create session."
        }