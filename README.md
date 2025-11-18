# 🤖 AI Code Agent Dashboard

**Advanced AI-powered code assistant with visual context understanding and multi-language support.**

A professional, locally-running AI code agent that understands your code, sees your screen, and helps you build better software. 100% local processing - no data sent to the cloud.

![Status](https://img.shields.io/badge/Status-Beta-yellow)
![License](https://img.shields.io/badge/License-MIT-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)

---

## ✨ Features

### 🧠 **Intelligent Code Understanding**
- Support for 10+ programming languages (Python, JavaScript, TypeScript, Java, C++, Go, Rust, SQL, HTML, CSS)
- Deep code analysis and understanding
- Smart bug detection and fixing
- Code quality assessment and scoring

### 💻 **Modern Dashboard Interface**
- Beautiful, responsive web-based dashboard
- Real-time chat with AI agent
- Code syntax highlighting and formatting
- Keyboard shortcuts for power users
- Auto-save chat history

### 📊 **Advanced Analysis Tools**
- Single file code analysis
- Entire project analysis
- Performance issue detection
- Security vulnerability scanning
- Code smell identification

### 🖥️ **Screen Capture & Understanding**
- Capture current screen
- Visual context analysis
- UI element detection
- OCR text extraction
- Context-aware suggestions

### 📁 **File Management**
- Browse project files
- Quick file navigation
- File tree visualization
- Integrated code viewer

### 🔒 **Security First**
- 100% local processing
- Approval-required actions
- Safe sandboxed code execution
- Permission-based access control
- Audit logging of all operations

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or conda
- Modern web browser

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd CodeAgneter-
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   # Start the backend (Terminal 1)
   python backend/main.py

   # Start the frontend (Terminal 2)
   # Open http://localhost:8000 in your browser
   ```

---

## 📖 Usage Guide

### Chat Mode
- Type naturally to ask for help with your code
- Supports code blocks for analysis
- Use Ctrl+Enter to send messages
- Attach files with the 📎 button

### Code Analysis
- Upload code files or paste directly
- Analyze entire projects
- View detailed quality reports
- Get specific improvement suggestions

### Screen Capture
- Click "Capture Screen" to take a screenshot
- Agent analyzes visual context
- Get smart suggestions based on what you see

### Keyboard Shortcuts
- `Ctrl+N` - New chat
- `Ctrl+K` - Focus chat input
- `Ctrl+S` - Save chat history
- `Ctrl+A` - Go to analyze page
- `Ctrl+P` - Go to screen page
- `Ctrl+Enter` - Send message

---

## 🏗️ Architecture

```
CodeAgneter-/
├── backend/
│   └── main.py              # FastAPI application
├── agent/
│   ├── core/
│   │   ├── agent.py         # Main AI agent logic
│   │   └── security.py      # Security manager
│   ├── analysis/
│   │   └── code_analyzer.py # Code analysis engine
│   └── screen/
│       └── screen_capture.py # Screen capture module
├── frontend/
│   ├── index.html           # Main HTML
│   └── src/
│       ├── styles/
│       │   └── main.css     # Styling
│       ├── components/
│       │   ├── chat.js      # Chat component
│       │   ├── analyzer.js  # Analyzer component
│       │   ├── screen.js    # Screen component
│       │   └── files.js     # File manager component
│       ├── utils/
│       │   ├── api.js       # API client
│       │   └── ui.js        # UI utilities
│       └── app.js           # Main app
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

---

## 🔧 Configuration

Edit `config/settings.yaml` to customize:

```yaml
agent:
  model: "neural-chat"
  response_speed: 5
  auto_save_history: true

security:
  require_approval: true
  sandbox_code: true

ui:
  theme: "light"
  syntax_highlighting: true
```

---

## 🛠️ API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Send message to agent |
| POST | `/api/analyze` | Analyze code file |
| POST | `/api/fix-code` | Auto-fix code issues |
| POST | `/api/analyze-project` | Analyze entire project |
| GET | `/api/screen-capture` | Capture screen |
| WS | `/ws/agent` | WebSocket for real-time chat |

---

## 💡 Example Use Cases

### Bug Fixing
```
User: "Fix this Python function - it's returning wrong results"
Agent: Analyzes code → Finds bugs → Suggests fixes → Explains changes
```

### Code Review
```
User: "Review this code for performance issues"
Agent: Scans for bottlenecks → Suggests optimizations → Provides examples
```

### Project Analysis
```
User: "Analyze my entire project"
Agent: Maps structure → Finds issues → Generates report → Recommends improvements
```

### Learning & Documentation
```
User: "Explain how this algorithm works"
Agent: Breaks down logic → Explains concepts → Shows examples
```

---

## 🔐 Security & Privacy

- **100% Local**: All processing happens on your machine
- **No Cloud Upload**: Your code never leaves your computer
- **Approval Required**: You must approve sensitive operations
- **Audit Log**: All actions are logged for review
- **Sandboxed Execution**: Code runs in isolated environment

---

## 🚧 Roadmap

- [ ] Integration with version control (Git)
- [ ] Advanced AI models (GPT-4, Claude)
- [ ] Real-time code collaboration
- [ ] IDE plugins (VSCode, JetBrains)
- [ ] Database query optimization
- [ ] DevOps automation assistance
- [ ] CI/CD pipeline suggestions

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

MIT License - see [LICENSE](LICENSE) for details

---

## 💬 Support & Feedback

- 📧 Email: support@codeagent.local
- 🐛 Report bugs: Create an issue
- 💡 Suggest features: Discussions tab
- 📚 Documentation: Check [docs/](docs/)

---

## 🎯 Key Capabilities at a Glance

| Feature | Status | Details |
|---------|--------|---------|
| Multi-language support | ✅ | 10+ languages |
| Code analysis | ✅ | Quality scoring |
| Bug detection | ✅ | Automatic fixing |
| Screen capture | ✅ | Visual context |
| Chat interface | ✅ | Real-time communication |
| Project analysis | ✅ | Full codebase review |
| File management | ✅ | Browser integration |
| Security sandbox | ✅ | Safe execution |
| Keyboard shortcuts | ✅ | Power user support |
| History tracking | ✅ | Conversation memory |

---

**Built with ❤️ for developers, by developers.**

Ready to code smarter? Let's go! 🚀
