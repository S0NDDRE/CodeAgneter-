"""
AI Code Agent - Main FastAPI Application
Advanced code understanding and automation with visual context
"""

from fastapi import FastAPI, WebSocket, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
import json
import logging
from pathlib import Path
from datetime import datetime

from agent.core.agent import CodeAgent
from agent.core.security import SecurityManager
from agent.analysis.code_analyzer import CodeAnalyzer
from agent.screen.screen_capture import ScreenCapture

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Code Agent Dashboard",
    description="Advanced AI-powered code understanding and automation",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
code_agent = CodeAgent()
security_manager = SecurityManager()
code_analyzer = CodeAnalyzer()
screen_capture = ScreenCapture()

# Store active websocket connections
active_connections: dict[str, WebSocket] = {}

# Health check
@app.get("/health")
async def health():
    agent_status = code_agent.get_status()
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "agent": agent_status,
        "version": "1.0.0"
    }

# Agent status endpoint
@app.get("/api/agent-status")
async def agent_status_endpoint():
    """Get agent status and OLLAMA availability"""
    return code_agent.get_status()

# API Routes

@app.post("/api/chat")
async def chat(message: dict):
    """Send a message to the AI agent"""
    try:
        user_message = message.get("message")
        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required")

        # Get response from agent
        response = await code_agent.process_message(user_message)

        return {
            "status": "success",
            "response": response,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.post("/api/analyze")
async def analyze_code(file: UploadFile = File(...)):
    """Analyze uploaded code file"""
    try:
        content = await file.read()
        text_content = content.decode('utf-8')

        # Analyze code
        analysis = await code_analyzer.analyze(text_content, file.filename)

        return {
            "status": "success",
            "analysis": analysis,
            "filename": file.filename,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.post("/api/fix-code")
async def fix_code(data: dict):
    """Auto-fix code issues"""
    try:
        code = data.get("code")
        language = data.get("language", "python")

        if not code:
            raise HTTPException(status_code=400, detail="Code is required")

        # Get fixes from agent
        fixes = await code_agent.fix_code(code, language)

        return {
            "status": "success",
            "original": code,
            "fixed": fixes["fixed_code"],
            "issues": fixes["issues"],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Fix code error: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.post("/api/analyze-project")
async def analyze_project(data: dict):
    """Analyze entire project"""
    try:
        project_path = data.get("path")
        if not project_path:
            raise HTTPException(status_code=400, detail="Project path is required")

        # Analyze project
        analysis = await code_analyzer.analyze_project(project_path)

        return {
            "status": "success",
            "project": project_path,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Project analysis error: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/api/screen-capture")
async def capture_screen():
    """Capture current screen for visual context"""
    try:
        screenshot = await screen_capture.capture()

        return {
            "status": "success",
            "image": screenshot,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Screen capture error: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.websocket("/ws/agent")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket connection for real-time agent communication"""
    await websocket.accept()
    connection_id = str(id(websocket))
    active_connections[connection_id] = websocket

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)

            logger.info(f"WebSocket message: {message.get('type')}")

            # Process based on message type
            msg_type = message.get("type")

            if msg_type == "chat":
                response = await code_agent.process_message(message.get("content"))
                await websocket.send_json({
                    "type": "response",
                    "content": response,
                    "timestamp": datetime.now().isoformat()
                })

            elif msg_type == "analyze":
                analysis = await code_analyzer.analyze(message.get("code"))
                await websocket.send_json({
                    "type": "analysis",
                    "data": analysis,
                    "timestamp": datetime.now().isoformat()
                })

            elif msg_type == "execute":
                if not security_manager.check_permission(message.get("action")):
                    await websocket.send_json({
                        "type": "error",
                        "message": "Action not permitted"
                    })
                    continue

                result = await code_agent.execute_action(message.get("action"))
                await websocket.send_json({
                    "type": "result",
                    "data": result,
                    "timestamp": datetime.now().isoformat()
                })

    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
    finally:
        del active_connections[connection_id]

# Root route
@app.get("/")
async def root():
    return {"message": "AI Code Agent API - Use /docs for API documentation"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
