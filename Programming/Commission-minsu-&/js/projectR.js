// 성인 인증 로직
function checkAge() {
    const age = document.getElementById('age-input').value;
    const modal = document.getElementById('age-gate');

    if (age === "") {
        alert("나이를 입력하거라!");
        return;
    }

    if (age >= 19) {
        alert("음, 어엿한 성인이구나. 랑이의 은밀한 왕국에 입장하는 것을 허가하노라.");
        modal.style.display = 'none';
        sessionStorage.setItem('isAdult', 'true'); // 세션에 저장하여 재인증 방지
    } else {
        alert("꼬맹이는 아직 올 곳이 아니니라! 더 자라서 오너라.");
        window.location.href = "https://www.google.com"; // 미성년자 퇴출
    }
}

// 지도 노드 클릭 이벤트
document.querySelectorAll('.map-node').forEach(node => {
    node.addEventListener('click', function() {
        const isAdultNode = this.classList.contains('adult-zone');
        const isVerified = sessionStorage.getItem('isAdult');

        if (isAdultNode && isVerified !== 'true') {
            document.getElementById('age-gate').style.display = 'flex';
        } else {
            // 사이드바 정보 업데이트 (기존 projectM.js 로직 호출 가능)
            updateSidebar(this);
        }
    });
});

function updateSidebar(node) {
    const name = node.getAttribute('data-name');
    const info = node.getAttribute('data-info');
    document.getElementById('sidebar-title').innerText = name;
    document.getElementById('sidebar-desc').innerText = info;
    document.getElementById('main-sidebar').classList.add('active');
}