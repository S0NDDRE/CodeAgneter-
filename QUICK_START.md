# 🚀 AI Code Agent - Quick Start Guide for Windows 11

## ⚡ TL;DR (Fastest Way)

1. Extract ZIP file
2. Double-click `run.bat`
3. Browser opens → Done! 🎉

---

## 📋 Prerequisites

You need:
- ✅ **Python 3.8+** (you have 3.14, perfect!)
- ✅ **OLLAMA** running (download from ollama.ai)

### Install Python
- Download from: https://python.org
- **IMPORTANT**: Check "Add Python to PATH" during installation

### Install & Run OLLAMA
1. Download from: https://ollama.ai
2. Open a new Command Prompt/PowerShell
3. Run: `ollama serve`
4. Keep this window open while using the agent!

---

## 🏃 Step-by-Step Setup

### Step 1: Extract ZIP
- Right-click `CodeAgneter-complete.zip`
- Select "Extract All..."
- Choose location (Desktop recommended)
- Open the extracted `CodeAgneter-` folder

### Step 2: Run the Application
- **Double-click** `run.bat` in the project folder
- Wait ~3-5 seconds for setup
- Your browser automatically opens to `http://localhost:8000`

### Step 3: Start Using
- Type in the chat box
- Click buttons for analysis, monitoring, etc.
- Everything is local - enjoy! 🎊

---

## ✅ What Happens When You Run `run.bat`

1. ✓ Creates virtual environment (one time)
2. ✓ Installs dependencies with pip (one time)
3. ✓ Starts FastAPI backend server
4. ✓ Opens browser to the dashboard
5. ✓ Ready to chat with AI agent!

---

## 🛑 Troubleshooting

### "Python not found"
- Restart your computer after Python installation
- Make sure you checked "Add to PATH"

### "OLLAMA not responding"
- Open Command Prompt
- Run: `ollama serve`
- Keep it running in background

### "Address already in use"
- Another app is using port 8000
- Change port in `config/settings.yaml` → `api.port: 8001`

### Browser doesn't open
- Manually go to: `http://localhost:8000`

### Dependencies installation fails
- Delete the `venv` folder
- Delete `.venv_installed` file
- Run `run.bat` again

---

## 📁 Folder Structure

```
CodeAgneter-/
├── backend/              # FastAPI server
├── agent/               # AI agent logic
│   ├── core/           # Agent, dialogue, models
│   ├── analysis/       # Code analysis
│   └── monitor/        # Folder monitoring
├── frontend/           # Web dashboard
│   ├── index.html
│   └── src/           # JS components
├── config/            # Settings
├── requirements.txt   # Dependencies
├── run.bat           # Windows startup
└── README.md         # Full documentation
```

---

## 🎯 Features

Once running, you can:
- 💬 **Chat** with the AI agent naturally
- 🔍 **Analyze** your code
- 📁 **Monitor** folders in real-time
- 🖥️ **Capture** and analyze screens
- 🤖 **Switch** OLLAMA models
- ✅ **Negotiate** with AI before actions

---

## 🔧 Common Commands

| Action | How |
|--------|-----|
| Stop the app | Press Ctrl+C in the run.bat window |
| Change OLLAMA model | Use the Models tab in the dashboard |
| Monitor a folder | Use the Monitor tab |
| Check logs | Look in the `logs/` folder |

---

## 📞 Need Help?

Check these files in the project:
- `README.md` - Full documentation
- `FEATURES.md` - All features explained
- `INSTALLATION.md` - Detailed installation
- `OLLAMA_SETUP.md` - OLLAMA guide

---

## ✨ You're Ready!

Everything is tested and working. Just:
1. Make sure Python 3.14 + OLLAMA are installed
2. Double-click `run.bat`
3. Enjoy your local AI agent! 🚀

---

**Made with ❤️ - 100% local, 100% free, 100% yours!**
