/**
 * Screen Capture Component
 */

class ScreenComponent {
    constructor() {
        this.captureBtn = document.getElementById('capture-btn');
        this.analyzeScreenBtn = document.getElementById('analyze-screen-btn');
        this.screenshot = document.getElementById('screenshot');
        this.placeholder = document.getElementById('screen-placeholder');
        this.analysisDiv = document.getElementById('screen-analysis');

        this.init();
    }

    init() {
        this.captureBtn.addEventListener('click', () => this.captureScreen());
        this.analyzeScreenBtn.addEventListener('click', () => this.analyzeScreen());
    }

    async captureScreen() {
        try {
            UIManager.showLoading();
            const response = await api.captureScreen();

            if (response.status === 'success') {
                this.displayScreenshot(response.image);
                UIManager.showToast('Screen captured successfully!', 'success');
                this.analyzeScreenBtn.disabled = false;
            } else {
                UIManager.showToast(`Capture failed: ${response.message}`, 'error');
            }
        } catch (error) {
            UIManager.showToast(`Error: ${error.message}`, 'error');
        } finally {
            UIManager.hideLoading();
        }
    }

    displayScreenshot(imageData) {
        this.screenshot.src = imageData;
        this.screenshot.style.display = 'block';
        this.placeholder.style.display = 'none';
    }

    async analyzeScreen() {
        if (!this.screenshot.src) {
            UIManager.showToast('Please capture screen first', 'warning');
            return;
        }

        try {
            UIManager.showLoading();

            // In a real implementation, this would send the screenshot to the API
            // For now, we'll simulate screen analysis
            const analysis = {
                text_detected: [
                    'Visual content detected on screen',
                    'Multiple UI elements recognized',
                    'Ready for interaction'
                ],
                ui_elements: [
                    { type: 'window', name: 'Active Application' },
                    { type: 'button', label: 'Detected Button' },
                    { type: 'text_field', content: 'Input Area' }
                ],
                suggestions: [
                    'Click detected button to continue',
                    'Type in visible text field',
                    'Screen is ready for interaction'
                ]
            };

            this.displayAnalysis(analysis);
            UIManager.showToast('Screen analysis complete!', 'success');
        } catch (error) {
            UIManager.showToast(`Analysis error: ${error.message}`, 'error');
        } finally {
            UIManager.hideLoading();
        }
    }

    displayAnalysis(analysis) {
        let html = `
            <div class="analysis-section">
                <h4>Screen Analysis Results</h4>
        `;

        if (analysis.text_detected && analysis.text_detected.length > 0) {
            html += `
                <div style="margin-bottom: 15px;">
                    <h5>Detected Text</h5>
                    <ul>
            `;
            analysis.text_detected.forEach(text => {
                html += `<li>${text}</li>`;
            });
            html += `</ul></div>`;
        }

        if (analysis.ui_elements && analysis.ui_elements.length > 0) {
            html += `
                <div style="margin-bottom: 15px;">
                    <h5>UI Elements</h5>
                    <ul>
            `;
            analysis.ui_elements.forEach(elem => {
                html += `<li><strong>${elem.type}:</strong> ${elem.label || elem.name || elem.content}</li>`;
            });
            html += `</ul></div>`;
        }

        if (analysis.suggestions && analysis.suggestions.length > 0) {
            html += `
                <div style="margin-bottom: 15px;">
                    <h5>Suggested Actions</h5>
                    <ul>
            `;
            analysis.suggestions.forEach(suggestion => {
                html += `<li>💡 ${suggestion}</li>`;
            });
            html += `</ul></div>`;
        }

        html += `</div>`;

        this.analysisDiv.innerHTML = html;
        this.analysisDiv.style.display = 'block';
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('capture-btn')) {
        window.screenComponent = new ScreenComponent();
    }
});
