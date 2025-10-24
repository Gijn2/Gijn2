document.addEventListener('DOMContentLoaded', () => {
    
    // ================== Nav Link & Scroll Behavior (One-Page) ==================
    const navLinks = document.querySelectorAll('.nav-list a');

    navLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            const targetHref = link.getAttribute('href');
            
            if (targetHref.startsWith('#')) {
                event.preventDefault();

                const id = targetHref.substring(1);
                const targetSection = document.querySelector(`#${id}`);
                
                if (targetSection) {
                    // 고정된 헤더 높이(60px)와 왼쪽 네비게이션으로 인한 오프셋을 고려
                    window.scrollTo({
                        top: targetSection.offsetTop - 70, 
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    // ================== Hero Banner Button Scroll Logic (추가) ==================
    const viewAllWorksBtn = document.querySelector('.hero-banner .cta-button');
    const worksSection = document.getElementById('novels'); 

    if (viewAllWorksBtn && worksSection) {
        viewAllWorksBtn.addEventListener('click', () => {
            window.scrollTo({
                top: worksSection.offsetTop - 70, // 헤더 높이(약 60px)를 고려한 조정값 70px
                behavior: 'smooth'
            });
        });
    }


    // ================== Works Carousel Logic ==================
    const carousel = document.querySelector('.work-carousel');
    const prevBtn = document.querySelector('.carousel-btn.prev');
    const nextBtn = document.querySelector('.carousel-btn.next');
    const dotsContainer = document.querySelector('.carousel-dots');
    
    if (carousel) {
        const groups = document.querySelectorAll('.carousel-item-group');
        let currentSlide = 0;
        const totalSlides = groups.length;

        for (let i = 0; i < totalSlides; i++) {
            const dot = document.createElement('span');
            dot.classList.add('dot');
            if (i === 0) dot.classList.add('active');
            dot.addEventListener('click', () => {
                goToSlide(i);
            });
            dotsContainer.appendChild(dot);
        }

        const dots = document.querySelectorAll('.carousel-dots .dot');

        function updateDots() {
            dots.forEach((dot, index) => {
                dot.classList.toggle('active', index === currentSlide);
            });
        }

        function goToSlide(index) {
            currentSlide = (index + totalSlides) % totalSlides;
            const offset = -currentSlide * 100;
            carousel.style.transform = `translateX(${offset}%)`;
            updateDots();
        }

        prevBtn.addEventListener('click', () => {
            goToSlide(currentSlide - 1);
        });

        nextBtn.addEventListener('click', () => {
            goToSlide(currentSlide + 1);
        });
    }

    // ================== Work Detail Modal Logic ==================
    const workItems = document.querySelectorAll('.work-item');
    const modal = document.getElementById('work-detail-modal');
    const closeBtn = document.querySelector('.close-btn');
    const modalTitle = document.getElementById('modal-work-title');
    const modalGenre = document.getElementById('modal-work-genre');
    const modalImage = document.getElementById('modal-work-image');

    workItems.forEach(item => {
        item.addEventListener('click', () => {
            const title = item.getAttribute('data-title');
            const genre = item.getAttribute('data-genre');
            const workClass = Array.from(item.classList).find(cls => cls !== 'work-item' && !cls.includes('work-item'));

            modalTitle.textContent = title;
            modalGenre.textContent = genre;
            modalImage.style.backgroundImage = `url('../images/placeholder-${workClass}.jpg')`; 
            
            modal.style.display = "block";
        });
    });

    closeBtn.addEventListener('click', () => {
        modal.style.display = "none";
    });

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});