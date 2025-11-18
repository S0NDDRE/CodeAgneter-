"""Ultra simple AI Chat - just works"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Msg(BaseModel):
    msg: str

@app.post("/ask")
def ask(data: Msg):
    """Send message to OLLAMA"""
    try:
        result = subprocess.run(
            f'ollama run mistral "{data.msg}"',
            shell=True,
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            return {"reply": result.stdout.strip()}
        else:
            return {"reply": f"Error: {result.stderr[:200]}"}
    except Exception as e:
        return {"reply": f"Error: {str(e)[:100]}"}

@app.get("/")
def home():
    return {"status": "OK - open http://localhost:8000 in browser"}

# Serve frontend
from pathlib import Path
frontend = Path(__file__).parent.parent / "frontend"
if frontend.exists():
    app.mount("/", StaticFiles(directory=str(frontend), html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 AI Chat Server\nGo to: http://localhost:8000\nMake sure: ollama serve\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
