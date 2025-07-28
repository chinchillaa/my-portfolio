# GitHub Secrets 設定ガイド

## 概要

GitHub Actionsを使用して、APIキーを安全にGitHub Pagesにデプロイする方法を説明します。

## 手順

### 1. GitHub Secretsの設定

1. GitHubリポジトリ（`my-portfolio`）にアクセス
2. **Settings** タブをクリック
3. 左側メニューの **Secrets and variables** → **Actions** をクリック
4. **New repository secret** ボタンをクリック
5. 以下を入力：
   - **Name**: `CHATBOT_API_KEY`
   - **Secret**: `Edj3wOdaVx2Fkx0jfcMy34f1kCqazDkY`
6. **Add secret** をクリック

### 2. GitHub Pagesの設定確認

1. **Settings** → **Pages**
2. **Source** が **GitHub Actions** に設定されていることを確認
   - もし **Deploy from a branch** になっている場合は、**GitHub Actions** に変更

### 3. デプロイの実行

プッシュすると自動的にGitHub Actionsが実行され、以下が行われます：

1. リポジトリのコードをチェックアウト
2. GitHub Secretsから`CHATBOT_API_KEY`を取得
3. `config.json`ファイルを自動生成
4. GitHub Pagesにデプロイ

### 4. 動作確認

1. **Actions** タブで、ワークフローの実行状況を確認
2. 緑色のチェックマークが表示されたら成功
3. ポートフォリオサイトにアクセスして、チャットボットが動作することを確認

## セキュリティ上の利点

- APIキーはGitHub Secretsに安全に保管
- リポジトリのコードには一切含まれない
- GitHub Actionsのログにも表示されない
- デプロイ時のみ使用され、公開されない

## トラブルシューティング

### エラー: ワークフローが失敗する

1. **Actions** タブでエラーログを確認
2. `CHATBOT_API_KEY` secretが正しく設定されているか確認
3. GitHub Pagesの設定が **GitHub Actions** になっているか確認

### エラー: チャットボットが動作しない

1. ブラウザの開発者ツールでコンソールエラーを確認
2. Network タブで `config.json` が正しく読み込まれているか確認
3. キャッシュをクリアして再度アクセス

---

**作成日**: 2025-07-28  
**最終更新**: 2025-07-28