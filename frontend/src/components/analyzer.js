/**
 * Analyzer Component - Code analysis functionality
 */

class AnalyzerComponent {
    constructor() {
        this.uploadArea = document.getElementById('upload-area');
        this.fileInput = document.getElementById('file-input');
        this.projectPath = document.getElementById('project-path');
        this.analyzeBtn = document.getElementById('analyze-btn');

        this.init();
    }

    init() {
        // File upload
        this.uploadArea.addEventListener('click', () => this.fileInput.click());
        this.uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.uploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.uploadArea.addEventListener('drop', (e) => this.handleDrop(e));
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));

        // Analyze button
        this.analyzeBtn.addEventListener('click', () => this.analyzeProject());
    }

    handleDragOver(e) {
        e.preventDefault();
        this.uploadArea.style.borderColor = '#0078D4';
        this.uploadArea.style.backgroundColor = '#F0F7FF';
    }

    handleDragLeave(e) {
        e.preventDefault();
        this.uploadArea.style.borderColor = '#D0D0D0';
        this.uploadArea.style.backgroundColor = 'transparent';
    }

    handleDrop(e) {
        e.preventDefault();
        this.uploadArea.style.borderColor = '#D0D0D0';
        this.uploadArea.style.backgroundColor = 'transparent';

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.analyzeFile(files[0]);
        }
    }

    handleFileSelect(e) {
        const files = e.target.files;
        if (files.length > 0) {
            this.analyzeFile(files[0]);
        }
    }

    async analyzeFile(file) {
        try {
            UIManager.showLoading();
            const content = await file.text();

            const response = await api.analyzeCode(content, file.name);

            if (response.status === 'success') {
                UIManager.displayAnalysisResults(response.analysis);
                UIManager.showToast('Analysis complete!', 'success');
            } else {
                UIManager.showToast(`Analysis failed: ${response.message}`, 'error');
            }
        } catch (error) {
            UIManager.showToast(`Error: ${error.message}`, 'error');
        } finally {
            UIManager.hideLoading();
        }
    }

    async analyzeProject() {
        const path = this.projectPath.value.trim();
        if (!path) {
            UIManager.showToast('Please enter a project path', 'warning');
            return;
        }

        try {
            UIManager.showLoading();
            const response = await api.analyzeProject(path);

            if (response.status === 'success') {
                this.displayProjectAnalysis(response);
                UIManager.showToast('Project analysis complete!', 'success');
            } else {
                UIManager.showToast(`Analysis failed: ${response.message}`, 'error');
            }
        } catch (error) {
            UIManager.showToast(`Error: ${error.message}`, 'error');
        } finally {
            UIManager.hideLoading();
        }
    }

    displayProjectAnalysis(response) {
        const container = document.getElementById('analysis-results');
        if (!container) return;

        const summary = response.summary;
        const issues = response.issues || [];

        let html = `
            <div class="analysis-section">
                <h3>Project Analysis: ${response.project}</h3>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-bottom: 20px;">
                    <div>
                        <p><strong>Files Analyzed:</strong> ${summary.files_analyzed}</p>
                        <p><strong>Total Lines:</strong> ${summary.total_lines}</p>
                        <p><strong>Total Issues:</strong> ${summary.total_issues}</p>
                    </div>
                    <div>
                        <h4>Languages</h4>
                        <ul>
        `;

        for (const [lang, count] of Object.entries(summary.languages)) {
            html += `<li>${lang}: ${count} files</li>`;
        }

        html += `
                        </ul>
                    </div>
                </div>
            </div>
        `;

        if (issues.length > 0) {
            html += `
                <div class="analysis-section">
                    <h4>Issues Found (${issues.length})</h4>
                    <table style="width: 100%; border-collapse: collapse;">
                        <thead>
                            <tr style="border-bottom: 2px solid #D0D0D0;">
                                <th style="text-align: left; padding: 8px;">File</th>
                                <th style="text-align: left; padding: 8px;">Line</th>
                                <th style="text-align: left; padding: 8px;">Type</th>
                                <th style="text-align: left; padding: 8px;">Message</th>
                            </tr>
                        </thead>
                        <tbody>
            `;

            issues.slice(0, 20).forEach(issue => {
                const severityColor = {
                    'critical': '#E74C3C',
                    'warning': '#F39C12',
                    'info': '#3498DB'
                };

                html += `
                    <tr style="border-bottom: 1px solid #E8E8E8;">
                        <td style="padding: 8px; font-size: 12px;">${issue.file || 'unknown'}</td>
                        <td style="padding: 8px;">${issue.line || '-'}</td>
                        <td style="padding: 8px;">
                            <span style="background-color: ${severityColor[issue.severity] || '#666'}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">
                                ${issue.severity}
                            </span>
                        </td>
                        <td style="padding: 8px;">${issue.message}</td>
                    </tr>
                `;
            });

            html += `
                        </tbody>
                    </table>
                </div>
            `;
        }

        if (response.recommendations && response.recommendations.length > 0) {
            html += `
                <div class="analysis-section">
                    <h4>Recommendations</h4>
                    <ul>
            `;

            response.recommendations.forEach(rec => {
                html += `<li>💡 ${rec}</li>`;
            });

            html += `</ul></div>`;
        }

        container.innerHTML = html;
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('analyze-btn')) {
        window.analyzerComponent = new AnalyzerComponent();
    }
});
