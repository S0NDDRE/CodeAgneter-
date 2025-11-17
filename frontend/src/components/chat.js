/**
 * Chat Component - Handles user-agent conversation
 */

class ChatComponent {
    constructor() {
        this.chatInput = document.getElementById('chat-input');
        this.sendBtn = document.getElementById('send-btn');
        this.chatMessages = document.getElementById('chat-messages');
        this.attachBtn = document.getElementById('attach-btn');
        this.codeBtn = document.getElementById('code-btn');
        this.screenBtn = document.getElementById('screen-btn');
        this.fileInput = null;
        this.codeMode = false;

        this.init();
    }

    init() {
        // Send button click
        this.sendBtn.addEventListener('click', () => this.sendMessage());

        // Enter to send (Ctrl+Enter)
        this.chatInput.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                this.sendMessage();
            }
        });

        // File attachment
        this.attachBtn.addEventListener('click', () => this.attachFile());

        // Code mode toggle
        this.codeBtn.addEventListener('click', () => this.toggleCodeMode());

        // Screen capture
        this.screenBtn.addEventListener('click', () => this.captureScreen());

        // Load chat history if available
        this.loadChatHistory();
    }

    async sendMessage() {
        const message = this.chatInput.value.trim();
        if (!message) return;

        // Show user message
        UIManager.addChatMessage(message, 'user');
        this.chatInput.value = '';
        this.chatInput.style.height = 'auto';

        // Show loading
        UIManager.showLoading();

        try {
            // Send to API
            const response = await api.sendMessage(message);

            if (response.status === 'success') {
                UIManager.addChatMessage(response.response, 'assistant');
                this.saveChatHistory();
            } else {
                UIManager.addChatMessage(`Error: ${response.message}`, 'system');
            }
        } catch (error) {
            UIManager.addChatMessage(`Connection error: ${error.message}`, 'system');
        } finally {
            UIManager.hideLoading();
        }
    }

    attachFile() {
        if (!this.fileInput) {
            this.fileInput = document.createElement('input');
            this.fileInput.type = 'file';
            this.fileInput.accept = '.py,.js,.ts,.java,.cpp,.c,.go,.rs,.sql,.html,.css,.json,.yaml,.yml,.txt';
            this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        }
        this.fileInput.click();
    }

    async handleFileSelect(e) {
        const file = e.target.files[0];
        if (!file) return;

        try {
            UIManager.showLoading();
            const content = await file.text();

            // Add code block to chat
            this.chatInput.value = `\`\`\`${this.getLanguageFromFile(file.name)}\n${content}\n\`\`\``;

            UIManager.showToast(`Loaded: ${file.name}`, 'success');
        } catch (error) {
            UIManager.showToast(`Error loading file: ${error.message}`, 'error');
        } finally {
            UIManager.hideLoading();
        }
    }

    toggleCodeMode() {
        this.codeMode = !this.codeMode;

        if (this.codeMode) {
            this.codeBtn.style.opacity = '1';
            this.codeBtn.style.color = '#0078D4';
            this.chatInput.placeholder = 'Paste code here... (Ctrl+Enter to send)';
        } else {
            this.codeBtn.style.opacity = '0.6';
            this.codeBtn.style.color = 'inherit';
            this.chatInput.placeholder = 'Ask me anything... (Ctrl+Enter to send)';
        }
    }

    async captureScreen() {
        try {
            UIManager.showLoading();
            const result = await api.captureScreen();

            if (result.status === 'success') {
                UIManager.showToast('Screen captured! Adding to message...', 'success');
                this.chatInput.value += '\n[Screen captured and analyzed]';
                this.chatInput.focus();
            } else {
                UIManager.showToast('Failed to capture screen', 'error');
            }
        } catch (error) {
            UIManager.showToast(`Screen capture error: ${error.message}`, 'error');
        } finally {
            UIManager.hideLoading();
        }
    }

    getLanguageFromFile(filename) {
        const ext = filename.split('.').pop().toLowerCase();
        const languages = {
            'py': 'python',
            'js': 'javascript',
            'jsx': 'javascript',
            'ts': 'typescript',
            'tsx': 'typescript',
            'java': 'java',
            'cpp': 'cpp',
            'cc': 'cpp',
            'c': 'c',
            'h': 'c',
            'go': 'go',
            'rs': 'rust',
            'sql': 'sql',
            'html': 'html',
            'css': 'css',
            'json': 'json',
            'yaml': 'yaml',
            'yml': 'yaml'
        };
        return languages[ext] || 'text';
    }

    saveChatHistory() {
        const messages = [];
        this.chatMessages.querySelectorAll('.message').forEach((msg) => {
            const role = msg.classList.contains('user') ? 'user' : 'assistant';
            const content = msg.querySelector('.message-content').textContent;
            messages.push({ role, content, timestamp: new Date().toISOString() });
        });

        localStorage.setItem('chatHistory', JSON.stringify(messages));
    }

    loadChatHistory() {
        const settings = JSON.parse(localStorage.getItem('chatSettings') || '{"autoSave": true}');
        if (!settings.autoSave) return;

        const history = JSON.parse(localStorage.getItem('chatHistory') || '[]');
        if (history.length === 0) return;

        this.chatMessages.innerHTML = '';
        history.forEach((msg) => {
            UIManager.addChatMessage(msg.content, msg.role);
        });
    }

    clearHistory() {
        this.chatMessages.innerHTML = `
            <div class="message system">
                <div class="message-content">
                    <p>👋 Welcome to AI Code Agent!</p>
                    <p>I can help you with:</p>
                    <ul>
                        <li>💻 Code analysis and understanding</li>
                        <li>🐛 Bug detection and fixing</li>
                        <li>✨ Code generation and completion</li>
                        <li>📊 Project analysis</li>
                        <li>🔍 Code review and optimization</li>
                    </ul>
                </div>
            </div>
        `;
        localStorage.removeItem('chatHistory');
        UIManager.showToast('Chat history cleared', 'info');
    }
}

// Initialize chat when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('chat-input')) {
        window.chatComponent = new ChatComponent();
    }
});
