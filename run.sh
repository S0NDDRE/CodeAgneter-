#!/bin/bash
# AI Code Agent Dashboard - Startup Script

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════╗"
echo "║    🤖 AI Code Agent Dashboard - Startup         ║"
echo "║       Smart Local Code Assistant                 ║"
echo "╚═══════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is required but not installed.${NC}"
    echo "Please install Python 3.8 or higher from https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} detected${NC}"

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}→ Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate venv
echo -e "${YELLOW}→ Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
if [ ! -f ".venv_installed" ]; then
    echo -e "${YELLOW}→ Installing dependencies...${NC}"
    pip install -q -r requirements.txt
    touch .venv_installed
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${GREEN}✓ Dependencies already installed${NC}"
fi

# Check if port 8000 is available
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}⚠ Port 8000 is already in use${NC}"
    echo "Please close the application using port 8000 or use a different port"
    exit 1
fi

# Start backend
echo -e "${GREEN}✓ Starting backend server...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
python3 backend/main.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 2

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}✗ Failed to start backend${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Backend is running (PID: $BACKEND_PID)${NC}"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ AI Code Agent is ready!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Open your browser and go to:"
echo -e "   ${BLUE}http://localhost:8000${NC}"
echo ""
echo "2. Start using the AI Code Agent:"
echo "   - Chat with the AI agent"
echo "   - Analyze your code"
echo "   - Capture and understand screens"
echo ""
echo "3. Keyboard shortcuts:"
echo "   - Ctrl+K: Focus chat input"
echo "   - Ctrl+Enter: Send message"
echo "   - Ctrl+S: Save chat history"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Handle Ctrl+C
trap "echo -e '\n${YELLOW}Stopping server...${NC}'; kill $BACKEND_PID 2>/dev/null; exit 0" INT TERM

# Keep script running
wait $BACKEND_PID
