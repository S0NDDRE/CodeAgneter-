/**
 * Files Component - File browser and management
 */

class FilesComponent {
    constructor() {
        this.pathInput = document.getElementById('path-input');
        this.browseBtn = document.getElementById('browse-btn');
        this.fileTree = document.getElementById('file-tree');

        this.init();
    }

    init() {
        this.browseBtn.addEventListener('click', () => this.browsePath());
        this.pathInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                this.browsePath();
            }
        });

        // Show home directory by default
        this.loadDirectory(process.env.HOME || '/home');
    }

    async browsePath() {
        const path = this.pathInput.value.trim();
        if (!path) {
            UIManager.showToast('Please enter a path', 'warning');
            return;
        }

        this.loadDirectory(path);
    }

    async loadDirectory(path) {
        try {
            UIManager.showLoading();

            // In a real implementation, this would fetch from API
            // For now, we'll show a simulated file tree
            this.displayFileTree(path);

            this.pathInput.value = path;
            UIManager.showToast('Directory loaded', 'success');
        } catch (error) {
            UIManager.showToast(`Error loading directory: ${error.message}`, 'error');
        } finally {
            UIManager.hideLoading();
        }
    }

    displayFileTree(path) {
        // Simulated file tree for demonstration
        const files = [
            { name: 'README.md', type: 'file', size: '2.4 KB', icon: '📄' },
            { name: 'src', type: 'folder', icon: '📁', children: [
                { name: 'app.py', type: 'file', size: '1.2 KB', icon: '🐍' },
                { name: 'config.json', type: 'file', size: '0.5 KB', icon: '⚙️' },
                { name: 'utils', type: 'folder', icon: '📁', children: [
                    { name: 'helpers.py', type: 'file', size: '3.1 KB', icon: '🐍' }
                ] }
            ] },
            { name: 'tests', type: 'folder', icon: '📁', children: [
                { name: 'test_main.py', type: 'file', size: '1.8 KB', icon: '🧪' },
                { name: 'test_utils.py', type: 'file', size: '2.1 KB', icon: '🧪' }
            ] },
            { name: 'requirements.txt', type: 'file', size: '0.8 KB', icon: '📋' }
        ];

        let html = `<div style="padding: 10px 0;"><strong>${path}</strong></div>`;
        html += this.buildFileTreeHTML(files, 0);

        this.fileTree.innerHTML = html;
    }

    buildFileTreeHTML(files, level = 0) {
        let html = '<ul style="list-style: none; padding-left: ' + (level * 20) + 'px;">';

        files.forEach(file => {
            const itemId = `file-${Math.random().toString(36).substr(2, 9)}`;

            if (file.type === 'folder') {
                html += `
                    <li style="margin: 5px 0;">
                        <span style="cursor: pointer; display: inline-flex; align-items: center; gap: 8px;"
                              onclick="toggleFolder('${itemId}')">
                            <span id="arrow-${itemId}" style="display: inline-block; width: 16px; text-align: center;">▶</span>
                            <span>${file.icon}</span>
                            <strong>${file.name}</strong>
                        </span>
                        <div id="${itemId}" style="display: none;">
                `;
                if (file.children) {
                    html += this.buildFileTreeHTML(file.children, level + 1);
                }
                html += `</div></li>`;
            } else {
                html += `
                    <li style="margin: 5px 0; display: flex; align-items: center; gap: 8px;">
                        <span style="width: 16px;"></span>
                        <span>${file.icon}</span>
                        <span style="flex: 1;">${file.name}</span>
                        <span style="font-size: 12px; color: #999;">${file.size}</span>
                        <button style="padding: 4px 8px; font-size: 12px; cursor: pointer; background: #0078D4; color: white; border: none; border-radius: 4px;"
                                onclick="openFile('${file.name}')">Open</button>
                    </li>
                `;
            }
        });

        html += '</ul>';
        return html;
    }
}

// Global functions for file tree
function toggleFolder(id) {
    const folder = document.getElementById(id);
    const arrow = document.getElementById(`arrow-${id}`);

    if (folder.style.display === 'none') {
        folder.style.display = 'block';
        arrow.textContent = '▼';
    } else {
        folder.style.display = 'none';
        arrow.textContent = '▶';
    }
}

function openFile(filename) {
    UIManager.showToast(`Opening: ${filename}`, 'info');
    // In a real implementation, this would open the file in an editor or viewer
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('browse-btn')) {
        window.filesComponent = new FilesComponent();
    }
});
