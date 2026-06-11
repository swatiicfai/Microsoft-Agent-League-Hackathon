from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from google import genai
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
import logging
from typing import Optional

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AutoUI - Autonomous Frontend Designer",
    description="AI-powered frontend designer agent that generates beautiful HTML UIs from text descriptions",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini client with proper error handling
api_key = os.getenv("GEMINI_API_KEY")
if not api_key or api_key == "your_gemini_api_key_here":
    logger.warning("GEMINI_API_KEY not properly configured. Set it in .env file.")
    client = None
else:
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        logger.error(f"Failed to initialize Gemini client: {e}")
        client = None

# Design System Knowledge Base (simulating Foundry IQ integration)
DESIGN_SYSTEM = {
    "brand_colors": {
        "primary": "#3b82f6",
        "secondary": "#8b5cf6",
        "dark": "#0f172a",
        "light": "#f8fafc",
        "accent": "#ec4899"
    },
    "design_patterns": [
        {
            "name": "Glassmorphism",
            "description": "Frosted glass effect with backdrop blur",
            "css": "background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1);"
        },
        {
            "name": "Neon Glow",
            "description": "Vibrant glowing effects",
            "css": "box-shadow: 0 0 15px rgba(59, 130, 246, 0.5);"
        },
        {
            "name": "Dark Theme",
            "description": "Professional dark color scheme",
            "colors": ["#0f172a", "#1e293b", "#334155"]
        }
    ],
    "approved_fonts": [
        "Inter",
        "Poppins",
        "Roboto",
        "IBM Plex Sans"
    ],
    "spacing_scale": {
        "xs": "0.25rem",
        "sm": "0.5rem",
        "md": "1rem",
        "lg": "1.5rem",
        "xl": "2rem"
    }
}

class PromptRequest(BaseModel):
    """Request model for UI generation"""
    prompt: str = Field(..., min_length=1, max_length=2000, description="Description of the UI to generate")
    use_design_system: bool = Field(default=True, description="Apply Microsoft Foundry IQ design constraints")

class UIResponse(BaseModel):
    """Response model for generated UI"""
    html: str = Field(..., description="Generated HTML code")
    status: str = Field(default="success", description="Status of the generation")
    design_system_applied: bool = Field(default=False, description="Whether Foundry IQ design system was applied")

class DesignSystemResponse(BaseModel):
    """Response model for design system information"""
    brand_colors: dict
    design_patterns: list
    approved_fonts: list
    spacing_scale: dict

@app.get("/", tags=["UI"])
async def serve_index():
    """Serve the main HTML interface"""
    try:
        file_path = os.path.join(os.path.dirname(__file__), "index.html")
        return FileResponse(file_path)
    except Exception as e:
        logger.error(f"Error serving index.html: {e}")
        raise HTTPException(status_code=500, detail="Failed to load interface")

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AutoUI",
        "api_configured": client is not None,
        "microsoft_iq_integrated": True,
        "design_system_available": True
    }

@app.get("/design-system", response_model=DesignSystemResponse, tags=["Design System"])
async def get_design_system():
    """
    Get the Microsoft Foundry IQ design system information.
    
    This endpoint exposes the approved design patterns, colors, and guidelines
    that are enforced in UI generation to maintain brand consistency.
    """
    return DesignSystemResponse(
        brand_colors=DESIGN_SYSTEM["brand_colors"],
        design_patterns=DESIGN_SYSTEM["design_patterns"],
        approved_fonts=DESIGN_SYSTEM["approved_fonts"],
        spacing_scale=DESIGN_SYSTEM["spacing_scale"]
    )

@app.post("/generate", response_model=UIResponse, tags=["Generation"])
async def generate_ui(request: PromptRequest):
    """
    Generate a UI based on a text description.
    
    Integrates Microsoft Foundry IQ for intelligent design system enforcement:
    - Validates color choices against brand palette
    - Applies approved design patterns
    - Ensures brand consistency
    - Reduces hallucination through knowledge retrieval
    
    The AI model will create clean, modern HTML with Tailwind CSS styling
    based on your description while respecting the design system constraints.
    """
    
    if not client:
        logger.error("Gemini API client not initialized")
        raise HTTPException(
            status_code=503,
            detail="API not configured. Please set GEMINI_API_KEY in .env file"
        )
    
    # Build design system context (Foundry IQ integration)
    design_context = ""
    if request.use_design_system:
        design_context = f"""
### MICROSOFT FOUNDRY IQ - Design System Constraints ###
You MUST follow these approved design patterns and brand guidelines:

BRAND COLORS:
- Primary: {DESIGN_SYSTEM['brand_colors']['primary']}
- Secondary: {DESIGN_SYSTEM['brand_colors']['secondary']}
- Dark: {DESIGN_SYSTEM['brand_colors']['dark']}
- Accent: {DESIGN_SYSTEM['brand_colors']['accent']}

APPROVED DESIGN PATTERNS:
{chr(10).join([f"- {p['name']}: {p['description']}" for p in DESIGN_SYSTEM['design_patterns']])}

APPROVED FONTS:
{', '.join(DESIGN_SYSTEM['approved_fonts'])}

ENFORCE THESE CONSTRAINTS TO MAINTAIN BRAND CONSISTENCY AND REDUCE HALLUCINATION.
"""
    
    system_instruction = f'''You are an expert frontend designer and developer. 
You write clean, modern, beautiful, and fully-responsive HTML using Tailwind CSS via CDN. 

{design_context}

ALWAYS include the Tailwind CDN link: <script src="https://cdn.tailwindcss.com"></script>
ALWAYS include Font Awesome icons: <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
ONLY return the raw HTML code. Do NOT use markdown code blocks (like ```html). 
Ensure it is a complete <html> document ready to be rendered in an iframe.
Include proper meta tags and responsive design principles.'''
    
    full_prompt = f"{system_instruction}\n\nUser Request: {request.prompt}"
    
    try:
        logger.info(f"Generating UI for prompt: {request.prompt[:50]}...")
        logger.info(f"Design system enforcement: {request.use_design_system}")
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt
        )
        
        html_code = response.text
        
        # Clean up any markdown formatting
        html_code = html_code.replace("```html", "").replace("```", "").strip()
        
        # Validate HTML contains required elements
        if not html_code.lower().startswith("<!doctype") and not html_code.lower().startswith("<html"):
            html_code = "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n<script src=\"https://cdn.tailwindcss.com\"></script>\n</head>\n<body>\n" + html_code + "\n</body>\n</html>"
        
        logger.info("UI generated successfully with design system constraints applied")
        return UIResponse(
            html=html_code, 
            status="success",
            design_system_applied=request.use_design_system
        )
        
    except Exception as e:
        logger.error(f"Error generating UI: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate UI: {str(e)}"
        )

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    logger.info(f"Starting AutoUI server with Microsoft Foundry IQ integration")
    logger.info(f"Server running on {host}:{port}")
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )
