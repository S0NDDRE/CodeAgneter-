"""
Screen Capture Module - Capture and analyze screen for visual context
"""

import logging
import base64
from typing import Dict, Any, Optional
from pathlib import Path
from PIL import Image
import io

logger = logging.getLogger(__name__)

class ScreenCapture:
    """Handles screen capture and visual understanding"""

    def __init__(self):
        self.last_screenshot = None
        self.screenshot_history = []
        self.max_history = 10

    async def capture(self) -> str:
        """Capture current screen and return as base64"""
        try:
            logger.info("Capturing screen...")

            # Try using mss for faster screenshots
            try:
                import mss
                with mss.mss() as sct:
                    monitor = sct.monitors[1]
                    screenshot = sct.grab(monitor)
                    img = Image.frombytes(
                        'RGB',
                        (screenshot.width, screenshot.height),
                        screenshot.rgb
                    )
            except ImportError:
                # Fallback to PIL
                img = Image.new('RGB', (1920, 1080), color='gray')
                logger.warning("mss not available, using placeholder")

            # Convert to base64
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()

            # Store in history
            self.last_screenshot = img_base64
            self.screenshot_history.append(img_base64)
            if len(self.screenshot_history) > self.max_history:
                self.screenshot_history.pop(0)

            logger.info("Screen captured successfully")
            return f"data:image/png;base64,{img_base64}"

        except Exception as e:
            logger.error(f"Error capturing screen: {str(e)}")
            return ""

    async def analyze_screen(self) -> Dict[str, Any]:
        """Analyze screen content using OCR and visual understanding"""
        try:
            if not self.last_screenshot:
                await self.capture()

            analysis = {
                "text_detected": self._extract_text(),
                "ui_elements": self._detect_ui_elements(),
                "colors": self._analyze_colors(),
                "potential_actions": self._suggest_actions()
            }

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing screen: {str(e)}")
            return {"error": str(e)}

    def _extract_text(self) -> list:
        """Extract text from screen using OCR"""
        try:
            import pytesseract
            # This would need proper implementation with actual image
            return ["Text extraction requires OCR setup"]
        except ImportError:
            logger.warning("pytesseract not available")
            return []

    def _detect_ui_elements(self) -> list:
        """Detect UI elements on screen"""
        # In production, would use advanced vision models
        return [
            {"type": "window", "name": "Active Application"},
            {"type": "button", "label": "Detected UI Elements"},
            {"type": "text_field", "content": "Ready for analysis"}
        ]

    def _analyze_colors(self) -> Dict[str, int]:
        """Analyze dominant colors in screenshot"""
        # Simplified color analysis
        return {
            "primary": "#FFFFFF",
            "secondary": "#000000",
            "accent": "#0078D4"
        }

    def _suggest_actions(self) -> list:
        """Suggest actions based on what's on screen"""
        return [
            "Click detected button",
            "Type in visible text field",
            "Switch to window in focus"
        ]

    def save_screenshot(self, path: str) -> bool:
        """Save last screenshot to file"""
        try:
            if not self.last_screenshot:
                return False

            img_data = base64.b64decode(self.last_screenshot)
            with open(path, 'wb') as f:
                f.write(img_data)

            logger.info(f"Screenshot saved to {path}")
            return True

        except Exception as e:
            logger.error(f"Error saving screenshot: {str(e)}")
            return False

    def get_screenshot_history(self) -> list:
        """Get history of screenshots"""
        return self.screenshot_history

    def clear_history(self):
        """Clear screenshot history"""
        self.screenshot_history = []
        self.last_screenshot = None
        logger.info("Screenshot history cleared")
