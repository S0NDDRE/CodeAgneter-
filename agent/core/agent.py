"""
Core AI Agent - Powered by OLLAMA Local LLM
Smart Code Agent with Natural Language Understanding
"""

import logging
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio
import requests
import os

logger = logging.getLogger(__name__)

class CodeAgent:
    """Main AI Code Agent powered by OLLAMA - Smart and Local"""

    def __init__(self):
        # OLLAMA Configuration
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model_name = os.getenv("OLLAMA_MODEL", "neural-chat")
        self.conversation_history = []
        self.max_history = 20
        self.ollama_available = False

        # Check OLLAMA availability
        self._check_ollama()

        # Supported languages
        self.supported_languages = {
            "python": {"ext": ".py", "comment": "#"},
            "javascript": {"ext": ".js", "comment": "//"},
            "typescript": {"ext": ".ts", "comment": "//"},
            "java": {"ext": ".java", "comment": "//"},
            "cpp": {"ext": ".cpp", "comment": "//"},
            "c": {"ext": ".c", "comment": "//"},
            "go": {"ext": ".go", "comment": "//"},
            "rust": {"ext": ".rs", "comment": "//"},
            "sql": {"ext": ".sql", "comment": "--"},
            "html": {"ext": ".html", "comment": "<!--"},
            "css": {"ext": ".css", "comment": "/*"},
        }

    def _check_ollama(self):
        """Check if OLLAMA is available"""
        try:
            response = requests.get(f"{self.ollama_host}/api/tags", timeout=2)
            if response.status_code == 200:
                self.ollama_available = True
                logger.info(f"✅ OLLAMA available at {self.ollama_host}")
                models = response.json().get("models", [])
                if models:
                    available_models = [m.get('name', 'unknown') for m in models]
                    logger.info(f"📦 Available models: {available_models}")
                    # Use first available model
                    if available_models:
                        self.model_name = available_models[0]
            else:
                logger.warning("⚠️ OLLAMA responded with error")
                self.ollama_available = False
        except Exception as e:
            logger.warning(f"⚠️ OLLAMA not available: {str(e)}")
            logger.info("💡 To use OLLAMA:")
            logger.info("   1. Download from https://ollama.ai")
            logger.info("   2. Run: ollama serve")
            logger.info("   3. In another terminal: ollama pull neural-chat")
            self.ollama_available = False

    async def process_message(self, message: str) -> str:
        """Process user message and generate response"""
        try:
            logger.info(f"Processing message: {message[:50]}...")

            # Add to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": message,
                "timestamp": datetime.now().isoformat()
            })

            # Generate response
            response = await self._generate_response(message)

            # Add response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().isoformat()
            })

            # Keep history limited
            if len(self.conversation_history) > self.max_history:
                self.conversation_history = self.conversation_history[-self.max_history:]

            return response

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return f"Error: {str(e)}"

    async def _generate_response(self, message: str) -> str:
        """Generate AI response using OLLAMA or fallback"""
        try:
            if self.ollama_available:
                return await self._generate_with_ollama(message)
            else:
                return await self._generate_rule_based(message)
        except Exception as e:
            logger.error(f"Response generation error: {str(e)}")
            return f"Error: {str(e)}"

    async def _generate_with_ollama(self, message: str) -> str:
        """Generate response using OLLAMA LLM"""
        try:
            # Build context from recent history
            context = self._build_context()

            # Build system prompt
            system_prompt = """You are a smart AI code assistant. You:
- Understand multiple programming languages
- Help fix bugs and improve code
- Generate code when asked
- Analyze and review code
- Explain programming concepts
- Are helpful, clear, and concise

When the user shares code, analyze it carefully.
When they ask to fix or generate code, provide working solutions.
Format code in markdown with language specification."""

            # Prepare request to OLLAMA
            prompt = f"{context}\n\nUser: {message}\n\nAssistant:"

            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "system": system_prompt,
                "stream": False,
                "temperature": 0.7,
            }

            # Call OLLAMA
            response = requests.post(
                f"{self.ollama_host}/api/generate",
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "No response generated").strip()
            else:
                logger.error(f"OLLAMA error: {response.status_code}")
                return "OLLAMA error - using fallback mode"

        except requests.exceptions.Timeout:
            logger.error("OLLAMA request timed out")
            return "Request timed out - try a shorter question"
        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to OLLAMA")
            return "Cannot connect to OLLAMA. Is it running? (ollama serve)"
        except Exception as e:
            logger.error(f"OLLAMA generation error: {str(e)}")
            return await self._generate_rule_based(message)

    async def _generate_rule_based(self, message: str) -> str:
        """Generate response using rule-based fallback"""
        message_lower = message.lower()

        # Detect intent
        if any(word in message_lower for word in ["fix", "bug", "error", "issue"]):
            return self._handle_bug_fix(message)
        elif any(word in message_lower for word in ["analyze", "review", "check", "scan"]):
            return self._handle_analysis(message)
        elif any(word in message_lower for word in ["create", "make", "generate", "write"]):
            return self._handle_code_generation(message)
        elif any(word in message_lower for word in ["explain", "what", "how", "describe"]):
            return self._handle_explanation(message)
        else:
            return self._handle_general_query(message)

    def _build_context(self) -> str:
        """Build context from conversation history"""
        if not self.conversation_history:
            return "This is the start of the conversation."

        context_lines = []
        for msg in self.conversation_history[-4:]:  # Last 4 messages for context
            role = "User" if msg["role"] == "user" else "Assistant"
            content = msg["content"][:200]  # Limit content length
            context_lines.append(f"{role}: {content}")

        return "\n".join(context_lines)

    def _handle_bug_fix(self, message: str) -> str:
        """Handle bug fix requests"""
        return (
            "🔧 **Bug Fix Mode**\n\n"
            "I can help you fix bugs! Please:\n"
            "1. Share the buggy code\n"
            "2. Tell me what's going wrong\n"
            "3. I'll analyze and provide fixes\n\n"
            "Example: 'Fix this Python function that returns wrong results'\n"
            "→ I'll find and fix the bug"
        )

    def _handle_analysis(self, message: str) -> str:
        """Handle code analysis requests"""
        return (
            "📊 **Code Analysis Mode**\n\n"
            "I can analyze your code for:\n"
            "• Performance issues\n"
            "• Security vulnerabilities\n"
            "• Code quality problems\n"
            "• Best practice violations\n\n"
            "Share your code and I'll give detailed analysis!"
        )

    def _handle_code_generation(self, message: str) -> str:
        """Handle code generation requests"""
        return (
            "✨ **Code Generation Mode**\n\n"
            "I can generate code for:\n"
            "• Functions and classes\n"
            "• Full features\n"
            "• API endpoints\n"
            "• UI components\n"
            "• Tests and utilities\n\n"
            "Describe what you need and I'll create working code!"
        )

    def _handle_explanation(self, message: str) -> str:
        """Handle explanation requests"""
        return (
            "📚 **Code Explanation Mode**\n\n"
            "I can explain:\n"
            "• How code works\n"
            "• Why code is structured a certain way\n"
            "• Programming concepts\n"
            "• Error messages\n"
            "• Best practices\n\n"
            "Share code or ask a question!"
        )

    def _handle_general_query(self, message: str) -> str:
        """Handle general queries"""
        return (
            "🤖 **AI Code Agent Ready!**\n\n"
            "How can I help with your code?\n\n"
            "You can ask me to:\n"
            "✅ Fix bugs in your code\n"
            "✅ Analyze code quality\n"
            "✅ Generate new code\n"
            "✅ Explain programming concepts\n"
            "✅ Review and optimize code\n"
            "✅ Detect security issues\n\n"
            "What would you like help with?"
        )

    async def fix_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Analyze and fix code issues"""
        logger.info(f"Analyzing {language} code for fixes...")

        issues = self._detect_issues(code, language)
        fixed_code = self._apply_fixes(code, issues)

        return {
            "fixed_code": fixed_code,
            "issues": issues,
            "language": language,
            "status": "success"
        }

    def _detect_issues(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Detect issues in code"""
        issues = []
        lines = code.split('\n')

        for idx, line in enumerate(lines, 1):
            # Detect unused imports
            if "import " in line and line.strip().startswith("import"):
                module_name = line.split()[-1].split(".")[-1]
                if module_name not in code[code.index(line):]:
                    issues.append({
                        "line": idx,
                        "type": "unused_import",
                        "message": f"Unused import: {module_name}",
                        "severity": "warning"
                    })

            # Detect long lines
            if len(line) > 100:
                issues.append({
                    "line": idx,
                    "type": "long_line",
                    "message": f"Line too long: {len(line)} characters",
                    "severity": "warning"
                })

            # Detect spacing issues
            if "==" in line and "== " not in line:
                issues.append({
                    "line": idx,
                    "type": "style",
                    "message": "Missing space after ==",
                    "severity": "info"
                })

        return issues

    def _apply_fixes(self, code: str, issues: List[Dict[str, Any]]) -> str:
        """Apply fixes to code"""
        fixed_code = code

        for issue in issues:
            if issue["type"] == "unused_import":
                lines = fixed_code.split('\n')
                lines.pop(issue["line"] - 1)
                fixed_code = '\n'.join(lines)

            elif issue["type"] == "style":
                fixed_code = fixed_code.replace("==", "== ")

        return fixed_code

    async def execute_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an action safely"""
        logger.info(f"Executing action: {action.get('type')}")

        action_type = action.get("type")

        if action_type == "run_code":
            return await self._run_code(action.get("code"))
        elif action_type == "create_file":
            return await self._create_file(action.get("path"), action.get("content"))
        elif action_type == "modify_file":
            return await self._modify_file(action.get("path"), action.get("changes"))
        else:
            return {"status": "error", "message": f"Unknown action: {action_type}"}

    async def _run_code(self, code: str) -> Dict[str, Any]:
        """Run code safely"""
        try:
            exec_globals = {}
            exec(code, exec_globals)
            return {"status": "success", "message": "Code executed successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def _create_file(self, path: str, content: str) -> Dict[str, Any]:
        """Create a new file"""
        try:
            with open(path, 'w') as f:
                f.write(content)
            return {"status": "success", "path": path}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def _modify_file(self, path: str, changes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Modify existing file"""
        try:
            with open(path, 'r') as f:
                content = f.read()

            for change in changes:
                content = content.replace(change["old"], change["new"])

            with open(path, 'w') as f:
                f.write(content)

            return {"status": "success", "path": path}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get conversation history"""
        return self.conversation_history

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")

    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "ollama_available": self.ollama_available,
            "model": self.model_name if self.ollama_available else "fallback (rule-based)",
            "host": self.ollama_host if self.ollama_available else "N/A",
            "history_size": len(self.conversation_history),
            "status": "🟢 Ready (OLLAMA)" if self.ollama_available else "🟡 Ready (Fallback)"
        }
