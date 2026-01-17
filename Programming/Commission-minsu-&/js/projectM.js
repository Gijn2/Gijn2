document.addEventListener('DOMContentLoaded', () => {
    // 파티클 및 로딩 애니메이션
    const canvas = document.getElementById('particle-canvas');
    const ctx = canvas.getContext('2d');
    const progressBar = document.getElementById('progress-bar');
    const statusText = document.getElementById('status-text');
    const loadingScreen = document.getElementById('loading-screen');
    const mainContent = document.getElementById('main-content');

    let width, height, particles = [], progress = 0;
    const chars = "망상MANGSANG0101ARCHIVE데이터복구SYSTEM";

    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resize);
    resize();

    class Particle {
        constructor() { this.reset(); this.y = Math.random() * height; }
        reset() {
            this.x = Math.random() * width; this.y = -20;
            this.char = chars[Math.floor(Math.random() * chars.length)];
            this.fontSize = Math.random() * 12 + 10;
            this.speed = Math.random() * 1 + 0.5;
            this.opacity = Math.random() * 0.5;
        }
        draw() {
            ctx.fillStyle = `rgba(212, 175, 55, ${this.opacity})`;
            ctx.font = `${this.fontSize}px Orbitron`;
            ctx.fillText(this.char, this.x, this.y);
        }
        update() { this.y += this.speed; if (this.y > height) this.reset(); }
    }

    for (let i = 0; i < 150; i++) particles.push(new Particle());

    function animate() {
        ctx.clearRect(0, 0, width, height);
        particles.forEach(p => { p.update(); p.draw(); });
        requestAnimationFrame(animate);
    }
    animate();

    const interval = setInterval(() => {
        progress += Math.random() * 8;
        if (progress >= 100) {
            progress = 100;
            clearInterval(interval);
            setTimeout(() => {
                loadingScreen.classList.add('fade-out');
                mainContent.style.display = 'flex';
                setTimeout(() => loadingScreen.style.display = 'none', 1200);
            }, 500);
        }
        progressBar.style.width = progress + '%';
    }, 100);

    // --- 사이드바 및 노드 로직 ---
    const nodes = document.querySelectorAll('.map-node');
    const mainSidebar = document.getElementById('main-sidebar');
    const subSidebar = document.getElementById('sub-sidebar');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    const charList = document.getElementById('char-list');
    
    // 헤더 내비게이션 요소들
    const navItems = document.querySelectorAll('.nav-item');

    let currentActiveNodeId = null;

    // 모든 사이드바 닫기 (초기화)
    function allClose() {
        mainSidebar.classList.remove('active');
        subSidebar.classList.remove('active');
        currentActiveNodeId = null;
        updateHeaderNav('world'); // 사이드바가 다 닫히면 다시 WORLD로 복구 (선택 사항)
    }

    // 헤더 내비게이션 상태 업데이트 함수
    function updateHeaderNav(targetName) {
        navItems.forEach(item => {
            if (item.innerText === targetName.toUpperCase()) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
    }

    // 탭 전환 로직
    function switchTab(tabId) {
        tabBtns.forEach(btn => btn.classList.toggle('active', btn.dataset.tab === tabId));
        tabPanes.forEach(pane => pane.classList.toggle('active', pane.id === `tab-${tabId}`));
        
        if (tabId === 'info') {
            subSidebar.classList.remove('active');
            updateHeaderNav('world'); // INFO 탭일 때는 WORLD 강조
        } else if (tabId === 'chars') {
            updateHeaderNav('characters'); // CHARACTERS 탭일 때는 헤더의 CHARACTERS 강조
        }
    }

    nodes.forEach(node => {
        node.addEventListener('click', () => {
            const nodeId = node.dataset.id;

            if (currentActiveNodeId === nodeId) {
                allClose();
                return;
            }

            allClose();
            currentActiveNodeId = nodeId;

            document.getElementById('sidebar-title').innerText = node.dataset.name;
            document.getElementById('sidebar-desc').innerText = node.dataset.info;
            
            const chars = node.dataset.chars.split(', ');
            charList.innerHTML = '';
            chars.forEach(c => {
                const li = document.createElement('li');
                li.innerText = c;
                li.onclick = () => {
                    document.getElementById('sub-title').innerText = c;
                    document.getElementById('sub-desc').innerText = `${c}는 이 지역의 핵심 인물입니다. 자세한 프로필은 암호화 해제 중입니다.`;
                    
                    // 탭 전환 및 헤더 강조 변경
                    switchTab('chars');
                    subSidebar.classList.add('active');
                };
                charList.appendChild(li);
            });

            switchTab('info');
            mainSidebar.classList.add('active');
        });
    });

    tabBtns.forEach(btn => {
        btn.onclick = () => switchTab(btn.dataset.tab);
    });

    document.querySelector('.close-sidebar').onclick = allClose;
    
});