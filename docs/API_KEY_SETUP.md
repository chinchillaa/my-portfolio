# APIキー設定ガイド

## 概要

このガイドでは、ポートフォリオチャットボットのAPIキー認証を設定する手順を説明します。

## セキュリティの重要性

APIキー認証を実装することで：
- 不正なAPI利用を防止
- Gemini APIの使用コストを管理
- サービスの安定性を確保

## 設定手順

### 1. APIキーの生成

まず、安全なAPIキーを生成します。以下のPythonスクリプトを使用できます：

```python
import secrets
import string

def generate_api_key(length=32):
    """安全なAPIキーを生成"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# APIキーを生成
api_key = generate_api_key()
print(f"Generated API Key: {api_key}")
```

または、オンラインツールを使用：
- https://www.uuidgenerator.net/
- https://passwordsgenerator.net/

### 2. Railway環境変数の設定

1. Railwayダッシュボードにログイン
2. プロジェクト「portfolio-chatbot」を選択
3. 「Variables」タブをクリック
4. 以下の環境変数を追加：

```
API_KEY=生成したAPIキー
```

例：
```
API_KEY=xK9mP2nQ8rT5vY3wA6bC4dE7fG1hJ0kL
```

### 3. フロントエンド設定

1. プロジェクトルートに`config.json`ファイルを作成：

```json
{
  "apiKey": "生成したAPIキー"
}
```

2. **重要**: `config.json`は`.gitignore`に含まれているため、GitHubにはプッシュされません。

3. GitHub Pagesにデプロイする際は、手動で`config.json`をアップロードする必要があります。

### 4. 動作確認

1. Railway環境変数が正しく設定されているか確認：
   - Railwayログで「API Key authentication enabled」のメッセージを確認

2. フロントエンドでの確認：
   - ブラウザの開発者ツールでNetworkタブを開く
   - チャットメッセージを送信
   - リクエストヘッダーに`X-API-Key`が含まれていることを確認

## セキュリティベストプラクティス

### ✅ DO（推奨事項）

1. **APIキーの定期的な更新**
   - 3-6ヶ月ごとにAPIキーを更新

2. **最小権限の原則**
   - APIキーはチャットボット専用に使用

3. **監視とログ**
   - 不正なアクセス試行を監視
   - Railwayのログを定期的に確認

4. **HTTPS必須**
   - APIキーは必ずHTTPS経由で送信

### ❌ DON'T（禁止事項）

1. **APIキーの共有禁止**
   - APIキーを他人と共有しない
   - パブリックリポジトリにコミットしない

2. **クライアントサイドでの生成禁止**
   - APIキーをJavaScriptで生成しない
   - ソースコードに直接記載しない

3. **平文での保存禁止**
   - メールやチャットでAPIキーを送信しない
   - ローカルファイルに平文で保存しない

## トラブルシューティング

### 問題: 401 Unauthorized エラー

**原因**: APIキーが正しく設定されていない

**解決方法**:
1. Railway環境変数を確認
2. config.jsonのAPIキーが一致しているか確認
3. ブラウザキャッシュをクリア

### 問題: 403 Forbidden エラー

**原因**: APIキーが無効

**解決方法**:
1. APIキーの形式を確認（スペースや改行が含まれていないか）
2. Railway環境変数とconfig.jsonのAPIキーが完全に一致しているか確認

### 問題: チャットボットが初期化に失敗

**原因**: config.jsonが見つからない

**解決方法**:
1. config.jsonがプロジェクトルートに存在するか確認
2. ファイル名が正確か確認（config.json.exampleではない）
3. JSONフォーマットが正しいか確認

## APIキーのローテーション手順

1. **新しいAPIキーを生成**
   ```python
   new_api_key = generate_api_key()
   ```

2. **Railway環境変数を更新**
   - 既存のAPI_KEYを新しい値に更新

3. **config.jsonを更新**
   ```json
   {
     "apiKey": "新しいAPIキー"
   }
   ```

4. **動作確認後、古いAPIキーを無効化**
   - 24時間の移行期間を設ける

## セキュリティインシデント対応

APIキーが漏洩した場合：

1. **即座にAPIキーを無効化**
   - Railway環境変数を更新

2. **新しいAPIキーを生成・設定**
   - 上記のローテーション手順に従う

3. **ログを確認**
   - 不正使用の痕跡を調査

4. **インシデントレポート作成**
   - 漏洩の原因と対策を文書化

---

**最終更新**: 2025-07-28  
**作成者**: AI Assistant