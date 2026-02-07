// ========================================
// KAYNEL - Premium Digital Agency
// JavaScript Functionality
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    // Initialize all functionality
    initNavbar();
    initMobileMenu();
    initLanguageSwitcher();
    initScrollAnimations();
    initSmoothScroll();
    initContactForm();
});

// ========================================
// NAVBAR - Scroll Effect
// ========================================
function initNavbar() {
    const navbar = document.getElementById('navbar');
    let lastScrollY = window.scrollY;
    
    window.addEventListener('scroll', () => {
        const currentScrollY = window.scrollY;
        
        if (currentScrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        lastScrollY = currentScrollY;
    }, { passive: true });
}

// ========================================
// MOBILE MENU
// ========================================
function initMobileMenu() {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navLinks = document.getElementById('navLinks');
    
    if (!mobileMenuBtn || !navLinks) return;
    
    mobileMenuBtn.addEventListener('click', () => {
        mobileMenuBtn.classList.toggle('active');
        navLinks.classList.toggle('active');
    });
    
    // Close menu when clicking on a link
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            mobileMenuBtn.classList.remove('active');
            navLinks.classList.remove('active');
        });
    });
    
    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!mobileMenuBtn.contains(e.target) && !navLinks.contains(e.target)) {
            mobileMenuBtn.classList.remove('active');
            navLinks.classList.remove('active');
        }
    });
}

// ========================================
// LANGUAGE SWITCHER
// ========================================
function initLanguageSwitcher() {
    const langButtons = document.querySelectorAll('.lang-btn');
    const currentLang = localStorage.getItem('kaynel-lang') || 'en';
    
    // Set initial language
    setLanguage(currentLang);
    
    // Update button states
    langButtons.forEach(btn => {
        if (btn.dataset.lang === currentLang) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
        
        btn.addEventListener('click', () => {
            const lang = btn.dataset.lang;
            setLanguage(lang);
            localStorage.setItem('kaynel-lang', lang);
            
            // Update button states
            langButtons.forEach(b => {
                b.classList.toggle('active', b.dataset.lang === lang);
            });
        });
    });
}

function setLanguage(lang) {
    // Update HTML lang attribute
    document.documentElement.lang = lang;
    
    // Update all elements with data-en and data-pl attributes
    document.querySelectorAll('[data-en][data-pl]').forEach(element => {
        const text = element.getAttribute(`data-${lang}`);
        if (text) {
            // Handle different element types
            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                element.placeholder = text;
            } else {
                // Preserve child elements (like SVG icons) if they exist
                const svg = element.querySelector('svg');
                if (svg) {
                    element.innerHTML = text + ' ';
                    element.appendChild(svg);
                } else {
                    element.textContent = text;
                }
            }
        }
    });
    
    // Handle placeholders separately
    document.querySelectorAll('[data-placeholder-en][data-placeholder-pl]').forEach(element => {
        const text = element.getAttribute(`data-placeholder-${lang}`);
        if (text) {
            element.placeholder = text;
        }
    });
    
    // Handle select options
    document.querySelectorAll('select option[data-en][data-pl]').forEach(option => {
        const text = option.getAttribute(`data-${lang}`);
        if (text) {
            option.textContent = text;
        }
    });
    
    // Update page title based on language
    if (lang === 'pl') {
        document.title = 'Kaynel - Podnieś Swoją Obecność Cyfrową';
    } else {
        document.title = 'Kaynel - Elevate Your Digital Presence';
    }
}

// ========================================
// SCROLL ANIMATIONS
// ========================================
function initScrollAnimations() {
    // Add fade-in class to elements
    const animatedElements = [
        '.service-card',
        '.stat-card',
        '.process-step',
        '.about-content',
        '.contact-info',
        '.contact-form-wrapper',
        '.section-header'
    ];
    
    animatedElements.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
            el.classList.add('fade-in');
        });
    });
    
    // Intersection Observer for scroll animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // Optional: stop observing after animation
                // observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.fade-in').forEach(el => {
        observer.observe(el);
    });
    
    // Stagger animation for grid items
    const staggerContainers = ['.services-grid', '.stats-grid', '.process-steps'];
    
    staggerContainers.forEach(containerSelector => {
        const container = document.querySelector(containerSelector);
        if (container) {
            const items = container.querySelectorAll('.fade-in');
            items.forEach((item, index) => {
                item.style.transitionDelay = `${index * 0.1}s`;
            });
        }
    });
}

// ========================================
// SMOOTH SCROLL
// ========================================
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            
            if (targetId === '#') return;
            
            const target = document.querySelector(targetId);
            if (target) {
                const navbarHeight = document.getElementById('navbar').offsetHeight;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navbarHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ========================================
// CONTACT FORM
// ========================================
function initContactForm() {
    const form = document.getElementById('contactForm');
    const newsletterForms = document.querySelectorAll('.newsletter-form');
    
    if (form) {
        form.addEventListener('submit', handleContactSubmit);
    }
    
    newsletterForms.forEach(nForm => {
        nForm.addEventListener('submit', handleNewsletterSubmit);
    });
}

function handleContactSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    const lang = localStorage.getItem('kaynel-lang') || 'en';
    
    // Gather form data
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    // Show loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = lang === 'pl' ? 'Wysyłanie...' : 'Sending...';
    
    // Simulate form submission (replace with actual endpoint)
    setTimeout(() => {
        // Success state
        submitBtn.innerHTML = lang === 'pl' ? 
            '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg> ' + (lang === 'pl' ? 'Wysłano!' : 'Sent!') :
            '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg> Sent!';
        submitBtn.style.background = '#22c55e';
        
        // Reset form
        form.reset();
        
        // Reset button after 3 seconds
        setTimeout(() => {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
            submitBtn.style.background = '';
        }, 3000);
        
        // Log data (for testing - replace with actual API call)
        console.log('Form submitted:', data);
        
    }, 1500);
}

function handleNewsletterSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const input = form.querySelector('input[type="email"]');
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalHTML = submitBtn.innerHTML;
    const lang = localStorage.getItem('kaynel-lang') || 'en';
    
    // Show loading
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="animate-spin"><circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="12"/></svg>';
    
    // Simulate submission
    setTimeout(() => {
        // Success
        submitBtn.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 12l2 2 4-4"/></svg>';
        submitBtn.style.background = '#22c55e';
        input.value = '';
        
        // Reset
        setTimeout(() => {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalHTML;
            submitBtn.style.background = '';
        }, 2000);
        
    }, 1000);
}

// ========================================
// UTILITY FUNCTIONS
// ========================================

// Debounce function for performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function for scroll events
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Check if element is in viewport
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// ========================================
// ADDITIONAL MICRO-INTERACTIONS
// ========================================

// Button hover effects
document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('mouseenter', function(e) {
        const x = e.clientX - this.getBoundingClientRect().left;
        const y = e.clientY - this.getBoundingClientRect().top;
        
        this.style.setProperty('--x', `${x}px`);
        this.style.setProperty('--y', `${y}px`);
    });
});

// Card tilt effect on hover (subtle)
document.querySelectorAll('.service-card, .stat-card').forEach(card => {
    card.addEventListener('mousemove', function(e) {
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const rotateX = (y - centerY) / 20;
        const rotateY = (centerX - x) / 20;
        
        this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px)`;
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = '';
    });
});

// Typing effect for hero title (optional - uncomment to enable)
/*
function typeWriter(element, text, speed = 50) {
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
*/

// Console branding
console.log('%c Kaynel ', 'background: #2563eb; color: white; font-size: 24px; font-weight: bold; padding: 10px 20px; border-radius: 8px;');
console.log('%c Premium Digital Agency ', 'color: #6b7280; font-size: 14px; padding: 5px 0;');
