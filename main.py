import spacy
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from typing import List

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Initialize FastAPI
app = FastAPI()

# Set up logging
logging.basicConfig(filename='chatbot.log', level=logging.INFO)

# Request schema for single input
class UserInput(BaseModel):
    message: str

# Request schema for batch input
class BatchInput(BaseModel):
    messages: List[str]

# Predefined responses for common greetings and questions
GREETINGS = ["hello", "hi", "greetings", "hey", "good morning", "good afternoon", "good evening"]
FAREWELLS = ["bye", "goodbye", "see you", "later", "take care"]

def analyze_sentiment(message: str) -> str:
    doc = nlp(message)
    # For simplicity, use naive rule-based sentiment
    if "good" in message:
        return "positive"
    elif "bad" in message:
        return "negative"
    else:
        return "neutral"

def extract_keywords(message: str) -> List[str]:
    doc = nlp(message)
    return [token.text for token in doc if token.is_alpha and not token.is_stop]

def detect_intent(message: str) -> str:
    # Naive rule-based intent detection
    message = message.lower()
    if any(greeting in message for greeting in GREETINGS):
        return "greeting"
    elif any(farewell in message for farewell in FAREWELLS):
        return "farewell"
    elif "how are you" in message:
        return "status_check"
    elif "weather" in message:
        return "weather_request"
    elif "joke" in message:
        return "joke_request"
    else:
        return "unknown"

def generate_response(intent: str, sentiment: str, keywords: List[str]) -> str:
    if intent == "greeting":
        return "Hello! How can I assist you today?"
    elif intent == "farewell":
        return "Goodbye! Have a wonderful day!"
    elif intent == "status_check":
        return "I'm doing great, thanks for asking!"
    elif intent == "weather_request":
        return "I'm not connected to a weather API, but I hope the weather is good!"
    elif intent == "joke_request":
        return "Why don’t scientists trust atoms? Because they make up everything!"
    elif "help" in keywords:
        return "It seems like you need help. How can I assist?"
    else:
        return "I’m sorry, I didn’t understand that. Can you rephrase?"

def chatbot_response(message: str) -> str:
    sentiment = analyze_sentiment(message)
    keywords = extract_keywords(message)
    intent = detect_intent(message)
    
    logging.info(f"Message: {message}, Intent: {intent}, Sentiment: {sentiment}, Keywords: {keywords}")
    
    response = generate_response(intent, sentiment, keywords)
    return response

# Batch processing for multiple inputs
def chatbot_batch_response(messages: List[str]) -> List[str]:
    responses = []
    for message in messages:
        response = chatbot_response(message)
        responses.append(response)
    return responses

@app.post("/chat/")
async def chat(user_input: UserInput):
    message = user_input.message
    response = chatbot_response(message)
    return {"response": response}

@app.post("/chat/batch/")
async def chat_batch(batch_input: BatchInput):
    responses = chatbot_batch_response(batch_input.messages)
    return {"responses": responses}

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Chatbot. Use /chat to interact."}

# Error handling for HTTP exceptions
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {"message": f"HTTP Exception: {exc.detail}"}

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logging.error(f"Error occurred: {exc}")
    return {"message": "An unexpected error occurred. Please try again."}

# Extract keywords from a given message
@app.post("/extract_keywords/")
async def extract(user_input: UserInput):
    keywords = extract_keywords(user_input.message)
    if not keywords:
        raise HTTPException(status_code=400, detail="No valid keywords found")
    return {"keywords": keywords}

# More conversational enhancements with sentiment and advanced logging
def chatbot_batch_response(messages: List[str]) -> List[str]:
    responses = []
    for message in messages:
        try:
            response = chatbot_response(message)
            logging.info(f"Processed message: {message}")
        except Exception as e:
            logging.error(f"Error processing message {message}: {str(e)}")
            response = "There was an error processing your message."
        responses.append(response)
    return responses

# Enhanced response generation for better handling
def generate_response(intent: str, sentiment: str, keywords: List[str]) -> str:
    if intent == "greeting":
        return "Hey! How's your day going?"
    elif intent == "farewell":
        return "Goodbye! It was great chatting with you!"
    elif intent == "status_check":
        return "I'm doing well! How about you?"
    elif intent == "weather_request":
        return "I wish I could tell you the weather, but I'm not connected to a weather API."
    elif intent == "joke_request":
        return "Why don’t skeletons fight each other? They don’t have the guts."
    elif "help" in keywords:
        return "It seems like you need help. How can I assist?"
    else:
        return "I’m not sure what you're asking. Can you give me more details?"

@app.post("/chat/")
async def chat(user_input: UserInput):
    try:
        message = user_input.message
        response = chatbot_response(message)
        logging.info(f"Response sent: {response}")
        return {"response": response}
    except Exception as e:
        logging.error(f"Failed to generate response: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# More detailed response generation logic
def generate_response(intent: str, sentiment: str, keywords: List[str]) -> str:
    if intent == "greeting":
        return "Hey! How's your day going?"
    elif intent == "farewell":
        return "Goodbye! It was great chatting with you!"
    elif intent == "status_check":
        return "I'm doing well! How about you?"
    elif intent == "weather_request":
        return "I wish I could tell you the weather, but I'm not connected to a weather API."
    elif intent == "joke_request":
        return "Why don’t skeletons fight each other? They don’t have the guts."
    elif "help" in keywords:
        return "It seems like you need help. How can I assist?"
    else:
        return "I’m not sure what you're asking. Can you give me more details?"

# Error handling for batch processing
def chatbot_batch_response(messages: List[str]) -> List[str]:
    responses = []
    for message in messages:
        try:
            response = chatbot_response(message)
            logging.info(f"Processed message: {message}")
        except Exception as e:
            logging.error(f"Error processing message {message}: {str(e)}")
            response = "There was an error processing your message."
        responses.append(response)
    return responses
