// スムーススクロール機能
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const headerOffset = 60;
            const elementPosition = target.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// お問い合わせフォームの処理
document.getElementById('contact-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // フォームデータを取得
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        message: document.getElementById('message').value
    };
    
    // ここで実際のメール送信処理を実装できます
    // 現在は単純にアラートを表示
    alert(`お問い合わせありがとうございます、${formData.name}様。\n\nメッセージを受け取りました。\n返信まで少々お待ちください。`);
    
    // フォームをリセット
    this.reset();
});

// スクロールに応じてヘッダーの背景を変更
let lastScroll = 0;
window.addEventListener('scroll', () => {
    const header = document.querySelector('header');
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
        header.style.backgroundColor = 'rgba(51, 51, 51, 0.95)';
        header.style.boxShadow = '0 2px 5px rgba(0,0,0,0.1)';
    } else {
        header.style.backgroundColor = '#333';
        header.style.boxShadow = 'none';
    }
    
    lastScroll = currentScroll;
});

// アニメーション効果（要素が画面に入ったらフェードイン）
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// 監視する要素を設定
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.skill-item, .timeline-item, .portfolio-item');
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});

// タイピングエフェクト（オプション）
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.textContent = '';
    
    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// ページ読み込み時にヒーローセクションのテキストにタイピングエフェクトを適用
window.addEventListener('load', () => {
    const heroTitle = document.querySelector('#hero h1');
    if (heroTitle) {
        const originalText = heroTitle.textContent;
        typeWriter(heroTitle, originalText, 80);
    }
});