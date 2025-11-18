"""
Security Manager - Handles permissions and safety checks
"""

import logging
from typing import List, Dict, Any
from pathlib import Path
import json

logger = logging.getLogger(__name__)

class SecurityManager:
    """Manages security permissions and approvals"""

    def __init__(self):
        self.allowed_actions = {
            "read_files": True,
            "write_files": False,  # Requires approval
            "execute_code": False,  # Requires approval
            "modify_system": False,  # Requires approval
            "delete_files": False,  # Requires approval
            "install_packages": False,  # Requires approval
        }

        self.allowed_paths = [
            str(Path.home() / "projects"),
            str(Path.home() / "code"),
            "/tmp"
        ]

        self.dangerous_keywords = [
            "rm -rf",
            "del /s /q",
            "drop database",
            "truncate table",
            "chmod 777",
            "sudo",
        ]

    def check_permission(self, action: str) -> bool:
        """Check if action is permitted"""
        if action not in self.allowed_actions:
            logger.warning(f"Unknown action: {action}")
            return False

        return self.allowed_actions.get(action, False)

    def request_approval(self, action: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """Request user approval for sensitive action"""
        logger.warning(f"Approval requested for: {action}")

        return {
            "status": "pending",
            "action": action,
            "details": details,
            "requires_user_approval": True,
            "message": f"User approval required for: {action}"
        }

    def grant_approval(self, action: str, approved: bool):
        """Grant or deny approval for action"""
        if approved:
            self.allowed_actions[action] = True
            logger.info(f"Action approved: {action}")
        else:
            logger.warning(f"Action denied: {action}")

    def is_safe_path(self, path: str) -> bool:
        """Check if path is safe to access"""
        try:
            path_obj = Path(path).resolve()

            for allowed_path in self.allowed_paths:
                allowed_obj = Path(allowed_path).resolve()
                try:
                    path_obj.relative_to(allowed_obj)
                    return True
                except ValueError:
                    continue

            logger.warning(f"Unsafe path access attempted: {path}")
            return False
        except Exception as e:
            logger.error(f"Error checking path safety: {str(e)}")
            return False

    def is_safe_code(self, code: str) -> bool:
        """Check if code contains dangerous operations"""
        code_lower = code.lower()

        for keyword in self.dangerous_keywords:
            if keyword.lower() in code_lower:
                logger.warning(f"Dangerous keyword detected: {keyword}")
                return False

        return True

    def sanitize_path(self, path: str) -> str:
        """Sanitize file path"""
        # Remove potentially dangerous path traversal attempts
        path = path.replace("../", "").replace("..\\", "")
        return path

    def log_action(self, action: str, details: Dict[str, Any], allowed: bool):
        """Log security-relevant actions"""
        log_entry = {
            "action": action,
            "allowed": allowed,
            "details": details
        }
        logger.info(f"Security log: {json.dumps(log_entry)}")
