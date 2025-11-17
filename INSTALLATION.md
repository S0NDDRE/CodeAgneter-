# 📥 Installation Guide - AI Code Agent Dashboard

Detaljerte instruksjoner for installasjon og oppsett av AI Code Agent Dashboard.

---

## 🖥️ System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|------------|
| Python | 3.8 | 3.10+ |
| RAM | 2GB | 4GB+ |
| Disk Space | 500MB | 2GB |
| OS | Linux/macOS/Windows | Any modern OS |
| Browser | Modern browser | Chrome/Firefox/Edge |

---

## 📦 Step 1: Prerequisites

### macOS & Linux
```bash
# Check Python version
python3 --version  # Should be 3.8 or higher

# Install pip if needed
sudo apt-get install python3-pip  # Ubuntu/Debian
brew install python3  # macOS
```

### Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, **check "Add Python to PATH"**
3. Open Command Prompt and verify:
   ```cmd
   python --version
   ```

---

## 🚀 Step 2: Clone Repository

```bash
# Using HTTPS
git clone https://github.com/S0NDDRE/CodeAgneter-.git
cd CodeAgneter-

# Or using SSH
git clone git@github.com:S0NDDRE/CodeAgneter-.git
cd CodeAgneter-
```

---

## 🔧 Step 3: Setup Virtual Environment

### macOS & Linux
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

### Windows
```cmd
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate.bat

# Or in PowerShell:
venv\Scripts\Activate.ps1

# You should see (venv) in your terminal prompt
```

---

## 📚 Step 4: Install Dependencies

```bash
# Upgrade pip (recommended)
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# This may take 2-5 minutes depending on internet speed
```

**If you get errors:**
- On macOS: Install Xcode Command Line Tools: `xcode-select --install`
- On Linux: Install build tools: `sudo apt-get install build-essential python3-dev`
- On Windows: Ensure Python is added to PATH, then restart your terminal

---

## 🎯 Step 5: Configure Application

1. **Edit `config/settings.yaml` if needed:**
   ```bash
   nano config/settings.yaml  # Linux/macOS
   notepad config\settings.yaml  # Windows
   ```

2. **Default settings are fine for most users**

---

## ▶️ Step 6: Start the Application

### Option A: Using the startup script (Recommended)

**macOS & Linux:**
```bash
./run.sh
```

**Windows:**
```cmd
run.bat
```

### Option B: Manual startup

**All platforms:**
```bash
# Make sure venv is activated
# (venv) should appear in your terminal

python backend/main.py
```

---

## 🌐 Step 7: Access the Dashboard

1. Open your web browser
2. Navigate to: **http://localhost:8000**
3. You should see the AI Code Agent Dashboard
4. Start chatting! 💬

---

## 🎮 Usage After Installation

### First Time Setup
1. Welcome to the agent
2. Try the chat feature
3. Upload a code file to analyze
4. Explore other features

### Keyboard Shortcuts
| Shortcut | Action |
|----------|--------|
| `Ctrl+K` | Focus chat input |
| `Ctrl+Enter` | Send message |
| `Ctrl+S` | Save chat |
| `Ctrl+N` | New chat |
| `Ctrl+A` | Go to analyze |

---

## 🔧 Troubleshooting

### Issue: "Python not found"
**Solution:**
- Ensure Python is installed and added to PATH
- Restart your terminal after installation
- Try `python3` instead of `python`

### Issue: "Port 8000 is already in use"
**Solution:**
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process (get PID from above)
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Or use a different port - edit backend/main.py:
# Change: uvicorn.run(app, host="0.0.0.0", port=8000)
# To: uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Issue: "Module not found" errors
**Solution:**
```bash
# Make sure virtual environment is activated
# (venv) should show in terminal

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: "Connection refused" when opening http://localhost:8000
**Solution:**
1. Check if backend is running (should see output in terminal)
2. Wait 3-5 seconds for backend to fully start
3. Refresh the browser page (F5)
4. Check browser console for errors (F12)

### Issue: Dashboard loads but no functionality works
**Solution:**
1. Open browser developer console (F12)
2. Check the Console tab for errors
3. Ensure backend is running in the other terminal
4. Restart both backend and refresh browser

---

## 📝 Advanced Configuration

### Using a Different Port
Edit `backend/main.py`:
```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Change 8000 to 8001
```

Then update `frontend/src/utils/api.js`:
```javascript
constructor(baseURL = 'http://localhost:8001/api') {
```

### Enable Debug Mode
Edit `backend/main.py`:
```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
```

### Custom AI Model
Edit `config/settings.yaml`:
```yaml
agent:
  model: "codellama"  # or mistral, etc.
```

---

## 🔄 Updating the Application

```bash
# Fetch latest changes
git fetch origin

# Update to latest version
git pull origin main

# Reinstall dependencies (in case new packages were added)
pip install -r requirements.txt --upgrade
```

---

## 📦 Optional: Install for Development

If you want to contribute:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/
```

---

## 🚪 Uninstalling

```bash
# Deactivate virtual environment
deactivate

# Remove venv folder
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows

# Remove project folder
cd ..
rm -rf CodeAgneter-  # macOS/Linux
rmdir /s CodeAgneter-  # Windows
```

---

## 💬 Need Help?

1. **Check the README.md** for features and overview
2. **Review troubleshooting section above**
3. **Check browser console** (F12) for error messages
4. **Review logs** in the terminal where backend is running
5. **Create an issue** on GitHub with error details

---

## ✅ Installation Checklist

- [ ] Python 3.8+ installed
- [ ] Repository cloned
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] `run.sh` or `run.bat` executed
- [ ] Dashboard accessible at http://localhost:8000
- [ ] Can send messages in chat
- [ ] Can analyze code
- [ ] Ready to use!

---

**Happy coding! 🚀**
