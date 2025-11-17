"""
Core AI Agent - Code understanding and automation
Supports multiple languages and AI models
"""

import logging
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)

class CodeAgent:
    """Main AI Code Agent for code understanding and automation"""

    def __init__(self):
        self.model_name = "neural-chat"  # Default model
        self.conversation_history = []
        self.max_history = 20
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
        """Generate AI response using local model"""
        # This would integrate with Ollama or local LLM
        # For now, returning a smart response based on message analysis

        # Detect what the user is asking for
        message_lower = message.lower()

        if any(word in message_lower for word in ["fix", "bug", "error", "issue"]):
            return await self._handle_bug_fix(message)
        elif any(word in message_lower for word in ["analyze", "review", "check"]):
            return await self._handle_analysis(message)
        elif any(word in message_lower for word in ["create", "make", "generate", "write"]):
            return await self._handle_code_generation(message)
        elif any(word in message_lower for word in ["explain", "what", "how", "describe"]):
            return await self._handle_explanation(message)
        else:
            return await self._handle_general_query(message)

    async def _handle_bug_fix(self, message: str) -> str:
        return (
            "🔧 **Bug Fix Assistant**\n\n"
            "I can help you fix bugs! Please:\n"
            "1. Share the code with the issue\n"
            "2. Tell me what's going wrong\n"
            "3. I'll analyze and provide fixes\n\n"
            "Ready when you are! 🚀"
        )

    async def _handle_analysis(self, message: str) -> str:
        return (
            "📊 **Code Analysis**\n\n"
            "I can analyze your code for:\n"
            "- Performance issues\n"
            "- Security vulnerabilities\n"
            "- Best practice violations\n"
            "- Complexity assessment\n\n"
            "Share your code and I'll provide detailed analysis! 📈"
        )

    async def _handle_code_generation(self, message: str) -> str:
        return (
            "✨ **Code Generation**\n\n"
            "I can generate code for:\n"
            "- Functions and classes\n"
            "- Full features\n"
            "- UI components\n"
            "- API endpoints\n\n"
            "Describe what you need and I'll create it! 💻"
        )

    async def _handle_explanation(self, message: str) -> str:
        return (
            "📚 **Code Explanation**\n\n"
            "I can explain:\n"
            "- How code works\n"
            "- Why code is structured a certain way\n"
            "- Best practices and patterns\n"
            "- Error messages\n\n"
            "Share the code and ask your question! 🤔"
        )

    async def _handle_general_query(self, message: str) -> str:
        return (
            "🤖 **AI Code Agent**\n\n"
            "How can I help you with coding?\n"
            "- Fix bugs\n"
            "- Analyze code\n"
            "- Generate new code\n"
            "- Explain code\n"
            "- Optimize performance\n\n"
            "What do you need help with?"
        )

    async def fix_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Analyze and fix code issues"""
        logger.info(f"Fixing {language} code...")

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

        # Basic issue detection
        lines = code.split('\n')

        for idx, line in enumerate(lines, 1):
            # Detect unused variables (basic heuristic)
            if "import " in line and line.strip().startswith("import"):
                # Check if imported module is used
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

            # Detect missing spaces after operators
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
        """Run code safely (with restrictions)"""
        try:
            # This would need proper sandboxing in production
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
