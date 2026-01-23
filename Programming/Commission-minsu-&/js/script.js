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
    const carousel = document.querySelector('.work-carousel:not(.team-carousel)'); // 작품 캐러셀 선택
    const prevBtn = document.querySelector('.carousel-btn.prev:not(.team-prev)');
    const nextBtn = document.querySelector('.carousel-btn.next:not(.team-next)');
    const dotsContainer = document.querySelector('.carousel-dots:not(.team-dots)');
    
    if (carousel) {
        const groups = carousel.querySelectorAll('.carousel-item-group');
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

        const dots = dotsContainer.querySelectorAll('.dot');

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

    // ================== Team Carousel Logic (추가) ==================
    const teamCarousel = document.querySelector('.team-carousel');
    const teamPrevBtn = document.querySelector('.carousel-btn.team-prev');
    const teamNextBtn = document.querySelector('.carousel-btn.team-next');
    const teamDotsContainer = document.querySelector('.carousel-dots.team-dots');

    if (teamCarousel) {
        const teamGroups = teamCarousel.querySelectorAll('.team-item-group');
        let teamCurrentSlide = 0;
        const teamTotalSlides = teamGroups.length;

        // 닷 생성
        for (let i = 0; i < teamTotalSlides; i++) {
            const dot = document.createElement('span');
            dot.classList.add('dot');
            if (i === 0) dot.classList.add('active');
            dot.addEventListener('click', () => {
                goToTeamSlide(i);
            });
            teamDotsContainer.appendChild(dot);
        }

        const teamDots = teamDotsContainer.querySelectorAll('.dot');

        function updateTeamDots() {
            teamDots.forEach((dot, index) => {
                dot.classList.toggle('active', index === teamCurrentSlide);
            });
        }

        function goToTeamSlide(index) {
            teamCurrentSlide = (index + teamTotalSlides) % teamTotalSlides;
            const offset = -teamCurrentSlide * 100;
            teamCarousel.style.transform = `translateX(${offset}%)`;
            updateTeamDots();
        }

        teamPrevBtn.addEventListener('click', () => {
            goToTeamSlide(teamCurrentSlide - 1);
        });

        teamNextBtn.addEventListener('click', () => {
            goToTeamSlide(teamCurrentSlide + 1);
        });
    }


    // ================== Work Detail Modal Logic ==================
    const workItems = document.querySelectorAll('.work-item');
    const modal = document.getElementById('work-detail-modal');
    const closeBtn = document.querySelector('.close-btn');
    const modalTitle = document.getElementById('modal-work-title');
    const modalGenre = document.getElementById('modal-work-genre');
    const modalImage = document.getElementById('modal-work-image');
    const modalDescription = document.getElementById('modal-work-description'); 
    
    // ⭐ 모달 내부의 CTA 버튼 요소를 가져옵니다.
    const ctaButton = modal.querySelector('.cta-button'); 

    workItems.forEach(item => {
        item.addEventListener('click', () => {
            const title = item.getAttribute('data-title');
            const genre = item.getAttribute('data-genre');
            const description = item.getAttribute('data-description'); 

            const backgroundImageStyle = item.style.backgroundImage;
            
            modalTitle.textContent = title;
            modalGenre.textContent = genre;
            modalImage.style.backgroundImage = backgroundImageStyle; 
            modalDescription.textContent = description || "상세 설명이 준비 중입니다."; 
            
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

    // ⭐ 핵심 수정: CTA 버튼 클릭 시 alert 메시지 출력
    if (ctaButton) {
        ctaButton.addEventListener('click', (event) => {
            event.preventDefault(); // 버튼의 기본 동작 방지 (필요하다면)
            
            // alert 메시지 출력
            alert("해당 작품은 현재 연재중이지 않습니다.");
        });
    }
});

    // 프로젝트 페이지로 이동하는 통합 함수 @param {string} projectName - 이동할 프로젝트 식별자
    function navigateToProject(projectName) {
        let targetPath = '';

        // 프로젝트별 경로 설정
        switch (projectName) {
            case 'projectM':
                targetPath = '../project/projectM.html';
                break;
            case 'projectR':
                targetPath = '../project/projectR.html';
                break;
            default:
                console.error("Unknown project:", projectName);
                return;
        }

        // 디버깅을 위해 콘솔에 출력 (도메인에서 경로 오류 시 확인 용도)
        console.log(`Navigating to ${projectName} via path: ${targetPath}`);
        
        // 페이지 이동
        window.location.href = targetPath;
    }