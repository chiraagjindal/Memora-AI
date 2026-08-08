"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = require("vscode");
const axios_1 = require("axios");
const BACKEND_URL = 'http://localhost:8000/api/v1/telemetry';
function activate(context) {
    console.log('Memora AI extension is now active!');
    // File Save Event
    vscode.workspace.onDidSaveTextDocument(async (document) => {
        const content = document.getText();
        const filePath = document.fileName;
        try {
            await axios_1.default.post(`${BACKEND_URL}/file-save`, {
                file_path: filePath,
                content: content,
                timestamp: new Date().toISOString()
            });
            console.log(`Saved event for ${filePath} sent to Memora AI`);
        }
        catch (error) {
            console.error('Failed to send save event to Memora AI', error);
        }
    });
    // Terminal Execution Event (basic intercept)
    vscode.window.onDidOpenTerminal((terminal) => {
        axios_1.default.post(`${BACKEND_URL}/terminal-event`, {
            name: terminal.name,
            event: 'opened',
            timestamp: new Date().toISOString()
        }).catch(console.error);
    });
    // Webview Command
    let disposable = vscode.commands.registerCommand('memora-ai.openChat', () => {
        const panel = vscode.window.createWebviewPanel('memoraChat', 'Memora AI Chat', vscode.ViewColumn.Two, {
            enableScripts: true
        });
        panel.webview.html = getWebviewContent();
    });
    context.subscriptions.push(disposable);
}
function getWebviewContent() {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Memora AI</title>
    <style>
      body { font-family: sans-serif; padding: 20px; }
      #chat-box { height: 300px; overflow-y: auto; border: 1px solid #ccc; margin-bottom: 10px; padding: 10px; }
      input { width: 80%; padding: 5px; }
      button { padding: 5px 10px; }
    </style>
</head>
<body>
    <h2>Memora AI Project Memory</h2>
    <div id="chat-box"></div>
    <input type="text" id="message-input" placeholder="Ask something about the project..."/>
    <button onclick="sendMessage()">Send</button>

    <script>
        const vscode = acquireVsCodeApi();
        function sendMessage() {
            const input = document.getElementById('message-input');
            const message = input.value;
            if (!message) return;
            
            const chatBox = document.getElementById('chat-box');
            chatBox.innerHTML += '<div><b>You:</b> ' + message + '</div>';
            input.value = '';

            fetch('http://localhost:8000/api/v1/chat/memora', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ message })
            })
            .then(res => res.json())
            .then(data => {
              chatBox.innerHTML += '<div><b>Memora AI:</b> ' + data.reply + '</div>';
              chatBox.scrollTop = chatBox.scrollHeight;
            }).catch(err => {
              chatBox.innerHTML += '<div><b>Error:</b> Could not connect to backend.</div>';
            });
        }
    </script>
</body>
</html>`;
}
function deactivate() { }
//# sourceMappingURL=extension.js.map