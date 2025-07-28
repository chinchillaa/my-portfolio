"""
XSS対策のテストケース
実際の攻撃ペイロードに対する防御を確認
"""
from app.core.security import SecurityService


def test_xss_payloads():
    """一般的なXSSペイロードに対するテスト"""
    
    # テスト用のXSSペイロード
    xss_payloads = [
        # 基本的なスクリプトタグ
        '<script>alert("XSS")</script>',
        '<SCRIPT>alert("XSS")</SCRIPT>',
        
        # エンコードされた攻撃
        '&#60;script&#62;alert("XSS")&#60;/script&#62;',
        '%3Cscript%3Ealert("XSS")%3C/script%3E',
        
        # イベントハンドラー
        '<img src=x onerror="alert(\'XSS\')">',
        '<body onload="alert(\'XSS\')">',
        '<svg onload="alert(\'XSS\')">',
        
        # JavaScriptプロトコル
        '<a href="javascript:alert(\'XSS\')">Click</a>',
        '<iframe src="javascript:alert(\'XSS\')"></iframe>',
        
        # データURL
        '<img src="data:text/html,<script>alert(\'XSS\')</script>">',
        
        # CSSインジェクション
        '<style>body{background:url("javascript:alert(\'XSS\')")}</style>',
        
        # 不正な属性
        '<div style="background-image: url(javascript:alert(\'XSS\'))">',
        
        # 難読化
        '<script>eval(atob("YWxlcnQoJ1hTUycp"))</script>',
        
        # 改行を使った回避
        '<script\n>alert("XSS")</\nscript>',
        
        # Null文字
        '<scr\x00ipt>alert("XSS")</scr\x00ipt>',
    ]
    
    print("=== XSS対策テスト結果 ===\n")
    
    for payload in xss_payloads:
        # HTMLを許可しない場合
        sanitized_no_html = SecurityService.sanitize_input(payload, allow_html=False)
        
        # HTMLを許可する場合
        sanitized_with_html = SecurityService.sanitize_input(payload, allow_html=True)
        
        print(f"元のペイロード: {payload}")
        print(f"サニタイズ後（HTML不許可）: {sanitized_no_html}")
        print(f"サニタイズ後（HTML許可）: {sanitized_with_html}")
        print("-" * 80)
    
    # Markdownのテスト
    print("\n=== Markdownサニタイズテスト ===\n")
    
    markdown_payloads = [
        "# 見出し\n<script>alert('XSS')</script>",
        "[リンク](javascript:alert('XSS'))",
        "![画像](x\" onerror=\"alert('XSS'))",
        "```javascript\nalert('XSS')\n```",
    ]
    
    for payload in markdown_payloads:
        sanitized = SecurityService.sanitize_markdown(payload)
        print(f"Markdown: {payload}")
        print(f"サニタイズ後HTML: {sanitized}")
        print("-" * 80)
    
    # URLバリデーションテスト
    print("\n=== URLバリデーションテスト ===\n")
    
    urls = [
        "https://example.com",
        "javascript:alert('XSS')",
        "data:text/html,<script>alert('XSS')</script>",
        "vbscript:msgbox('XSS')",
        "http://example.com/page?param=value",
    ]
    
    for url in urls:
        is_valid = SecurityService.validate_url(url)
        print(f"URL: {url}")
        print(f"有効: {is_valid}")
        print("-" * 40)


if __name__ == "__main__":
    test_xss_payloads()