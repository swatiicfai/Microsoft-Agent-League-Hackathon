# AutoUI Setup Guide

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- A Gemini API Key (get one at [Google AI Studio](https://aistudio.google.com/app/apikey))

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/swatiicfai/Microsoft-Agent-League-Hackathon.git
cd Microsoft-Agent-League-Hackathon
```

### 2. Create a Virtual Environment (Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Key

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Open `.env` and add your Gemini API Key:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

**Get your API Key:**
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key and paste it in `.env`

## Running the Application

### Local Development
```bash
python main.py
```

The server will start at `http://localhost:8000`

### Using Uvicorn Directly
```bash
uvicorn main:app --reload
```

### Access the Application
Open your browser and navigate to:
```
http://localhost:8000
```

## Docker Setup (Optional)

### Build Docker Image
```bash
docker build -t autoui .
```

### Run Docker Container
```bash
docker run -p 8000:8000 -e GEMINI_API_KEY=your_api_key autoui
```

## Deployment

### Deploy to Heroku
```bash
heroku create your-app-name
heroku config:set GEMINI_API_KEY=your_api_key
git push heroku main
```

### Deploy to Replit
1. Fork this repository to Replit
2. Create a `.env` file with your API key
3. Run `python main.py`
4. Click "Open in new tab" to view

## Troubleshooting

### "ModuleNotFoundError: No module named 'google'"
```bash
pip install google-genai
```

### "GEMINI_API_KEY not properly configured"
- Ensure `.env` file exists in the project root
- Verify the API key is correct
- Restart the server after updating `.env`

### "Failed to generate UI"
- Check your internet connection
- Verify your Gemini API key is valid
- Check that your API key has sufficient quota

### Port 8000 already in use
```bash
# Use a different port
uvicorn main:app --port 8001
```

## Features

✅ **Autonomous UI Generation** - Describe what you want, the AI builds it
✅ **Live Preview** - See your UI rendered in real-time
✅ **Production-Ready Code** - Clean HTML with Tailwind CSS
✅ **Modern Design** - Built-in support for glassmorphism, neon effects, dark themes
✅ **Easy API Key Management** - Simple environment variable configuration

## Architecture

```
┌─────────────────────────────────────────┐
│     Web Browser (index.html)            │
│  - Chat Interface                       │
│  - Live Preview iframe                  │
│  - API Key Input                        │
└────────────┬────────────────────────────┘
             │
             │ HTTP POST /generate
             │
┌────────────▼────────────────────────────┐
│     FastAPI Server (main.py)            │
│  - Request validation                   │
│  - Error handling                       │
│  - CORS middleware                      │
└────────────┬────────────────────────────┘
             │
             │ API Call
             │
┌────────────▼────────────────────────────┐
│   Google Gemini 2.5 Flash API           │
│  - HTML generation                      │
│  - Markdown cleanup                     │
└─────────────────────────────────────────┘
```

## Support

For issues or questions:
1. Check the [GitHub Issues](https://github.com/swatiicfai/Microsoft-Agent-League-Hackathon/issues)
2. Review this setup guide
3. Create a new issue with details about your problem

## License

MIT License - Feel free to use this project for personal and commercial purposes.
