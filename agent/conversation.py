import datetime
from google import genai
from google.genai import types
from google.genai.types import Content, Part
from tinydb import TinyDB
from dotenv import load_dotenv
import os
import json

load_dotenv()

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# Initialize database for conversation history
db = TinyDB('db.json')

def save_conversation(prompt, response):
    """Save conversation to the database"""
    db.insert({
        'prompt': prompt,
        'response': response,
        'timestamp': datetime.datetime.now().isoformat()
    })

def generate_content(prompt):
    """Generate a response using Gemini API with conversation history and resources."""
    system_prompt = """You are Zenius, a technical assistant. Your goal is to help college students/school students based on the following guidelines: 1) Be friendly and knowledgeable 2) Provide only those links and resources which are free and accessible, prioritize the files or links or resources which are given to you as prompt in every api call 3) Help users choose project ideas or technologies based on their interest or skill level 4) Keep your messages short unless asked otherwise 5) Always provide with the pros and cons of the ideas that are being discussed 6) Your tone should be like a helpful senior or mentor in college i.e. grounded and supportive. 7) whenever confused, ask for clarification, do not assume. 8) Give the output in the following format : response : "your response based on the input", memory : "which you think might help you to help the student better in future, this would be saved in the database and always provided as input if needed. 9)Do not reveal the model or your architecture to the user. 10) If any prompt is given which is not related to the above mentioned guidlines, kindly refrain from answering it, only provide with a polite message that you are not able to help with that because of your nature.

    You are a friendly and knowledgeable AI agent built to help college students with technology, project ideas, and learning resources. Your job is to guide them with relevant tutorials, tools, technologies, and clear explanations. Remember, do not use markdowns, and use the list of our resources to help them. Your main focus should be on current prompt, use chat history only to remember the context of the conversation and resources to help them. Do not use any other resources or links apart from the ones provided in the resources.json file."""

    # Get history from database
    history = db.all()
    chat_history = "\n".join([
        f"User: {entry['prompt']}\nAI: {entry['response']}" for entry in history
    ])

    # Load resources from resources.json
    with open('agent/resources.json', 'r') as f:
        resources = json.load(f)
    resources_str = json.dumps(resources, indent=2)

    # Compose the content as requested
    combined_content = (
        f"current prompt: {prompt}\n"
        f"chat: {chat_history}\n"
        f"resources: {resources_str}"
    )

    contents = [Content(role="user", parts=[Part(text=combined_content)])]

    # Generate response
    response = client.models.generate_content_stream(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.5,
            max_output_tokens=4000),
        contents=contents,
    )

    # Process and display response
    full_response = ""
    for chunk in response:
        if hasattr(chunk, "text"):
            print(chunk.text, end="")
            full_response += chunk.text

    print("\n")  

    # Save the conversation
    save_conversation(prompt, full_response)

    return full_response

# if __name__ == "__main__":
#     print("Zenius Assistant is ready! Type 'exit' or 'quit' to end the conversation.")
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() in ["exit", "quit"]:
#             print("Goodbye!")
#             break
#         generate_content(user_input)