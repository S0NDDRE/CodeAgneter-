/**
 * Folder Monitor Component - Real-time code monitoring UI
 * Shows file changes, auto-analysis, and agent suggestions
 */

class MonitorComponent {
    constructor() {
        this.isMonitoring = false;
        this.monitorPath = null;
        this.changes = [];
        this.analysisResults = {};
        this.updateInterval = null;

        this.init();
    }

    init() {
        console.log('✅ Monitor component initialized');
    }

    async startMonitoring(path) {
        try {
            UIManager.showLoading();

            const response = await fetch('http://localhost:8000/api/monitor/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ path })
            });

            const data = await response.json();

            if (data.status === 'started') {
                this.isMonitoring = true;
                this.monitorPath = path;

                UIManager.showToast(`📁 Monitoring: ${path}`, 'success');
                this.displayMonitorStatus();

                // Start polling for changes
                this.startPolling();
            } else {
                UIManager.showToast(`Failed: ${data.message}`, 'error');
            }
        } catch (error) {
            UIManager.showToast(`Error: ${error.message}`, 'error');
        } finally {
            UIManager.hideLoading();
        }
    }

    async stopMonitoring() {
        try {
            UIManager.showLoading();

            const response = await fetch('http://localhost:8000/api/monitor/stop', {
                method: 'POST'
            });

            const data = await response.json();

            if (data.status === 'stopped') {
                this.isMonitoring = false;
                this.stopPolling();

                UIManager.showToast('📁 Monitoring stopped', 'info');
                this.displayMonitorStatus();
            }
        } catch (error) {
            UIManager.showToast(`Error: ${error.message}`, 'error');
        } finally {
            UIManager.hideLoading();
        }
    }

    startPolling() {
        /**
         * Poll for changes every 2 seconds
         */
        this.updateInterval = setInterval(async () => {
            try {
                // Get changes
                const changesResponse = await fetch(
                    'http://localhost:8000/api/monitor/changes?limit=10'
                );
                const changesData = await changesResponse.json();
                this.changes = changesData.changes;

                // Get analysis
                const analysisResponse = await fetch(
                    'http://localhost:8000/api/monitor/analysis'
                );
                const analysisData = await analysisResponse.json();
                this.analysisResults = analysisData.analysis;

                // Update display
                this.displayChanges();
                this.displayAnalysis();
            } catch (error) {
                console.error('Polling error:', error);
            }
        }, 2000);
    }

    stopPolling() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
    }

    displayMonitorStatus() {
        const statusDiv = document.createElement('div');
        statusDiv.id = 'monitor-status';
        statusDiv.style.cssText = `
            padding: 15px;
            background: ${this.isMonitoring ? '#e8f5e9' : '#fff3e0'};
            border-left: 4px solid ${this.isMonitoring ? '#4caf50' : '#ff9800'};
            border-radius: 4px;
            margin-bottom: 20px;
        `;

        if (this.isMonitoring) {
            statusDiv.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>🟢 Monitoring Active</strong><br/>
                        <small>${this.monitorPath}</small>
                    </div>
                    <button onclick="window.monitorComponent.stopMonitoring()"
                            style="padding: 8px 16px; background: #ff9800; color: white; border: none; border-radius: 4px; cursor: pointer;">
                        ⏹️ Stop
                    </button>
                </div>
            `;
        } else {
            statusDiv.innerHTML = `
                <div>
                    <strong>🔴 Monitoring Inactive</strong><br/>
                    <small>Enter a path to start monitoring</small>
                </div>
            `;
        }

        // Replace or add status
        const existing = document.getElementById('monitor-status');
        if (existing) {
            existing.replaceWith(statusDiv);
        } else {
            const container = document.querySelector('.settings-container') ||
                             document.querySelector('.content-container');
            if (container) {
                container.insertBefore(statusDiv, container.firstChild);
            }
        }
    }

    displayChanges() {
        if (this.changes.length === 0) return;

        const changesDiv = document.createElement('div');
        changesDiv.id = 'monitor-changes';
        changesDiv.innerHTML = `
            <div style="background: #f5f5f5; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h4>📝 Recent Changes (${this.changes.length})</h4>
                <div style="max-height: 300px; overflow-y: auto;">
        `;

        this.changes.forEach(change => {
            const icon = change.type === 'modified' ? '✏️' :
                        change.type === 'created' ? '✨' : '🗑️';

            changesDiv.innerHTML += `
                <div style="padding: 8px; border-bottom: 1px solid #ddd; font-size: 12px;">
                    ${icon} <strong>${change.type}</strong>
                    <br/>
                    <code>${change.file.split('/').pop()}</code>
                    <br/>
                    <small>${new Date(change.timestamp).toLocaleTimeString()}</small>
                </div>
            `;
        });

        changesDiv.innerHTML += `
                </div>
            </div>
        `;

        const existing = document.getElementById('monitor-changes');
        if (existing) {
            existing.replaceWith(changesDiv);
        } else {
            const container = document.querySelector('.content-container');
            if (container) {
                container.appendChild(changesDiv);
            }
        }
    }

    displayAnalysis() {
        const analysisDiv = document.createElement('div');
        analysisDiv.id = 'monitor-analysis';
        analysisDiv.innerHTML = `
            <div style="background: #fff3e0; padding: 15px; border-radius: 8px;">
                <h4>🔍 Analysis Results</h4>
        `;

        let totalIssues = 0;
        Object.values(this.analysisResults).forEach(analysis => {
            totalIssues += analysis.issues?.length || 0;
        });

        if (totalIssues > 0) {
            analysisDiv.innerHTML += `
                <div style="color: #e65100; font-weight: bold;">
                    ⚠️ ${totalIssues} issues found!
                </div>
                <div style="margin-top: 10px;">
            `;

            Object.entries(this.analysisResults).forEach(([file, analysis]) => {
                if (analysis.issues && analysis.issues.length > 0) {
                    analysisDiv.innerHTML += `
                        <details>
                            <summary style="cursor: pointer; padding: 8px;">
                                📄 ${file.split('/').pop()} (${analysis.issues.length} issues)
                            </summary>
                            <div style="padding-left: 20px; font-size: 12px;">
                    `;

                    analysis.issues.forEach(issue => {
                        const color = issue.severity === 'critical' ? '#d32f2f' :
                                    issue.severity === 'warning' ? '#f57c00' : '#0288d1';

                        analysisDiv.innerHTML += `
                            <div style="color: ${color}; margin: 5px 0;">
                                Line ${issue.line}: ${issue.message}
                            </div>
                        `;
                    });

                    analysisDiv.innerHTML += `
                            </div>
                        </details>
                    `;
                }
            });

            analysisDiv.innerHTML += `
                </div>
                <button onclick="window.monitorComponent.askAgentToFix()"
                        style="margin-top: 10px; padding: 8px 16px; background: #4caf50; color: white; border: none; border-radius: 4px; cursor: pointer;">
                    ✅ Ask Agent to Fix Issues
                </button>
            `;
        } else {
            analysisDiv.innerHTML += `
                <div style="color: #2e7d32;">
                    ✅ No issues found!
                </div>
            `;
        }

        analysisDiv.innerHTML += `</div>`;

        const existing = document.getElementById('monitor-analysis');
        if (existing) {
            existing.replaceWith(analysisDiv);
        } else {
            const container = document.querySelector('.content-container');
            if (container) {
                container.appendChild(analysisDiv);
            }
        }
    }

    async askAgentToFix() {
        const issues = this.getIssuesString();

        if (!issues) {
            UIManager.showToast('No issues to fix', 'info');
            return;
        }

        // Switch to chat and send message to agent
        UIManager.switchPage('chat');

        const message = `I have some code issues detected by the monitor:\n\n${issues}\n\nCan you help me fix these?`;
        document.getElementById('chat-input').value = message;

        // Send message
        await window.chatComponent.sendMessage();
    }

    getIssuesString() {
        let issuesStr = '';

        Object.entries(this.analysisResults).forEach(([file, analysis]) => {
            if (analysis.issues && analysis.issues.length > 0) {
                issuesStr += `\n**${file}:**\n`;
                analysis.issues.forEach(issue => {
                    issuesStr += `- Line ${issue.line}: ${issue.message} (${issue.severity})\n`;
                });
            }
        });

        return issuesStr;
    }

    async getStatus() {
        try {
            const response = await fetch('http://localhost:8000/api/monitor/status');
            return await response.json();
        } catch (error) {
            console.error('Status error:', error);
            return null;
        }
    }
}

// Initialize monitor component
document.addEventListener('DOMContentLoaded', () => {
    window.monitorComponent = new MonitorComponent();
    console.log('✅ Folder monitor ready');
});
