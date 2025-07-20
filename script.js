// ハンバーガーメニュー
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

hamburger.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    hamburger.classList.toggle('active');
});

// ナビゲーションリンクをクリックしたときにメニューを閉じる
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
    });
});

// スムーススクロール
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const headerOffset = 80;
            const elementPosition = target.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// スクロール時のヘッダーエフェクト
const header = document.querySelector('.header');
const heroScroll = document.querySelector('.hero-scroll');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
    
    // hero-scrollを非表示にする（少しでもスクロールしたら非表示）
    if (currentScroll > 50) {
        heroScroll.classList.add('hidden');
    } else {
        heroScroll.classList.remove('hidden');
    }
    
    lastScroll = currentScroll;
});

// 要素のフェードインアニメーション
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            // アニメーションを一度だけ実行
            if (entry.target.classList.contains('once')) {
                observer.unobserve(entry.target);
            }
        }
    });
}, observerOptions);

// フェードインアニメーションを適用する要素
document.addEventListener('DOMContentLoaded', () => {
    // セクションタイトル
    document.querySelectorAll('.section-title').forEach(el => {
        el.classList.add('fade-in');
        observer.observe(el);
    });
    
    // スキルカテゴリー
    document.querySelectorAll('.skill-category').forEach((el, index) => {
        el.classList.add('fade-in');
        el.style.transitionDelay = `${index * 0.1}s`;
        observer.observe(el);
    });
    
    // タイムラインアイテム
    document.querySelectorAll('.timeline-item').forEach((el, index) => {
        el.classList.add('fade-in');
        el.style.transitionDelay = `${index * 0.2}s`;
        observer.observe(el);
    });
    
    // ポートフォリオアイテム
    document.querySelectorAll('.portfolio-item').forEach((el, index) => {
        el.classList.add('fade-in');
        el.style.transitionDelay = `${index * 0.1}s`;
        observer.observe(el);
    });
    
    // 統計
    document.querySelectorAll('.stat-item').forEach((el, index) => {
        el.classList.add('fade-in');
        el.style.transitionDelay = `${index * 0.1}s`;
        observer.observe(el);
    });
});

// お問い合わせフォーム
const contactForm = document.getElementById('contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            message: document.getElementById('message').value
        };
        
        // ここで実際のメール送信処理を実装
        alert(`お問い合わせありがとうございます、${formData.name}様。\n\nメッセージを受け取りました。\n返信まで少々お待ちください。`);
        
        // フォームをリセット
        this.reset();
    });
}

// タイピングアニメーション
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

// ページ読み込み時のアニメーション
window.addEventListener('load', () => {
    // タイトルのタイピングアニメーションは削除（モダンなフェードインを維持）
    
    // 数値のカウントアップアニメーション
    const statNumbers = document.querySelectorAll('.stat-number');
    
    statNumbers.forEach(stat => {
        const updateCount = () => {
            const target = stat.textContent;
            
            // 数値の場合のみカウントアップ
            if (target.includes('%')) {
                const finalValue = parseInt(target);
                let currentValue = 0;
                const increment = finalValue / 50;
                
                const timer = setInterval(() => {
                    currentValue += increment;
                    if (currentValue >= finalValue) {
                        currentValue = finalValue;
                        clearInterval(timer);
                    }
                    stat.textContent = Math.floor(currentValue) + '%';
                }, 30);
            } else if (target.includes('years+')) {
                const finalValue = parseInt(target);
                let currentValue = 0;
                const increment = finalValue / 50;
                
                const timer = setInterval(() => {
                    currentValue += increment;
                    if (currentValue >= finalValue) {
                        currentValue = finalValue;
                        clearInterval(timer);
                    }
                    stat.textContent = Math.floor(currentValue) + 'years+';
                }, 30);
            } else if (target.includes('+')) {
                const finalValue = parseInt(target.replace('+', ''));
                let currentValue = 0;
                const increment = finalValue / 50;
                
                const timer = setInterval(() => {
                    currentValue += increment;
                    if (currentValue >= finalValue) {
                        currentValue = finalValue;
                        clearInterval(timer);
                    }
                    stat.textContent = Math.floor(currentValue) + '+';
                }, 30);
            }
        };
        
        // 要素が表示されたときにカウントアップを開始
        const countObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    updateCount();
                    countObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        countObserver.observe(stat);
    });
});

// パララックス効果（ヒーロー部分）
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero');
    
    if (hero && scrolled < window.innerHeight) {
        // パララックス効果を弱める（0.5から0.2に変更）
        hero.style.transform = `translateY(${scrolled * 0.2}px)`;
    }
});

// スキルタグのホバーエフェクト
document.querySelectorAll('.skill-tag').forEach(tag => {
    tag.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.05)';
    });
    
    tag.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
    });
});

// ポートフォリオアイテムの詳細表示（将来的な実装用）
document.querySelectorAll('.portfolio-item').forEach(item => {
    item.addEventListener('click', function() {
        // 将来的にモーダルやページ遷移を実装
        console.log('Portfolio item clicked:', this.querySelector('h3').textContent);
    });
});