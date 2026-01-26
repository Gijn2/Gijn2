document.addEventListener('DOMContentLoaded', () => {
    // --- 1. 파티클 및 로딩 애니메이션 ---
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
        constructor() {
            this.reset();
            this.y = Math.random() * height;
        }
        reset() {
            this.x = Math.random() * width;
            this.y = -20;
            this.char = chars[Math.floor(Math.random() * chars.length)];
            this.fontSize = Math.random() * 12 + 10;
            this.speed = Math.random() * 1 + 0.5;
            this.baseOpacity = Math.random() * 0.5; // 원래 투명도 저장
            this.opacity = this.baseOpacity;
        }
        draw() {
            ctx.fillStyle = `rgba(212, 175, 55, ${this.opacity})`;
            ctx.font = `${this.fontSize}px Orbitron`;
            ctx.fillText(this.char, this.x, this.y);
        }
        update(currentProgress) {
            this.y += this.speed;

            // [연출 수정] 97.5% 지점부터 그라데이션으로 소멸
            if (currentProgress >= 97.5) {
                // 1. 선형적인 비율 계산 (0 ~ 1)
                const progressRatio = (currentProgress - 97.5) / 2.5;

                // 2. 코사인 함수를 이용해 곡선형 감쇄 (Ease-Out 느낌)
                // Math.cos를 이용해 1에서 0으로 부드럽게 떨어뜨림
                const smoothFade = Math.cos((progressRatio * Math.PI) / 2);

                // 3. 파티클의 위치(y)에 따라 미세한 시차 부여 (위쪽부터 사라지는 효과)
                const yOffset = (this.y / height) * 0.2;
                this.opacity = this.baseOpacity * (smoothFade - yOffset);

                if (this.opacity < 0) this.opacity = 0;
            }

            if (this.y > height) this.reset();
        }
    }

    for (let i = 0; i < 100; i++) particles.push(new Particle());

    function animateLoading() {
        ctx.clearRect(0, 0, width, height);
        particles.forEach(p => {
            p.draw();
            p.update(progress);
        });

        if (progress < 100) {
            progress += 0.4;
            progressBar.style.width = `${progress}%`;

            if (progress > 30) statusText.innerText = "ACCESSING ARCHIVE...";
            if (progress > 60) statusText.innerText = "DECRYPTING DATA...";
            if (progress > 90) {
                statusText.innerText = "FINALIZING...";
            }
            requestAnimationFrame(animateLoading);
        } else {
            loadingScreen.style.opacity = '0';
            setTimeout(() => {
                loadingScreen.style.display = 'none';
                mainContent.style.display = 'block';
            }, 1000);
        }
    }
    animateLoading();

    // --- 2. 사이드바 및 노드 로직 ---
    const nodes = document.querySelectorAll('.map-node');
    const mainSidebar = document.getElementById('main-sidebar');
    const subSidebar = document.getElementById('sub-sidebar');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    const charList = document.getElementById('char-list');

    // 추가 기능 제어용 변수
    const charTabBtn = document.querySelector('.tab-btn[data-tab="chars"]');
    const charContent = document.getElementById('tab-chars');

    const navItems = document.querySelectorAll('.nav-item');
    let currentActiveNodeId = null;

    function allClose() {
        mainSidebar.classList.remove('active');
        subSidebar.classList.remove('active');
        currentActiveNodeId = null;
        updateHeaderNav('world');
    }

    function updateHeaderNav(targetName) {
        navItems.forEach(item => {
            if (item.innerText === targetName.toUpperCase()) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
    }

    function switchTab(tabId) {
        tabBtns.forEach(btn => btn.classList.toggle('active', btn.dataset.tab === tabId));
        tabPanes.forEach(pane => pane.classList.toggle('active', pane.id === `tab-${tabId}`));

        if (tabId === 'info') {
            subSidebar.classList.remove('active');
            updateHeaderNav('world');
        } else if (tabId === 'chars') {
            updateHeaderNav('characters');
        }
    }

    nodes.forEach(node => {
        node.addEventListener('click', () => {
            const nodeId = node.dataset.id;
            const charData = node.dataset.chars;

            if (currentActiveNodeId === nodeId) {
                allClose();
                return;
            }

            allClose();
            currentActiveNodeId = nodeId;

            document.getElementById('sidebar-title').innerText = node.dataset.name;
            document.getElementById('sidebar-desc').innerText = node.dataset.info;

            // [추가 기능] data-chars 유무에 따른 캐릭터 탭 제어
            if (!charData || charData.trim() === "") {
                if (charTabBtn) charTabBtn.style.display = 'none';
                if (charContent) charContent.style.display = 'none';
                charList.innerHTML = '';
                switchTab('info'); // 데이터가 없으므로 정보 탭 강제 활성화
            } else {
                if (charTabBtn) charTabBtn.style.display = 'block';

                const chars = charData.split(', ');
                charList.innerHTML = '';
                chars.forEach(c => {
                    const li = document.createElement('li');
                    li.innerText = c;
                    li.onclick = () => {
                        document.getElementById('sub-title').innerText = c;
                        document.getElementById('sub-desc').innerText = `자세한 프로필은 암호화 해제 중입니다.`;
                        switchTab('chars');
                        subSidebar.classList.add('active');
                    };
                    charList.appendChild(li);
                });
                switchTab('info');
            }

            mainSidebar.classList.add('active');
        });
    });

    tabBtns.forEach(btn => {
        btn.onclick = () => switchTab(btn.dataset.tab);
    });

    document.querySelector('.close-sidebar').onclick = allClose;
});