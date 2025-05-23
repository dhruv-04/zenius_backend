import datetime
from google import genai
from google.genai import types
from google.genai.types import Content, Part
from tinydb import TinyDB
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def analyze_resume_content(resume_text):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction="You are a resume analysis assistant. Your goal is to analyze the resume content and provide feedback. Highlight strengths, weaknesses, and areas for improvement. Provide a summary of the resume and suggest any additional skills or experiences that could enhance the candidate's profile.",
                temperature=0.5,
                max_output_tokens=4000
            ),
        contents=[Content(role="user", parts=[Part(text=resume_text)])]
        )
        # print(response.text)
        return response.text
    except Exception as e:
        raise Exception(f"Error analyzing resume content: {str(e)}")