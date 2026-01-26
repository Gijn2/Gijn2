/**
 * Project R: 통합 가이드 및 멀티버스 제어 시스템
 * 수정 사항: 성인 인증 로직 복구 및 존재하지 않는 ID 참조 제거
 */

// 1. 배경 실시간 연결망 (Connection Canvas)
const canvas = document.getElementById('connection-canvas');
const ctx = canvas.getContext('2d');
let particles = [];
let activeParticleColor = '212, 175, 55'; // 초기값: Gold (RGB)

function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener('resize', resize);
resize();

class Particle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.vx = (Math.random() - 0.5) * 0.4;
        this.vy = (Math.random() - 0.5) * 0.4;
    }
    update() {
        this.x += this.vx;
        this.y += this.vy;
        if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
        if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
    }
    draw() {
        ctx.fillStyle = `rgba(${activeParticleColor}, 0.4)`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, 1.2, 0, Math.PI * 2);
        ctx.fill();
    }
}

function initCanvas() {
    particles = [];
    for (let i = 0; i < 80; i++) particles.push(new Particle());
}

function connectParticles() {
    for (let a = 0; a < particles.length; a++) {
        for (let b = a; b < particles.length; b++) {
            let dist = Math.hypot(particles[a].x - particles[b].x, particles[a].y - particles[b].y);
            if (dist < 180) {
                ctx.strokeStyle = `rgba(${activeParticleColor}, ${1 - dist / 180 * 0.2})`;
                ctx.lineWidth = 0.5;
                ctx.beginPath();
                ctx.moveTo(particles[a].x, particles[a].y);
                ctx.lineTo(particles[b].x, particles[b].y);
                ctx.stroke();
            }
        }
    }
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => { p.update(); p.draw(); });
    connectParticles();
    requestAnimationFrame(animate);
}
initCanvas();
animate();


// 2. 우측 하단 스토리 조각 진행 바 (Progress Circle)
const circle = document.getElementById('fragment-progress');
const radius = circle.r.baseVal.value;
const circumference = radius * 2 * Math.PI;

circle.style.strokeDasharray = `${circumference} ${circumference}`;
circle.style.strokeDashoffset = circumference;

function setProgress(percent) {
    const offset = circumference - (percent / 100 * circumference);
    circle.style.strokeDashoffset = offset;
    document.getElementById('fragment-percent').innerText = Math.floor(percent);
}


// 3. 통합 제어 로직 (가이드 랑 + 구역 감지 + 성인 인증 trigger)
const rangMsg = document.getElementById('rang-message');
let isVerified = false;  // 성인 인증 여부
let overlayShown = false; // 인증창 노출 여부
let isLocked = false;    // 미인증 시 접근 차단 상태

window.addEventListener('scroll', () => {
    const scrollPos = window.scrollY;
    const totalHeight = document.body.scrollHeight - window.innerHeight;
    const progress = (scrollPos / totalHeight) * 100;

    setProgress(progress);
    updateMultiverse(scrollPos);
});

function updateMultiverse(pos) {
    // ID가 존재하는지 먼저 확인 (오류 방지)
    const sectorAbyss = document.getElementById('sector-abyss');
    if (!sectorAbyss) return;

    const abyssTop = sectorAbyss.offsetTop - 400;
    const mapItems = document.querySelectorAll('.map-item');

    mapItems.forEach(item => item.classList.remove('active'));

    // 1. 광장 및 테마파크 구역
    if (pos < abyssTop) {
        mapItems[0].classList.add('active'); // Plaza
        mapItems[1].classList.add('active'); // Park
        
        // 현재 스크롤 위치에 있는 부스 찾기
        const booths = document.querySelectorAll('.booth-section');
        let currentBoothName = "테마파크";
        
        booths.forEach(booth => {
            if (pos >= booth.offsetTop - 500) {
                currentBoothName = booth.querySelector('h3').innerText;
            }
        });

        rangMsg.innerText = `지금 보시는 곳은 '${currentBoothName}' 부스예요! 정말 멋지죠?`;
        activeParticleColor = '212, 175, 55'; // Gold
        isLocked = false;
    } 
    // 2. Abyss 구역 (성인 인증 필요)
    else {
        mapItems[2].classList.add('active');
        activeParticleColor = '77, 0, 0'; // Dark Red
        
        if (!isVerified && !isLocked) {
            rangMsg.innerText = "잠시만요! 여기부터는 확인이 필요해요! (찡긋)";
            if (!overlayShown) showVerificationOverlay();
        } else if (isVerified) {
            rangMsg.innerText = "Abyss의 비밀스러운 공간에 들어오셨군요. 환영합니다.";
        }
    }
}

// 4. 성인 인증 시스템 기능
function showVerificationOverlay() {
    overlayShown = true;
    const overlay = document.getElementById('verification-overlay');
    overlay.style.display = 'flex';
    setTimeout(() => { overlay.style.opacity = '1'; }, 10);
    document.body.style.overflow = 'hidden'; // 스크롤 금지
}

function verifyAge() {
    const ageInput = document.getElementById('age-input').value;
    if (!ageInput) return alert("생년월일을 선택해주세요.");

    const birthDate = new Date(ageInput);
    const today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear();
    const m = today.getMonth() - birthDate.getMonth();
    
    // 생일이 지나지 않았으면 한 살 차감
    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) age--;

    if (age >= 19) {
        isVerified = true;
        isLocked = false;
        const overlay = document.getElementById('verification-overlay');
        overlay.style.opacity = '0';
        setTimeout(() => {
            overlay.style.display = 'none';
            document.body.style.overflow = 'auto'; // 스크롤 허용
            rangMsg.innerText = "인증 완료! 어른들의 공간 '어비스'를 에스코트해 드릴게요.";
        }, 500);
    } else {
        alert("죄송합니다. 만 19세 미만은 접근할 수 없습니다.");
        isLocked = true;
        exitVerification("에구.. 여긴 아직 위험해요! 안전한 테마파크로 돌아가요!");
    }
}

function closeVerification() {
    isLocked = true;
    exitVerification("알겠어요! 안전한 광장으로 다시 안내해 드릴게요!");
}

function exitVerification(msg) {
    const overlay = document.getElementById('verification-overlay');
    overlay.style.opacity = '0';
    setTimeout(() => {
        overlay.style.display = 'none';
        document.body.style.overflow = 'auto';
        window.scrollTo({ top: 0, behavior: 'smooth' }); // 광장으로 튕겨냄
        overlayShown = false;
        if (msg) rangMsg.innerText = msg;
    }, 500);
}


// 5. 미니맵 점프 기능
function jumpTo(id) {
    const target = document.getElementById(id);
    if (target) {
        window.scrollTo({ top: target.offsetTop, behavior: 'smooth' });
    }
}