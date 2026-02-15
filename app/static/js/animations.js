/**
 * Scroll-triggered animations using Intersection Observer
 */
(function() {
    'use strict';

    // Elements to animate on scroll
    var animatedElements = document.querySelectorAll(
        '.feature-item, .program-card, .gallery-item, .menu-box, .contact-item, .info-content, .download-container, .intro-text, .intro-image'
    );

    if (!animatedElements.length || !('IntersectionObserver' in window)) return;

    // Add initial hidden state
    animatedElements.forEach(function(el) {
        el.classList.add('scroll-hidden');
    });

    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('scroll-visible');
                entry.target.classList.remove('scroll-hidden');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    animatedElements.forEach(function(el) {
        observer.observe(el);
    });

    // Staggered animations for grids
    var grids = document.querySelectorAll('.features-grid, .menu-grid, .contact-info');
    grids.forEach(function(grid) {
        var children = grid.children;
        for (var i = 0; i < children.length; i++) {
            children[i].style.transitionDelay = (i * 0.1) + 's';
        }
    });
})();
