import os, uvicorn, uuid, pickle, asyncio
from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from openai import AsyncOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from filelock import FileLock
from datetime import datetime

load_dotenv()

sessions: Dict[str, dict] = {}
# Initialize or load sessions from file
async def load_sessions() -> Dict[str, dict]:
    global sessions
    async with asyncio.Lock():
        with file_lock:
            if SESSIONS_FILE.exists():
                with open(SESSIONS_FILE, 'rb') as f:
                    try:
                        sessions = pickle.load(f)
                        print(f"Loaded {len(sessions)} sessions from {SESSIONS_FILE}")
                    except (pickle.UnpicklingError, EOFError):
                        return {}
            return {}

app = FastAPI(on_startup=[load_sessions])
templates = Jinja2Templates(directory="templates")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure the data directory exists
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
SESSIONS_FILE = DATA_DIR / "sessions.pkl"
LOCK_FILE = DATA_DIR / "sessions.lock"

# Create a lock for file access
file_lock = FileLock(str(LOCK_FILE))

async def save_sessions(sessions: Dict[str, dict]):
    async with asyncio.Lock():
        with file_lock:
            with open(SESSIONS_FILE, 'wb') as f:
                pickle.dump(sessions, f, protocol=pickle.HIGHEST_PROTOCOL)

# Load sessions at startup

# In-memory lock for sessions dictionary
sessions_lock = asyncio.Lock()

DEFAULT_HTML = """
<!DOCTYPE html>
<html>
<body>
    <h1>Welcome!</h1>
    <p>Use the input above to start building your website.</p>
</body>
</html>
"""

class Message(BaseModel):
    message: str
    session_id: str
    api_key: str | None = None
    model: str | None = "gpt-4o-mini"  # Changed default to gpt-4o-mini

async def create_session() -> str:
    session_id = str(uuid.uuid4())
    async with sessions_lock:
        sessions[session_id] = {
            "chat_history": [],
            "current_html": DEFAULT_HTML
        }
        await save_sessions(sessions)
    return session_id

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, response: Response):
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in sessions:
        session_id = await create_session()
    
    response = templates.TemplateResponse("index.html", {
        "request": request,
        "session_id": session_id
    })
    response.set_cookie(key="session_id", value=session_id)
    return response

@app.get("/preview", response_class=HTMLResponse)
async def preview(request: Request):
    session_id = request.cookies.get("session_id")
    async with sessions_lock:
        if not session_id or session_id not in sessions:
            return HTMLResponse(content=DEFAULT_HTML)
        return HTMLResponse(content=sessions[session_id]["current_html"])

@app.post("/generate")
async def generate_website(message: Message):
    session_id = message.session_id
    
    if not message.api_key:
        return {"status": "error", "message": "OpenAI API key is required"}
    
    async with sessions_lock:
        if session_id not in sessions:
            sessions[session_id] = {
                "chat_history": [],
                "current_html": DEFAULT_HTML
            }
        
        session = sessions[session_id]
        session["chat_history"].append({"role": "user", "content": message.message})
        
        # Prepare messages based on model type
        if message.model in ['o1-mini', 'o1-preview']:
            if len(session["chat_history"]) > 0 and session["chat_history"][0]['role'] == "system":
                session["chat_history"][0] = {"role": "user", "content": session["chat_history"][0]['content']}
            messages = [
                {"role": "user", "content": "You are a website builder. Generate clean, valid HTML code based on user requests. Respond only with HTML code, no explanations."},
                {"role": "user", "content": message.message},
                *session["chat_history"]
            ]
        else:
            if len(session["chat_history"]) > 0 and session["chat_history"][0]['role'] == "user":
                session["chat_history"][0] = {"role": "system", "content": session["chat_history"][0]['content']}
            messages = [
                {"role": "system", "content": "You are a website builder. Generate clean, valid HTML code based on user requests. Respond only with HTML code, no explanations."},
                *session["chat_history"]
            ]
    
    try:
        print(message.model)
        client = AsyncOpenAI(api_key=message.api_key)
        response = await client.chat.completions.create(
            model=message.model,
            messages=messages,
            temperature=0.7 if message.model not in ['o1-mini', 'o1-preview'] else 1,
        )
        
        ai_message = response.choices[0].message.content.replace("```html", "").split("```")[0]
        
        async with sessions_lock:
            session["chat_history"].append({"role": "assistant", "content": ai_message})
            session["current_html"] = ai_message
            await save_sessions(sessions)
            
            return {
                "status": "success",
                "chat_history": session["chat_history"],
                "current_html": session["current_html"]
            }
    except Exception as e:
        print(e)
        return {
            "status": "error",
            "message": str(e) if "Unsupported value" in str(e) else "Invalid API key or API error"
        }

@app.post("/restore")
async def restore_version(request: Request):
    session_id = request.cookies.get("session_id")
    
    async with sessions_lock:
        if not session_id or session_id not in sessions:
            return {"status": "error", "message": "Invalid session"}
        
        data = await request.json()
        sessions[session_id]["current_html"] = data["html"]
        
        # Save sessions after updating
        await save_sessions(sessions)
        
        return {"status": "success"}

@app.post("/clear")
async def clear_history(request: Request):
    session_id = request.cookies.get("session_id")
    
    async with sessions_lock:
        if not session_id or session_id not in sessions:
            return {"status": "error", "message": "Invalid session"}
        
        # Reset the session to initial state
        sessions[session_id] = {
            "chat_history": [],
            "current_html": DEFAULT_HTML
        }
        
        await save_sessions(sessions)
        return {"status": "success"}

@app.post("/publish")
async def publish_website(request: Request):
    session_id = request.cookies.get("session_id")
    
    async with sessions_lock:
        if not session_id or session_id not in sessions:
            return {"status": "error", "message": "Invalid session"}
        
        # Generate a shorter, readable ID for the public URL
        public_id = str(uuid.uuid4())[:8]
        
        # Store publish info in the session
        sessions[session_id]["published"] = {
            "id": public_id,
            "date": datetime.now().isoformat(),
            "html": sessions[session_id]["current_html"]
        }
        
        await save_sessions(sessions)
        
        return {
            "status": "success",
            "public_id": public_id
        }

@app.get("/p/{public_id}")
async def view_published(public_id: str):
    # Search for the published page in all sessions
    for session in sessions.values():
        if "published" in session and session["published"]["id"] == public_id:
            return HTMLResponse(content=session["published"]["html"])
    
    return HTMLResponse(content="<h1>Page not found</h1>", status_code=404)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)
