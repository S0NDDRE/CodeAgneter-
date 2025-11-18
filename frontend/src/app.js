/**
 * AI Code Agent Dashboard - Main Application
 */

class App {
    constructor() {
        this.initialized = false;
        this.components = {};

        this.init();
    }

    async init() {
        try {
            console.log('🚀 Initializing AI Code Agent Dashboard...');

            // Check backend health
            const health = await api.health();
            if (health.status !== 'ok') {
                console.warn('⚠️ Backend may not be fully ready');
                UIManager.showToast('Waiting for backend... using local mode', 'warning');
            } else {
                console.log('✅ Backend is ready');
            }

            // Setup navigation
            this.setupNavigation();

            // Setup settings
            this.setupSettings();

            // Load components
            this.loadComponents();

            // Setup keyboard shortcuts
            this.setupKeyboardShortcuts();

            console.log('✅ Dashboard initialized successfully');
            this.initialized = true;

            UIManager.showToast('Ready! Start chatting with your code agent', 'success', 3000);

        } catch (error) {
            console.error('Initialization error:', error);
            UIManager.showToast(`Initialization error: ${error.message}`, 'error');
        }
    }

    setupNavigation() {
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const page = item.dataset.page;
                UIManager.switchPage(page);
            });
        });
    }

    setupSettings() {
        const modelSelect = document.getElementById('model-select');
        const autoSaveCheckbox = document.getElementById('auto-save');
        const syntaxHighlight = document.getElementById('syntax-highlight');
        const requireApproval = document.getElementById('require-approval');
        const codeSandbox = document.getElementById('code-sandbox');
        const clearHistoryBtn = document.getElementById('clear-history-btn');

        // Load saved settings
        const settings = JSON.parse(localStorage.getItem('chatSettings') || '{}');
        if (settings.model) modelSelect.value = settings.model;
        if (typeof settings.autoSave === 'boolean') autoSaveCheckbox.checked = settings.autoSave;
        if (typeof settings.syntaxHighlight === 'boolean') syntaxHighlight.checked = settings.syntaxHighlight;
        if (typeof settings.requireApproval === 'boolean') requireApproval.checked = settings.requireApproval;
        if (typeof settings.codeSandbox === 'boolean') codeSandbox.checked = settings.codeSandbox;

        // Save settings on change
        const saveSettings = () => {
            const newSettings = {
                model: modelSelect.value,
                autoSave: autoSaveCheckbox.checked,
                syntaxHighlight: syntaxHighlight.checked,
                requireApproval: requireApproval.checked,
                codeSandbox: codeSandbox.checked
            };
            localStorage.setItem('chatSettings', JSON.stringify(newSettings));
            UIManager.showToast('Settings saved', 'success', 2000);
        };

        modelSelect.addEventListener('change', saveSettings);
        autoSaveCheckbox.addEventListener('change', saveSettings);
        syntaxHighlight.addEventListener('change', saveSettings);
        requireApproval.addEventListener('change', saveSettings);
        codeSandbox.addEventListener('change', saveSettings);

        // Clear history
        clearHistoryBtn.addEventListener('click', async () => {
            const confirm = await UIManager.showApprovalModal('Are you sure you want to clear chat history?');
            if (confirm && window.chatComponent) {
                window.chatComponent.clearHistory();
            }
        });
    }

    loadComponents() {
        // Components will be auto-initialized when their scripts load
        console.log('Components loaded and initialized');
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl+N: New chat
            if (e.ctrlKey && e.key === 'n') {
                e.preventDefault();
                if (window.chatComponent) {
                    window.chatComponent.clearHistory();
                }
            }

            // Ctrl+K: Focus chat input
            if (e.ctrlKey && e.key === 'k') {
                e.preventDefault();
                const chatInput = document.getElementById('chat-input');
                if (chatInput) chatInput.focus();
            }

            // Ctrl+S: Save chat
            if (e.ctrlKey && e.key === 's') {
                e.preventDefault();
                if (window.chatComponent) {
                    window.chatComponent.saveChatHistory();
                    UIManager.showToast('Chat saved', 'success', 1000);
                }
            }

            // Ctrl+A: Analyze
            if (e.ctrlKey && e.key === 'a') {
                e.preventDefault();
                UIManager.switchPage('analyze');
            }

            // Ctrl+P: Screen
            if (e.ctrlKey && e.key === 'p') {
                e.preventDefault();
                UIManager.switchPage('screen');
            }
        });

        // Auto-expand textarea
        const textarea = document.getElementById('chat-input');
        if (textarea) {
            textarea.addEventListener('input', () => {
                textarea.style.height = 'auto';
                textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
            });
        }
    }

    // Public API methods
    async sendMessage(message) {
        if (window.chatComponent) {
            document.getElementById('chat-input').value = message;
            await window.chatComponent.sendMessage();
        }
    }

    async analyzeCode(code) {
        UIManager.switchPage('analyze');
        document.getElementById('file-input').value = '';
        if (window.analyzerComponent) {
            // Trigger analysis
        }
    }

    switchPage(page) {
        UIManager.switchPage(page);
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
});

// Handle window close
window.addEventListener('beforeunload', (e) => {
    const settings = JSON.parse(localStorage.getItem('chatSettings') || '{}');
    if (settings.autoSave && window.chatComponent) {
        window.chatComponent.saveChatHistory();
    }
});
