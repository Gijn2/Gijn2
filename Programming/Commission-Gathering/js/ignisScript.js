// IgnisScript.js - lore.html 전용 목차, 툴팁, 미디어 캐러셀 기능
// --------------------------------------
// 1. LORE 페이지 목차 기능 
// --------------------------------------

function setupTableOfContents() {
    const article = document.querySelector('.lore-article');
    const tocList = document.getElementById('toc-list');
    if (!article || !tocList) return;

    // H2와 H3 제목을 모두 목차 항목으로 가져옵니다.
    const headings = article.querySelectorAll('section h2, section h3');
    tocList.innerHTML = ''; 

    headings.forEach(heading => {
        // ID가 없으면 텍스트 기반으로 ID 생성
        const id = heading.id || heading.textContent.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
        heading.id = id;

        const listItem = document.createElement('li');
        const link = document.createElement('a');
        link.href = `#${id}`;
        link.textContent = heading.textContent;
        // H3에 대해 서브 항목 스타일을 적용하기 위한 클래스 추가
        link.classList.add(heading.tagName.toLowerCase()); 

        listItem.appendChild(link);
        tocList.appendChild(listItem);
    });

    // 목차 항목 클릭 시 부드러운 스크롤
    tocList.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                // 상단 헤더 높이와 여백을 고려하여 스크롤 위치 조정
                const headerHeight = document.querySelector('.minimal-header').offsetHeight || 70;
                // 10px 여백 추가
                const offsetTop = targetElement.offsetTop - headerHeight - 10; 
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}


// --------------------------------------
// 2. LORE 페이지 툴팁 기능 (setupLoreTooltips)
// --------------------------------------

function setupLoreTooltips() {
    const logItems = document.querySelectorAll('.lore-log');
    
    logItems.forEach(item => {
        const logText = item.getAttribute('data-log');
        const tooltip = document.createElement('div');
        tooltip.classList.add('lore-tooltip');
        tooltip.textContent = logText;
        item.appendChild(tooltip);

        // 마우스 오버 시 툴팁 표시
        item.addEventListener('mouseover', () => {
             // 다른 열린 툴팁 닫기
            document.querySelectorAll('.lore-log .lore-tooltip').forEach(t => {
                if (t !== tooltip) {
                    t.style.opacity = 0;
                }
            });
            tooltip.style.opacity = 1;
        });
        
        // 마우스 아웃 시 툴팁 숨기기
        item.addEventListener('mouseout', () => {
            tooltip.style.opacity = 0;
        });

        // 클릭 시 고정 토글 (모바일 대비)
        item.addEventListener('click', (e) => {
             e.stopPropagation();
             document.querySelectorAll('.lore-log .lore-tooltip').forEach(t => {
                if (t !== tooltip) {
                    t.style.opacity = 0;
                }
            });
            tooltip.style.opacity = tooltip.style.opacity === '1' ? '0' : '1';
        });
    });
    
    // 문서 클릭 시 모든 툴팁 닫기
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.lore-log')) {
            document.querySelectorAll('.lore-log .lore-tooltip').forEach(t => {
                t.style.opacity = 0;
            });
        }
    });
}

// --------------------------------------
// 3. 미디어 캐러셀 기능 (setupMediaCarousel)
// --------------------------------------

function setupMediaCarousel() {
    const carousel = document.querySelector('.media-carousel-container');
    const slidesContainer = carousel?.querySelector('.media-carousel-slides');
    const slides = slidesContainer ? Array.from(slidesContainer.querySelectorAll('.media-slide')) : [];
    const nextBtn = carousel?.querySelector('#media-next-btn');
    const prevBtn = carousel?.querySelector('#media-prev-btn');

    if (slides.length < 2 || !nextBtn || !prevBtn) {
        // 슬라이드가 2개 미만이면 버튼 숨김
        if (nextBtn) nextBtn.style.display = 'none';
        if (prevBtn) prevBtn.style.display = 'none';
        return; 
    }

    let currentSlide = 0;

    function showSlide(index) {
        if (index >= slides.length) {
            currentSlide = 0;
        } else if (index < 0) {
            currentSlide = slides.length - 1;
        } else {
            currentSlide = index;
        }

        slides.forEach((slide, i) => {
            slide.classList.toggle('active', i === currentSlide);
        });
        
        // 미디어 캐러셀은 무한 루프이므로 버튼은 항상 활성화
        prevBtn.disabled = false;
        nextBtn.disabled = false;
    }

    nextBtn.addEventListener('click', () => showSlide(currentSlide + 1));
    prevBtn.addEventListener('click', () => showSlide(currentSlide - 1));

    showSlide(currentSlide);
}


// --------------------------------------
// 4. LORE 페이지 초기화 함수
// --------------------------------------
function initializeLorePage() {
    if (document.querySelector('.ignis-container')) {
        setupLoreTooltips();
        setupTableOfContents(); 
        setupMediaCarousel();
    }
}

// window.onload에서 호출될 수 있도록 전역에 노출
// initializeLorePage(); // 실제 HTML 파일에 삽입될 때는 이 함수를 window.onload에서 호출해야 합니다.