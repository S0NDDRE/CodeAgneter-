/**
 * Models Component - Select, download, switch OLLAMA models
 * and Negotiation Component - Agreement-based action system
 */

class ModelsComponent {
    constructor() {
        this.currentModel = null;
        this.availableModels = [];
        this.popularModels = [];
        this.downloadingModel = null;

        this.init();
    }

    async init() {
        await this.loadModels();
        this.setupUI();
    }

    async loadModels() {
        try {
            const response = await fetch('http://localhost:8000/api/models');
            const data = await response.json();

            this.currentModel = data.current;
            this.availableModels = data.available;

            const popularResponse = await fetch('http://localhost:8000/api/models/popular');
            const popularData = await popularResponse.json();
            this.popularModels = popularData.models;

            console.log('✅ Models loaded:', this.availableModels);
        } catch (error) {
            console.error('Error loading models:', error);
            UIManager.showToast('Could not load models', 'warning');
        }
    }

    setupUI() {
        // This would be called from the main app to setup model UI
        this.displayModels();
    }

    displayModels() {
        // Models will be displayed in settings panel
        const modelsSection = document.createElement('div');
        modelsSection.className = 'models-section';
        modelsSection.innerHTML = `
            <h4>🤖 AI Models (OLLAMA)</h4>
            <div class="current-model">
                <strong>Current:</strong> ${this.currentModel || 'None'}
            </div>
            <div id="available-models" class="models-list"></div>
            <div id="popular-models" class="popular-models-list"></div>
        `;

        return modelsSection;
    }

    async switchModel(modelName) {
        try {
            UIManager.showLoading();
            const response = await fetch('http://localhost:8000/api/models/switch', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ model_name: modelName })
            });

            const data = await response.json();

            if (data.status === 'success') {
                this.currentModel = modelName;
                UIManager.showToast(`Switched to ${modelName}`, 'success');
                await this.loadModels();
            } else {
                UIManager.showToast(`Failed: ${data.message}`, 'error');
            }
        } catch (error) {
            UIManager.showToast(`Error: ${error.message}`, 'error');
        } finally {
            UIManager.hideLoading();
        }
    }

    async downloadModel(modelName) {
        try {
            this.downloadingModel = modelName;
            UIManager.showLoading();

            const response = await fetch('http://localhost:8000/api/models/download', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ model_name: modelName })
            });

            const data = await response.json();

            if (data.status === 'success') {
                UIManager.showToast(`Downloaded ${modelName}!`, 'success', 5000);
                await this.loadModels();
            } else {
                UIManager.showToast(`Download failed: ${data.message}`, 'error');
            }
        } catch (error) {
            UIManager.showToast(`Error: ${error.message}`, 'error');
        } finally {
            UIManager.hideLoading();
            this.downloadingModel = null;
        }
    }

    async deleteModel(modelName) {
        const confirmed = await UIManager.showApprovalModal(
            `Delete ${modelName}? This cannot be undone.`
        );

        if (!confirmed) return;

        try {
            UIManager.showLoading();
            const response = await fetch(`http://localhost:8000/api/models/${modelName}`, {
                method: 'DELETE'
            });

            const data = await response.json();

            if (data.status === 'success') {
                UIManager.showToast(`Deleted ${modelName}`, 'success');
                await this.loadModels();
            } else {
                UIManager.showToast(`Failed: ${data.message}`, 'error');
            }
        } catch (error) {
            UIManager.showToast(`Error: ${error.message}`, 'error');
        } finally {
            UIManager.hideLoading();
        }
    }
}

class NegotiationComponent {
    constructor() {
        this.currentSession = null;
        this.sessionHistory = [];
    }

    /**
     * Start negotiation with agent proposal
     */
    async proposeAction(actionType, description, details = {}) {
        try {
            const sessionId = `session_${Date.now()}`;

            const response = await fetch('http://localhost:8000/api/negotiate/propose', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: sessionId,
                    action_type: actionType,
                    description: description,
                    details: details
                })
            });

            const data = await response.json();

            if (data.status === 'proposed') {
                this.currentSession = sessionId;
                this.displayProposal(data);
                return sessionId;
            }
        } catch (error) {
            UIManager.showToast(`Error proposing action: ${error.message}`, 'error');
        }
    }

    displayProposal(data) {
        const modal = document.getElementById('approval-modal');
        const message = document.getElementById('approval-message');

        message.innerHTML = `
            <strong>Agent Proposal:</strong><br/>
            ${data.message}<br/><br/>
            <div style="background: #f0f0f0; padding: 10px; border-radius: 5px;">
                <strong>${data.action.description}</strong><br/>
                ${data.action.type}
            </div>
        `;

        modal.style.display = 'flex';

        // Handle approval
        const approveBtn = document.getElementById('approve-btn');
        const denyBtn = document.getElementById('deny-btn');

        approveBtn.onclick = () => {
            this.respondToProposal(data.session_id, 'yes');
            modal.style.display = 'none';
        };

        denyBtn.onclick = () => {
            this.respondToProposal(data.session_id, 'no');
            modal.style.display = 'none';
        };
    }

    async respondToProposal(sessionId, response) {
        try {
            UIManager.showLoading();

            const resp = await fetch('http://localhost:8000/api/negotiate/respond', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: sessionId,
                    response: response
                })
            });

            const data = await resp.json();

            if (data.status === 'agreed') {
                UIManager.showToast('✅ Agreed! Executing action...', 'success');
                await this.executeAction(sessionId);
            } else if (data.status === 'rejected') {
                UIManager.showToast('❌ Action cancelled', 'warning');
            } else if (data.status === 'discussing') {
                UIManager.addChatMessage(data.message, 'assistant');
            }
        } catch (error) {
            UIManager.showToast(`Error: ${error.message}`, 'error');
        } finally {
            UIManager.hideLoading();
        }
    }

    async executeAction(sessionId) {
        try {
            const response = await fetch('http://localhost:8000/api/negotiate/execute', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: sessionId })
            });

            const data = await response.json();

            if (data.status === 'success') {
                UIManager.showToast(data.message, 'success');
                UIManager.addChatMessage(
                    `✅ ${data.message}\n\nAction completed successfully!`,
                    'assistant'
                );
            } else {
                UIManager.showToast(`Error: ${data.message}`, 'error');
            }
        } catch (error) {
            UIManager.showToast(`Execution error: ${error.message}`, 'error');
        }
    }

    async getSessionStatus(sessionId) {
        try {
            const response = await fetch(
                `http://localhost:8000/api/negotiate/${sessionId}`
            );
            return await response.json();
        } catch (error) {
            console.error('Error getting session status:', error);
            return null;
        }
    }

    async getHistory() {
        try {
            const response = await fetch('http://localhost:8000/api/negotiate/history');
            return await response.json();
        } catch (error) {
            console.error('Error getting history:', error);
            return [];
        }
    }
}

// Initialize when DOM ready
document.addEventListener('DOMContentLoaded', () => {
    window.modelsComponent = new ModelsComponent();
    window.negotiationComponent = new NegotiationComponent();

    console.log('✅ Models and Negotiation components initialized');
});
