from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from datetime import datetime

app = FastAPI()

# Allow CORS so the frontend can communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model for the contact form data
class ContactForm(BaseModel):
    firstName: str
    lastName: str
    email: str
    subject: str
    message: str

# Database file to store messages
DB_FILE = "messages.json"

@app.post("/api/contact")
async def submit_contact(form: ContactForm):
    # Print the received data to the terminal
    print(f"\n--- New Message Received ---")
    print(f"From: {form.firstName} {form.lastName} ({form.email})")
    print(f"Subject: {form.subject}")
    print(f"Message: {form.message}")
    print(f"----------------------------\n")
    
    # Save the message to a JSON file
    message_data = form.dict()
    message_data["timestamp"] = datetime.now().isoformat()
    
    messages = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try:
                messages = json.load(f)
            except:
                pass
                
    messages.append(message_data)
    
    with open(DB_FILE, "w") as f:
        json.dump(messages, f, indent=4)
        
    return {"status": "success", "message": "Message saved successfully"}

@app.get("/api/messages")
def get_messages():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

@app.get("/")
def read_root():
    return {"message": "Kavindu's Portfolio Backend is running!"}

