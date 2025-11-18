/**
 * Enhanced Chat Component - ChatGPT-style streaming and natural dialogue
 */

class ChatComponentEnhanced {
    constructor() {
        this.chatInput = document.getElementById('chat-input');
        this.sendBtn = document.getElementById('send-btn');
        this.chatMessages = document.getElementById('chat-messages');
        this.attachBtn = document.getElementById('attach-btn');
        this.codeBtn = document.getElementById('code-btn');
        this.screenBtn = document.getElementById('screen-btn');
        this.fileInput = null;
        this.codeMode = false;
        this.isStreaming = false;
        this.currentMessageElement = null;

        this.init();
    }

    init() {
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.chatInput.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter' && !this.isStreaming) {
                this.sendMessage();
            }
        });

        this.attachBtn.addEventListener('click', () => this.attachFile());
        this.codeBtn.addEventListener('click', () => this.toggleCodeMode());
        this.screenBtn.addEventListener('click', () => this.captureScreen());

        this.loadChatHistory();
    }

    async sendMessage() {
        const message = this.chatInput.value.trim();
        if (!message || this.isStreaming) return;

        // Show user message
        UIManager.addChatMessage(message, 'user');
        this.chatInput.value = '';
        this.chatInput.style.height = 'auto';

        // Create message element for streaming response
        this.createMessageElement('assistant');

        UIManager.showLoading();

        try {
            // Get streaming response from agent
            await this.getStreamingResponse(message);

            // After response, show follow-up suggestions
            this.showFollowUpSuggestions();

            // Save to history
            this.saveChatHistory();
        } catch (error) {
            UIManager.addChatMessage(
                `Connection error: ${error.message}`,
                'system'
            );
        } finally {
            UIManager.hideLoading();
            this.sendBtn.disabled = false;
        }
    }

    createMessageElement(role) {
        const messagesEl = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.id = `msg-${Date.now()}`;
        contentDiv.style.minHeight = '20px';

        messageDiv.appendChild(contentDiv);
        messagesEl.appendChild(messageDiv);

        this.currentMessageElement = contentDiv;
        messagesEl.scrollTop = messagesEl.scrollHeight;

        return contentDiv;
    }

    async getStreamingResponse(message) {
        try {
            this.isStreaming = true;
            this.sendBtn.disabled = true;

            const response = await api.sendMessage(message);

            // Simulate streaming effect - show response word by word
            if (response.status === 'success') {
                await this.streamText(response.response);
            } else {
                this.currentMessageElement.textContent = `Error: ${response.message}`;
            }
        } catch (error) {
            this.currentMessageElement.textContent = `Error: ${error.message}`;
        } finally {
            this.isStreaming = false;
        }
    }

    async streamText(text) {
        /**
         * Stream text word by word (ChatGPT style)
         * Gives illusion of real-time typing
         */
        const words = text.split(' ');
        let displayText = '';

        for (let word of words) {
            displayText += word + ' ';

            // Format and display
            if (displayText.includes('```')) {
                // Handle code blocks
                this.currentMessageElement.innerHTML = UIManager.parseMarkdown(displayText);
            } else if (displayText.includes('**') || displayText.includes('_')) {
                // Handle markdown
                this.currentMessageElement.innerHTML = UIManager.parseMarkdown(displayText);
            } else {
                this.currentMessageElement.textContent = displayText;
            }

            // Small delay for streaming effect
            await new Promise(resolve => setTimeout(resolve, 20));
        }

        // Final render with formatting
        this.currentMessageElement.innerHTML = UIManager.parseMarkdown(displayText);

        // Scroll to bottom
        document.getElementById('chat-messages').scrollTop =
            document.getElementById('chat-messages').scrollHeight;
    }

    showFollowUpSuggestions() {
        /**
         * Show smart follow-up suggestions like ChatGPT
         */
        const suggestions = [
            "Can you explain that more?",
            "Show me an example",
            "How do I implement this?",
            "What are the alternatives?"
        ];

        // Randomly pick 2 suggestions
        const picked = suggestions.sort(() => 0.5 - Math.random()).slice(0, 2);

        const suggestionsDiv = document.createElement('div');
        suggestionsDiv.style.cssText = `
            margin: 10px 0;
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        `;

        picked.forEach(suggestion => {
            const btn = document.createElement('button');
            btn.style.cssText = `
                padding: 8px 12px;
                background: #f0f0f0;
                border: 1px solid #ddd;
                border-radius: 20px;
                cursor: pointer;
                font-size: 12px;
                transition: all 0.2s;
            `;
            btn.textContent = suggestion;
            btn.onmouseover = () => btn.style.background = '#e0e0e0';
            btn.onmouseout = () => btn.style.background = '#f0f0f0';
            btn.onclick = () => {
                this.chatInput.value = suggestion;
                this.sendMessage();
            };

            suggestionsDiv.appendChild(btn);
        });

        if (this.currentMessageElement) {
            this.currentMessageElement.parentElement.appendChild(suggestionsDiv);
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

            this.chatInput.value = `📄 **File: ${file.name}**\n\`\`\`${this.getLanguageFromFile(file.name)}\n${content}\n\`\`\`\n\nPlease analyze this.`;

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
                this.chatInput.value += '\n🖥️ [Screen captured and ready for analysis]';
                this.chatInput.focus();
            } else {
                UIManager.showToast('Failed to capture screen', 'error');
            }
        } catch (error) {
            UIManager.showToast(`Error: ${error.message}`, 'error');
        } finally {
            UIManager.hideLoading();
        }
    }

    getLanguageFromFile(filename) {
        const ext = filename.split('.').pop().toLowerCase();
        const languages = {
            'py': 'python', 'js': 'javascript', 'jsx': 'javascript',
            'ts': 'typescript', 'tsx': 'typescript', 'java': 'java',
            'cpp': 'cpp', 'cc': 'cpp', 'c': 'c', 'h': 'c',
            'go': 'go', 'rs': 'rust', 'sql': 'sql',
            'html': 'html', 'css': 'css', 'json': 'json',
            'yaml': 'yaml', 'yml': 'yaml'
        };
        return languages[ext] || 'text';
    }

    saveChatHistory() {
        const messages = [];
        document.querySelectorAll('#chat-messages .message').forEach((msg) => {
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

        document.getElementById('chat-messages').innerHTML = '';
        history.forEach((msg) => {
            UIManager.addChatMessage(msg.content, msg.role);
        });
    }

    clearHistory() {
        document.getElementById('chat-messages').innerHTML = `
            <div class="message system">
                <div class="message-content">
                    <p>🤖 Ready for a new conversation!</p>
                </div>
            </div>
        `;
        localStorage.removeItem('chatHistory');
        UIManager.showToast('Chat history cleared', 'info');
    }
}

// Initialize enhanced chat when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('chat-input')) {
        // Keep original for compatibility, but enhance it
        if (!window.chatComponent) {
            window.chatComponent = new ChatComponentEnhanced();
        }
    }
});
