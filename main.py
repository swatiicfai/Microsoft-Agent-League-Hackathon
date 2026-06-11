from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure the API key
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE"))

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(os.path.dirname(__file__), "index.html"))

@app.post("/generate")
async def generate_ui(request: PromptRequest):
    system_instruction = '''You are an expert frontend designer and developer. 
    You write clean, modern, beautiful, and fully-responsive HTML using Tailwind CSS via CDN. 
    ALWAYS include the Tailwind CDN link: <script src="https://cdn.tailwindcss.com"></script>
    ONLY return the raw HTML code. Do NOT use markdown code blocks (like ```html). 
    Ensure it is a complete <html> document ready to be rendered in an iframe.'''
    
    full_prompt = f"{system_instruction}\n\nUser Request: {request.prompt}"
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt
        )
        html_code = response.text
        
        # Clean up any markdown formatting just in case the model includes it
        html_code = html_code.replace("```html", "").replace("```", "").strip()
            
        return {"html": html_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
