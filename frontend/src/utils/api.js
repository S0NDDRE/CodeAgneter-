/**
 * API Client for communication with backend
 */

class APIClient {
    constructor(baseURL = 'http://localhost:8000/api') {
        this.baseURL = baseURL;
        this.ws = null;
        this.messageHandlers = [];
    }

    /**
     * Send chat message
     */
    async sendMessage(message) {
        try {
            const response = await fetch(`${this.baseURL}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('Chat error:', error);
            throw error;
        }
    }

    /**
     * Analyze code
     */
    async analyzeCode(code, filename = 'unknown') {
        try {
            const blob = new Blob([code], { type: 'text/plain' });
            const formData = new FormData();
            formData.append('file', blob, filename);

            const response = await fetch(`${this.baseURL}/analyze`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('Analysis error:', error);
            throw error;
        }
    }

    /**
     * Fix code
     */
    async fixCode(code, language = 'python') {
        try {
            const response = await fetch(`${this.baseURL}/fix-code`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code, language })
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('Fix code error:', error);
            throw error;
        }
    }

    /**
     * Analyze project
     */
    async analyzeProject(path) {
        try {
            const response = await fetch(`${this.baseURL}/analyze-project`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ path })
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('Project analysis error:', error);
            throw error;
        }
    }

    /**
     * Capture screen
     */
    async captureScreen() {
        try {
            const response = await fetch(`${this.baseURL}/screen-capture`, {
                method: 'GET'
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('Screen capture error:', error);
            throw error;
        }
    }

    /**
     * Check backend health
     */
    async health() {
        try {
            const response = await fetch(`${this.baseURL.replace('/api', '')}/health`, {
                method: 'GET'
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('Health check error:', error);
            return { status: 'error', message: 'Backend unreachable' };
        }
    }

    /**
     * Connect WebSocket for real-time communication
     */
    connectWebSocket(onMessage) {
        return new Promise((resolve, reject) => {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsURL = `${protocol}//${window.location.host}/ws/agent`;

            try {
                this.ws = new WebSocket(wsURL);

                this.ws.onopen = () => {
                    console.log('WebSocket connected');
                    resolve(this.ws);
                };

                this.ws.onmessage = (event) => {
                    const data = JSON.parse(event.data);
                    onMessage(data);
                };

                this.ws.onerror = (error) => {
                    console.error('WebSocket error:', error);
                    reject(error);
                };

                this.ws.onclose = () => {
                    console.log('WebSocket disconnected');
                };
            } catch (error) {
                reject(error);
            }
        });
    }

    /**
     * Send message via WebSocket
     */
    sendWebSocketMessage(message) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(message));
        } else {
            console.error('WebSocket not connected');
        }
    }

    /**
     * Close WebSocket connection
     */
    closeWebSocket() {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
    }
}

// Global API client instance
const api = new APIClient();
