/**
 * UI Utilities - Helper functions for UI manipulation
 */

class UIManager {
    /**
     * Show loading spinner
     */
    static showLoading() {
        const spinner = document.getElementById('loading-spinner');
        if (spinner) spinner.style.display = 'flex';
    }

    /**
     * Hide loading spinner
     */
    static hideLoading() {
        const spinner = document.getElementById('loading-spinner');
        if (spinner) spinner.style.display = 'none';
    }

    /**
     * Show toast notification
     */
    static showToast(message, type = 'info', duration = 3000) {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;

        container.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, duration);
    }

    /**
     * Show approval modal
     */
    static showApprovalModal(message) {
        return new Promise((resolve) => {
            const modal = document.getElementById('approval-modal');
            const messageEl = document.getElementById('approval-message');
            const approveBtn = document.getElementById('approve-btn');
            const denyBtn = document.getElementById('deny-btn');

            messageEl.textContent = message;
            modal.style.display = 'flex';

            const cleanup = () => {
                modal.style.display = 'none';
                approveBtn.removeEventListener('click', onApprove);
                denyBtn.removeEventListener('click', onDeny);
            };

            const onApprove = () => {
                cleanup();
                resolve(true);
            };

            const onDeny = () => {
                cleanup();
                resolve(false);
            };

            approveBtn.addEventListener('click', onApprove);
            denyBtn.addEventListener('click', onDeny);
        });
    }

    /**
     * Switch page view
     */
    static switchPage(pageName) {
        // Hide all pages
        document.querySelectorAll('.page').forEach(page => {
            page.style.display = 'none';
        });

        // Show selected page
        const page = document.getElementById(`${pageName}-page`);
        if (page) {
            page.style.display = 'block';

            // Update nav
            document.querySelectorAll('.nav-item').forEach(item => {
                item.classList.remove('active');
            });
            const navItem = document.querySelector(`[data-page="${pageName}"]`);
            if (navItem) navItem.classList.add('active');

            // Update title
            const titles = {
                chat: 'Chat with AI Agent',
                analyze: 'Code Analysis',
                screen: 'Screen Capture',
                files: 'File Manager',
                settings: 'Settings'
            };
            document.getElementById('page-title').textContent = titles[pageName] || 'AI Code Agent';
        }
    }

    /**
     * Format code for display
     */
    static formatCodeBlock(code, language = 'python') {
        const pre = document.createElement('pre');
        const codeEl = document.createElement('code');
        codeEl.className = `language-${language}`;
        codeEl.textContent = code;

        pre.appendChild(codeEl);

        // Syntax highlighting if available
        if (window.hljs) {
            hljs.highlightElement(codeEl);
        }

        return pre;
    }

    /**
     * Add message to chat
     */
    static addChatMessage(content, role = 'assistant') {
        const messagesEl = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        // If content looks like markdown/code, format it
        if (content.includes('```')) {
            contentDiv.innerHTML = UIManager.parseMarkdown(content);
        } else {
            contentDiv.textContent = content;
        }

        messageDiv.appendChild(contentDiv);
        messagesEl.appendChild(messageDiv);

        // Scroll to bottom
        messagesEl.scrollTop = messagesEl.scrollHeight;
    }

    /**
     * Parse markdown-like content
     */
    static parseMarkdown(content) {
        let html = content;

        // Code blocks
        html = html.replace(/```(\w+)?\n([\s\S]*?)```/g, (match, lang, code) => {
            const highlighted = window.hljs && lang
                ? `<pre><code class="language-${lang}">${escapeHtml(code.trim())}</code></pre>`
                : `<pre><code>${escapeHtml(code.trim())}</code></pre>`;
            return highlighted;
        });

        // Inline code
        html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

        // Bold
        html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

        // Italic
        html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');

        // Links
        html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');

        // Line breaks
        html = html.replace(/\n/g, '<br>');

        return html;
    }

    /**
     * Copy text to clipboard
     */
    static copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            UIManager.showToast('Copied to clipboard!', 'success', 2000);
        }).catch(() => {
            UIManager.showToast('Failed to copy', 'error');
        });
    }

    /**
     * Display code analysis results
     */
    static displayAnalysisResults(analysis) {
        const container = document.getElementById('analysis-results');
        if (!container) return;

        let html = `
            <div class="analysis-section">
                <h3>${analysis.filename}</h3>
                <p><strong>Language:</strong> ${analysis.language}</p>
                <p><strong>Quality Score:</strong> <span style="font-weight: bold; color: ${analysis.quality_score >= 70 ? '#27AE60' : '#E74C3C'}">${analysis.quality_score.toFixed(0)}/100</span></p>
                <p>${analysis.summary}</p>
            </div>

            <div class="analysis-section">
                <h4>Metrics</h4>
                <ul>
                    <li>Total Lines: ${analysis.metrics.total_lines}</li>
                    <li>Non-empty Lines: ${analysis.metrics.non_empty_lines}</li>
                    <li>Comment Lines: ${analysis.metrics.comment_lines}</li>
                    <li>Average Line Length: ${analysis.metrics.average_line_length.toFixed(0)} chars</li>
                </ul>
            </div>
        `;

        if (analysis.issues && analysis.issues.length > 0) {
            html += `
                <div class="analysis-section">
                    <h4>Issues Found (${analysis.issues.length})</h4>
                    <ul>
            `;
            analysis.issues.forEach(issue => {
                html += `
                    <li>
                        <strong>[${issue.severity.toUpperCase()}]</strong> Line ${issue.line}: ${issue.message}
                    </li>
                `;
            });
            html += `</ul></div>`;
        }

        if (analysis.suggestions && analysis.suggestions.length > 0) {
            html += `
                <div class="analysis-section">
                    <h4>Suggestions</h4>
                    <ul>
            `;
            analysis.suggestions.forEach(suggestion => {
                html += `<li>${suggestion}</li>`;
            });
            html += `</ul></div>`;
        }

        container.innerHTML = html;
    }
}

/**
 * Escape HTML special characters
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
