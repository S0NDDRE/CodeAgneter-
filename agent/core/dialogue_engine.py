"""
Dialogue Engine - Natural conversation with smart follow-ups
ChatGPT-style interaction with context awareness
"""

import logging
from typing import Dict, List, Any, Optional, AsyncGenerator
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class DialogueEngine:
    """Smart dialogue system for natural conversations"""

    def __init__(self):
        self.conversation_context = []
        self.max_context = 10
        self.follow_up_suggestions = []
        self.clarifying_questions = []

    def add_to_context(self, role: str, message: str, metadata: Dict = None):
        """Add message to conversation context"""
        context_item = {
            "role": role,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.conversation_context.append(context_item)

        # Keep context limited
        if len(self.conversation_context) > self.max_context:
            self.conversation_context = self.conversation_context[-self.max_context:]

        logger.info(f"Context added: {role} - {message[:50]}...")

    def get_context_summary(self) -> str:
        """Get summary of recent conversation"""
        if not self.conversation_context:
            return "Start of conversation"

        summary_lines = []
        for item in self.conversation_context[-5:]:
            role = "User" if item["role"] == "user" else "Assistant"
            msg = item["message"][:100]
            summary_lines.append(f"{role}: {msg}")

        return "\n".join(summary_lines)

    def detect_intent(self, message: str) -> Dict[str, Any]:
        """Detect user intent from message"""
        message_lower = message.lower()

        intents = {
            "code_fix": ["fix", "bug", "error", "wrong", "broken", "crash"],
            "code_generation": ["create", "make", "generate", "write", "build", "implement"],
            "explanation": ["explain", "what", "how", "why", "describe", "tell me"],
            "analysis": ["analyze", "review", "check", "scan", "audit", "evaluate"],
            "optimization": ["optimize", "faster", "performance", "improve", "speed"],
            "learning": ["learn", "teach", "tutorial", "example", "understand"],
            "clarification": ["what do you mean", "clarify", "unclear", "confused"],
            "follow_up": ["and", "also", "plus", "more", "what about"],
        }

        detected = []
        for intent, keywords in intents.items():
            if any(kw in message_lower for kw in keywords):
                detected.append(intent)

        return {
            "primary_intent": detected[0] if detected else "general",
            "all_intents": detected,
            "confidence": len(detected) / len(intents)
        }

    def generate_follow_ups(self, last_response: str, intent: str) -> List[str]:
        """Generate smart follow-up suggestions"""
        follow_ups = {
            "code_fix": [
                "Do you want me to explain what was wrong?",
                "Should I also optimize this while I'm at it?",
                "Want me to add error handling too?",
            ],
            "code_generation": [
                "Would you like me to add error handling?",
                "Do you want tests for this code?",
                "Should I add documentation?",
            ],
            "explanation": [
                "Do you want a more detailed explanation?",
                "Want to see a practical example?",
                "Should I explain related concepts?",
            ],
            "analysis": [
                "Do you want specific recommendations?",
                "Should I prioritize the issues?",
                "Want me to show the fixes?",
            ],
            "optimization": [
                "Do you want benchmarks?",
                "Should I implement the optimization?",
                "Want to see before/after comparison?",
            ],
        }

        return follow_ups.get(intent, [
            "Is there anything else you'd like to know?",
            "Do you have other questions?",
            "Want me to help with something else?",
        ])

    def generate_clarifying_questions(self, message: str) -> List[str]:
        """Generate clarifying questions if message is ambiguous"""
        message_lower = message.lower()

        # Check for vague requests
        if "it" in message_lower and message.count(" it ") > 1:
            return [
                "What specifically do you mean by 'it'?",
                "Can you be more specific about what you want me to fix?",
            ]

        if "that" in message_lower:
            return [
                "Can you clarify what you're referring to?",
                "Which part exactly do you mean?",
            ]

        if len(message.split()) < 5:
            return [
                "Can you give me more details?",
                "What specifically would you like me to help with?",
            ]

        if "?" not in message and any(x in message_lower for x in ["please", "can you", "could you"]):
            return [
                "Do you want me to do this now?",
                "Should I implement this immediately?",
            ]

        return []

    def format_response(
        self,
        main_response: str,
        intent: str,
        include_follow_ups: bool = True
    ) -> Dict[str, Any]:
        """Format response with follow-ups and suggestions"""
        follow_ups = self.generate_follow_ups(main_response, intent) if include_follow_ups else []

        return {
            "main_response": main_response,
            "intent": intent,
            "follow_ups": follow_ups[:2],  # Max 2 follow-ups
            "timestamp": datetime.now().isoformat()
        }

    def should_ask_clarifying_questions(self, message: str) -> bool:
        """Determine if clarifying questions are needed"""
        message_lower = message.lower()

        # Too short
        if len(message.split()) < 3:
            return True

        # Ambiguous pronouns
        if message_lower.count(" it ") > 0 or message_lower.count(" that ") > 0:
            return True

        # Multiple potential meanings
        if message.count(",") > 2:
            return True

        return False

    def create_dialogue_turn(
        self,
        user_message: str,
        agent_response: str,
        intent: str
    ) -> Dict[str, Any]:
        """Create a complete dialogue turn with context"""
        self.add_to_context("user", user_message)
        self.add_to_context("assistant", agent_response)

        clarifying = self.generate_clarifying_questions(user_message)
        follow_ups = self.generate_follow_ups(agent_response, intent)

        return {
            "user_message": user_message,
            "agent_response": agent_response,
            "intent": intent,
            "clarifying_questions": clarifying if self.should_ask_clarifying_questions(user_message) else [],
            "follow_up_suggestions": follow_ups[:2],
            "context_length": len(self.conversation_context),
            "timestamp": datetime.now().isoformat()
        }

    def get_conversation_summary(self) -> str:
        """Get summary of entire conversation"""
        if not self.conversation_context:
            return "No conversation yet"

        user_msgs = sum(1 for m in self.conversation_context if m["role"] == "user")
        agent_msgs = sum(1 for m in self.conversation_context if m["role"] == "assistant")

        summary = f"Conversation: {user_msgs} user messages, {agent_msgs} agent responses\n\n"
        summary += "Recent exchange:\n"
        for item in self.conversation_context[-4:]:
            role = "User" if item["role"] == "user" else "Agent"
            msg = item["message"][:80]
            summary += f"{role}: {msg}...\n"

        return summary

    def reset_context(self):
        """Clear conversation context"""
        self.conversation_context = []
        logger.info("Conversation context reset")
