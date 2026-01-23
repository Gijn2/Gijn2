const zoneData = {
    "port": {
        yt: "qP0Hk6H6_yY",
        imgs: ["https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b", "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4"],
        secret: "랑 항구 VIP 구역: 은빛 안개가 짙게 깔리는 밤, 선택받은 자들만의 크루즈 파티가 시작됩니다."
    },
    "land": {
        yt: "v7zn_1_p7gY",
        imgs: ["https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3", "https://images.unsplash.com/photo-1505673542670-a5e3ff5b14a3"],
        secret: "랑 랜드 비밀 구역: 거대한 백호 조각상 아래, 금기된 유희를 즐길 수 있는 지하 클럽이 존재합니다."
    },
    "promenade": {
        yt: "L0X7X8X8x8",
        imgs: ["https://images.unsplash.com/photo-1549490349-8643362247b5", "https://images.unsplash.com/photo-1493306462441-df09240368e7"],
        secret: "갤러리 '무아': 랑이의 실제 목소리와 체온을 느낄 수 있는 초감각 전시가 진행 중입니다."
    },
    "station": {
        yt: "example_id",
        imgs: ["https://images.unsplash.com/photo-1497366216548-37526070297c", "https://images.unsplash.com/photo-1497366811353-6870744d04b2"],
        secret: "랑 스테이션: 왕국의 심장부. 최상위 1%만을 위한 프리미엄 라운지가 위치해 있습니다."
    }
};

const swiper = new Swiper('.swiper', { pagination: { el: '.swiper-pagination' }, autoplay: { delay: 3000 } });
const clickSnd = document.getElementById('snd-click');
const hoverSnd = document.getElementById('snd-hover');
const sidebar = document.getElementById('main-sidebar');
const overlay = document.getElementById('sidebar-overlay');

// 시간대 필터
function applyTimeFilter() {
    const hour = new Date().getHours();
    const ov = document.getElementById('time-overlay');
    if (hour >= 18 || hour <= 6) ov.style.background = "rgba(10, 20, 50, 0.3)";
    else if (hour >= 16) ov.style.background = "rgba(255, 100, 0, 0.1)";
}
applyTimeFilter();

// 마커 이벤트
document.querySelectorAll('.map-node').forEach(node => {
    node.addEventListener('mouseenter', () => { hoverSnd.currentTime = 0; hoverSnd.play(); });
    node.addEventListener('click', function(e) {
        e.stopPropagation();
        clickSnd.currentTime = 0; clickSnd.play();
        
        const id = this.dataset.id;
        const name = this.dataset.name;
        const info = this.dataset.info;
        const isAdult = this.classList.contains('adult-zone');

        document.getElementById('sidebar-title').innerText = name;
        document.getElementById('sidebar-desc').innerText = info;

        if (isAdult && sessionStorage.getItem('rangAdult') !== 'true') {
            document.getElementById('adult-auth-section').style.display = 'block';
            document.getElementById('secret-content').style.display = 'none';
        } else if (isAdult) {
            showContent(id);
        }

        sidebar.classList.add('active');
        overlay.style.display = 'block';
    });
});

// 사이드바 내부 클릭 시 닫힘 방지
sidebar.addEventListener('click', (e) => e.stopPropagation());

function showContent(id) {
    const data = zoneData[id] || zoneData["port"];
    document.getElementById('adult-auth-section').style.display = 'none';
    document.getElementById('secret-content').style.display = 'block';
    document.getElementById('youtube-vid').src = `https://www.youtube.com/embed/${data.yt}?autoplay=1&mute=1`;
    document.getElementById('sidebar-secret-text').innerText = data.secret;
    
    const wrapper = document.getElementById('carousel-wrapper');
    wrapper.innerHTML = data.imgs.map(img => `<div class="swiper-slide"><img src="${img}"></div>`).join('');
    swiper.update();
}

// 닫기 로직
function closeSidebar() {
    sidebar.classList.remove('active');
    overlay.style.display = 'none';
    document.getElementById('youtube-vid').src = "";
}

overlay.addEventListener('click', closeSidebar);
document.querySelector('.close-sidebar').addEventListener('click', closeSidebar);

// 정교한 생년월일 검증
function verifyAgeStrict() {
    const y = parseInt(document.getElementById('auth-year').value);
    const m = parseInt(document.getElementById('auth-month').value);
    const d = parseInt(document.getElementById('auth-day').value);
    
    const inputDate = new Date(y, m - 1, d);
    const today = new Date();
    const isValidDate = inputDate.getFullYear() === y && inputDate.getMonth() === m - 1 && inputDate.getDate() === d;
    
    if (!isValidDate || y < 1920 || y > today.getFullYear()) {
        alert("올바르지 않은 생년월일이니라!"); return;
    }

    if (today.getFullYear() - y >= 19) {
        alert("성인임을 확인했노라.");
        sessionStorage.setItem('rangAdult', 'true');
        location.reload();
    } else {
        alert("애들은 가라!");
        window.location.href = "https://www.google.com";
    }
}