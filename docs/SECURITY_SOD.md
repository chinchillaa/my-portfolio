# セキュリティ脆弱性修正 Statement of Direction (SOD)

## エグゼクティブサマリー

本ドキュメントは、ポートフォリオサイトのチャットボットシステムにおいて発見されたセキュリティ脆弱性に対する修正計画を定義します。重大な脆弱性として、API認証の欠如、XSS対策の不備、レート制限のバイパス可能性が確認されており、これらは早急な対応が必要です。

## 1. 現状の脆弱性評価

### 1.1 重大度別脆弱性一覧

#### Critical（緊急）
- なし

#### High（重大）
1. **API認証の完全な欠如**
   - 影響：無制限のAPI呼び出しによるコスト増大
   - リスク：Gemini APIの悪用、サービス停止

2. **不完全なXSS対策**
   - 影響：ユーザーデータの窃取、セッション乗っ取り
   - リスク：信頼性の喪失、法的責任

3. **Redisダウン時のレート制限無効化**
   - 影響：DoS攻撃への脆弱性
   - リスク：サービスの可用性低下

#### Medium（中程度）
1. CSRF保護の未実装
2. デバッグ情報の露出リスク
3. 過度に寛容なCORS設定
4. センシティブ情報のログ出力
5. 依存関係の脆弱性

#### Low（低）
1. セッションIDの予測可能性
2. APIエンドポイントのハードコーディング

## 2. 修正実装計画

### 2.1 フェーズ1：緊急対応（1-2日）

#### タスク1：API認証システムの実装
**アプローチ：** シンプルなAPIキー認証
- 実装内容：
  - APIキーの生成と管理機能
  - リクエストヘッダーでの認証
  - 環境変数での安全な管理
- 理由：JWTより実装が簡単で、現在の要件に十分

#### タスク2：XSS対策の強化
**アプローチ：** bleachライブラリの導入
- 実装内容：
  - bleachによる入力サニタイゼーション
  - フロントエンドでのtextContent使用への移行
  - Content Security Policy (CSP)の追加

#### タスク3：レート制限のフォールバック実装
**アプローチ：** メモリ内カウンターの実装
- 実装内容：
  - Redisダウン時のインメモリレート制限
  - サーキットブレーカーパターンの実装
  - グレースフルデグラデーション

### 2.2 フェーズ2：中期対応（3-5日）

#### タスク4：CSRF保護の完全実装
- Double Submit Cookieパターンの採用
- トークン生成と検証ロジック

#### タスク5：ログのサニタイゼーション
- PII（個人識別情報）のマスキング
- 構造化ログの採用

#### タスク6：セキュリティヘッダーの追加
- X-Frame-Options
- X-Content-Type-Options
- Strict-Transport-Security

### 2.3 フェーズ3：継続的改善（1週間以降）

- 依存関係の定期更新プロセス確立
- セキュリティ監査の自動化
- ペネトレーションテストの実施

## 3. 実装の技術的詳細

### 3.1 API認証（APIキー方式）

```python
# backend/app/core/auth.py
class APIKeyAuth:
    def __init__(self):
        self.api_key = settings.API_KEY
    
    async def verify_api_key(self, x_api_key: str = Header(...)):
        if not secrets.compare_digest(x_api_key, self.api_key):
            raise HTTPException(status_code=403, detail="Invalid API Key")
```

### 3.2 XSS対策

```python
# requirements.txt に追加
bleach==6.1.0

# backend/app/core/security.py の改善
import bleach

def sanitize_input(text: str) -> str:
    allowed_tags = []  # タグを一切許可しない
    return bleach.clean(text, tags=allowed_tags, strip=True)
```

### 3.3 レート制限フォールバック

```python
# backend/app/services/rate_limiter.py の改善
from collections import defaultdict
from datetime import datetime, timedelta

class InMemoryRateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
    
    def check_rate_limit(self, key: str, limit: int, window: int):
        now = datetime.now()
        cutoff = now - timedelta(seconds=window)
        
        # 古いリクエストを削除
        self.requests[key] = [req for req in self.requests[key] if req > cutoff]
        
        if len(self.requests[key]) >= limit:
            return False
        
        self.requests[key].append(now)
        return True
```

## 4. リスク評価とミティゲーション

### 4.1 実装リスク
1. **既存機能への影響**
   - ミティゲーション：段階的なロールアウト、十分なテスト

2. **パフォーマンス低下**
   - ミティゲーション：キャッシング、最適化

3. **ユーザー体験の悪化**
   - ミティゲーション：透明性のあるエラーメッセージ

### 4.2 未対応時のリスク
1. **コスト増大**：月額$1000以上の不正利用の可能性
2. **レピュテーション損失**：セキュリティインシデントによる信頼失墜
3. **法的責任**：データ漏洩による損害賠償リスク

## 5. 成功基準

### 5.1 技術的成功基準
- [ ] すべてのAPIエンドポイントが認証で保護されている
- [ ] OWASP Top 10の脆弱性に対する対策が実装されている
- [ ] 自動セキュリティテストが100%パスする

### 5.2 ビジネス成功基準
- [ ] 不正利用によるコスト増加がゼロ
- [ ] セキュリティインシデントゼロ
- [ ] ユーザーからのセキュリティ関連クレームゼロ

## 6. タイムライン

```
Week 1: フェーズ1完了（API認証、XSS対策、レート制限）
Week 2: フェーズ2完了（CSRF、ログ、ヘッダー）
Week 3: フェーズ3開始（継続的改善）
```

## 7. 承認と次のステップ

本SODの承認後、以下のアクションを実行します：

1. 詳細な技術設計ドキュメントの作成
2. 開発環境でのPoCの実装
3. セキュリティテストケースの作成
4. 段階的な本番環境への適用

---

**作成日**: 2025-07-28  
**作成者**: AI Assistant  
**承認者**: [承認待ち]  
**最終更新**: 2025-07-28