import socket, uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from SLM import load_json, determine_command, COMMAND_VECTOR_FILE, WORD_VECTOR_FILE


# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

ERROR_TOLORANCE = 0.4

HTML_FILE = "index.html"
CSS_FILE = "style.css"
JS_FILE = "script.js"


# ------------------------------------------------------------
# FastAPI
# ------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_vectors()
    yield


app = FastAPI(
    title="Semion API",
    description="Semantic-search language model API",
    version="1.0.0",
    lifespan=lifespan
)

# ------------------------------------------------------------
# Semion data
# ------------------------------------------------------------

word_vectors = {}
command_vectors = {}


# ------------------------------------------------------------
# Local Semion responses
# ------------------------------------------------------------

responses = {

    "greet":
        "Hi there! How can I help you?",

    "hello":
        "Hello! It's nice to meet you.",

    "goodbye":
        "Goodbye! Have a great day.",

    "thanks":
        "You're welcome!",

    "how_doing":
        "I don't really have feelings, but if I did I would be doing well. How about you?",

    "user_doing_well":
        "That's great to hear!",

    "user_doing_bad":
        "I'm sorry to hear that. I hope things get better.",

    "name":
        "My name is Semion, a Semantic Language Model!",

    "what_are_you":
        "I am Semion, a small semantic-search language model created as a proof of concept.",

    "capabilities":
        "I can recognize the semantic meaning of certain phrases and respond to them.",

    "how_work":
        "I compare the meaning of your words to semantic vectors that I have been given.",

    "creator":
        "I was made by Evan Hill.",

    "why_made":
        "I was created as a personal project. Although that project originated from a BYU math camp project.",

    "purpose":
        "My purpose is to demonstrate how semantic language processing can work on a small scale.",

    "compliment":
        "Thank you! That's nice of you to say.",

    "joke":
        "The square root of negative four equals two... It's all fun and games until someone loses an i!",

    "math":
        "Mathematics is very important to my existence. My semantic-search model relies on vectors and mathematical similarity.",

    "woodchuck":
        "A woodchuck could chuck as much wood as a woodchuck could chuck if a woodchuck could chuck wood.",

    "question":
        "That's an interesting question.",

    "age":
        "I don't really have an age. I am a computer program. Though I was initially created during the summer of 2023. My latest training was in September of 2026.",

    "human":
        "No, I am not human. I am a computer program.",

    "ai":
        "I am a small semantic-search language model, but I am not designed to be a general-purpose artificial intelligence.",

    "understand":
        "I don't understand language the same way a person does. I use mathematical representations of words and compare their similarity.",

    "language":
        "Language is complicated, but mathematics gives me a way to represent some of its relationships.",

    "vector":
        "A vector is a mathematical representation containing a collection of numerical values. I use vectors to represent words and their meanings.",

    "similarity":
        "I use cosine similarity to compare semantic vectors and determine which meaning is closest to your input.",

    "semantic":
        "Semantics is the study of meaning in language. My purpose is to use mathematical representations to recognize some of that meaning.",

    "67":
        "Six-Seven!!!!",

    "unknown":
        "I am unable to understand what you just said. Don't take it personally - it likely was not in my training."
}


# ------------------------------------------------------------
# Request / Response models
# ------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    command: str
    confidence: float


# ------------------------------------------------------------
# Load semantic model
# ------------------------------------------------------------

def load_vectors():
    global word_vectors
    global command_vectors

    try:
        word_vectors = load_json(WORD_VECTOR_FILE, {})
        command_vectors = load_json(COMMAND_VECTOR_FILE, {})

        if word_vectors == {} or command_vectors == {}:
            raise BaseException("Vector files failed to load. Train model to fix issue.")

        print("Semantic model loaded successfully.")

        print(
            f"Loaded {len(word_vectors)} word vectors "
            f"and {len(command_vectors)} command vectors."
        )

    except Exception as error:
        print("Unable to load semantic model:")
        print(error)

        word_vectors = {}
        command_vectors = {}


# ------------------------------------------------------------
# Process Semion input
# ------------------------------------------------------------

def process_semion(input_text):

    result = determine_command(input_text, word_vectors, command_vectors)

    command = result["command"]

    confidence = result["confidence"]

    response = responses.get(
        command if result["confidence"] > ERROR_TOLORANCE else "unknown",
        responses["unknown"]
    )

    return {
        "response": response,
        "command": command,
        "confidence": confidence
    }


# ------------------------------------------------------------
# API endpoints
# ------------------------------------------------------------

@app.get("/")
def home():
    return FileResponse(HTML_FILE)

@app.get("/style.css")
def css():
    return FileResponse(CSS_FILE)

@app.get("/script.js")
def js():
    return FileResponse(JS_FILE)


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    return process_semion(
        request.message
    )


@app.get("/api/status")
def status():

    return {
        "status": "online",
        "model": "Semion-1.0",
        "word_vectors": len(word_vectors),
        "command_vectors": len(command_vectors)
    }

# run server
def get_local_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

if __name__ == "__main__":
    ip = get_local_ip()

    print(f"\nServer running at:")
    print(f"  Local:   http://127.0.0.1:8000")
    print(f"  Network: http://{ip}:8000\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)