"""
AI Code Agent - Simple, Bulletproof Backend
Chat with OLLAMA, local only, no bloat
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import logging
import subprocess
import sys
import os
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="AI Code Agent",
    description="Local AI Assistant",
    version="2.0"
)

# CORS - allow all for local use
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    model: str = None

class ChatResponse(BaseModel):
    response: str
    model: str

class ModelInfo(BaseModel):
    name: str
    current: bool = False

# Global state
current_model = None
available_models = []
ollama_available = False

def get_ollama_models():
    """Get list of installed OLLAMA models"""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            models = []
            for line in lines[1:]:  # Skip header
                if line.strip():
                    try:
                        model_name = line.split()[0]
                        models.append(model_name)
                    except:
                        pass
            return models
    except:
        pass

    return []

# Startup event
@app.on_event("startup")
async def startup():
    """Initialize on startup"""
    global current_model, available_models, ollama_available

    logger.info("🚀 Starting AI Code Agent...")

    # Try to get OLLAMA models
    models = get_ollama_models()

    if models:
        available_models = models
        current_model = models[0]
        ollama_available = True
        logger.info(f"✅ OLLAMA connected - {len(models)} models available")
        for model in models:
            logger.info(f"   - {model}")
    else:
        logger.warning("⚠️  OLLAMA not responding or no models installed")
        logger.warning("   Make sure to run: ollama serve")
        logger.warning("   And install a model: ollama pull mistral")
        available_models = []
        current_model = None
        ollama_available = False

# Routes

@app.get("/")
async def root():
    """Serve the frontend"""
    frontend_path = Path(__file__).parent.parent / "frontend" / "index.html"
    if frontend_path.exists():
        return FileResponse(frontend_path)
    return {"message": "Open http://localhost:8000 in your browser"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok" if ollama_available else "degraded",
        "ollama": "connected" if ollama_available else "offline",
        "models": available_models,
        "current_model": current_model
    }

@app.get("/api/models")
async def get_models():
    """Get available models"""
    models = []
    for m in available_models:
        models.append({
            "name": m,
            "current": m == current_model
        })

    return {
        "models": models,
        "current": current_model,
        "status": "ok" if ollama_available else "no_models"
    }

@app.post("/api/models/select")
async def select_model(body: dict):
    """Switch to a different model"""
    global current_model

    model_name = body.get("model")

    if not model_name:
        raise HTTPException(status_code=400, detail="No model specified")

    if model_name not in available_models:
        raise HTTPException(status_code=400, detail=f"Model not found: {model_name}")

    current_model = model_name
    logger.info(f"Switched to model: {current_model}")

    return {
        "model": current_model,
        "status": "ok"
    }

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Chat with OLLAMA"""

    # Check OLLAMA is available
    if not ollama_available or not current_model:
        raise HTTPException(
            status_code=503,
            detail="OLLAMA not available. Run 'ollama serve' and 'ollama pull mistral'"
        )

    message = request.message.strip()
    model = request.model or current_model

    # Validate input
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    if len(message) > 5000:
        raise HTTPException(status_code=400, detail="Message too long (max 5000 chars)")

    if model not in available_models:
        raise HTTPException(status_code=400, detail=f"Model not available: {model}")

    try:
        logger.info(f"Chat request with model: {model}")

        # Call OLLAMA - directly pass the command as a string for Windows compatibility
        cmd = f'ollama run {model} "{message}"'

        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode != 0:
            error_msg = result.stderr.strip() or result.stdout.strip()
            logger.error(f"OLLAMA error: {error_msg}")
            raise HTTPException(
                status_code=500,
                detail=f"OLLAMA error: {error_msg[:200]}"
            )

        response_text = result.stdout.strip()

        if not response_text:
            response_text = "OLLAMA gave no response. Try again."

        return {
            "response": response_text,
            "model": model
        }

    except subprocess.TimeoutExpired:
        logger.error("OLLAMA timeout")
        raise HTTPException(
            status_code=504,
            detail="OLLAMA took too long (timeout)"
        )
    except FileNotFoundError:
        logger.error("OLLAMA not found")
        raise HTTPException(
            status_code=503,
            detail="OLLAMA not installed or not in PATH"
        )
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)[:100]}"
        )

# Mount frontend static files
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="static")
    logger.info(f"✅ Frontend mounted from {frontend_path}")
else:
    logger.warning(f"⚠️  Frontend not found at {frontend_path}")

if __name__ == "__main__":
    import uvicorn

    print("\n" + "="*60)
    print("  AI Code Agent - Chat Backend")
    print("="*60)
    print("\n📡 Server starting at: http://localhost:8000")
    print("\n⚠️  BEFORE USING:")
    print("  1. Make sure OLLAMA is running: ollama serve")
    print("  2. Install a model: ollama pull mistral")
    print("  3. Open http://localhost:8000 in your browser")
    print("\n" + "="*60 + "\n")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
