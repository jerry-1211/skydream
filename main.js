document.addEventListener('DOMContentLoaded', function() {
    // 히어로 슬라이드 기능
    let currentSlide = 0;
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;

    function changeSlide(direction) {
        if (slides.length === 0) return;
        
        slides[currentSlide].classList.remove('active');
        
        currentSlide += direction;
        
        if (currentSlide >= totalSlides) {
            currentSlide = 0;
        }
        if (currentSlide < 0) {
            currentSlide = totalSlides - 1;
        }
        
        slides[currentSlide].classList.add('active');
    }

    // 전역 함수로 등록
    window.changeSlide = changeSlide;

    // 자동 슬라이드
    if (slides.length > 0) {
        setInterval(() => {
            changeSlide(1);
        }, 5000);
    }

    // 갤러리 스와이퍼 초기화
    const gallerySwiper = new Swiper('.gallery-swiper', {
        slidesPerView: 1,
        spaceBetween: 30,
        loop: true,
        autoplay: {
            delay: 3000,
            disableOnInteraction: false,
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        breakpoints: {
            640: {
                slidesPerView: 2,
                spaceBetween: 20,
            },
            768: {
                slidesPerView: 2,
                spaceBetween: 30,
            },
            1024: {
                slidesPerView: 3,
                spaceBetween: 30,
            },
        },
    });

    // 햄버거 메뉴
    const burger = document.getElementById('burger');
    const nav = document.getElementById('navLinks');

    if (burger && nav) {
        burger.addEventListener('click', () => {
            nav.classList.toggle('nav-active');
            burger.classList.toggle('toggle');
        });
    }

    // 부드러운 스크롤
    const navLinks = document.querySelectorAll('.nav-links a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const headerHeight = 80;
                const targetPosition = targetElement.offsetTop - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
            
            if (nav.classList.contains('nav-active')) {
                nav.classList.remove('nav-active');
                burger.classList.remove('toggle');
            }
        });
    });

    // 탭 기능
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            const parentSection = this.closest('section');
            
            if (parentSection) {
                const sectionTabBtns = parentSection.querySelectorAll('.tab-btn');
                const sectionTabContents = parentSection.querySelectorAll('.tab-content');
                
                sectionTabBtns.forEach(btn => btn.classList.remove('active'));
                sectionTabContents.forEach(content => content.classList.remove('active'));
                
                this.classList.add('active');
                const targetContent = document.getElementById(targetTab);
                if (targetContent) {
                    targetContent.classList.add('active');
                }
            }
        });
    });

    // 메뉴 박스 클릭 시 섹션 이동 및 탭 전환
    window.scrollToSection = function(sectionId, tabId = null) {
        const section = document.querySelector(sectionId);
        if (section) {
            const headerHeight = 80;
            const targetPosition = section.offsetTop - headerHeight;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
            
            // 탭이 지정된 경우 해당 탭 활성화
            if (tabId) {
                setTimeout(() => {
                    const tabBtn = document.querySelector(`[data-tab="${tabId}"]`);
                    if (tabBtn) {
                        tabBtn.click();
                    }
                }, 500);
            }
        }
    };

    // 푸터에서 탭 전환 함수
    window.switchTab = function(tabId) {
        setTimeout(() => {
            const tabBtn = document.querySelector(`[data-tab="${tabId}"]`);
            if (tabBtn) {
                tabBtn.click();
            }
        }, 100);
    };
});
