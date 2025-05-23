import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException

# Secret key for signing JWT tokens
SECRET_KEY = "tCKvpPEp5K8t1nhYD0FtinlpF23ftXUQ"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def generate_token(username: str) -> str:
    """Generate a JWT token for the authenticated user."""
    try:
        payload = {
            "sub": username,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating authentication token: {str(e)}")

def verify_token(token: str) -> str:
    """Verify a JWT token and return the username if valid."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]  # Return the username from the token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")