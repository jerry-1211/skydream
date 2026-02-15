/**
 * Enhanced Hero Slider
 * - Keyboard navigation (arrow keys)
 * - Pause on hover
 * - ARIA live region updates
 */
(function() {
    'use strict';

    var heroSection = document.getElementById('hero');
    if (!heroSection) return;

    var slider = heroSection.querySelector('.hero-slider');
    if (!slider) return;

    var autoplayInterval;
    var AUTOPLAY_DELAY = 5000;

    function startAutoplay() {
        stopAutoplay();
        autoplayInterval = setInterval(function() {
            if (window.changeSlide) window.changeSlide(1);
        }, AUTOPLAY_DELAY);
    }

    function stopAutoplay() {
        if (autoplayInterval) {
            clearInterval(autoplayInterval);
            autoplayInterval = null;
        }
    }

    // Pause on hover
    slider.addEventListener('mouseenter', stopAutoplay);
    slider.addEventListener('mouseleave', startAutoplay);

    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        // Only when hero is visible in viewport
        var rect = heroSection.getBoundingClientRect();
        if (rect.bottom < 0 || rect.top > window.innerHeight) return;

        if (e.key === 'ArrowLeft' && window.changeSlide) {
            window.changeSlide(-1);
            stopAutoplay();
            startAutoplay();
        } else if (e.key === 'ArrowRight' && window.changeSlide) {
            window.changeSlide(1);
            stopAutoplay();
            startAutoplay();
        }
    });

    // Start autoplay (centralized here instead of main.js)
    startAutoplay();
})();
