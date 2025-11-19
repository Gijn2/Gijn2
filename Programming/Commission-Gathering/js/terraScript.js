// terraScript.js - 세계관 페이지 (terra.html) 전용 기능

// 요청하신 상세 세계관 정보 (HTML 형식으로 구조화)
const LORE_CONTENT = `
    <h2>1. 이그니스 여신: 군주, 고통, 그리고 권능의 기제</h2>
    
    <h3>1-1. 신성한 존재와 역할 (Role & Essence)</h3>
    <p><strong>존재 양식:</strong> 이그니스 여신은 판게아 대륙의 척추인 15000m 활화산 산맥의 활력과 순환을 관장하는 군주입니다. 그녀의 피는 마그마이며, 그녀의 호흡은 지열 가스입니다.</p>
    <p><strong>통치 모순:</strong> 그녀는 창조와 파괴의 순환을 통해 생태계를 유지하나, 이 파괴적 규제 행위는 자기 파괴적인 고통을 수반합니다. 즉, 그녀의 분노와 정화는 곧 의무이자 고통의 표현입니다.</p>
    <p><strong>권능의 이중 동력:</strong></p>
    <ul>
        <li><strong>물리적 동력 (열기):</strong> 지각 심층의 마그마 온도에 직결됩니다. 이 열기는 노바코퍼리카의 모든 산업을 움직이는 가장 근원적인 에너지원입니다.</li>
        <li><strong>영적 동력 (신앙심):</strong> 숭배자들의 신앙심은 그녀의 고통을 경감하고 활력을 안정시키는 정신적 방화벽 역할을 합니다. 신앙이 약해지면 재해 발생 빈도가 증가합니다.</li>
    </ul>

    <h3>1-2. 분노의 스펙트럼과 산업적 이용</h3>
    <p>여신의 감정 변화는 단순한 색 변화를 넘어, 에너지 출력의 등급이며 노바코퍼리카의 기술 표준으로 사용됩니다.</p>
    <ul>
        <li><strong>안정 (깊은 적색):</strong> 희미한 적외선 단계. 일상적인 난방과 저전력 장치 구동에 사용됩니다.</li>
        <li><strong>불안 (주황색/노란색):</strong> 일반적인 에너지 생산 단계. 대부분의 도시 전력과 일반 제련소에서 사용됩니다.</li>
        <li><strong>격정/경고 (푸른색/보라색):</strong> 초고온 고밀도 에너지. 파장이 짧아 극한의 열을 응축하며, 순환 합금 제련과 같은 노바코퍼리카의 1류 독점 산업에 필수적으로 사용됩니다. (최고가 거래)</li>
        <li><strong>진노/정화 (흰색):</strong> 최종적인 백색광 에너지. 통제 불능의 파괴력을 가지며, 오직 재난 방어 시스템의 최종 비상 동력원으로만 극소량 사용이 시도됩니다.</li>
    </ul>

    <h3>1-3. 신성한 외형과 장비의 의미</h3>
    <ul>
        <li><strong>영원한 화로 (심장):</strong> 그녀의 감정과 스펙트럼이 가장 직접적으로 맥동하는 지점. 신앙심의 안정도를 시각적으로 보여줍니다.</li>
        <li><strong>정화의 삽 (주 무기):</strong> <strong>파괴(지각 파쇄)</strong>와 <strong>경작(비옥한 토양 생성)</strong>을 동시에 수행. 여신의 고통스러운 의무를 가장 명확히 드러내는 상징물입니다.</li>
        <li><strong>흑요석 중장갑:</strong> 산맥의 방어력과 불변성을 상징하며, 산맥의 능선 패턴이 새겨진 등고선의 띠는 그녀의 지배 영역에 대한 변치 않는 책임을 의미합니다.</li>
    </ul>
    
    <h2>2. 정치-사회 구조 및 노바코퍼리카 (Novacorporica) 상세</h2>
    
    <h3>2-1. 통치 체제의 작동 원리 (재정일치 사회국가)</h3>
    <p>노바코퍼리카는 기업의 효율성과 종교의 신성성을 결합하여 시민들을 통제합니다.</p>
    <p><strong>48% 지분과 신성 거부권:</strong> 종교단체는 기업 지분 48%를 소유함으로써 모든 전략적 결정, 대규모 투자, 핵심 인력 임명에 대해 <strong>'신의 뜻에 따른다'</strong>는 명분으로 <strong>신성 거부권(Divine Mandate Veto)</strong>을 행사합니다. 이는 CEO의 세속적 권력을 효과적으로 견제하며, 기업 운영을 종교적 교리에 종속시킵니다.</p>
    <p><strong>권력의 삼각 구도:</strong></p>
    <ul>
        <li><strong>CEO (세속 행정):</strong> 외부 무역, 생산 목표, 재무 건전성 등 가시적인 경제 효율을 책임집니다. 종교적 권위는 없으나, 기업의 생존을 담보하는 실질적인 운영자입니다.</li>
        <li><strong>종교단체 (윤리 규정):</strong> 신성 권위와 교리로 사회의 도덕적, 윤리적 기준을 규정하고, 배당금 분배의 정당성을 부여합니다.</li>
        <li><strong>이단심판관 (무력 집행):</strong> 종교와 기업의 법을 집행하는 무력 기관. 마녀 사냥 및 배당 감소로 인한 폭동 진압이 주 임무입니다.</li>
    </ul>

    <h3>2-2. 시민의 생존과 통제 메커니즘</h3>
    <p><strong>배당금 복지 등급제:</strong> 시민 복지는 배당금 수준에 따라 등급화되어 제공되며, 이는 시민의 계층을 명확하게 구분합니다.</p>
    <ul>
        <li><strong>고등급 배당:</strong> 영구 주거권, 무제한 식량 보급, 자녀 교육 특권, 첨단 안보 서비스.</li>
        <li><strong>저등급 배당:</strong> 임시 주거, 배급 식량, 단순 직업 훈련, 최소한의 안보 서비스.</li>
    </ul>
    <p><strong>갈등 세력:</strong></p>
    <ul>
        <li><strong>마녀회:</strong> <strong>"불의 신의 뜻을 다르게 해석하는 자"</strong>로 낙인찍힌 반체제 단체. 이단심판관의 공포 조성을 위한 주요 타겟이며, 실제 초자연적인 힘을 보유했을 가능성이 스토리의 핵심 요소입니다.</li>
    </ul>

    <h2>3. 지역별 지리, 산업 및 생물군 상세 정리</h2>
    
    <h3>3-1. 화산 핵 및 고고도 지대 (The Igneous Core & High Altitude)</h3>
    <p><strong>산업:</strong> 지열 에너지 (판게아 1류), 특수 합금 제련, 희귀 광물 심층 채굴.</p>
    <p><strong>토착 생물 (극한 환경 적응):</strong></p>
    <ul>
        <li><strong>유황 균류:</strong> 화학합성으로 생존 (생명공학 효소).</li>
        <li><strong>열기 포식자:</strong> 특수 냉각액으로 열 평형 유지 (냉각 시스템 설계 응용).</li>
        <li><strong>테로르버드 고산종:</strong> 고효율 헤모글로빈으로 희박 산소 환경 적응 (고고도 탐사 기술).</li>
    </ul>

    <h3>3-2. 정화의 대지 (The Purified Lands)</h3>
    <p><strong>산업:</strong> 재난 방어 시스템 (지열 장벽, 용암 우회), 특수 소재 및 공예 (흑요석 광학 기기), 지열 농업.</p>
    <p><strong>토착 생물 (방어 및 정화):</strong></p>
    <ul>
        <li><strong>자화 선인장:</strong> 중금속 흡수 및 저장, 바늘이 자성을 띔 (자기 센서 원료).</li>
        <li><strong>불꽃 이끼:</strong> 내열성 세포벽으로 고열 버팀 (내화복 소재).</li>
        <li><strong>갑옷 두꺼비:</strong> 피부 골판화 및 유황 가스 정화 능력 (해독제 연구).</li>
    </ul>

    <h3>3-3. 내륙 사막 및 홍수 해안 (Desert & Coastal Zones)</h3>
    <p><strong>산업:</strong> 특수 운송 및 물류 (지열 추진 운송 시스템), 유황 화학 산업, 수력 및 지열 혼합 발전.</p>
    <p><strong>토착 생물 (수분 및 환경 회피):</strong></p>
    <ul>
        <li><strong>결정 나무:</strong> 광물성 결정체로 수분 증발 차단 (수분 저장 기술 모델).</li>
        <li><strong>모래 잠복 거북:</strong> 지하 잠복 및 미세 진동 감지 (지진 감지 센서 설계).</li>
        <li><strong>황철석 벌레:</strong> 독성 광물을 먹고 고순도 철산화물 축적 (채굴 자원).</li>
    </ul>
`;

const REGION_DATA = {
    'ignis': {
        // 30% 아래, 10% 오른쪽으로 이동된 좌표
        coords: "477, 285, 546, 285, 613, 350, 635, 388, 626, 458, 606, 509, 558, 545, 517, 545, 470, 513, 428, 511, 433, 462, 452, 412, 457, 347",
        title: "불의 영역: 순환의 고원 (IGNIS)",
        imageSrc: "../../images/main/worldImg/terraIgnis.png", 
        descriptionHTML: LORE_CONTENT 
    }
};

let mapImage = null;
let mapElement = null;
let mapContainer = null;
let mapOverlay = null;
let infoPanel = null;


/**
 * 이미지 맵의 좌표를 현재 이미지 크기에 맞게 스케일링하여 호버 오버레이를 생성합니다.
 */
function createRegionOverlay(regionId) {
    const region = REGION_DATA[regionId];
    if (!region || !mapContainer || !mapImage) return;

    let areaElement = document.getElementById(`area-${regionId}`);
    if (areaElement) areaElement.remove();
    
    areaElement = document.createElement('div');
    areaElement.id = `area-${regionId}`;
    areaElement.classList.add('map-hover-area');
    areaElement.classList.add(`map-area-${regionId}`);
    
    const coords = region.coords.split(',').map(c => parseInt(c.trim()));
    if (coords.length % 2 !== 0) return;

    // Boundary Calculation
    let minX = Infinity, minY = Infinity;
    let maxX = -Infinity, maxY = -Infinity;
    for (let i = 0; i < coords.length; i += 2) {
        minX = Math.min(minX, coords[i]);
        minY = Math.min(minY, coords[i + 1]);
        maxX = Math.max(maxX, coords[i]);
        maxY = Math.max(maxY, coords[i + 1]);
    }

    // Scaling Calculation (Assuming original map size 800x800)
    const originalWidth = 800;
    const currentWidth = mapImage.offsetWidth;
    const scaleFactor = currentWidth / originalWidth;

    const width = (maxX - minX) * scaleFactor;
    const height = (maxY - minY) * scaleFactor;
    const left = minX * scaleFactor;
    const top = minY * scaleFactor;
    
    areaElement.style.width = `${width}px`;
    areaElement.style.height = `${height}px`;
    areaElement.style.left = `${left}px`;
    areaElement.style.top = `${top}px`;

    // Clip-Path for Polygon Shape
    const clipPathPoints = [];
    for (let i = 0; i < coords.length; i += 2) {
        const xPercent = ((coords[i] - minX) / (maxX - minX)) * 100;
        const yPercent = ((coords[i + 1] - minY) / (maxY - minY)) * 100;
        clipPathPoints.push(`${xPercent}% ${yPercent}%`);
    }
    areaElement.style.clipPath = `polygon(${clipPathPoints.join(', ')})`;
    
    // Event Listeners for Hover and Click
    areaElement.addEventListener('mouseenter', () => areaElement.classList.add('hovered'));
    areaElement.addEventListener('mouseleave', () => areaElement.classList.remove('hovered'));
    
    const mapArea = mapElement.querySelector(`area[data-region="${regionId}"]`);
    if (mapArea) {
        mapArea.addEventListener('click', (e) => {
            e.preventDefault();
            displayRegionInfo(regionId);
        });
        mapArea.addEventListener('mouseenter', () => areaElement.classList.add('hovered'));
        mapArea.addEventListener('mouseleave', () => areaElement.classList.remove('hovered'));
    }
    
    mapOverlay.appendChild(areaElement);
}

/**
 * 지역 정보를 패널에 표시하고 지도 변형을 활성화합니다.
 */
function displayRegionInfo(regionId) {
    const region = REGION_DATA[regionId];
    if (!region || !infoPanel) return;

    // 패널 내용 업데이트 (HTML 삽입)
    infoPanel.querySelector('#region-info-img').src = region.imageSrc;
    infoPanel.querySelector('#region-info-img').alt = region.title;

    // 상세 내용을 HTML로 삽입하여 스크롤 가능한 영역을 채웁니다.
    infoPanel.querySelector('.info-text').innerHTML = `
        <h3>${region.title}</h3>
        ${region.descriptionHTML}
    `;

    // 지도 변형 활성화 (오른쪽 기울임)
    mapContainer.classList.add('active');
    
    // 정보 패널 슬라이드 인
    infoPanel.classList.add('visible');

    // 스크롤 가능한 영역의 맨 위로 스크롤
    const infoTextElement = infoPanel.querySelector('.info-text');
    if (infoTextElement) {
        infoTextElement.scrollTop = 0;
    }

    // (모바일 환경 대비) 정보 패널이 화면에 보이도록 스크롤 이동
    if (window.innerWidth <= 900) {
        infoPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

/**
 * 정보 패널 오버레이를 닫고 지도 변형을 해제합니다.
 */
function closeRegionInfo() {
    if (infoPanel && mapContainer) {
        infoPanel.classList.remove('visible');
        mapContainer.classList.remove('active');
    }
}

/**
 * 맵 초기화 및 이벤트 리스너 설정
 */
function initializeWorldPage() {
    mapImage = document.getElementById('terra-map-image');
    mapElement = document.getElementById('terra-map');
    mapContainer = document.querySelector('.map-container');
    mapOverlay = document.getElementById('map-overlay');
    infoPanel = document.getElementById('region-info-panel');
    
    if (!mapImage || !mapElement || !mapContainer || !mapOverlay || !infoPanel) {
        console.error('World map elements not found.');
        return;
    }

    // 닫기 버튼 이벤트 리스너 설정
    const closeButton = infoPanel.querySelector('#info-close-btn');
    if (closeButton) {
        closeButton.addEventListener('click', closeRegionInfo);
    }

    // 1. 초기 오버레이 생성
    createRegionOverlay('ignis');

    // 2. 리사이즈 이벤트 처리 (반응형 맵 오버레이 위치 조정)
    const handleResize = () => {
        mapOverlay.innerHTML = '';
        createRegionOverlay('ignis');
        // 리사이즈 시 정보 패널 닫기 (변형 충돌 방지)
        closeRegionInfo();
    };
    
    window.addEventListener('resize', handleResize);
}

// terra.html 페이지가 로드될 때 실행
window.addEventListener('load', initializeWorldPage);