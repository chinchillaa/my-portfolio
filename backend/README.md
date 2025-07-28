# ポートフォリオチャットボット バックエンドAPI

FastAPI + Gemini APIを使用したチャットボットのバックエンドAPIです。

## 機能

- Gemini Pro APIを使用した自然な会話
- レート制限（1分10リクエスト、1時間100リクエスト）
- セキュリティ対策（CORS、CSP、入力検証）
- セッション管理
- ヘルスチェックエンドポイント

## セットアップ

### 1. 環境変数の設定

`.env.example`をコピーして`.env`を作成し、必要な値を設定：

```bash
cp .env.example .env
```

必須の環境変数：
- `GEMINI_API_KEY`: Google AI StudioからGemini APIキーを取得
- `SECRET_KEY`: `openssl rand -hex 32`で生成
- `REDIS_URL`: RedisのURL（Railway提供）

### 2. ローカル開発

```bash
# 仮想環境の作成
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt

# Redisの起動（Docker使用）
docker run -d -p 6379:6379 redis:alpine

# 開発サーバーの起動
uvicorn app.main:app --reload
```

APIドキュメント: http://localhost:8000/docs

### 3. Railway へのデプロイ

#### 3.1 Railway プロジェクトの作成

1. [Railway](https://railway.app)にログイン
2. 「New Project」→「Deploy from GitHub repo」を選択
3. リポジトリを選択（`backend`ディレクトリを指定）

#### 3.2 サービスの追加

**Redis の追加：**
1. 「New」→「Database」→「Add Redis」
2. 接続情報をコピー

#### 3.3 環境変数の設定

Railway ダッシュボードで以下を設定：

```
GEMINI_API_KEY=your-gemini-api-key
SECRET_KEY=your-secret-key
REDIS_URL=${{Redis.REDIS_URL}}
ALLOWED_ORIGINS=https://chinchillaa.github.io
ENVIRONMENT=production
DEBUG=false
```

#### 3.4 デプロイ設定

1. 「Settings」→「Root Directory」を`backend`に設定
2. 「Deploy」タブでデプロイを確認

## API エンドポイント

### ヘルスチェック
```
GET /api/v1/health
```

### チャット
```
POST /api/v1/chat
Content-Type: application/json

{
    "message": "こんにちは",
    "session_id": "optional-session-id",
    "context": []
}
```

### レート制限クォータ
```
GET /api/v1/chat/quota
```

## フロントエンドとの接続

`chatbot/chatbot.js`内のAPIURLを更新：

```javascript
this.apiUrl = 'https://your-app.railway.app/api/v1';
```

## セキュリティ考慮事項

1. **CORS**: 特定のオリジンのみ許可
2. **レート制限**: IPベースでリクエスト制限
3. **入力検証**: Pydanticによる厳格な検証
4. **CSP**: Content Security Policyの実装
5. **HTTPS**: Railway は自動的にHTTPSを提供

## トラブルシューティング

### Redis接続エラー
- Redis URLが正しく設定されているか確認
- Railway のRedisサービスが起動しているか確認

### Gemini APIエラー
- APIキーが有効か確認
- クォータ制限に達していないか確認

### CORS エラー
- `ALLOWED_ORIGINS`に正しいURLが設定されているか確認
- フロントエンドのURLがHTTPSか確認