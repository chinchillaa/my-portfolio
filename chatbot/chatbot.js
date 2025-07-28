// チャットボットのメインロジック
class PortfolioChatbot {
    constructor() {
        this.apiUrl = 'https://your-backend.railway.app/api/v1'; // Railway URL に置き換え
        this.sessionId = this.getOrCreateSessionId();
        this.messages = [];
        this.isTyping = false;
        this.initializeElements();
        this.attachEventListeners();
    }

    // セッションIDの取得または作成
    getOrCreateSessionId() {
        let sessionId = localStorage.getItem('chatbot_session_id');
        if (!sessionId) {
            sessionId = this.generateSessionId();
            localStorage.setItem('chatbot_session_id', sessionId);
        }
        return sessionId;
    }

    // セッションIDの生成
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    // DOM要素の初期化
    initializeElements() {
        // チャットボタンの作成
        this.createChatButton();
        
        // チャットウィンドウの作成
        this.createChatWindow();
        
        // 必要な要素の参照を取得
        this.chatButton = document.getElementById('chatbot-button');
        this.chatWindow = document.getElementById('chatbot-window');
        this.messagesContainer = document.getElementById('chatbot-messages');
        this.inputTextarea = document.getElementById('chatbot-input');
        this.sendButton = document.getElementById('chatbot-send');
        this.closeButton = document.getElementById('chatbot-close');
    }

    // チャットボタンの作成
    createChatButton() {
        const button = document.createElement('button');
        button.id = 'chatbot-button';
        button.className = 'chatbot-button';
        button.innerHTML = `
            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2C6.48 2 2 6.48 2 12c0 1.54.36 3 .97 4.29L1 23l6.71-1.97C9 21.64 10.46 22 12 22c5.52 0 10-4.48 10-10s-4.48-10-10-10zm0 18c-1.41 0-2.73-.36-3.88-.99l-.28-.15-2.9.85.85-2.9-.15-.28C4.36 14.73 4 13.41 4 12c0-4.41 3.59-8 8-8s8 3.59 8 8-3.59 8-8 8z"/>
                <path d="M8 9h8v2H8zm0 3h5v2H8z"/>
            </svg>
        `;
        document.body.appendChild(button);
    }

    // チャットウィンドウの作成
    createChatWindow() {
        const window = document.createElement('div');
        window.id = 'chatbot-window';
        window.className = 'chatbot-window';
        window.innerHTML = `
            <div class="chatbot-header">
                <div>
                    <h3>AIアシスタント</h3>
                    <div class="chatbot-status">
                        <span class="status-dot"></span>
                        <span>オンライン</span>
                    </div>
                </div>
                <button id="chatbot-close" class="chatbot-close">×</button>
            </div>
            <div id="chatbot-messages" class="chatbot-messages">
                <div class="message assistant">
                    <div class="message-content">
                        こんにちは！津川聡のポートフォリオへようこそ。<br>
                        私について、スキルや経験など、何でもお聞きください。
                    </div>
                </div>
            </div>
            <div class="chatbot-input">
                <div class="input-wrapper">
                    <textarea 
                        id="chatbot-input" 
                        class="chatbot-textarea" 
                        placeholder="メッセージを入力..."
                        rows="1"
                    ></textarea>
                    <button id="chatbot-send" class="send-button">
                        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                        </svg>
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(window);
    }

    // イベントリスナーの設定
    attachEventListeners() {
        // チャットボタンのクリック
        this.chatButton.addEventListener('click', () => this.toggleChat());
        
        // 閉じるボタン
        this.closeButton.addEventListener('click', () => this.closeChat());
        
        // 送信ボタン
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        // Enterキーで送信（Shift+Enterは改行）
        this.inputTextarea.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // テキストエリアの自動リサイズ
        this.inputTextarea.addEventListener('input', () => this.autoResize());
    }

    // チャットの開閉
    toggleChat() {
        const isActive = this.chatWindow.classList.contains('active');
        if (isActive) {
            this.closeChat();
        } else {
            this.openChat();
        }
    }

    // チャットを開く
    openChat() {
        this.chatWindow.classList.add('active');
        this.inputTextarea.focus();
    }

    // チャットを閉じる
    closeChat() {
        this.chatWindow.classList.remove('active');
    }

    // メッセージ送信
    async sendMessage() {
        const message = this.inputTextarea.value.trim();
        if (!message || this.isTyping) return;

        // ユーザーメッセージを追加
        this.addMessage(message, 'user');
        
        // 入力をクリア
        this.inputTextarea.value = '';
        this.autoResize();
        
        // 送信ボタンを無効化
        this.isTyping = true;
        this.sendButton.disabled = true;
        
        // タイピングインジケーターを表示
        this.showTypingIndicator();
        
        try {
            // APIリクエスト
            const response = await this.callChatAPI(message);
            
            // タイピングインジケーターを削除
            this.hideTypingIndicator();
            
            // アシスタントの返答を追加
            this.addMessage(response.message, 'assistant');
            
        } catch (error) {
            console.error('Chat API error:', error);
            this.hideTypingIndicator();
            this.showError('申し訳ございません。エラーが発生しました。');
        } finally {
            this.isTyping = false;
            this.sendButton.disabled = false;
        }
    }

    // Chat APIの呼び出し
    async callChatAPI(message) {
        const response = await fetch(`${this.apiUrl}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Session-ID': this.sessionId,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({
                message: message,
                session_id: this.sessionId,
                context: this.messages.slice(-10) // 直近10件のコンテキスト
            })
        });

        if (!response.ok) {
            if (response.status === 429) {
                throw new Error('リクエスト制限に達しました。しばらく待ってから再度お試しください。');
            }
            throw new Error('APIエラーが発生しました。');
        }

        return await response.json();
    }

    // メッセージを追加
    addMessage(content, role) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;
        messageDiv.innerHTML = `
            <div class="message-content">${this.escapeHtml(content)}</div>
        `;
        
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
        
        // メッセージ履歴に追加
        this.messages.push({
            content: content,
            role: role,
            timestamp: new Date().toISOString()
        });
    }

    // タイピングインジケーターを表示
    showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'typing-indicator';
        indicator.className = 'message assistant';
        indicator.innerHTML = `
            <div class="typing-indicator">
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
            </div>
        `;
        this.messagesContainer.appendChild(indicator);
        this.scrollToBottom();
    }

    // タイピングインジケーターを削除
    hideTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }

    // エラーメッセージを表示
    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        this.messagesContainer.appendChild(errorDiv);
        this.scrollToBottom();
        
        // 5秒後に削除
        setTimeout(() => errorDiv.remove(), 5000);
    }

    // テキストエリアの自動リサイズ
    autoResize() {
        this.inputTextarea.style.height = 'auto';
        this.inputTextarea.style.height = Math.min(this.inputTextarea.scrollHeight, 120) + 'px';
    }

    // 最下部にスクロール
    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    // HTMLエスケープ
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML.replace(/\n/g, '<br>');
    }
}

// ページ読み込み時に初期化
document.addEventListener('DOMContentLoaded', () => {
    window.portfolioChatbot = new PortfolioChatbot();
});