"""
OLLAMA Model Manager - Download, switch, manage models
"""

import logging
import requests
import json
from typing import Dict, List, Any, Optional
import subprocess
import os

logger = logging.getLogger(__name__)

class ModelManager:
    """Manage OLLAMA models - download, list, switch"""

    def __init__(self, ollama_host: str = "http://localhost:11434"):
        self.ollama_host = ollama_host
        self.available_models = []
        self.current_model = None
        self.refresh_models()

    def refresh_models(self):
        """Refresh list of available models"""
        try:
            response = requests.get(f"{self.ollama_host}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                self.available_models = [
                    {
                        "name": m.get("name", "unknown"),
                        "size": m.get("size", 0),
                        "modified": m.get("modified_at", "unknown")
                    }
                    for m in models
                ]
                if self.available_models:
                    self.current_model = self.available_models[0]["name"]
                logger.info(f"✅ Found {len(self.available_models)} models")
                return True
            return False
        except Exception as e:
            logger.error(f"Error refreshing models: {str(e)}")
            return False

    def get_models(self) -> Dict[str, Any]:
        """Get all available models"""
        return {
            "available": self.available_models,
            "current": self.current_model,
            "count": len(self.available_models)
        }

    def get_popular_models(self) -> List[Dict[str, Any]]:
        """Get list of popular models to download"""
        return [
            {
                "name": "neural-chat",
                "size": "4.7GB",
                "description": "Balansert og rask - ANBEFALT",
                "type": "general",
                "recommended": True
            },
            {
                "name": "codellama",
                "size": "3.8GB",
                "description": "Spesialisert på kode - BEST FOR KODING",
                "type": "code",
                "recommended": True
            },
            {
                "name": "mistral",
                "size": "4.1GB",
                "description": "Liten og rask - FOR GAMLE PC",
                "type": "general",
                "recommended": False
            },
            {
                "name": "llama2",
                "size": "3.8GB",
                "description": "Smart og kraftig - TRENGER RAM",
                "type": "general",
                "recommended": False
            },
            {
                "name": "openhermes",
                "size": "7.7GB",
                "description": "Veldig smart - TRENGER MYKJE RAM",
                "type": "general",
                "recommended": False
            },
            {
                "name": "dolphin-mixtral",
                "size": "26GB",
                "description": "Enorm kraft - KUN FOR KRAFTIG PC",
                "type": "general",
                "recommended": False
            }
        ]

    async def download_model(self, model_name: str) -> Dict[str, Any]:
        """Download a model from OLLAMA"""
        try:
            logger.info(f"📥 Starting download: {model_name}")

            # Call OLLAMA pull API
            payload = {"name": model_name}
            response = requests.post(
                f"{self.ollama_host}/api/pull",
                json=payload,
                stream=True,
                timeout=3600  # 1 hour timeout
            )

            if response.status_code == 200:
                # Parse streaming response
                chunks = []
                for line in response.iter_lines():
                    if line:
                        try:
                            chunk = json.loads(line)
                            chunks.append(chunk)
                            status = chunk.get("status", "")
                            digest = chunk.get("digest", "")[:12]
                            logger.info(f"  {status} {digest}")
                        except json.JSONDecodeError:
                            pass

                # Refresh models
                self.refresh_models()

                return {
                    "status": "success",
                    "model": model_name,
                    "message": f"Model {model_name} downloaded successfully!"
                }
            else:
                return {
                    "status": "error",
                    "message": f"Download failed: HTTP {response.status_code}"
                }

        except requests.exceptions.Timeout:
            return {
                "status": "error",
                "message": "Download timed out - try again or check internet"
            }
        except Exception as e:
            logger.error(f"Download error: {str(e)}")
            return {
                "status": "error",
                "message": f"Download failed: {str(e)}"
            }

    async def delete_model(self, model_name: str) -> Dict[str, Any]:
        """Delete a model"""
        try:
            logger.info(f"🗑️ Deleting model: {model_name}")

            payload = {"name": model_name}
            response = requests.delete(
                f"{self.ollama_host}/api/delete",
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                # Refresh models
                self.refresh_models()

                return {
                    "status": "success",
                    "message": f"Model {model_name} deleted"
                }
            else:
                return {
                    "status": "error",
                    "message": f"Delete failed: HTTP {response.status_code}"
                }

        except Exception as e:
            logger.error(f"Delete error: {str(e)}")
            return {
                "status": "error",
                "message": f"Delete failed: {str(e)}"
            }

    def switch_model(self, model_name: str) -> Dict[str, Any]:
        """Switch to a different model"""
        try:
            # Check if model exists
            if not any(m["name"] == model_name for m in self.available_models):
                return {
                    "status": "error",
                    "message": f"Model {model_name} not found"
                }

            self.current_model = model_name
            logger.info(f"🔄 Switched to model: {model_name}")

            return {
                "status": "success",
                "current_model": model_name,
                "message": f"Switched to {model_name}"
            }

        except Exception as e:
            logger.error(f"Switch error: {str(e)}")
            return {
                "status": "error",
                "message": f"Switch failed: {str(e)}"
            }

    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get info about a specific model"""
        for model in self.available_models:
            if model["name"] == model_name:
                return {
                    "status": "found",
                    "model": model
                }

        return {
            "status": "not_found",
            "message": f"Model {model_name} not found"
        }

    def get_status(self) -> Dict[str, Any]:
        """Get model manager status"""
        return {
            "current_model": self.current_model,
            "available_count": len(self.available_models),
            "available_models": [m["name"] for m in self.available_models],
            "total_size": self._calculate_total_size(),
            "status": "🟢 Ready" if self.available_models else "🟡 No models"
        }

    def _calculate_total_size(self) -> str:
        """Calculate total size of all models"""
        total = sum(m.get("size", 0) for m in self.available_models)
        if total < 1024**3:
            return f"{total / (1024**2):.1f}MB"
        else:
            return f"{total / (1024**3):.1f}GB"
