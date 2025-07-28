# チャットボット デプロイメント詳細手順

このガイドでは、ポートフォリオサイトにチャットボット機能を追加するための手順を、初めてRailwayを使う方でも分かりやすく説明します。

## 🎯 完成イメージ

デプロイが完了すると、ポートフォリオサイトの右下にチャットボタンが表示され、AIアシスタントと会話できるようになります。

## 📋 前提条件

- GitHubアカウントを持っていること
- このリポジトリ（my-portfolio）がGitHubにプッシュされていること
- Googleアカウントを持っていること（Gemini API用）

## 🚀 全体の流れ（所要時間：約30分）

1. **Gemini API キーの取得**（5分）
2. **Railwayアカウントの作成とセットアップ**（10分）
3. **バックエンドAPIのデプロイ**（10分）
4. **フロントエンドの更新**（5分）

---

## 📝 STEP 1: Gemini API キーの取得

### 1.1 Google AI Studioにアクセス

1. ブラウザで [Google AI Studio](https://makersuite.google.com/app/apikey) を開きます
2. Googleアカウントでログインします

### 1.2 APIキーの作成

1. 画面に表示される「**Create API Key**」ボタンをクリックします
2. 「**Create API key in new project**」を選択します
3. 少し待つと、APIキーが表示されます（例：`AIzaSy...`で始まる文字列）

### 1.3 APIキーの保管

⚠️ **重要**: このAPIキーは後で使うので、以下の方法で安全に保管してください：

1. メモ帳などのテキストエディタにコピー＆ペーストする
2. 「gemini-api-key.txt」などの名前で保存する
3. **絶対に公開しない**（GitHubにアップロードしない）

---

## 🚂 STEP 2: Railwayのセットアップ

### 2.1 Railwayアカウントの作成

1. [Railway.app](https://railway.app) にアクセスします
2. 「**Start a New Project**」ボタンをクリックします
3. 「**Login with GitHub**」を選択します
   - GitHubの認証画面が表示されます
   - 「Authorize Railway」をクリックして連携を許可します

### 2.2 料金プランについて

- Railwayは**月$5の使用料**がかかります（最初の$5分は無料クレジット）
- クレジットカードの登録が必要です
- 「**Upgrade**」ボタンから「Developer Plan」を選択してください

---

## 🔧 STEP 3: バックエンドAPIのデプロイ

### 3.1 新規プロジェクトの作成

1. Railwayダッシュボードで「**+ New Project**」ボタンをクリックします

2. 「**Deploy from GitHub repo**」を選択します

3. リポジトリ選択画面で：
   - 「**Configure GitHub App**」をクリック（初回のみ）
   - 「my-portfolio」リポジトリを探して選択
   - 「**Deploy Now**」をクリック

### 3.2 プロジェクト名の設定（オプション）

1. 作成されたプロジェクトをクリックして開きます
2. 画面上部のプロジェクト名（ランダムな名前）をクリック
3. 分かりやすい名前に変更（例：`portfolio-chatbot`）

### 3.3 Root Directoryの設定 ⚠️重要

1. デプロイされたサービス（紫色のボックス）をクリックします
2. 「**Settings**」タブをクリックします
3. 下にスクロールして「**Service**」セクションを探します
4. 「**Root Directory**」の欄に `backend` と入力します
5. 画面右上の「**Save**」ボタンをクリックします

### 3.4 環境変数の設定

1. 同じ画面で「**Variables**」タブをクリックします

2. 「**+ New Variable**」ボタンをクリックして、以下の変数を1つずつ追加します：

   #### 変数1: GEMINI_API_KEY
   - **Variable name**: `GEMINI_API_KEY`
   - **Value**: 先ほどコピーしたGemini APIキー
   - 「**Add**」をクリック

   #### 変数2: SECRET_KEY
   - **Variable name**: `SECRET_KEY`
   - **Value**: 以下のサイトで生成した32文字のランダム文字列
     - [パスワード生成ツール](https://www.graviness.com/app/pwg/) にアクセス
     - 文字数を「32」に設定
     - 「生成」ボタンをクリック
     - 生成された文字列をコピー
   - 「**Add**」をクリック

   #### 変数3: ALLOWED_ORIGINS
   - **Variable name**: `ALLOWED_ORIGINS`
   - **Value**: `https://chinchillaa.github.io`
   - 「**Add**」をクリック

   #### 変数4: ENVIRONMENT
   - **Variable name**: `ENVIRONMENT`
   - **Value**: `production`
   - 「**Add**」をクリック

   #### 変数5: DEBUG
   - **Variable name**: `DEBUG`
   - **Value**: `false`
   - 「**Add**」をクリック

   #### 変数6: RATE_LIMIT_PER_MINUTE
   - **Variable name**: `RATE_LIMIT_PER_MINUTE`
   - **Value**: `10`
   - 「**Add**」をクリック

   #### 変数7: RATE_LIMIT_PER_HOUR
   - **Variable name**: `RATE_LIMIT_PER_HOUR`
   - **Value**: `100`
   - 「**Add**」をクリック

3. すべての変数を追加したら、画面右上の「**Deploy**」ボタンをクリックします

### 3.5 Redisデータベースの追加

1. プロジェクトのメイン画面に戻ります（左上のプロジェクト名をクリック）

2. 「**+ New**」ボタンをクリックします

3. 「**Database**」を選択します

4. 「**Add Redis**」をクリックします

5. Redisが追加されたら、自動的に環境変数`REDIS_URL`が設定されます

### 3.6 デプロイの確認

1. サービス（紫色のボックス）をクリックします

2. 「**Deployments**」タブをクリックします

3. 最新のデプロイメントのステータスを確認：
   - 🟡 黄色の点：ビルド中（5-10分待ちます）
   - 🟢 緑色の点：デプロイ成功
   - 🔴 赤色の点：エラー（ログを確認）

4. デプロイが成功したら、サービス名の下に表示されるURL（例：`xxx-production.up.railway.app`）をクリックします

5. URLの末尾に `/api/v1/health` を追加してアクセス：
   - 例：`https://xxx-production.up.railway.app/api/v1/health`
   - 「healthy」と表示されれば成功です！

### 3.7 Railway URLのコピー

⚠️ **重要**: 表示されているURL（`https://xxx-production.up.railway.app`）をメモ帳にコピーしてください。次のステップで使用します。

---

## 💻 STEP 4: フロントエンドの更新

### 4.1 chatbot.jsの編集

1. VSCodeやお好みのエディタで `chatbot/chatbot.js` ファイルを開きます

2. 2行目付近の以下の部分を探します：
   ```javascript
   this.apiUrl = 'https://your-backend.railway.app/api/v1';
   ```

3. `https://your-backend.railway.app` の部分を、先ほどコピーしたRailway URLに置き換えます：
   ```javascript
   this.apiUrl = 'https://xxx-production.up.railway.app/api/v1';
   ```

4. ファイルを保存します

### 4.2 変更のコミットとプッシュ

ターミナル（コマンドプロンプト）で以下のコマンドを実行：

```bash
# プロジェクトフォルダに移動（必要に応じて）
cd /home/chinchilla/pjt/portfolio

# 変更をステージング
git add chatbot/chatbot.js

# コミット
git commit -m "fix: Railway APIのURLを更新"

# GitHubにプッシュ
git push origin main
```

### 4.3 GitHub Pagesの更新待機

GitHubにプッシュ後、GitHub Pagesが更新されるまで**2-3分**待ちます。

---

## ✅ STEP 5: 動作確認

### 5.1 基本的な動作確認

1. ブラウザで https://chinchillaa.github.io/my-portfolio/ を開きます
2. 画面右下に緑色の丸いチャットボタンが表示されることを確認
3. チャットボタンをクリックしてチャット窓が開くことを確認
4. 「こんにちは」と入力して送信
5. AIアシスタントから返答が来れば成功です！🎉

### 5.2 動作確認チェックリスト

- [ ] チャットボタンが表示される
- [ ] チャット窓が開く
- [ ] メッセージを送信できる
- [ ] AIから返答が返ってくる
- [ ] エラーが表示されない

---

## 🔧 トラブルシューティング

### 問題1: チャットボタンが表示されない

**原因と対処法：**
1. ブラウザのキャッシュをクリア：
   - `Ctrl + Shift + R`（Windows）または `Cmd + Shift + R`（Mac）
2. 別のブラウザで試す
3. GitHub Pagesの更新を待つ（最大5分）

### 問題2: メッセージを送信してもエラーになる

**確認手順：**

1. **ブラウザの開発者ツールでエラーを確認**：
   - `F12`キーを押してDevToolsを開く
   - 「Console」タブをクリック
   - 赤いエラーメッセージを確認

2. **よくあるエラーと対処法**：

   #### CORS エラー（"Access-Control-Allow-Origin"）
   - Railway の環境変数 `ALLOWED_ORIGINS` が正しく設定されているか確認
   - URLが `https://` で始まっているか確認（httpではなく）

   #### 404 Not Found エラー
   - chatbot.js のAPIURLが正しいか確認
   - 末尾に `/api/v1` が付いているか確認

   #### 429 Too Many Requests エラー
   - レート制限（1分間に10回まで）に達しています
   - 1分待ってから再試行してください

3. **Railway側の確認**：
   - Railwayダッシュボードでサービスをクリック
   - 「Logs」タブでエラーログを確認
   - よくあるエラー：
     - `GEMINI_API_KEY is not set`：環境変数の設定ミス
     - `Redis connection failed`：Redisが追加されていない

### 問題3: "Gemini API error" が表示される

**対処法：**
1. Gemini APIキーが正しくコピーされているか確認
2. [Google AI Studio](https://makersuite.google.com/app/apikey) でAPIキーの状態を確認
3. 新しいAPIキーを生成して再設定

### 問題4: Railwayのデプロイが失敗する

**確認項目：**
1. Root Directoryが `backend` に設定されているか
2. すべての環境変数が正しく設定されているか
3. 「Logs」タブでビルドログを確認

---

## 💰 料金について

### Railway
- **Developer Plan**: 月額$5（最初の$5分は無料）
- **含まれるもの**：
  - 8GB RAM
  - 100GB帯域幅/月
  - Redis込み

### Gemini API
- **無料枠**：
  - 1分あたり60リクエストまで
  - 1日あたり1,500リクエストまで
- 通常の使用では無料枠で十分です

---

## 🔒 セキュリティの注意点

1. **APIキーの管理**：
   - Gemini APIキーは絶対にGitHubにコミットしない
   - chatbot.jsなどのフロントエンドファイルに直接書かない

2. **環境変数**：
   - すべての機密情報はRailwayの環境変数で管理

3. **HTTPS**：
   - 必ずHTTPS（https://）でアクセスする
   - HTTPは使用しない

---

## 📚 参考リンク

- [Railway ドキュメント](https://docs.railway.app/)
- [Gemini API ドキュメント](https://ai.google.dev/docs)
- [FastAPI ドキュメント](https://fastapi.tiangolo.com/)

---

## 🎉 完了！

おめでとうございます！これでポートフォリオサイトにAIチャットボット機能が追加されました。

質問や問題があれば、GitHubのIssuesで報告してください。