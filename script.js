// ==========================================================================
// 津川聡 ポートフォリオ — インタラクション
// ==========================================================================

// ハンバーガーメニュー
const header = document.querySelector('.header');
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

hamburger.addEventListener('click', () => {
    const isOpen = navMenu.classList.toggle('active');
    hamburger.classList.toggle('active', isOpen);
    header.classList.toggle('menu-open', isOpen);
    hamburger.setAttribute('aria-expanded', String(isOpen));
    hamburger.setAttribute('aria-label', isOpen ? 'メニューを閉じる' : 'メニューを開く');
});

// ナビゲーションリンクをクリックしたときにメニューを閉じる
const closeMenu = () => {
    navMenu.classList.remove('active');
    hamburger.classList.remove('active');
    header.classList.remove('menu-open');
    hamburger.setAttribute('aria-expanded', 'false');
};

document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', closeMenu);
});

// スムーススクロール（固定ヘッダー分をオフセット）
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (!target) return;
        e.preventDefault();
        const headerOffset = 72;
        const top = target.getBoundingClientRect().top + window.pageYOffset - headerOffset;
        window.scrollTo({ top, behavior: 'smooth' });
    });
});

// スクロール時のヘッダー背景 / SCROLLインジケーター
const heroScroll = document.querySelector('.hero-scroll');

window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset > 50;
    header.classList.toggle('scrolled', scrolled);
    if (heroScroll) {
        heroScroll.classList.toggle('hidden', scrolled);
    }
}, { passive: true });

// スクロール時のフェードイン（.reveal 要素）
const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            revealObserver.unobserve(entry.target);
        }
    });
}, {
    threshold: 0.1,
    rootMargin: '0px 0px -60px 0px'
});

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

    // 同一セクション内の兄弟要素は段階的に遅延させる
    document.querySelectorAll('.skills-grid, .works, .career, .about-facts').forEach(group => {
        group.querySelectorAll('.reveal').forEach((el, i) => {
            el.style.setProperty('--stagger', `${Math.min(i * 0.1, 0.5)}s`);
        });
    });

    // 現在地のナビゲーションリンクをハイライト
    const sections = document.querySelectorAll('main section[id]');
    const navLinks = new Map(
        [...document.querySelectorAll('.nav-link')].map(link => [link.getAttribute('href'), link])
    );

    const currentObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            const link = navLinks.get(`#${entry.target.id}`);
            if (link) {
                link.classList.toggle('current', entry.isIntersecting);
            }
        });
    }, { rootMargin: '-40% 0px -55% 0px' });

    sections.forEach(section => currentObserver.observe(section));
});

// お問い合わせフォーム（Formspreeへ送信・二重送信防止のみ）
const contactForm = document.getElementById('contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', function () {
        const submitButton = this.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        submitButton.textContent = '送信中…';
    });
}
