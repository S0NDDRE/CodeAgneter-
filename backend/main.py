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
from agent.core.model_manager import ModelManager
from agent.core.negotiation import NegotiationManager
from agent.analysis.code_analyzer import CodeAnalyzer
from agent.screen.screen_capture import ScreenCapture
from agent.monitor.folder_monitor import FolderMonitor

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
model_manager = ModelManager()
negotiation_manager = NegotiationManager()
folder_monitor = FolderMonitor()  # Will be started on demand

# Store active websocket connections
active_connections: dict[str, WebSocket] = {}
monitor_notifications: List[Dict[str, Any]] = []  # Store monitor notifications

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

# Model Management Routes

@app.get("/api/models")
async def get_models():
    """Get available OLLAMA models"""
    return model_manager.get_models()

@app.get("/api/models/popular")
async def get_popular_models():
    """Get popular models available for download"""
    return {
        "status": "ok",
        "models": model_manager.get_popular_models()
    }

@app.post("/api/models/download")
async def download_model(data: dict):
    """Download a new OLLAMA model"""
    try:
        model_name = data.get("model_name")
        if not model_name:
            raise HTTPException(status_code=400, detail="model_name required")

        result = await model_manager.download_model(model_name)
        return result
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.post("/api/models/switch")
async def switch_model(data: dict):
    """Switch to a different model"""
    try:
        model_name = data.get("model_name")
        if not model_name:
            raise HTTPException(status_code=400, detail="model_name required")

        result = model_manager.switch_model(model_name)
        if result["status"] == "success":
            code_agent.model_name = model_name
        return result
    except Exception as e:
        logger.error(f"Switch error: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.delete("/api/models/{model_name}")
async def delete_model(model_name: str):
    """Delete a model"""
    try:
        result = await model_manager.delete_model(model_name)
        return result
    except Exception as e:
        logger.error(f"Delete error: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/api/models/status")
async def model_status():
    """Get model manager status"""
    return model_manager.get_status()

# Negotiation Routes

@app.post("/api/negotiate/propose")
async def propose_action(data: dict):
    """Agent proposes an action for user approval"""
    try:
        session_id = data.get("session_id", f"session_{datetime.now().timestamp()}")
        action_type = data.get("action_type")
        description = data.get("description")
        details = data.get("details", {})

        result = negotiation_manager.propose_action(
            session_id, action_type, description, details
        )
        return result
    except Exception as e:
        logger.error(f"Propose error: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.post("/api/negotiate/respond")
async def respond_to_proposal(data: dict):
    """User responds to proposed action"""
    try:
        session_id = data.get("session_id")
        response = data.get("response")

        if not session_id or not response:
            raise HTTPException(status_code=400, detail="session_id and response required")

        result = negotiation_manager.handle_user_response(session_id, response)
        return result
    except Exception as e:
        logger.error(f"Response error: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.post("/api/negotiate/execute")
async def execute_agreed_action(data: dict):
    """Execute agreed action"""
    try:
        session_id = data.get("session_id")
        if not session_id:
            raise HTTPException(status_code=400, detail="session_id required")

        # Check permission first
        session = negotiation_manager.get_session(session_id)
        if not session or not session.agreed_action:
            return {"status": "error", "message": "No agreed action found"}

        action = session.agreed_action
        if not security_manager.check_permission(action.get("type")):
            return {"status": "error", "message": "Action not permitted"}

        # Execute the action
        exec_result = await code_agent.execute_action(action)

        # Mark as completed
        negotiation_manager.execute_action(session_id)

        return {
            "status": "success",
            "execution": exec_result,
            "message": "Action executed and completed!"
        }
    except Exception as e:
        logger.error(f"Execute error: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/api/negotiate/{session_id}")
async def get_negotiation_status(session_id: str):
    """Get negotiation session status"""
    try:
        result = negotiation_manager.get_session_status(session_id)
        return result
    except Exception as e:
        logger.error(f"Status error: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/api/negotiate/history")
async def get_negotiation_history():
    """Get negotiation history"""
    return {
        "status": "ok",
        "history": negotiation_manager.get_history()
    }

# Folder Monitor Routes

@app.post("/api/monitor/start")
async def start_monitoring(data: dict):
    """Start monitoring a folder"""
    try:
        path = data.get("path")
        if not path:
            raise HTTPException(status_code=400, detail="path required")

        # Set watch path
        folder_monitor.watch_path = Path(path)

        # Start monitoring
        if folder_monitor.start():
            return {
                "status": "started",
                "path": path,
                "message": f"Monitoring {path}"
            }
        else:
            return {
                "status": "error",
                "message": f"Failed to start monitoring {path}"
            }
    except Exception as e:
        logger.error(f"Monitor start error: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.post("/api/monitor/stop")
async def stop_monitoring():
    """Stop monitoring"""
    try:
        folder_monitor.stop()
        return {
            "status": "stopped",
            "message": "Monitoring stopped"
        }
    except Exception as e:
        logger.error(f"Monitor stop error: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/api/monitor/status")
async def monitor_status():
    """Get monitor status"""
    return folder_monitor.get_status()

@app.get("/api/monitor/changes")
async def get_changes(limit: int = 20):
    """Get recent changes detected"""
    return {
        "status": "ok",
        "changes": folder_monitor.get_changes(limit)
    }

@app.get("/api/monitor/analysis")
async def get_analysis(file_path: str = None):
    """Get analysis results"""
    return {
        "status": "ok",
        "analysis": folder_monitor.get_analysis(file_path)
    }

@app.post("/api/monitor/clear")
async def clear_history():
    """Clear monitor history"""
    try:
        folder_monitor.clear_history()
        return {
            "status": "cleared",
            "message": "Monitor history cleared"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Root route
@app.get("/")
async def root():
    return {"message": "AI Code Agent API - Use /docs for API documentation"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
