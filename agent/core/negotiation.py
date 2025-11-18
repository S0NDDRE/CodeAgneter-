"""
Smart Negotiation System - User & Agent agree before action
Dialogue-based decision making
"""

import logging
from typing import Dict, List, Any, Optional
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)

class ActionState(Enum):
    """States of action negotiation"""
    PROPOSED = "proposed"      # Agent proposed action
    DISCUSSING = "discussing"   # User and agent discussing
    AGREED = "agreed"          # Both agreed
    REJECTED = "rejected"      # User rejected
    COMPLETED = "completed"    # Action completed

class NegotiationSession:
    """Single negotiation session between user and agent"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.state = ActionState.DISCUSSING
        self.conversation = []
        self.proposed_action = None
        self.user_concerns = []
        self.agent_suggestions = []
        self.agreed_action = None
        self.created_at = datetime.now()

    def add_user_message(self, message: str):
        """User sends message"""
        self.conversation.append({
            "speaker": "user",
            "message": message,
            "timestamp": datetime.now().isoformat()
        })

    def add_agent_message(self, message: str):
        """Agent sends message"""
        self.conversation.append({
            "speaker": "agent",
            "message": message,
            "timestamp": datetime.now().isoformat()
        })

    def propose_action(self, action: Dict[str, Any]):
        """Agent proposes an action"""
        self.proposed_action = action
        self.state = ActionState.PROPOSED
        logger.info(f"Action proposed: {action.get('type')}")

    def add_concern(self, concern: str):
        """User expresses concern"""
        self.user_concerns.append({
            "concern": concern,
            "timestamp": datetime.now().isoformat()
        })

    def add_suggestion(self, suggestion: str):
        """Agent makes suggestion"""
        self.agent_suggestions.append({
            "suggestion": suggestion,
            "timestamp": datetime.now().isoformat()
        })

    def agree(self, action: Dict[str, Any]):
        """User and agent agree on action"""
        self.agreed_action = action
        self.state = ActionState.AGREED
        logger.info(f"Action agreed: {action.get('type')}")

    def reject(self, reason: str):
        """User rejects action"""
        self.state = ActionState.REJECTED
        self.conversation.append({
            "speaker": "user",
            "message": f"Rejected: {reason}",
            "timestamp": datetime.now().isoformat()
        })
        logger.info(f"Action rejected: {reason}")

    def complete(self):
        """Mark action as completed"""
        self.state = ActionState.COMPLETED
        logger.info("Action completed")

    def get_summary(self) -> Dict[str, Any]:
        """Get negotiation summary"""
        return {
            "session_id": self.session_id,
            "state": self.state.value,
            "proposed_action": self.proposed_action,
            "agreed_action": self.agreed_action,
            "user_concerns": self.user_concerns,
            "agent_suggestions": self.agent_suggestions,
            "messages_count": len(self.conversation),
            "created_at": self.created_at.isoformat()
        }

class NegotiationManager:
    """Manage negotiation sessions"""

    def __init__(self):
        self.sessions: Dict[str, NegotiationSession] = {}
        self.history = []

    def create_session(self, session_id: str) -> NegotiationSession:
        """Create new negotiation session"""
        session = NegotiationSession(session_id)
        self.sessions[session_id] = session
        logger.info(f"Created negotiation session: {session_id}")
        return session

    def get_session(self, session_id: str) -> Optional[NegotiationSession]:
        """Get existing session"""
        return self.sessions.get(session_id)

    def propose_action(
        self,
        session_id: str,
        action_type: str,
        description: str,
        details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Agent proposes an action"""
        session = self.get_session(session_id)
        if not session:
            session = self.create_session(session_id)

        action = {
            "type": action_type,
            "description": description,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }

        session.propose_action(action)

        return {
            "status": "proposed",
            "session_id": session_id,
            "action": action,
            "message": f"Agent proposed: {description}\n\nDo you agree? (yes/no/modify)"
        }

    def handle_user_response(
        self,
        session_id: str,
        response: str,
        agent_model: Any = None
    ) -> Dict[str, Any]:
        """Handle user's response to proposed action"""
        session = self.get_session(session_id)
        if not session:
            return {"status": "error", "message": "Session not found"}

        session.add_user_message(response)
        response_lower = response.lower()

        # Parse user response
        if any(word in response_lower for word in ["yes", "ok", "agree", "do it", "go"]):
            # User agreed
            session.agree(session.proposed_action)
            return {
                "status": "agreed",
                "session_id": session_id,
                "action": session.agreed_action,
                "message": f"✅ Agreed! Executing: {session.agreed_action.get('description')}"
            }

        elif any(word in response_lower for word in ["no", "reject", "don't", "stop"]):
            # User rejected
            session.reject(response)
            return {
                "status": "rejected",
                "session_id": session_id,
                "message": "❌ Action cancelled. What would you like instead?"
            }

        elif any(word in response_lower for word in ["modify", "change", "different", "instead"]):
            # User wants to modify
            session.add_concern(response)
            return {
                "status": "discussing",
                "session_id": session_id,
                "message": "I understand your concern. Let me adjust the proposal...\n\n"
                          "What specifically would you like me to change?"
            }

        elif any(word in response_lower for word in ["why", "explain", "how", "tell"]):
            # User wants explanation
            session.add_concern(response)
            return {
                "status": "discussing",
                "session_id": session_id,
                "message": self._generate_explanation(session.proposed_action)
            }

        else:
            # Continue discussion
            session.add_user_message(response)
            return {
                "status": "discussing",
                "session_id": session_id,
                "message": "I understand. Let me help you with that.\n\n"
                          "Do you want me to proceed with the action, or would you like to modify it?"
            }

    def execute_action(self, session_id: str) -> Dict[str, Any]:
        """Execute agreed action"""
        session = self.get_session(session_id)
        if not session:
            return {"status": "error", "message": "Session not found"}

        if session.state != ActionState.AGREED:
            return {
                "status": "error",
                "message": "Action not agreed upon yet"
            }

        # Mark as completed
        session.complete()

        # Store in history
        self.history.append({
            "session_id": session_id,
            "action": session.agreed_action,
            "timestamp": datetime.now().isoformat()
        })

        return {
            "status": "executed",
            "session_id": session_id,
            "action": session.agreed_action,
            "message": "✅ Action completed successfully!"
        }

    def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get current session status"""
        session = self.get_session(session_id)
        if not session:
            return {"status": "error", "message": "Session not found"}

        return {
            "status": "ok",
            "session": session.get_summary(),
            "conversation": session.conversation[-5:]  # Last 5 messages
        }

    def get_history(self) -> List[Dict[str, Any]]:
        """Get negotiation history"""
        return self.history

    def _generate_explanation(self, action: Dict[str, Any]) -> str:
        """Generate explanation for proposed action"""
        action_type = action.get("type", "unknown")
        description = action.get("description", "")

        explanations = {
            "fix_code": f"I found and fixed issues in your code.\n\n{description}\n\n"
                       "This will improve code quality, performance, and reliability.",
            "generate_code": f"I'll create new code for you.\n\n{description}\n\n"
                            "This follows best practices and will be fully functional.",
            "analyze": f"I want to analyze your code.\n\n{description}\n\n"
                      "This will identify potential issues and improvements.",
            "create_file": f"I'll create a new file.\n\n{description}\n\n"
                          "The file will be created with the proposed content.",
        }

        return explanations.get(action_type, f"Action: {description}")

    def clear_old_sessions(self, max_age_hours: int = 24):
        """Clear old sessions"""
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(hours=max_age_hours)

        old_sessions = [
            sid for sid, session in self.sessions.items()
            if session.created_at < cutoff
        ]

        for sid in old_sessions:
            del self.sessions[sid]

        logger.info(f"Cleared {len(old_sessions)} old sessions")
