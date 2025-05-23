from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tinydb import TinyDB, Query
from agent.conversation import generate_content
from services.createSession import create_session
from utils.authentication import verify_token

app = FastAPI()
db = TinyDB('userinfo.json')

#allow cors for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserLoginRequest(BaseModel):
    username: str
    password: str

class UserLoginResponse(BaseModel):
    success: bool
    token: str

class UserPromptRequest(BaseModel):
    prompt: str

class UserPromptResponse(BaseModel):
    response: str

class UserSignUpRequest(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: str
    username: str
    password: str

# Dependency to verify JWT token
def get_current_user(token: str = Depends(verify_token)):
    """Middleware-like dependency to verify JWT token."""
    return token  # Returns the username if the token is valid

@app.post('/login', response_model=UserLoginResponse) 
async def login_user(user_request: UserLoginRequest):
    try:
        from models.login import loginUser
        response = loginUser(
            username=user_request.username,
            password=user_request.password
        )
        if response["success"]:
            return UserLoginResponse(success=True, token=response["token"])
        else:
            raise HTTPException(status_code=401, detail=response["message"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#endpoint to register the user
@app.post('/signup')
async def signup_user(user_request: UserSignUpRequest):
    try:
        from models.signUpDB import create_user
        response = create_user(
            firstName=user_request.firstName,
            lastName=user_request.lastName,
            email=user_request.email,
            phone=user_request.phone,
            username=user_request.username,
            password=user_request.password
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#endpoint to handle user prompt
@app.post('/generate_prompt', response_model=UserPromptResponse)
async def generate_prompt(user_request: UserPromptRequest):
    try:
        response = generate_content(user_request.prompt)
        return UserPromptResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#endpoint to analyse resume
@app.post('/analyze_resume')
async def analyze_resume(request: Request):
    try:
        data = await request.json()
        resume_text = data.get("resume")
        if not resume_text:
            raise HTTPException(status_code=400, detail="Resume text is required")

        # Call the resume analysis function (to be implemented)
        from agent.resumeAnalyse import analyze_resume_content
        analysis_result = analyze_resume_content(resume_text)
        return {"analysis": analysis_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#endpoint to handle user session creation
@app.post('/create_new_session')
async def create_new_session(request: Request): 
    try:
        data = await request.json()
        username = data.get("username")
        if not username:
            raise HTTPException(status_code=400, detail="Username is required")

        # Create a new session
        response = create_session(username)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Example of a protected route
@app.get('/protected-route', dependencies=[Depends(get_current_user)])
async def protected_route():
    return {"message": "This is a protected route!"}


@app.post('/health_check')
async def health_check():
    return {"status": "ok"}