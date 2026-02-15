/**
 * main.js - 하늘 꿈나무 어린이집
 * Handles: burger menu, smooth scroll, tabs, hero slider, Swiper carousels
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

    // Auto-advance is handled by hero.js (with pause-on-hover support)

    /* ================================================
       2. Burger Menu
       ================================================ */
    var burger = document.getElementById('burger');
    var nav = document.getElementById('navLinks');

    if (burger && nav) {
        burger.addEventListener('click', function () {
            nav.classList.toggle('nav-active');
            burger.classList.toggle('toggle');

            // Update ARIA state
            var expanded = burger.getAttribute('aria-expanded') === 'true';
            burger.setAttribute('aria-expanded', String(!expanded));
        });
    }

    /* ================================================
       3. Smooth Scroll for Nav Links
       ================================================ */
    var navLinks = document.querySelectorAll('.nav-links a');
    var headerHeight = 80;

    navLinks.forEach(function (link) {
        link.addEventListener('click', function (e) {
            var href = this.getAttribute('href');
            // Only handle anchor links on the same page
            if (!href || href.charAt(0) !== '#') return;

            e.preventDefault();
            var target = document.querySelector(href);

            if (target) {
                var targetPosition = target.offsetTop - headerHeight;
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }

            // Close mobile menu if open
            if (nav && nav.classList.contains('nav-active')) {
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
       5. scrollToSection (used by menu boxes)
       ================================================ */
    window.scrollToSection = function (sectionId, tabId) {
        var section = document.querySelector(sectionId);
        if (!section) return;

        var targetPosition = section.offsetTop - headerHeight;
        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
        });

        if (tabId) {
            setTimeout(function () {
                var tabBtn = document.querySelector('[data-tab="' + tabId + '"]');
                if (tabBtn) tabBtn.click();
            }, 500);
        }
    };

    /* ================================================
       6. switchTab (used by footer links)
       ================================================ */
    window.switchTab = function (tabId) {
        setTimeout(function () {
            var tabBtn = document.querySelector('[data-tab="' + tabId + '"]');
            if (tabBtn) tabBtn.click();
        }, 100);
    };

    /* ================================================
       7. Swiper Initializations
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

});
