# チャットボット デプロイメント手順

## 全体の流れ

1. Gemini API キーの取得
2. バックエンドAPIのRailwayデプロイ
3. フロントエンドの更新とGitHub Pagesへのデプロイ

## 1. Gemini API キーの取得

1. [Google AI Studio](https://makersuite.google.com/app/apikey)にアクセス
2. 「Create API Key」をクリック
3. APIキーをコピーして安全に保管

## 2. Railway デプロイ

### 2.1 Railwayアカウントの作成

1. [Railway](https://railway.app)でアカウント作成
2. GitHubアカウントと連携

### 2.2 新規プロジェクトの作成

1. ダッシュボードで「New Project」をクリック
2. 「Deploy from GitHub repo」を選択
3. リポジトリ（my-portfolio）を選択

### 2.3 バックエンドサービスの設定

1. **Root Directory**を`backend`に設定：
   - Settings → Root Directory → `backend`を入力

2. **環境変数の設定**：
   - Variables タブで以下を設定：
   ```
   GEMINI_API_KEY=<取得したGemini APIキー>
   SECRET_KEY=<openssl rand -hex 32で生成>
   ALLOWED_ORIGINS=https://chinchillaa.github.io
   ENVIRONMENT=production
   DEBUG=false
   RATE_LIMIT_PER_MINUTE=10
   RATE_LIMIT_PER_HOUR=100
   ```

### 2.4 Redisの追加

1. プロジェクト内で「New」→「Database」→「Add Redis」
2. Redis が作成されたら、環境変数に自動的に`REDIS_URL`が追加される

### 2.5 デプロイの確認

1. 「Deployments」タブでビルド状況を確認
2. ビルド完了後、提供されたURLを確認（例：`https://your-app.railway.app`）
3. `https://your-app.railway.app/api/v1/health`にアクセスして動作確認

## 3. フロントエンドの更新

### 3.1 API URLの更新

`chatbot/chatbot.js`を編集：

```javascript
constructor() {
    this.apiUrl = 'https://your-app.railway.app/api/v1'; // RailwayのURLに更新
    // ...
}
```

### 3.2 GitHub Pagesへのデプロイ

```bash
# 変更をコミット
git add .
git commit -m "feat: チャットボット機能を追加"

# GitHubにプッシュ
git push origin main
```

## 4. 動作確認

1. https://chinchillaa.github.io/my-portfolio/ にアクセス
2. 右下のチャットボタンをクリック
3. メッセージを送信して動作確認

## トラブルシューティング

### チャットボットが応答しない

1. **ブラウザのコンソールを確認**：
   - F12でDevToolsを開く
   - ConsoleタブでJavaScriptエラーを確認

2. **CORS エラーの場合**：
   - RailwayのALLOWED_ORIGINSが正しいか確認
   - HTTPSでアクセスしているか確認

3. **API接続エラーの場合**：
   - Railway のデプロイが成功しているか確認
   - API URLが正しく設定されているか確認

### レート制限エラー

- 1分間に10回以上リクエストすると制限される
- しばらく待ってから再試行

### Gemini APIエラー

- APIキーが正しく設定されているか確認
- Google AI StudioでAPIキーの使用状況を確認

## セキュリティのベストプラクティス

1. **APIキーの管理**：
   - Gemini APIキーは絶対にフロントエンドに含めない
   - Railwayの環境変数で安全に管理

2. **HTTPS の使用**：
   - GitHub Pages、Railwayともに自動的にHTTPSを提供

3. **レート制限**：
   - 悪意のある使用を防ぐため、適切なレート制限を設定

4. **入力検証**：
   - バックエンドで全ての入力を検証

## 今後の拡張案

1. **会話履歴の永続化**：
   - PostgreSQLを追加して会話履歴を保存

2. **ユーザー認証**：
   - JWT認証を実装してパーソナライズ

3. **分析機能**：
   - 会話ログの分析とインサイトの取得

4. **多言語対応**：
   - 英語版の追加