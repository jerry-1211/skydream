/**
 * main.js - 하늘 꿈나무 어린이집
 * Handles: burger menu, smooth scroll, tabs, hero slider, Swiper carousels, dropdowns
 */
document.addEventListener('DOMContentLoaded', function () {

    /* ================================================
       1. Hero Slider
       ================================================ */
    let currentSlide = 0;
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;

    function changeSlide(direction) {
        if (totalSlides === 0) return;

        slides[currentSlide].classList.remove('active');
        currentSlide += direction;

        if (currentSlide >= totalSlides) currentSlide = 0;
        if (currentSlide < 0) currentSlide = totalSlides - 1;

        slides[currentSlide].classList.add('active');
    }

    // Expose globally for inline onclick handlers
    window.changeSlide = changeSlide;

    /* ================================================
       2. Burger Menu + Mobile Dropdown
       ================================================ */
    var burger = document.getElementById('burger');
    var nav = document.getElementById('navLinks');

    function closeNav() {
        if (nav) nav.classList.remove('nav-active');
        if (burger) {
            burger.classList.remove('toggle');
            burger.setAttribute('aria-expanded', 'false');
        }
    }

    if (burger && nav) {
        burger.addEventListener('click', function () {
            nav.classList.toggle('nav-active');
            burger.classList.toggle('toggle');

            // Update ARIA state
            var expanded = burger.getAttribute('aria-expanded') === 'true';
            burger.setAttribute('aria-expanded', String(!expanded));
        });

        // Close button inside mobile nav
        var navCloseBtn = document.getElementById('navCloseBtn');
        if (navCloseBtn) {
            navCloseBtn.addEventListener('click', closeNav);
        }

        // Mobile dropdown toggle
        var dropdownParents = nav.querySelectorAll('.has-dropdown');
        dropdownParents.forEach(function (item) {
            var link = item.querySelector('a');
            if (link && window.innerWidth <= 1025) {
                link.addEventListener('click', function (e) {
                    if (window.innerWidth <= 1025) {
                        var dropdown = item.querySelector('.dropdown-menu');
                        if (dropdown) {
                            e.preventDefault();
                            dropdown.classList.toggle('mobile-open');
                        }
                    }
                });
            }
        });
    }

    // Re-attach mobile dropdown on resize
    window.addEventListener('resize', function () {
        var dropdownParents = document.querySelectorAll('.has-dropdown');
        dropdownParents.forEach(function (item) {
            var dropdown = item.querySelector('.dropdown-menu');
            if (dropdown && window.innerWidth > 1025) {
                dropdown.classList.remove('mobile-open');
            }
        });
    });

    /* ================================================
       3. Close mobile menu on link click
       ================================================ */
    var navLinks = document.querySelectorAll('.nav-links a');
    navLinks.forEach(function (link) {
        link.addEventListener('click', function () {
            // Close mobile menu if open (for non-dropdown links)
            if (nav && nav.classList.contains('nav-active') && !this.parentElement.classList.contains('has-dropdown')) {
                nav.classList.remove('nav-active');
                if (burger) {
                    burger.classList.remove('toggle');
                    burger.setAttribute('aria-expanded', 'false');
                }
            }
        });
    });

    /* ================================================
       4. Tab Switching (Event Delegation)
       ================================================ */
    document.addEventListener('click', function (e) {
        var btn = e.target.closest('.tab-btn');
        if (!btn) return;

        var targetTab = btn.getAttribute('data-tab');
        var parentSection = btn.closest('section');
        if (!parentSection) return;

        // Deactivate all tabs and contents in this section
        parentSection.querySelectorAll('.tab-btn').forEach(function (b) {
            b.classList.remove('active');
        });
        parentSection.querySelectorAll('.tab-content').forEach(function (c) {
            c.classList.remove('active');
        });

        // Activate clicked tab
        btn.classList.add('active');
        var targetContent = document.getElementById(targetTab);
        if (targetContent) {
            targetContent.classList.add('active');
        }
    });

    /* ================================================
       5. Swiper Initializations
       ================================================ */

    // Shared config for program swipers
    var programSwiperConfig = {
        slidesPerView: 2,
        spaceBetween: 20,
        loop: true,
        autoplay: {
            delay: 4000,
            disableOnInteraction: false
        },
        breakpoints: {
            320: { slidesPerView: 1, spaceBetween: 15 },
            768: { slidesPerView: 2, spaceBetween: 20 }
        }
    };

    // Helper: create a program swiper with scoped nav/pagination
    function initProgramSwiper(selector) {
        var el = document.querySelector(selector);
        if (!el) return null;

        return new Swiper(selector, Object.assign({}, programSwiperConfig, {
            navigation: {
                nextEl: selector + ' .swiper-button-next',
                prevEl: selector + ' .swiper-button-prev'
            },
            pagination: {
                el: selector + ' .swiper-pagination',
                clickable: true
            }
        }));
    }

    // Gallery Swiper (different config)
    if (document.querySelector('.gallery-swiper')) {
        new Swiper('.gallery-swiper', {
            slidesPerView: 1,
            spaceBetween: 30,
            loop: true,
            autoplay: {
                delay: 3000,
                disableOnInteraction: false
            },
            pagination: {
                el: '.gallery-swiper .swiper-pagination',
                clickable: true
            },
            navigation: {
                nextEl: '.gallery-swiper .swiper-button-next',
                prevEl: '.gallery-swiper .swiper-button-prev'
            },
            breakpoints: {
                640: { slidesPerView: 2, spaceBetween: 20 },
                768: { slidesPerView: 2, spaceBetween: 30 },
                1024: { slidesPerView: 3, spaceBetween: 30 }
            }
        });
    }

    // Program tab swipers
    initProgramSwiper('.basic-swiper');
    initProgramSwiper('.story-swiper');
    initProgramSwiper('.special-swiper');
    initProgramSwiper('.action-swiper');
    initProgramSwiper('.act-swiper');

    /* ================================================
       6. Notice Ticker
       ================================================ */
    var tickerItems = document.querySelectorAll('.ticker-item');
    if (tickerItems.length > 1) {
        var tickerIndex = 0;
        setInterval(function () {
            tickerItems[tickerIndex].classList.remove('active');
            tickerIndex = (tickerIndex + 1) % tickerItems.length;
            tickerItems[tickerIndex].classList.add('active');
        }, 4000);
    }

    /* ================================================
       7. Popup Handling
       ================================================ */
    function getCookie(name) {
        var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        return match ? match[2] : null;
    }

    function setCookie(name, value, days) {
        var d = new Date();
        d.setTime(d.getTime() + (days * 24 * 60 * 60 * 1000));
        document.cookie = name + '=' + value + ';expires=' + d.toUTCString() + ';path=/';
    }

    // Show active popups that haven't been hidden today
    var popupOverlays = document.querySelectorAll('.popup-overlay');
    popupOverlays.forEach(function (overlay) {
        var popupId = overlay.getAttribute('data-popup-id');
        var cookieName = 'popup_hide_' + popupId;
        if (!getCookie(cookieName)) {
            overlay.classList.add('active');
        }
    });

    // Close popup when clicking overlay background
    popupOverlays.forEach(function (overlay) {
        overlay.addEventListener('click', function (e) {
            if (e.target === overlay) {
                overlay.classList.remove('active');
            }
        });
    });

    // Global functions for popup buttons
    window.closePopup = function (id) {
        var overlay = document.getElementById('popup-' + id);
        if (overlay) {
            overlay.classList.remove('active');
        }
    };

    window.hidePopupToday = function (id) {
        setCookie('popup_hide_' + id, '1', 1);
        var overlay = document.getElementById('popup-' + id);
        if (overlay) {
            overlay.classList.remove('active');
        }
    };

    /* ================================================
       8. Scroll Reveal Animations
       ================================================ */
    // Auto-tag elements for reveal
    var revealSelectors = [
        '.content-section h2',
        '.menu-box',
        '.program-card',
        '.gallery-card',
        '.teacher-card',
        '.highlight-card',
        '.notice-list-item',
        '.event-item',
        '.meal-table',
        '.page-header-banner',
        '.about-feature',
        '.trust-strip',
    ];

    revealSelectors.forEach(function (sel) {
        document.querySelectorAll(sel).forEach(function (el) {
            if (!el.classList.contains('reveal')) {
                el.classList.add('reveal');
            }
        });
    });

    // IntersectionObserver for reveal
    var revealElements = document.querySelectorAll('.reveal');
    if (revealElements.length > 0 && 'IntersectionObserver' in window) {
        var revealObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

        revealElements.forEach(function (el) {
            revealObserver.observe(el);
        });
    } else {
        // Fallback: show all
        revealElements.forEach(function (el) {
            el.classList.add('visible');
        });
    }

    /* ================================================
       9. Header Scroll Effect
       ================================================ */
    var header = document.querySelector('.site-header');
    if (header) {
        var lastScroll = 0;
        window.addEventListener('scroll', function () {
            var scrollY = window.scrollY;
            if (scrollY > 60) {
                header.classList.add('header-scrolled');
            } else {
                header.classList.remove('header-scrolled');
            }
            lastScroll = scrollY;
        }, { passive: true });
    }

});
