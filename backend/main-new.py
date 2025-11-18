"""
AI Code Agent - Simple, Working FastAPI Backend
Chat-focused, OLLAMA-powered, no bloat
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import subprocess
import sys
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
    description="Simple AI Code Assistant",
    version="2.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
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
current_model = "mistral"  # Default model
available_models = []

# Initialize
@app.on_event("startup")
async def startup():
    """Load available OLLAMA models on startup"""
    global available_models, current_model

    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            available_models = []
            for line in lines:
                if line.strip():
                    model_name = line.split()[0]
                    available_models.append(model_name)

            if available_models:
                current_model = available_models[0]
                logger.info(f"✅ Found {len(available_models)} OLLAMA models: {available_models}")
            else:
                logger.warning("⚠️ No OLLAMA models found. Run: ollama pull mistral")
        else:
            logger.warning("⚠️ OLLAMA not responding. Make sure 'ollama serve' is running")
    except Exception as e:
        logger.warning(f"⚠️ Could not load OLLAMA models: {e}")

# Routes

@app.get("/")
async def root():
    """Redirect to dashboard"""
    return {"message": "AI Code Agent - Open http://localhost:8000 in browser"}

@app.get("/api/models", response_model=dict)
async def get_models():
    """Get available OLLAMA models"""
    models = [
        ModelInfo(name=m, current=(m == current_model))
        for m in available_models
    ]
    return {
        "models": models,
        "current": current_model,
        "status": "ok" if available_models else "no_models"
    }

@app.post("/api/models/select")
async def select_model(body: dict):
    """Switch to different model"""
    global current_model
    model_name = body.get("model")

    if not model_name or model_name not in available_models:
        raise HTTPException(status_code=400, detail="Invalid model")

    current_model = model_name
    logger.info(f"Switched to model: {current_model}")
    return {"model": current_model, "status": "switched"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with OLLAMA AI"""

    if not available_models:
        raise HTTPException(
            status_code=503,
            detail="OLLAMA not available. Make sure 'ollama serve' is running and has models installed (ollama pull mistral)"
        )

    model = request.model or current_model
    message = request.message.strip()

    if not message:
        raise HTTPException(status_code=400, detail="Empty message")

    if len(message) > 5000:
        raise HTTPException(status_code=400, detail="Message too long")

    try:
        # Call OLLAMA
        result = subprocess.run(
            ["ollama", "run", model, message],
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout
        )

        if result.returncode != 0:
            logger.error(f"OLLAMA error: {result.stderr}")
            raise HTTPException(status_code=500, detail="OLLAMA error")

        response_text = result.stdout.strip()

        if not response_text:
            response_text = "I'm thinking... but got empty response from OLLAMA. Try again!"

        return ChatResponse(
            response=response_text,
            model=model
        )

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Response timeout - model taking too long")
    except FileNotFoundError:
        raise HTTPException(status_code=503, detail="OLLAMA not installed or not in PATH")
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/health")
async def health():
    """Health check"""
    ollama_ok = bool(available_models)
    return {
        "status": "ok" if ollama_ok else "degraded",
        "ollama": "connected" if ollama_ok else "not_responding",
        "models": available_models,
        "current_model": current_model
    }

# Mount static files (frontend)
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
    logger.info(f"✅ Frontend mounted from {frontend_path}")
else:
    logger.warning(f"⚠️ Frontend directory not found: {frontend_path}")

# Startup info
@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown"""
    logger.info("🛑 Shutting down...")

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting AI Code Agent...")
    logger.info("📡 Backend: http://localhost:8000")
    logger.info("💡 Make sure OLLAMA is running: ollama serve")
    uvicorn.run(app, host="0.0.0.0", port=8000)
