# Formspree セットアップ手順

## 重要な設定

1. **Formspreeアカウントの作成**
   - https://formspree.io にアクセス
   - 2gawasa10ru@gmail.com でアカウントを作成

2. **フォームの作成**
   - ダッシュボードで「New Form」をクリック
   - Form name: "Portfolio Contact Form"
   - Email: 2gawasa10ru@gmail.com を設定

3. **フォームIDの確認**
   - 作成後に表示されるForm ID（例：mwpkgkzr）を確認
   - このIDは既にindex.htmlに設定済み

4. **メール認証**
   - 最初の送信時に2gawasa10ru@gmail.comに確認メールが届きます
   - メール内のリンクをクリックして認証を完了してください

## 現在の実装

- HTMLフォームのaction属性に`https://formspree.io/f/mwpkgkzr`を設定
- method="POST"でフォームデータを送信
- JavaScriptで送信ボタンの二重送信防止を実装

## テスト方法

1. https://chinchillaa.github.io/my-portfolio/ にアクセス
2. Contactセクションまでスクロール
3. テストメッセージを入力して送信
4. 2gawasa10ru@gmail.comでメールを確認

## 注意事項

- 無料プランは月50件まで
- スパムフィルター機能付き
- 送信後はFormspreeのサンキューページにリダイレクトされます
- カスタムサンキューページを設定する場合は有料プランが必要