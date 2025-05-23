from tinydb import TinyDB, Query
import datetime
import os

user_db = TinyDB(os.path.join(os.path.dirname(__file__), '../userinfo.json'))
session_db = TinyDB(os.path.join(os.path.dirname(__file__), '../session.json'))

def update_session_on_creation(session_id: str, username: str) -> None:
    """Update the userinfo database and session database with the new session ID"""
    try:
        #update sessionID in userInfo database
        User = Query()
        user = user_db.search(User.username == username)

        if user and user[0]['role'] == 'free' and len(user[0]['sessions']) <= 5:
            user[0]['sessions'].append(session_id)
            user_db.update({'sessions': user[0]['sessions']}, User.username == username)

            #update sessionID in session database
            session_db.insert({
                "session_id": session_id,
                "created_at": datetime.datetime.now().isoformat(),
                "updated_at": datetime.datetime.now().isoformat(),
                "prompt": [],
                "response": [],
                "username": username
            })
            print(f"Session ID {session_id} created for user {username}.")
        elif user and user[0]['role'] == 'premium':
            user[0]['sessions'].append(session_id)
            user_db.update({'sessions': user[0]['sessions']}, User.username == username)

            #update sessionID in session database
            session_db.insert({
                "session_id": session_id,
                "created_at": datetime.datetime.now().isoformat(),
                "updated_at": datetime.datetime.now().isoformat(),
                "prompt": [],
                "response": [],
                "username": username
            })
            print(f"Session ID {session_id} created for user {username}.")
        elif user and user[0]['role'] == 'free' and len(user[0]['sessions']) > 5:
            print(f"User {username} has reached the session limit of 5.")
            return
        else:
            print(f"User {username} does not exist")
            return
    except Exception as e:
        print(f"Error updating user info: {e}")
        return
    
# update_session_on_creation('dhruv123_123434', 'dhruv123')