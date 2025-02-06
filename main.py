from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import uvicorn
from typing import List

load_dotenv()

openai_client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Store chat history in memory (you might want to use a database in production)
chat_history: List[dict] = []
current_html = """
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

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/preview", response_class=HTMLResponse)
async def preview():
    return HTMLResponse(content=current_html.replace("```html", "").replace("```", ""))

@app.post("/generate")
async def generate_website(message: Message):
    global current_html, chat_history
    
    chat_history.append({"role": "user", "content": message.message})
    
    messages = [
        {"role": "system", "content": "You are a website builder. Generate clean, valid HTML code based on user requests. Respond only with HTML code, no explanations."},
        *chat_history
    ]
    
    response = await openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
    )
    
    ai_message = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": ai_message})
    
    current_html = ai_message
    
    return {
        "chat_history": chat_history,
        "current_html": current_html
    }

@app.post("/restore")
async def restore_version(request: Request):
    global current_html
    data = await request.json()
    current_html = data["html"]
    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)
