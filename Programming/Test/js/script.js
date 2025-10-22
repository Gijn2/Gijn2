// --------------------------------------
// 1. 공통 유틸리티 함수
// --------------------------------------

/**
 * 메인 페이지 카테고리 블록 및 상단 내비게이션의 미개방 메뉴 클릭 시 경고
 * disabled-card 클래스가 있는 요소나 dropdown-item을 클릭했을 때 링크 이동을 막고 경고/메뉴 닫기 처리
 */
function handleCategoryClick(event) {
    const element = event.currentTarget;

    // disabled-card 또는 dropdown-item을 클릭한 경우
    if (element.classList.contains('disabled-card') || element.classList.contains('dropdown-item')) {
        event.preventDefault(); 

        // 드롭다운 항목 클릭 시 메뉴 닫기
        if (element.classList.contains('dropdown-item')) {
             // closest()와 optional chaining(?.)을 사용하여 안전하게 메뉴 찾기
             const menu = element.closest('.dropdown')?.querySelector('.dropdown-menu');
             if (menu) { menu.classList.remove('show'); }
        }

        // disabled-card 클릭 시 alert 띄우기
        if (element.classList.contains('disabled-card')) {
            alert("해당 기록은 현재 접근이 제한되어 있습니다. (Access Restricted)");
        }
        return false;
    }
    // 일반 링크 이동 허용
    return true;
}

/**
 * 미설정된 지도 영역 클릭 시 페이지 이동을 막고 경고 메시지를 표시
 */
function handleAreaClick(event) {
    event.preventDefault(); // 기본 링크 이동 방지
    const regionName = event.target.getAttribute('data-region') || "미개척 영역";
    
    // area shape="default"를 클릭했을 경우
    if (event.target.getAttribute('shape') === 'default') {
        alert(`[${regionName}]: 현재 이 지역은 이그니스 기록이 미흡하여 접근할 수 없습니다. 불의 영역 (세계관 정보)을 클릭해주세요.`);
        return false;
    }
    return true; 
}

/**
 * 드롭다운 메뉴 토글 기능 설정
 */
function setupDropdownToggle() {
    const dropdowns = document.querySelectorAll('.dropdown');

    dropdowns.forEach(dropdown => {
        const toggle = dropdown.querySelector('.dropdown-toggle');
        const menu = dropdown.querySelector('.dropdown-menu');

        if (!toggle || !menu) return;

        toggle.addEventListener('click', (e) => {
            e.preventDefault(); 
            e.stopPropagation(); 

            // 다른 드롭다운 메뉴 닫기
            document.querySelectorAll('.dropdown-menu.show').forEach(openMenu => {
                if (openMenu !== menu) {
                    openMenu.classList.remove('show');
                }
            });

            menu.classList.toggle('show');
        });
    });
    
    // 외부 클릭 시 드롭다운 닫기
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown-menu.show').forEach(openMenu => {
                openMenu.classList.remove('show');
            });
        }
    });
}


// --------------------------------------
// 2. 고급 로딩 화면 연출 함수 (index.html 전용)
// --------------------------------------

const loadingSteps = [
    { width: '25%', text: 'Verifying Archive Credentials...', duration: 800 },
    { width: '55%', text: 'Establishing Secure Data Link...', duration: 1000 },
    { width: '85%', text: 'Processing Fragmented Data...', duration: 1200 },
    { width: '100%', text: 'Access Granted. Entering Pangea...', duration: 1000 }
];

// 무지개 및 주황색 계열의 다양한 색상 배열 (RGBA)
const fragmentColors = [
    'rgba(255, 87, 34, 0.6)',  // Orange
    'rgba(255, 179, 0, 0.6)',  // Yellow
    'rgba(139, 195, 74, 0.6)', // Light Green
    'rgba(3, 169, 244, 0.6)',  // Light Blue
    'rgba(63, 81, 181, 0.6)',  // Indigo
    'rgba(156, 39, 176, 0.6)', // Purple
    'rgba(244, 67, 54, 0.6)',  // Red
    'rgba(0, 150, 136, 0.6)'   // Teal/Cyan
];

/**
 * 로고 텍스트에 CSS 애니메이션을 일회성으로 트리거하여 반짝이는 효과를 부여합니다.
 */
function triggerLogoFlash(logoElement) {
    // flash-glow 클래스를 추가하여 CSS 애니메이션 시작
    logoElement.classList.add('flash-glow');
    
    // 0.3초 후 클래스를 제거하여 애니메이션을 리셋하고 다음 트리거를 준비
    setTimeout(() => {
        logoElement.classList.remove('flash-glow');
    }, 300); 
}

// 데이터 조각을 로고 중앙으로 수렴시키는 함수
function startConvergence(fragment, loaderLogo) {
    const logoRect = loaderLogo.getBoundingClientRect();
    // 로고 중앙 주변의 랜덤 위치 계산
    const targetX = logoRect.left + logoRect.width / 2 + (Math.random() - 0.5) * 50;
    const targetY = logoRect.top + logoRect.height / 2 + (Math.random() - 0.5) * 20;
    
    // 이동 (Translate) 적용 및 페이드 아웃
    fragment.style.transform = `translate(${targetX - fragment.offsetLeft}px, ${targetY - fragment.offsetTop}px)`;
    fragment.style.opacity = '0';
}

// 데이터 조각을 생성하고 분산시키는 함수
function createFragments(loaderLogo, fragmentWrapper) {
    const fragmentCount = 100;
    const logoText = loaderLogo.textContent;
    const characters = logoText.split('');

    for (let i = 0; i < fragmentCount; i++) {
        const fragment = document.createElement('span');
        fragment.classList.add('data-fragment');
        
        // 조각 텍스트 할당 (로고 문자 또는 랜덤 ASCII 문자)
        const randomChar = characters[Math.floor(Math.random() * characters.length)];
        fragment.textContent = Math.random() < 0.8 ? randomChar : String.fromCharCode(48 + Math.floor(Math.random() * 75));
        
        // 랜덤 색상 할당
        fragment.style.color = fragmentColors[Math.floor(Math.random() * fragmentColors.length)];
        
        // 초기 랜덤 위치 설정
        const startX = Math.random() * window.innerWidth;
        const startY = Math.random() * window.innerHeight;
        
        fragment.style.left = `${startX}px`;
        fragment.style.top = `${startY}px`;
        fragment.style.opacity = '1';
        
        fragmentWrapper.appendChild(fragment);
        
        // 0.5초 후 수렴 애니메이션 시작
        setTimeout(() => {
            startConvergence(fragment, loaderLogo);
        }, 500);
    }
}

/**
 * 단계별 로딩 시퀀스를 시작하는 함수 (loaderLogo 인자 추가 및 반짝임 로직 삽입)
 */
function startLoadingSequence(progressBar, statusText, totalLoadingTime, loadingScreen, mainContent, loaderLogo) {
    let currentStep = 0;
    
    function processStep() {
        if (currentStep < loadingSteps.length) {
            const step = loadingSteps[currentStep];
            
            progressBar.style.width = step.width;
            statusText.textContent = step.text;
            
            // ✨ 2회 반짝임 트리거 로직 추가 ✨
            // currentStep 1: 2단계 시작 시점
            // currentStep 3: 4단계 시작 시점
            if (currentStep === 1 || currentStep === 3) {
                triggerLogoFlash(loaderLogo);
            }
            
            setTimeout(() => {
                currentStep++;
                processStep();
            }, step.duration);
        }
    }

    processStep(); // 시퀀스 시작

    // 총 로딩 시간 후 메인 콘텐츠 표시
    setTimeout(() => {
        loadingScreen.style.opacity = '0';
        setTimeout(() => {
            loadingScreen.style.display = 'none';
            mainContent.style.display = 'block';
            mainContent.classList.add('loaded');
        }, 500); // 로딩 화면 CSS transition 시간
    }, totalLoadingTime); 
}


// --------------------------------------
// 3. 메인 페이지 (index.html) 전용 함수
// --------------------------------------

/**
 * ARCHIVE CATEGORIES 캐러셀 슬라이드 기능 설정
 */
function setupCategoryCarousel() {
    const carousel = document.getElementById('category-carousel');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const scrollAmount = 330; // 카드 너비(300px) + 갭(30px)

    if (!carousel || !prevBtn || !nextBtn) return;
    
    prevBtn.addEventListener('click', () => {
        carousel.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    });
    nextBtn.addEventListener('click', () => {
        carousel.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    });
    
    // 버튼 활성화/비활성화 상태 업데이트
    const updateButtons = () => {
        prevBtn.style.opacity = carousel.scrollLeft < 10 ? '0.3' : '1'; 
        const maxScroll = carousel.scrollWidth - carousel.clientWidth;
        nextBtn.style.opacity = carousel.scrollLeft > maxScroll - 10 ? '0.3' : '1';
    };
    
    updateButtons();
    carousel.addEventListener('scroll', updateButtons);
    window.addEventListener('resize', updateButtons);
}

/**
 * 이미지 맵 하이라이트 설정
 */
function createAreaHighlights() {
    const mapImage = document.querySelector('.korea-map-image');
    const overlayContainer = document.getElementById('map-overlay-container');
    const infoBox = document.getElementById('map-info-box');
    
    if (!mapImage || !overlayContainer || !mapImage.complete) {
        return; 
    }

    overlayContainer.innerHTML = '';
    const originalWidth = 800; 
    const currentWidth = mapImage.offsetWidth;
    const currentHeight = mapImage.offsetHeight;
    const scale = currentWidth / originalWidth; 

    const mapArea = document.querySelector('#pangaeaMap area[data-region-id="gangwon"]');

    if (mapArea && mapArea.shape.toLowerCase() === 'poly') {
        const coords = mapArea.coords.split(',').map(c => parseInt(c.trim()));
        
        const polyPoints = [];
        for (let i = 0; i < coords.length; i += 2) {
            const scaledX = coords[i] * scale;
            const scaledY = coords[i + 1] * scale;
            polyPoints.push(`${(scaledX / currentWidth) * 100}% ${(scaledY / currentHeight) * 100}%`);
        }
        
        const clipPathValue = `polygon(${polyPoints.join(',')})`;

        const highlightDiv = document.createElement('div');
        highlightDiv.className = 'clickable-highlight';
        
        highlightDiv.style.clipPath = clipPathValue;
        highlightDiv.style.webkitClipPath = clipPathValue;
        
        highlightDiv.onclick = () => window.location.href = mapArea.href;
        highlightDiv.setAttribute('title', mapArea.alt);
        
        const regionName = mapArea.getAttribute('data-region');

        highlightDiv.addEventListener('mouseover', (e) => {
            highlightDiv.style.backgroundColor = 'rgba(255, 87, 34, 0.7)';
            highlightDiv.style.cursor = 'pointer';
            if (infoBox) {
                infoBox.textContent = regionName;
                infoBox.style.opacity = 1;
            }
        });
        
        highlightDiv.addEventListener('mouseout', () => {
            highlightDiv.style.backgroundColor = 'rgba(255, 87, 34, 0.4)';
            if (infoBox) {
                infoBox.style.opacity = 0;
            }
        });

        overlayContainer.appendChild(highlightDiv);
    }
}


// --------------------------------------
// 4. 세계관 상세 페이지 (lore.html) 전용 함수 및 공통 컴포넌트
// --------------------------------------

/**
 * 로어 로그 툴팁 설정
 */
function setupLoreTooltips() {
    const logs = document.querySelectorAll('.lore-log');
    
    logs.forEach(log => {
        const logContent = log.getAttribute('data-log');
        
        const tooltip = document.createElement('div');
        tooltip.className = 'lore-tooltip';
        tooltip.innerHTML = `<span>[금지된 기록 파편]</span>${logContent}`;
        
        log.appendChild(tooltip);
        
        log.addEventListener('click', (e) => {
            e.stopPropagation();
            
            // 다른 툴팁 닫기
            document.querySelectorAll('.lore-log .lore-tooltip').forEach(t => {
                if (t !== tooltip) {
                    t.style.opacity = 0;
                }
            });
            
            // 현재 툴팁 토글
            tooltip.style.opacity = tooltip.style.opacity === '1' ? '0' : '1';
        });
    });
    
    // 외부 클릭 시 모든 툴팁 닫기
    document.addEventListener('click', () => {
        document.querySelectorAll('.lore-log .lore-tooltip').forEach(t => t.style.opacity = 0);
    });
}

/**
 * Hero Section 캐러셀 설정 (lore.html 상단. 이제 비디오 배경만 처리합니다.)
 */
function setupHeroCarousel() {
    const heroCarousel = document.getElementById('hero-carousel');
    const heroVideo = heroCarousel ? heroCarousel.querySelector('.hero-video') : null;

    if (!heroVideo) return;

    // 비디오가 배경 역할을 하므로 항상 재생되도록 보장
    heroVideo.play();
    
    // 이미지 슬라이드를 제거했으므로, 이 섹션의 제어 버튼(prev-btn, next-btn)은 이제 기능하지 않습니다.
}


/**
 * 이미지 슬라이드 캐러셀 설정 (컨셉 아트 캐러셀처럼 재사용 가능한 일반 이미지 캐러셀)
 * @param {string} carouselId - 캐러셀 컨테이너의 ID (예: 'concept-art-carousel')
 * @param {string} slideClass - 슬라이드 항목의 클래스 이름 (예: 'image-slide')
 * @param {string} prevBtnId - 이전 버튼의 ID (예: 'art-prev-btn')
 * @param {string} nextBtnId - 다음 버튼의 ID (예: 'art-next-btn')
 */
function setupImageCarousel(carouselId, slideClass, prevBtnId, nextBtnId) {
    const slides = document.querySelectorAll(`#${carouselId} .${slideClass}`); 
    const nextBtn = document.getElementById(nextBtnId);
    const prevBtn = document.getElementById(prevBtnId);

    // 슬라이드가 1개 이하이거나 버튼이 없으면 기능 비활성화
    if (slides.length <= 1 || !nextBtn || !prevBtn) return; 

    let currentSlide = 0;

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.remove('active');
            
            if (i === index) {
                slide.classList.add('active');
            }
        });
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    }

    function prevSlide() {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(currentSlide);
    }

    showSlide(currentSlide);
    nextBtn.addEventListener('click', nextSlide);
    prevBtn.addEventListener('click', prevSlide);
}


/**
 * 목차(Table of Contents) 항목 클릭 시 해당 섹션으로 부드럽게 스크롤
 * @param {Event} event - 클릭 이벤트 객체
 */
function handleTocScroll(event) {
    event.preventDefault(); // 기본 앵커 이동 방지

    const targetId = event.currentTarget.getAttribute('href');
    const targetElement = document.querySelector(targetId);

    if (targetElement) {
        const headerHeight = document.querySelector('.minimal-header').offsetHeight || 70; // 헤더 높이

        // 부드러운 스크롤 실행
        window.scrollTo({
            top: targetElement.offsetTop - headerHeight - 20, // 헤더 높이 + 여백만큼 위에서 멈춤
            behavior: 'smooth'
        });
    }
}

/**
 * 목차 기능 설정 (이벤트 리스너 연결)
 */
function setupTableOfContents() {
    const tocLinks = document.querySelectorAll('#toc-list a');
    tocLinks.forEach(link => {
        link.addEventListener('click', handleTocScroll);
    });
}

/**
 * 미디어 (YouTube) 캐러셀 설정 (lore.html 하단 전용)
 */
function setupMediaCarousel() {
    const slides = document.querySelectorAll('#media-carousel .media-slide'); 
    const nextBtn = document.getElementById('media-next-btn');
    const prevBtn = document.getElementById('media-prev-btn');

    if (slides.length === 0 || !nextBtn || !prevBtn) return; 

    let currentSlide = 0;
    
    // 비디오 URL의 원본 SRC를 저장해 둡니다. (iframe 제어용)
    const originalSrcs = Array.from(slides).map(slide => {
        const iframe = slide.querySelector('iframe');
        return iframe ? iframe.getAttribute('src') : null;
    });

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.remove('active');
            slide.style.display = 'none'; // DOM 레벨에서 숨김
            
            const iframe = slide.querySelector('iframe');
            if (!iframe) return;

            if (i === index) {
                // 활성화: 원래 SRC 복원 및 표시 (비디오 재생 준비)
                iframe.setAttribute('src', originalSrcs[i]);
                slide.classList.add('active');
                slide.style.display = 'block';
            } else {
                // 비활성화: SRC를 지워 비디오 재생 중지 (오디오 중복 방지)
                iframe.setAttribute('src', ''); 
            }
        });
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    }

    function prevSlide() {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(currentSlide);
    }

    showSlide(currentSlide);
    nextBtn.addEventListener('click', nextSlide);
    prevBtn.addEventListener('click', prevSlide);
}


// --------------------------------------
// 5. DOM 로드 및 함수 실행
// --------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    
    setupDropdownToggle(); 

    // 전역 함수로 등록 (HTML에서 onclick="handleAreaClick" 형태로 사용)
    window.handleAreaClick = handleAreaClick;
    window.handleCategoryClick = handleCategoryClick; 

    // 메인 페이지 (index.html) 로직
    if (document.title.includes('IGNIS ARCHIVE: 불의 영역 기록 보관소')) { 
        
        // 로딩 화면 요소 정의
        const loadingScreen = document.getElementById('loading-screen');
        const progressBar = document.getElementById('progress-bar');
        const mainContent = document.getElementById('main-content');
        const loaderLogo = document.getElementById('loader-logo');
        const fragmentWrapper = document.getElementById('data-fragments');
        const statusText = document.getElementById('loading-status-text');

        // 로딩 시간 계산 및 시퀀스 시작
        const totalLoadingTime = loadingSteps.reduce((sum, step) => sum + step.duration, 0) + 500; 
        // loaderLogo를 인자로 전달하여 반짝임 함수에서 사용할 수 있도록 함
        startLoadingSequence(progressBar, statusText, totalLoadingTime, loadingScreen, mainContent, loaderLogo);
        
        // 데이터 조각 생성 및 수렴 시작
        setTimeout(() => createFragments(loaderLogo, fragmentWrapper), 200);

        // 지도 하이라이트 설정
        if (document.getElementById('pangaeaMap')) {
             createAreaHighlights();
             window.addEventListener('resize', createAreaHighlights);
        }

        // ARCHIVE CATEGORIES 캐러셀 설정
        setupCategoryCarousel();
    }

    // 세계관 상세 페이지 (lore.html) 전용 로직
    if (document.querySelector('.ignis-container')) {
        setupLoreTooltips();
        setupHeroCarousel(); // 상단 Hero Carousel (비디오 배경만)
        setupTableOfContents(); // 목차 스크롤 기능
        setupMediaCarousel(); // 하단 YouTube 미디어 캐러셀 
        
        // 🚀 새로운 컨셉 아트 캐러셀 추가 (재사용 함수 사용)
        setupImageCarousel('concept-art-carousel', 'image-slide', 'art-prev-btn', 'art-next-btn'); 
    }
});