#!/usr/bin/env python3
"""
APIキー生成スクリプト
安全なランダム文字列を生成してAPIキーとして使用
"""
import secrets
import string

def generate_api_key(length=32):
    """
    暗号学的に安全なAPIキーを生成
    
    Args:
        length: APIキーの長さ（デフォルト: 32文字）
    
    Returns:
        生成されたAPIキー
    """
    # 使用する文字（英数字）
    alphabet = string.ascii_letters + string.digits
    
    # secretsモジュールを使用して安全な乱数を生成
    api_key = ''.join(secrets.choice(alphabet) for _ in range(length))
    
    return api_key

def main():
    print("=== APIキー生成ツール ===\n")
    
    # APIキーを生成
    api_key = generate_api_key()
    
    print("生成されたAPIキー:")
    print(f"\033[92m{api_key}\033[0m")  # 緑色で表示
    print("\n" + "="*50)
    
    print("\n【次の手順】\n")
    print("1. Railway設定:")
    print("   - Railwayダッシュボードにログイン")
    print("   - Variables タブで以下を追加:")
    print(f"   API_KEY={api_key}")
    
    print("\n2. フロントエンド設定:")
    print("   - プロジェクトルートに config.json を作成:")
    print('   {')
    print(f'     "apiKey": "{api_key}"')
    print('   }')
    
    print("\n3. 重要な注意事項:")
    print("   - このAPIキーは一度だけ表示されます")
    print("   - 安全な場所に保管してください")
    print("   - GitHubにコミットしないでください")
    
    print("\n" + "="*50)

if __name__ == "__main__":
    main()