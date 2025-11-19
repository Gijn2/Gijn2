// mainScript.js - 공통 유틸리티 및 index.html 전용 기능 통합
// --------------------------------------
// 1. 공통 유틸리티 함수
// --------------------------------------

function handleCategoryClick(event) {
    const element = event.currentTarget;

    if (element.classList.contains('disabled-card') || element.classList.contains('dropdown-item')) {
        event.preventDefault(); 

        // 드롭다운 항목 클릭 시 메뉴 닫기
        if (element.classList.contains('dropdown-item')) {
             const menu = element.closest('.dropdown')?.querySelector('.dropdown-menu');
             if (menu) { menu.classList.remove('show'); }
        }

        // 비활성화된 카드 클릭 시 경고
        if (element.classList.contains('disabled-card')) {
            alert("해당 기록은 현재 접근이 제한되어 있습니다. (Access Restricted)");
        }
        return false;
    }
    return true;
}

function setupDropdownToggle() {
    const dropdowns = document.querySelectorAll('.dropdown');

    dropdowns.forEach(dropdown => {
        const toggle = dropdown.querySelector('.dropdown-toggle');
        const menu = dropdown.querySelector('.dropdown-menu');

        if (!toggle || !menu) return;

        toggle.addEventListener('click', (e) => {
            e.preventDefault(); 
            e.stopPropagation(); 

            // 다른 열린 메뉴 닫기
            document.querySelectorAll('.dropdown-menu.show').forEach(openMenu => {
                if (openMenu !== menu) {
                    openMenu.classList.remove('show');
                }
            });

            menu.classList.toggle('show');
        });
    });
    
    // 문서 클릭 시 모든 드롭다운 메뉴 닫기
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown-menu.show').forEach(openMenu => {
                openMenu.classList.remove('show');
            });
        }
    });
}


// --------------------------------------
// 2. Index 페이지 전용 - 고급 로딩 화면 연출 함수
// --------------------------------------

const loadingSteps = [
    { width: '25%', text: 'Verifying Archive Credentials...', duration: 800 },
    { width: '55%', text: 'Establishing Secure Data Link...', duration: 1000 },
    { width: '85%', text: 'Processing Fragmented Data...', duration: 1200 },
    { width: '100%', text: 'Access Granted. Entering Pangea...', duration: 1000 }
];

const fragmentColors = [
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

function createAndConvergeFragment(loaderLogo, fragmentWrapper, characters, fragmentColors) {
    const fragment = document.createElement('span');
    fragment.classList.add('data-fragment');
    
    const randomChar = characters[Math.floor(Math.random() * characters.length)];
    fragment.textContent = Math.random() < 0.8 ? randomChar : String.fromCharCode(48 + Math.floor(Math.random() * 75));
    fragment.style.color = fragmentColors[Math.floor(Math.random() * fragmentColors.length)];
    
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
                    createAndConvergeFragment(loaderLogo, fragmentWrapper, characters, fragmentColors);
                 }, i * 5); 
            }
        }, 500 + delay);
    }
    
    const remainingFragments = fragmentCount % blinkCycleCount;
    for (let i = 0; i < remainingFragments; i++) {
        setTimeout(() => {
            createAndConvergeFragment(loaderLogo, fragmentWrapper, characters, fragmentColors);
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
            // 로딩 완료 후 전환
            loadingScreen.style.opacity = '0';
            
            setTimeout(() => {
                loadingScreen.style.display = 'none';
                mainContent.style.display = 'block';
                
                // 메인 콘텐츠 표시 후 부드럽게 나타나게 함
                setTimeout(() => {
                    mainContent.classList.add('loaded');
                }, 50);
                
            }, 500); // 로딩 화면 opacity 전환 시간과 일치
        }
    }
    
    // 초기 로딩 시작
    processStep(); 
}


// --------------------------------------
// 3. Index 페이지 전용 - ARCHIVE CATEGORY 캐러셀 함수
// --------------------------------------

function setupCategoryCarousel() {
    const container = document.querySelector('.minimal-grid');
    const prevBtn = document.getElementById('category-prev-btn');
    const nextBtn = document.getElementById('category-next-btn');
    if (!container || !prevBtn || !nextBtn) return;

    const cardWidth = 150; 
    const gap = 30;
    const scrollAmount = cardWidth + gap;

    function updateControls() {
        // 스크롤이 시작점(0)이나 끝에 도달했는지 확인 (1px 오차 허용)
        prevBtn.disabled = container.scrollLeft <= 1;
        nextBtn.disabled = container.scrollLeft + container.clientWidth >= container.scrollWidth - 1; 
        
        prevBtn.classList.toggle('disabled', prevBtn.disabled);
        nextBtn.classList.toggle('disabled', nextBtn.disabled);
    }

    nextBtn.addEventListener('click', () => {
        container.scrollBy({ left: scrollAmount * 2, behavior: 'smooth' });
        setTimeout(updateControls, 300); 
    });

    prevBtn.addEventListener('click', () => {
        container.scrollBy({ left: -scrollAmount * 2, behavior: 'smooth' });
        setTimeout(updateControls, 300); 
    });

    container.addEventListener('scroll', updateControls);
    window.addEventListener('resize', updateControls);

    updateControls(); 
}


// --------------------------------------
// 4. Index 페이지 초기화 함수
// --------------------------------------
function initializeIndexPage() {
    if (document.getElementById('loading-screen')) {
        const loadingScreen = document.getElementById('loading-screen');
        const progressBar = document.getElementById('progress-bar');
        const mainContent = document.getElementById('main-content');
        const loaderLogo = document.getElementById('loader-logo');
        const fragmentWrapper = document.getElementById('data-fragments');
        const statusText = document.getElementById('loading-status-text');

        // 로딩 시작
        startLoadingSequence(progressBar, statusText, loadingScreen, mainContent, loaderLogo);
        
        setTimeout(() => createFragments(loaderLogo, fragmentWrapper), 200);

        setupCategoryCarousel(); // ARCHIVE CATEGORIES 캐러셀
    }
}


// --------------------------------------
// 5. 초기화 및 이벤트 리스너 (공통)
// --------------------------------------
window.onload = function() {
    setupDropdownToggle();

    // index.html 전용 기능 초기화
    initializeIndexPage();
    
    // lore.html 전용 스크립트가 로드되었는지 확인 후 호출 (index.html에서는 실행 안 됨)
    if (typeof initializeLorePage === 'function') {
        initializeLorePage();
    }
};