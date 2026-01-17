// 모바일 기기 여부 확인
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

if (isMobile) {
    document.body.classList.add('mobile-view');
    // 모바일 전용 로직 (예: 지도를 터치 슬라이드로 변경)
}

function openLore(sector) {
    // 게임 내 알림창(SweetAlert 같은 느낌)이나 사이드바를 여는 로직
    alert(`[SYSTEM] Accessing Lore: ${sector}\nConnecting to Database...`);
}

// 로그 애니메이션 효과
const logs = document.querySelectorAll('.log-entry');
logs.forEach((log, index) => {
    setTimeout(() => {
        log.style.opacity = '1';
        log.style.transform = 'translateX(0)';
    }, index * 500);
});