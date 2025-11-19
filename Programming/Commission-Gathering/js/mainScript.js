// mainScript.js - 공통 유틸리티 및 index.html 전용 기능 통합

// --------------------------------------
// 1. 공통 유틸리티 함수
// --------------------------------------

// 새로운 랜덤 색상 배열 (Hover 효과용)
const randomColors = [
    { color: 'white', shadow: 'rgba(255, 255, 255, 0.5)', bg: 'rgba(255, 255, 255, 0.1)' }, 
    { color: '#FF5722', shadow: 'rgba(255, 87, 34, 0.5)', bg: 'rgba(255, 87, 34, 0.1)' }, 
    { color: '#2196F3', shadow: 'rgba(33, 150, 243, 0.5)', bg: 'rgba(33, 150, 243, 0.1)' }, 
    { color: '#FFEB3B', shadow: 'rgba(255, 235, 59, 0.5)', bg: 'rgba(255, 235, 59, 0.1)' }, 
    { color: '#4CAF50', shadow: 'rgba(76, 175, 80, 0.5)', bg: 'rgba(76, 175, 80, 0.1)' }, 
    { color: '#795548', shadow: 'rgba(121, 85, 72, 0.5)', bg: 'rgba(121, 85, 72, 0.1)' }  
];

function handleCategoryClick(event) {
    const element = event.currentTarget;

    if (element.classList.contains('disabled-card') || element.classList.contains('dropdown-item')) {
        event.preventDefault(); 

        if (element.classList.contains('dropdown-item')) {
             const menu = element.closest('.dropdown')?.querySelector('.dropdown-menu');
             if (menu) { menu.classList.remove('show'); }
        }

        if (element.classList.contains('disabled-card')) {
            alert("해당 기록은 현재 접근이 제한되어 있습니다. (Access Restricted)");
        }
        return false;
    }
    return true;
}

function applyRandomHoverEffect(event) {
    const dropdown = event.currentTarget;
    
    if (event.type === 'mouseenter') {
        const randomColor = randomColors[Math.floor(Math.random() * randomColors.length)];
        
        dropdown.style.setProperty('color', randomColor.color, 'important');
        dropdown.style.setProperty('background-color', randomColor.bg, 'important');
        dropdown.style.setProperty('border-color', randomColor.color, 'important');
        dropdown.style.setProperty('box-shadow', `0 0 8px ${randomColor.shadow}`, 'important');
    } else if (event.type === 'mouseleave') {
        dropdown.style.removeProperty('color');
        dropdown.style.removeProperty('background-color');
        dropdown.style.removeProperty('border-color');
        dropdown.style.removeProperty('box-shadow');
    }
}


function setupDropdownToggle() {
    const dropdowns = document.querySelectorAll('.dropdown');

    dropdowns.forEach(dropdown => {
        const toggle = dropdown.querySelector('.dropdown-toggle');
        const menu = dropdown.querySelector('.dropdown-menu');

        if (!toggle || !menu) return;
        
        dropdown.addEventListener('mouseenter', applyRandomHoverEffect);
        dropdown.addEventListener('mouseleave', applyRandomHoverEffect);
        
        toggle.addEventListener('click', (e) => {
            e.preventDefault(); 
            e.stopPropagation(); 

            document.querySelectorAll('.dropdown-menu.show').forEach(openMenu => {
                if (openMenu !== menu) {
                    openMenu.classList.remove('show');
                }
            });

            menu.classList.toggle('show');
        });
    });
    
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown-menu.show').forEach(openMenu => {
                openMenu.classList.remove('show');
            });
        }
    });
}


// --------------------------------------
// 2. Index 페이지 전용 - 로딩 화면 연출 함수
// --------------------------------------
const loadingSteps = [
    { width: '25%', text: 'Verifying Archive Credentials...', duration: 800 },
    { width: '55%', text: 'Establishing Secure Data Link...', duration: 1000 },
    { width: '85%', text: 'Processing Fragmented Data...', duration: 1200 },
    { width: '100%', text: 'Access Granted. Entering Pangea...', duration: 1000 }
];

const fragmentColorsArray = [
    'rgba(255, 87, 34, 0.6)',
    'rgba(255, 179, 0, 0.6)',
    'rgba(139, 195, 74, 0.6)',
    'rgba(3, 169, 244, 0.6)',
    'rgba(63, 81, 181, 0.6)',
    'rgba(156, 39, 176, 0.6)',
    'rgba(244, 67, 54, 0.6)',
    'rgba(0, 150, 136, 0.6)'
];

function triggerLogoFlash(logoElement) {
    logoElement.classList.add('flash-glow');
    
    setTimeout(() => {
        logoElement.classList.remove('flash-glow');
    }, 300); 
}

function startConvergence(fragment, loaderLogo) {
    const logoRect = loaderLogo.getBoundingClientRect();
    const targetX = logoRect.left + logoRect.width / 2 + (Math.random() - 0.5) * 50;
    const targetY = logoRect.top + logoRect.height / 2 + (Math.random() - 0.5) * 20;
    
    fragment.style.transition = 'transform 0.8s ease-in-out, opacity 0.5s';
    fragment.style.transform = `translate(${targetX - fragment.offsetLeft}px, ${targetY - fragment.offsetTop}px)`;
    fragment.style.opacity = '0';

    setTimeout(() => {
        fragment.remove();
    }, 800); 
}

function createAndConvergeFragment(loaderLogo, fragmentWrapper, characters, colors) {
    const fragment = document.createElement('span');
    fragment.classList.add('data-fragment');
    
    const randomChar = characters[Math.floor(Math.random() * characters.length)];
    fragment.textContent = Math.random() < 0.8 ? randomChar : String.fromCharCode(48 + Math.floor(Math.random() * 75));
    fragment.style.color = colors[Math.floor(Math.random() * colors.length)];
    
    const startX = Math.random() * window.innerWidth;
    const startY = Math.random() * window.innerHeight;
    
    fragment.style.left = `${startX}px`;
    fragment.style.top = `${startY}px`;
    fragment.style.opacity = '1';
    
    fragmentWrapper.appendChild(fragment);
    
    setTimeout(() => {
        startConvergence(fragment, loaderLogo);
    }, 50);
}


function createFragments(loaderLogo, fragmentWrapper) {
    const fragmentCount = 580;
    const logoText = loaderLogo.textContent;
    const characters = logoText.split('');
    const blinkCycleCount = 5; 
    const fragmentsPerCycle = Math.floor(fragmentCount / blinkCycleCount);
    
    for (let cycle = 0; cycle < blinkCycleCount; cycle++) {
        const delay = cycle * 300;
        
        setTimeout(() => {
            for (let i = 0; i < fragmentsPerCycle; i++) {
                 setTimeout(() => {
                    createAndConvergeFragment(loaderLogo, fragmentWrapper, characters, fragmentColorsArray);
                 }, i * 5); 
            }
        }, 500 + delay);
    }
    
    const remainingFragments = fragmentCount % blinkCycleCount;
    for (let i = 0; i < remainingFragments; i++) {
        setTimeout(() => {
            createAndConvergeFragment(loaderLogo, fragmentWrapper, characters, fragmentColorsArray);
        }, 500 + (blinkCycleCount - 1) * 300 + i * 5);
    }
}

function startLoadingSequence(progressBar, statusText, loadingScreen, mainContent, loaderLogo) {
    let currentStep = 0;
    
    function processStep() {
        if (currentStep < loadingSteps.length) {
            const step = loadingSteps[currentStep];
            progressBar.style.width = step.width;
            statusText.textContent = step.text;
            
            if (currentStep === 1 || currentStep === 3) {
                 triggerLogoFlash(loaderLogo); 
            }
            
            currentStep++;
            setTimeout(processStep, step.duration);
        } else {
            loadingScreen.style.opacity = '0';
            
            setTimeout(() => {
                loadingScreen.style.display = 'none';
                mainContent.style.display = 'block';
                
                setTimeout(() => {
                    mainContent.classList.add('loaded');
                }, 50);
                
            }, 500); 
        }
    }
    
    processStep(); 
}


// --------------------------------------
// 3. Index 페이지 전용 - 스크롤 스파이 함수
// --------------------------------------

function setupScrollSpyNav() {
    const scrollContainer = document.getElementById('scroll-container');
    if (!scrollContainer) return; 
    
    const sections = document.querySelectorAll('#scroll-container section[id]');
    const navLinks = document.querySelectorAll('.main-nav .dropdown-toggle');
    const header = document.querySelector('.minimal-header');
    const headerHeight = header.offsetHeight;

    const navMap = [
        ['section-hero', '메인'], 
        ['section-world', '세계관 ▼'],
        ['section-event', '이벤트'],
        ['section-categories', '카테고리'] 
    ];

    const observerOptions = {
        root: scrollContainer,
        rootMargin: `-${headerHeight + 1}px 0px -50% 0px`, 
        threshold: 0 
    };
    
    const sectionInView = {}; 
    sections.forEach(section => sectionInView[section.id] = false);

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            sectionInView[entry.target.id] = entry.isIntersecting;
        });
        
        let determinedActiveId = 'section-hero'; 
        
        for(const [id, text] of navMap) {
            if (sectionInView[id]) {
                determinedActiveId = id;
                break; 
            }
        }
        
        navLinks.forEach(link => link.classList.remove('active'));

        const targetNavText = navMap.find(map => map[0] === determinedActiveId)?.[1];
                
        if (targetNavText) {
            const searchBaseText = targetNavText.includes('▼') ? targetNavText.split(' ')[0] : targetNavText;
            
            const targetLink = Array.from(navLinks).find(link => 
                link.textContent.trim().startsWith(searchBaseText)
            );
                    
            if (targetLink) {
                targetLink.classList.add('active');
            }
        }

    }, observerOptions);

    sections.forEach(section => {
        observer.observe(section);
    });
}


// --------------------------------------
// 4. Index 페이지 전용 - 이벤트 캐러셀 함수 (요구사항 3: 단일 배너 회전)
// --------------------------------------
function setupEventCarousel() {
    const list = document.getElementById('event-slide-list');
    const dotsContainer = document.getElementById('event-carousel-dots');
    if (!list || !dotsContainer) return;

    const items = list.querySelectorAll('.event-slide-item');
    const totalSlides = items.length;
    let currentIndex = 0;
    const slideDuration = 3000; // 3초 간격 자동 회전

    // 1. Dot 생성
    for (let i = 0; i < totalSlides; i++) {
        const dot = document.createElement('span');
        dot.classList.add('dot');
        dot.dataset.index = i;
        dot.addEventListener('click', () => {
            moveToSlide(i);
            // 수동 클릭 시 인터벌 초기화 및 재시작
            clearInterval(rotationInterval);
            rotationInterval = setInterval(autoRotate, slideDuration);
        });
        dotsContainer.appendChild(dot);
    }
    const dots = dotsContainer.querySelectorAll('.dot');
    
    // 2. 슬라이드 및 Dot 업데이트
    function updateDots() {
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === currentIndex);
        });
    }

    function moveToSlide(index) {
        currentIndex = index;
        // 3개의 슬라이드가 list에 100%씩 차지하므로, 전체 300% 중 현재 인덱스만큼 이동
        const offset = -currentIndex * 100 / totalSlides; 
        list.style.transform = `translateX(${offset}%)`;
        updateDots();
    }
    
    // 3. 자동 회전 로직
    function autoRotate() {
        currentIndex = (currentIndex + 1) % totalSlides;
        moveToSlide(currentIndex);
    }

    let rotationInterval = setInterval(autoRotate, slideDuration);
    
    // 4. 초기 설정
    moveToSlide(currentIndex);
    
    // Hover 시 회전 일시 정지
    list.closest('.event-carousel-wrapper').addEventListener('mouseenter', () => {
        clearInterval(rotationInterval);
    });
    list.closest('.event-carousel-wrapper').addEventListener('mouseleave', () => {
        rotationInterval = setInterval(autoRotate, slideDuration);
    });
}


// --------------------------------------
// 5. Index 페이지 전용 - 카테고리 그리드 함수 (요구사항 4: 버튼 제거)
// --------------------------------------
function setupCategoryGrid() {
    // 버튼 제거 및 너비 축소는 CSS에서 처리되었으므로, JS에서는 초기화만 수행합니다.
    const container = document.getElementById('category-grid');
    if (!container) return;
    
    // (선택 사항) 마우스 드래그 스크롤을 활성화하는 로직은 필요에 따라 추가될 수 있습니다.
}


// --------------------------------------
// 6. Index 페이지 초기화 함수
// --------------------------------------
function initializeIndexPage() {
    if (document.getElementById('loading-screen')) {
        const loadingScreen = document.getElementById('loading-screen');
        const progressBar = document.getElementById('progress-bar');
        const mainContent = document.getElementById('main-content');
        const loaderLogo = document.getElementById('loader-logo');
        const fragmentWrapper = document.getElementById('data-fragments');
        const statusText = document.getElementById('loading-status-text');

        startLoadingSequence(progressBar, statusText, loadingScreen, mainContent, loaderLogo);
        
        setTimeout(() => createFragments(loaderLogo, fragmentWrapper), 200);

        setupScrollSpyNav();     
        setupEventCarousel(); 
        setupCategoryGrid(); 
    }
}


// --------------------------------------
// 7. 초기화 및 이벤트 리스너 (공통)
// --------------------------------------
window.onload = function() {
    setupDropdownToggle();

    initializeIndexPage();
    
    if (typeof initializeLorePage === 'function') {
        initializeLorePage();
    }
};