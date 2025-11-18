"""
Folder Monitor - Real-time code monitoring with auto-analysis
Watches folders, detects changes, analyzes, suggests fixes
"""

import logging
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
from datetime import datetime
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

logger = logging.getLogger(__name__)

class CodeChangeHandler(FileSystemEventHandler):
    """Handle file system events"""

    def __init__(self, callback: Callable, ignore_patterns: List[str] = None):
        self.callback = callback
        self.ignore_patterns = ignore_patterns or ['.git', '__pycache__', 'node_modules', '.venv', 'venv']
        self.debounce_timer = {}

    def should_ignore(self, path: str) -> bool:
        """Check if path should be ignored"""
        for pattern in self.ignore_patterns:
            if pattern in path:
                return True
        return False

    def on_modified(self, event):
        """File modified event"""
        if event.is_directory or self.should_ignore(event.src_path):
            return

        # Debounce rapid changes (wait 2 seconds)
        if event.src_path in self.debounce_timer:
            self.debounce_timer[event.src_path].cancel()

        timer = asyncio.Timer(
            2.0,
            lambda: self.callback('modified', event.src_path)
        )
        self.debounce_timer[event.src_path] = timer
        timer.start()

    def on_created(self, event):
        """File created event"""
        if event.is_directory or self.should_ignore(event.src_path):
            return

        asyncio.create_task(
            self._async_callback('created', event.src_path)
        )

    def on_deleted(self, event):
        """File deleted event"""
        if event.is_directory or self.should_ignore(event.src_path):
            return

        asyncio.create_task(
            self._async_callback('deleted', event.src_path)
        )

    async def _async_callback(self, event_type: str, path: str):
        """Async callback wrapper"""
        self.callback(event_type, path)


class FolderMonitor:
    """Monitor folder for code changes"""

    def __init__(self, watch_path: str = None):
        self.watch_path = Path(watch_path) if watch_path else Path.home()
        self.observer = None
        self.is_monitoring = False
        self.change_history = []
        self.max_history = 100
        self.last_analysis = {}
        self.notification_callbacks = []

    def start(self) -> bool:
        """Start monitoring folder"""
        try:
            if not self.watch_path.exists():
                logger.error(f"Path not found: {self.watch_path}")
                return False

            # Create observer
            self.observer = Observer()

            # Create event handler
            handler = CodeChangeHandler(self._on_file_change)

            # Watch folder recursively
            self.observer.schedule(handler, str(self.watch_path), recursive=True)
            self.observer.start()

            self.is_monitoring = True
            logger.info(f"✅ Monitoring: {self.watch_path}")

            return True

        except Exception as e:
            logger.error(f"Error starting monitor: {str(e)}")
            return False

    def stop(self):
        """Stop monitoring"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.is_monitoring = False
            logger.info("⏹️ Monitoring stopped")

    def _on_file_change(self, event_type: str, file_path: str):
        """Handle file change event"""
        try:
            change = {
                "type": event_type,
                "file": file_path,
                "timestamp": datetime.now().isoformat(),
                "status": "detected"
            }

            self.change_history.append(change)
            if len(self.change_history) > self.max_history:
                self.change_history.pop(0)

            logger.info(f"📝 {event_type.upper()}: {Path(file_path).name}")

            # Notify subscribers
            self._notify_subscribers("file_change", change)

            # If code file, analyze it
            if self._is_code_file(file_path) and event_type == "modified":
                asyncio.create_task(self._analyze_changed_file(file_path))

        except Exception as e:
            logger.error(f"Error handling change: {str(e)}")

    async def _analyze_changed_file(self, file_path: str):
        """Analyze changed file"""
        try:
            path = Path(file_path)

            # Read file
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Basic analysis
            analysis = {
                "file": str(path),
                "timestamp": datetime.now().isoformat(),
                "lines": len(content.split('\n')),
                "size": len(content),
                "issues": self._quick_analyze(content, path.suffix),
            }

            self.last_analysis[file_path] = analysis

            # Notify if issues found
            if analysis["issues"]:
                logger.warning(f"⚠️ Issues in {path.name}: {len(analysis['issues'])} found")
                self._notify_subscribers("analysis_complete", analysis)

        except Exception as e:
            logger.error(f"Error analyzing file: {str(e)}")

    def _quick_analyze(self, content: str, extension: str) -> List[Dict[str, Any]]:
        """Quick analysis of code"""
        issues = []
        lines = content.split('\n')

        for idx, line in enumerate(lines, 1):
            # Check for common issues
            if "TODO" in line or "FIXME" in line:
                issues.append({
                    "line": idx,
                    "type": "todo",
                    "message": line.strip()[:50],
                    "severity": "info"
                })

            if "print(" in line or "console.log" in line:
                issues.append({
                    "line": idx,
                    "type": "debug_statement",
                    "message": "Debug statement found",
                    "severity": "warning"
                })

            if any(x in line for x in ["password=", "api_key=", "secret="]):
                issues.append({
                    "line": idx,
                    "type": "security",
                    "message": "Potential hardcoded secret",
                    "severity": "critical"
                })

        return issues

    def _is_code_file(self, file_path: str) -> bool:
        """Check if file is code file"""
        extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c',
            '.go', '.rs', '.sql', '.html', '.css', '.json', '.yaml', '.yml'
        }
        return Path(file_path).suffix.lower() in extensions

    def subscribe(self, callback: Callable):
        """Subscribe to notifications"""
        self.notification_callbacks.append(callback)

    def _notify_subscribers(self, event_type: str, data: Dict[str, Any]):
        """Notify all subscribers"""
        for callback in self.notification_callbacks:
            try:
                asyncio.create_task(self._run_callback(callback, event_type, data))
            except Exception as e:
                logger.error(f"Error notifying subscriber: {str(e)}")

    async def _run_callback(self, callback: Callable, event_type: str, data: Dict):
        """Run callback safely"""
        try:
            if asyncio.iscoroutinefunction(callback):
                await callback(event_type, data)
            else:
                callback(event_type, data)
        except Exception as e:
            logger.error(f"Callback error: {str(e)}")

    def get_status(self) -> Dict[str, Any]:
        """Get monitor status"""
        return {
            "is_monitoring": self.is_monitoring,
            "watch_path": str(self.watch_path),
            "changes_detected": len(self.change_history),
            "last_changes": self.change_history[-5:] if self.change_history else [],
            "status": "🟢 Monitoring" if self.is_monitoring else "🔴 Stopped"
        }

    def get_changes(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent changes"""
        return self.change_history[-limit:]

    def get_analysis(self, file_path: str = None) -> Dict[str, Any]:
        """Get analysis results"""
        if file_path:
            return self.last_analysis.get(file_path, {})
        return self.last_analysis

    def clear_history(self):
        """Clear change history"""
        self.change_history = []
        self.last_analysis = {}
        logger.info("History cleared")
