// script.js

// --------------------------------------
// 메인 맵 기능 (index.html)
// --------------------------------------

/**
 * 미설정된 지도 영역 클릭 시 페이지 이동을 막고 경고 메시지를 표시
 */
function handleAreaClick(event) {
    event.preventDefault(); // 기본 링크 이동 방지
    const regionName = event.target.getAttribute('data-region') || "미개척 영역";
    
    // area shape="default"를 클릭했을 경우
    if (event.target.getAttribute('shape') === 'default') {
        alert(`[${regionName}]: 현재 이 지역은 이그니스 기록이 미흡하여 접근할 수 없습니다. 불의 영역 (강원도)을 클릭해주세요.`);
        return false;
    }
    return true; 
}

/**
 * 이미지 맵의 <area> 좌표를 읽어와 다각형 하이라이트 DIV를 생성합니다.
 */
function createAreaHighlights() {
    const mapContainer = document.querySelector('.korea-map-container');
    const mapImage = document.querySelector('.korea-map-image');
    const overlayContainer = document.getElementById('map-overlay-container');
    
    // 필요한 요소가 없으면 종료
    if (!mapImage || !overlayContainer || !mapImage.complete) {
        // 이미지가 로드되지 않았다면 로드 완료 후 다시 시도
        mapImage.onload = createAreaHighlights; 
        return;
    }

    // 이미지 맵의 원본 너비를 800px로 가정합니다. (CSS max-width와 일치)
    const originalWidth = 800; 
    const currentWidth = mapImage.offsetWidth;
    const currentHeight = mapImage.offsetHeight;
    const scale = currentWidth / originalWidth; 

    // 강원도 영역의 area 태그만 선택
    const mapArea = document.querySelector('#pangaeaMap area[data-region-id="gangwon"]');

    if (mapArea && mapArea.shape.toLowerCase() === 'poly') {
        const coords = mapArea.coords.split(',').map(c => parseInt(c.trim()));
        
        const polyPoints = [];
        for (let i = 0; i < coords.length; i += 2) {
            // 원본 좌표를 현재 이미지 크기에 맞게 스케일링
            const scaledX = coords[i] * scale;
            const scaledY = coords[i + 1] * scale;
            
            // 스케일링된 픽셀 좌표를 이미지 전체 너비/높이에 대한 백분율로 변환 (clip-path용)
            polyPoints.push(`${(scaledX / currentWidth) * 100}% ${(scaledY / currentHeight) * 100}%`);
        }
        
        const clipPathValue = `polygon(${polyPoints.join(',')})`;

        const highlightDiv = document.createElement('div');
        highlightDiv.className = 'clickable-highlight';
        
        // clip-path 적용하여 다각형 모양으로 자르기
        highlightDiv.style.clipPath = clipPathValue;
        highlightDiv.style.webkitClipPath = clipPathValue;
        
        // 클릭 이벤트 연결 (area 태그와 동일한 링크로 이동)
        highlightDiv.onclick = () => window.location.href = mapArea.href;
        highlightDiv.setAttribute('title', mapArea.alt);

        // 호버 효과
        highlightDiv.addEventListener('mouseover', () => {
            highlightDiv.style.backgroundColor = 'rgba(255, 87, 34, 0.7)';
            highlightDiv.style.cursor = 'pointer';
        });
        highlightDiv.addEventListener('mouseout', () => {
            highlightDiv.style.backgroundColor = 'rgba(255, 87, 34, 0.4)';
        });

        overlayContainer.appendChild(highlightDiv);
    }
}


// --------------------------------------
// DOM 로드 및 함수 실행
// --------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    
    // 메인 페이지 (index.html) 전용 로직
    if (document.getElementById('pangaeaMap')) {
         window.handleAreaClick = handleAreaClick;
         createAreaHighlights();
         
         // 창 크기가 변경될 때 하이라이트 위치를 재조정 (반응형 대응)
         window.addEventListener('resize', () => {
             const overlayContainer = document.getElementById('map-overlay-container');
             if (overlayContainer) {
                 overlayContainer.innerHTML = '';
             }
             createAreaHighlights();
         });
    }

    // 캐러셀 슬라이드 기능 (ignis.html)
    const slides = document.querySelectorAll('.slide-image');
    const nextBtn = document.getElementById('next-btn');
    const prevBtn = document.getElementById('prev-btn');

    if (slides.length === 0 || !nextBtn || !prevBtn) return; 

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
    
    // (배경음악 로직은 주석 처리되어 있습니다. 필요시 주석 해제 후 파일 경로 확인)
});