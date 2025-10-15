// 캐러셀 슬라이드 기능 (ignis.html)
document.addEventListener('DOMContentLoaded', () => {
    const slides = document.querySelectorAll('.slide-image');
    if (slides.length === 0) return; // ignis.html이 아닌 경우 실행 안 함

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

    // 초기 슬라이드 표시
    showSlide(currentSlide);

    // 버튼 이벤트 리스너 할당
    document.getElementById('next-btn').addEventListener('click', nextSlide);
    document.getElementById('prev-btn').addEventListener('click', prevSlide);
    
    // 자동 슬라이드 (선택 사항)
    // setInterval(nextSlide, 5000); 

    // 배경음악 설정 (실제 오디오 파일 경로 필요)
    // const bgm = new Audio('audio/ignis_bgm.mp3');
    // bgm.loop = true;
    // bgm.volume = 0.3; 
    // bgm.play().catch(error => {
    //     console.log('BGM 자동 재생 실패: 사용자의 상호작용 필요', error);
    //     // 사용자에게 재생 버튼을 제공할 수 있습니다.
    // });
});


// 메인 맵 기능 (index.html) - 호버 텍스트 표시 등 추가 가능
// 현재는 CSS만으로 충분합니다.