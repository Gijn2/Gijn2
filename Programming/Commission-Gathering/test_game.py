import pygame
import random
import math
import os
import numpy
import hashlib

# --- 0. 경로 설정 ---
IMGS_PATH = os.path.join(os.path.dirname(__file__), "imgs")

# --- 1. 초기화 및 화면 설정 ---
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Legendary Bosses: Final Edition (Visual Enhanced)")
clock = pygame.time.Clock()

# --- 2. 에셋 로드 (화면 설정 후 로드해야 함) --
# 해킹을 막기 위한 비밀 키
secretSalt = "MyLegendaryGameSecret2026"

# 플레이어 및 적 이미지 로드
bgImg = pygame.image.load(os.path.join(IMGS_PATH, "background.png")).convert()
playerImg = pygame.image.load(os.path.join(IMGS_PATH, "player.png")).convert_alpha()
playerImg = pygame.transform.scale(playerImg, (60, 60))

# 몬스터 종류 수
MAX_ENEMY_TYPES = 10
ENEMY_IMGS = {}
for i in range(1, MAX_ENEMY_TYPES + 1):
    type_key = f"type_{i}"
    try:
        ENEMY_IMGS[type_key] = {
            "STAND": pygame.transform.scale(pygame.image.load(os.path.join(IMGS_PATH, f"normalEnemy_{i}_stand.png")).convert_alpha(), (50, 50)),
            "ATTACK": pygame.transform.scale(pygame.image.load(os.path.join(IMGS_PATH, f"normalEnemy_{i}_attack.png")).convert_alpha(), (50, 50)),
        }
    except FileNotFoundError:
        # 이미지가 없는 경우를 대비한 방어적 프로그래밍
        ENEMY_IMGS[type_key] = ENEMY_IMGS.get("type_1")

bossSwarmImg = pygame.image.load(os.path.join(IMGS_PATH, "boss_swarm.png")).convert_alpha()
bossSwarmImg = pygame.transform.scale(bossSwarmImg, (100, 100))
bossZeroImg = pygame.image.load(os.path.join(IMGS_PATH, "boss_zero.png")).convert_alpha()
bossZeroImg = pygame.transform.scale(bossZeroImg, (50, 50))

try:
    snd_hit = pygame.mixer.Sound(os.path.join(IMGS_PATH, "hit.wav"))
    snd_expl = pygame.mixer.Sound(os.path.join(IMGS_PATH, "explosion.wav"))
except:
    snd_hit = None
    snd_expl = None


# 색상 및 폰트
WHITE, RED, GOLD, BLACK, GREEN, CYAN, PURPLE, GRAY = (255, 255, 255), (255, 50, 50), (255, 215, 0), (10, 10, 15), (50, 255, 50), (0, 255, 255), (200, 50, 255), (50, 50, 50)
font_s = pygame.font.SysFont("malgungothic", 16)
font_m = pygame.font.SysFont("malgungothic", 24)
font_l = pygame.font.SysFont("malgungothic", 40)

try:
    sndHit = pygame.mixer.Sound(os.path.join(IMGS_PATH, "hit.wav"))
    sndExpl = pygame.mixer.Sound(os.path.join(IMGS_PATH, "explosion.wav"))
except Exception as e:
    sndHit = None
    sndExpl = None

# 바로 이 위치에 폰트 정의를 넣으세요!
try:
    fontS = pygame.font.SysFont("malgungothic", 16)
    fontM = pygame.font.SysFont("malgungothic", 24)
    fontL = pygame.font.SysFont("malgungothic", 40)
except:
    fontS = pygame.font.Font(None, 20)
    fontM = pygame.font.Font(None, 32)
    fontL = pygame.font.Font(None, 50)

# --- 3. 게임 상태 관리 변수 (camelCase 반영) ---
stats = {"damage": 100, "speed": 5, "gold": 1000, "maxHp": 100, "pierce": False, "specialAmmo": 3}
playerHp = 100
score = 0
gameState = 'PLAYING'
shootCooldown = 0
specialEffectTimer = 0
shakeTimer = 0
zeroTicket = False 
STAGE_DURATION = 1800 
stageTimer = STAGE_DURATION
bossAlertTimer = 0
currentStage = 1
invincibleTimer = 0
particles = []    
highScore = 0    

shopTab = "ITEM"
stocks = {"A": 100, "B": 100, "C": 100}
bankBalance = 0

# 지분에 따른 할인율 계산 함수 (C구역: 정밀 합금 기업이 물가 담당)
# 기능 분리: 함수는 camelCase 사용 (KISS & DRY)
def getDiscountRatio():
    ratio = 2.0 - (stocks["C"] / 100.0)
    return max(0.5, min(2.0, ratio))

# 예외 처리 반영
def loadHighscore():
    if os.path.exists("highscore.txt"):
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read())
        except Exception:
            return 0
    return 0

highScore = loadHighscore()
    
# 상점 아이템 리스트
UPGRADE_POOL = [
    {"name": "공격력 강화", "desc": "데미지 +1.5", "effect": "dmg", "price": 1200},
    {"name": "기동성 강화", "desc": "이동속도 +2", "effect": "speed", "price": 720},
    {"name": "긴급 수리", "desc": "체력 50 회복", "effect": "heal", "price": 960},
    {"name": "레일건", "desc": "탄환 관통 부여", "effect": "pierce", "price": 1920},
    {"name": "장갑 강화", "desc": "최대 체력 +40", "effect": "maxhp", "price": 1440},
    {"name": "특수기 보급", "desc": "W 횟수 +2회", "effect": "ammo", "price": 1080},
    {"name": "고대 무전기", "desc": "크러셔 소환권", "effect": "call_crusher", "price": 4000},
]

# --- 4. 클래스 정의 ---
class Particle:
    def __init__(self, x, y, color):
        self.pos = [x, y]
        self.vel = [random.uniform(-3, 3), random.uniform(-3, 3)]
        self.life = 255  # 투명도 및 수명
        self.color = color

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.life -= 8  # 매 프레임 수명 감소

    def draw(self, surf):
        if self.life > 0:
            p_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(p_surf, (*self.color, self.life), (3, 3), 3)
            surf.blit(p_surf, (self.pos[0]-3, self.pos[1]-3))

class Projectile:
    # radius(반지름) 파라미터 추가
    def __init__(self, x, y, vel, color, dmg, radius=5):
        self.pos = pygame.Vector2(x, y)
        self.vel = vel
        self.color = color
        self.dmg = dmg
        self.radius = radius

    def update(self): 
        self.pos += self.vel

    def draw(self, surf): 
        # 중앙은 하얗게, 테두리는 색상으로 렌더링하여 시인성 극대화
        pygame.draw.circle(surf, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
        pygame.draw.circle(surf, WHITE, (int(self.pos.x), int(self.pos.y)), self.radius - 2)

class BossZero:
    def __init__(self):
        self.type = "REAPER"
        self.pos = pygame.Vector2(WIDTH//2, 100)
        self.hp = 150; self.maxHp = 150
        self.timer = 0
        self.visible = True
        self.state = "TELEPORT"
        
    def update(self, eProjs, pPos):
        self.timer += 1
        
        if self.state == "TELEPORT":
            self.visible = False
            if self.timer > 60: # 1초 후 플레이어 상단으로 텔레포트
                self.pos.x = max(50, min(WIDTH-50, pPos.x + random.randint(-100, 100)))
                self.pos.y = max(50, min(HEIGHT-200, pPos.y - 150))
                self.state = "SCYTHE"
                self.timer = 0
                self.visible = True
                
        elif self.state == "SCYTHE":
            # 낫 휘두르기 (크고 빠른 투사체 3갈래)
            if self.timer == 30:
                for angle in [-15, 0, 15]:
                    dirVec = pygame.Vector2(0, 7).rotate(angle)
                    eProjs.append(Projectile(self.pos.x, self.pos.y, dirVec, RED, 10, 12))
            elif self.timer > 90:
                self.state = "SOULS"
                self.timer = 0
                
        elif self.state == "SOULS":
            # 영혼 소환 (느리게 따라가는 투사체)
            if self.timer % 20 == 0 and self.timer <= 60:
                dist = pPos - self.pos
                dirVec = dist.normalize() * 2 if dist.length() > 0 else pygame.Vector2(0, 2)
                eProjs.append(Projectile(self.pos.x, self.pos.y, dirVec, CYAN, 5, 8))
            elif self.timer > 120:
                self.state = "TELEPORT"
                self.timer = 0

    def draw(self, surf):
        if self.visible:
            surf.blit(bossZeroImg, (self.pos.x - 25, self.pos.y - 25))

class BossCrusher:
    def __init__(self):
        self.type = "CHERNOBOG"
        self.hp = 500; self.maxHp = 500
        self.rect = pygame.Rect(0, -100, WIDTH, 150)
        self.pos = pygame.Vector2(0, -100)
        self.mode = "MOVE"
        self.timer = 0
        self.beamAlpha = 0

    def update(self, eProjs, pPos): 
        self.timer += 1
        self.pos.x += math.sin(self.timer/20) * 5
        self.rect.topleft = self.pos

        if self.mode == "MOVE":
            if self.timer % 120 == 0: 
                self.mode = random.choice(["BEAM_READY", "HOMING"])
                self.timer = 0 
        elif self.mode == "BEAM_FIRE":
            if abs(pPos.x - (self.pos.x + WIDTH//2)) < 60:
                global playerHp 
                playerHp -= 2

class BossSwarm:
    def __init__(self):
        self.type = "SWARM"
        self.hp = 250; self.maxHp = 250
        self.centers = [pygame.Vector2(random.randint(100,800), random.randint(50,200)) for _ in range(8)]
        # 60~150 프레임 (1초 ~ 2.5초) 개별 타이머 할당
        self.fireTimers = [random.randint(60, 150) for _ in range(8)]
        self.maxTimers = list(self.fireTimers) # 크기 계산을 위한 원본 저장

    def update(self, eProjs, pPos):
        for i in range(8):
            self.centers[i].x += math.sin(pygame.time.get_ticks() / 500 + i) * 2
            self.fireTimers[i] -= 1
            
            if self.fireTimers[i] <= 0:
                # 대기 시간에 비례한 크기 계산 로직 (DRY 원칙)
                waitRatio = self.maxTimers[i] / 60.0 # 1.0 ~ 2.5 비율 산출
                pSize = int(4 + (waitRatio * 3))     # 반지름 7 ~ 11
                pDmg = int(5 + (waitRatio * 2))      # 데미지 7 ~ 10
                
                diff = pPos - self.centers[i]
                dirVec = diff.normalize() * 4 if diff.length() > 0 else pygame.Vector2(0, 4)
                
                # 계산된 크기(pSize)를 넘겨 투사체 생성
                eProjs.append(Projectile(self.centers[i].x, self.centers[i].y, dirVec, PURPLE, pDmg, pSize))
                
                # 발사 후 타이머 재설정
                self.fireTimers[i] = random.randint(60, 150)
                self.maxTimers[i] = self.fireTimers[i]

    def draw(self, surf):
        for c in self.centers:
            surf.blit(bossSwarmImg, (c.x - 50, c.y - 50))

ENEMY_CONFIG = {
    "type1": {"hp": 5,  "vy": 1.5, "img": "type_1"},
    "type2": {"hp": 8,  "vy": 1.5, "img": "type_2"},
    "type3": {"hp": 6,  "vy": 1.0, "img": "type_3"},
    "type4": {"hp": 5,  "vy": 0.0, "img": "type_4"},
    # 추후 여기에 type5 ~ type10까지 한 줄씩만 추가하면 됩니다.
    "type5": {"hp": 10, "vy": 1.2, "img": "type_5"}, 
    "elite": {"hp": 50, "vy": 0.5, "img": "type_1"}, # 예외 케이스
}

class Enemy:
    def __init__(self, eType="type1", offset=0):
        self.eType = eType

        config = ENEMY_CONFIG.get(eType, ENEMY_CONFIG["type1"])
        self.hp = config["hp"]
        self.vy = config["vy"]
        self.imgType = config["img"]

        # 공통 로직
        self.pos = pygame.Vector2(random.randint(50, WIDTH-50), -50)
        self.offset = offset
        self.vx = 0
        self.vy = 1.5  
        self.state = "STAND"
        self.shootDelay = random.randint(80, 160)
        self.attackTimer = 0
        self.orbitBullets = [] # type3를 위한 회전 총알 저장소
        
        # 타입별 초기화 로직 분리 (KISS)
        if eType == "type1":
            self.hp = 5
        elif eType == "type2":
            self.hp = 8
        elif eType == "type3":
            self.hp = 6
            self.vy = 1.0
        elif eType == "type4":
            self.hp = 5
            self.vy = 0
            self.pos.y = random.randint(50, 200)
            self.pos.x = -30 if random.random() > 0.5 else WIDTH + 30
            self.vx = 2.5 if self.pos.x < 0 else -2.5

        if self.eType.startswith("type"):
            self.imgType = self.eType.replace("type", "type_")
        else:
            self.imgType = "type_1"

    def update(self, eProjs, pPos):
        # 1. 이동 로직 (type4는 수평 이동만)
        if self.eType == "type3":
            self.pos.y += self.vy
            self.pos.x += math.sin(pygame.time.get_ticks() / 200) * 4 
        else:
            self.pos.y += self.vy
            self.pos.x += self.vx
            if self.eType != "type4" and (self.pos.x <= 0 or self.pos.x >= WIDTH-30): 
                self.vx *= -1

        # 2. 공격 상태 전환
        if self.state == "STAND":
            self.shootDelay -= 1
            if self.shootDelay <= 0:
                self.state = "ATTACK"
                self.attackTimer = 0 
                if self.eType == "type3":
                    self.orbitAngles = [0, 120, 240] # type3 회전 총알 초기화
                
        # 3. 공격 패턴 실행 (모션 동기화)
        elif self.state == "ATTACK":
            self.attackTimer += 1
            
            # 일반몬스터 1: 아래로 내려오며 플레이어 조준 사격
            if self.eType == "type1":
                if self.attackTimer == 1: 
                    dist = pPos - self.pos
                    dirVec = dist.normalize() * 4 if dist.length() > 0 else pygame.Vector2(0, 1)
                    eProjs.append(Projectile(self.pos.x+15, self.pos.y+15, dirVec, RED, 5, 6))
                if self.attackTimer > 30: 
                    self.state = "STAND"; self.shootDelay = 120
                    
            # 일반몬스터 2: 부채꼴 0.1초(6프레임) 간격 발사
            elif self.eType == "type2":
                if self.attackTimer % 6 == 0 and self.attackTimer <= 30:
                    angles = [-0.2, 0, 0.2]
                    for angle in angles:
                        dirVec = pygame.Vector2(0, 4).rotate(math.degrees(angle))
                        eProjs.append(Projectile(self.pos.x+15, self.pos.y+15, dirVec, PURPLE, 4, 5))
                if self.attackTimer > 40:
                    self.state = "STAND"; self.shootDelay = 150
                    
            # 일반몬스터 3: 궤도 회전 후 대기 상태 복귀 시 발사
            elif self.eType == "type3":
                if self.attackTimer < 60:
                    for i in range(len(self.orbitAngles)):
                        self.orbitAngles[i] += 5 # 프레임당 5도씩 회전
                elif self.attackTimer == 60:
                    for angle in self.orbitAngles:
                        dirVec = pygame.Vector2(0, 4).rotate(angle)
                        eProjs.append(Projectile(self.pos.x+15, self.pos.y+15, dirVec, GOLD, 6, 6))
                    self.state = "STAND"; self.shootDelay = 180
                    
            # 일반몬스터 4: 수평 이동 중 발사
            elif self.eType == "type4":
                if self.attackTimer == 1:
                    eProjs.append(Projectile(self.pos.x+15, self.pos.y+15, pygame.Vector2(0, 5), RED, 5, 7))
                if self.attackTimer > 30:
                    self.state = "STAND"; self.shootDelay = 90

    def draw(self, surf):
        currentImg = ENEMY_IMGS.get(self.imgType, ENEMY_IMGS["type_1"])[self.state]
        surf.blit(currentImg, self.pos)
        
        # type3의 회전하는 투사체 시각화 (STAND 전환 전까지)
        if self.state == "ATTACK" and self.eType == "type3":
            for angle in getattr(self, 'orbitAngles', []):
                offset = pygame.Vector2(0, 25).rotate(angle)
                pygame.draw.circle(surf, GOLD, (int(self.pos.x+25 + offset.x), int(self.pos.y+25 + offset.y)), 5)

# --- 5. 유틸리티 함수 ---
# 해킹을 막기 위한 함수
def saveHighscoreSecure(scoreValue):
    # 점수와 비밀키를 합쳐 해시값(Checksum) 생성
    dataStr = str(scoreValue) + secretSalt
    checksum = hashlib.sha256(dataStr.encode()).hexdigest()
    
    with open("highscore.dat", "w") as f:
        # 점수와 해시값을 같이 저장
        f.write(f"{scoreValue}\n{checksum}")

def loadHighscoreSecure():
    if os.path.exists("highscore.dat"):
        try:
            with open("highscore.dat", "r") as f:
                lines = f.readlines()
                scoreValue = int(lines[0].strip())
                savedChecksum = lines[1].strip()
                
                # 파일을 읽을 때 동일한 공식으로 해시를 재계산하여 검증
                calcChecksum = hashlib.sha256((str(scoreValue) + secretSalt).encode()).hexdigest()
                
                if savedChecksum == calcChecksum:
                    return scoreValue
                else:
                    print("점수 조작이 감지되었습니다.")
                    return 0 # 조작 감지 시 0점으로 초기화
        except Exception:
            return 0
    return 0

# 유틸리티 함수
def saveHighscore(s):
    try:
        with open("highscore.txt", "w") as f:
            f.write(str(s))
    except Exception: pass

def getShopItems():
    return [{"data": item, "sold": False} for item in random.sample(UPGRADE_POOL, 4)]

def applyUpgrade(itemData):
    global playerHp, boss
    eff = itemData['effect']
    if eff == "dmg": stats["damage"] += 1.5
    elif eff == "speed": stats["speed"] += 2
    elif eff == "heal": playerHp = min(stats["maxHp"], playerHp + 50)
    elif eff == "pierce": stats["pierce"] = True
    elif eff == "maxhp": stats["maxHp"] += 40; playerHp += 40
    elif eff == "ammo": stats["specialAmmo"] += 2

# --- 6. 메인 게임 루프 ---
playerPos = pygame.Vector2(WIDTH//2, HEIGHT-80)
enemies, pProjs, eProjs, boss = [], [], [], None
shopOptions = []
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    clock.tick(60)
    
    # 화면 흔들림 계산
    render_offset = pygame.Vector2(0, 0)
    if shakeTimer > 0:
        render_offset = pygame.Vector2(random.randint(-7, 7), random.randint(-7, 7))
        shakeTimer -= 1

    # 투명도를 지원하는 도화지 생성
    temp_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    temp_surf.fill((0, 0, 0, 0)) # 투명하게 초기화

    # [1] Input & Event Handling (책임 분리)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        
        if event.type == pygame.KEYDOWN:
            if gameState == 'SHOP':
                # 탭 전환
                if event.key in (pygame.K_1, pygame.K_F1): shopTab = "ITEM"
                if event.key in (pygame.K_2, pygame.K_F2): shopTab = "BANK"
                if event.key in (pygame.K_3, pygame.K_F3): shopTab = "INVEST"
                
                # 은행 탭 기능 연동 (D: 입금, F: 출금)
                if shopTab == "BANK":
                    if event.key == pygame.K_d and stats["gold"] > 0: 
                        bankBalance += stats["gold"]
                        stats["gold"] = 0
                    if event.key == pygame.K_f and bankBalance > 0: 
                        stats["gold"] += int(bankBalance * 0.95) # 5% 수수료
                        bankBalance = 0
                
                # 투자 탭 기능 연동 (1, 2, 3 키)
                if shopTab == "INVEST":
                    keys = {pygame.K_q: "A", pygame.K_w: "B", pygame.K_e: "C"}
                    if event.key in keys:
                        sid = keys[event.key]
                        if stats["gold"] >= 500:
                            stats["gold"] -= 500
                            stocks[sid] += 10 
                            # C 투자 시 상점 물가 할인율이 자동 적용됨 (getDiscountRatio 함수 연동)
                            if sid == "A": stats["speed"] += 0.5
                            if sid == "B": shootCooldown -= 1 # B 투자 시 쿨타임 감소 효과 추가
                            if sid == "C": stats["damage"] += 1

                # 다음 스테이지로 진행 (S키)
                if event.key == pygame.K_s:
                    bankBalance = int(bankBalance * 1.1) # 배당금 10% 추가
                    gameState = 'PLAYING'
                    currentStage += 1
                    stageTimer = STAGE_DURATION

        # 마우스 클릭 처리 (UI 분리 및 로직 통합)
        if event.type == pygame.MOUSEBUTTONDOWN and gameState == 'SHOP':
            mousePos = pygame.mouse.get_pos()
            
            # 탭 영역 클릭 판정 (AABB 충돌)
            if pygame.Rect(50, 20, 180, 50).collidepoint(mousePos): shopTab = "ITEM"
            if pygame.Rect(250, 20, 180, 50).collidepoint(mousePos): shopTab = "BANK"
            if pygame.Rect(450, 20, 180, 50).collidepoint(mousePos): shopTab = "INVEST"
            
            # 아이템 구매 클릭 로직
            if shopTab == "ITEM":
                for i, opt in enumerate(shopOptions):
                    rect = pygame.Rect(30 + i * 215, 150, 200, 320)
                    discount = getDiscountRatio()
                    displayPrice = int(opt["data"]["price"] * discount)
                    if rect.collidepoint(mouse_pos) and not opt["sold"] and stats["gold"] >= displayPrice:
                        stats["gold"] -= displayPrice
                        applyUpgrade(opt["data"])
                        opt["sold"] = True
                    
    # --- 1. 배경 및 탭 UI ---
    temp_surf.fill((20, 20, 30))
    # 탭 버튼 (A: 아이템, B: 은행, C: 투자)
    tabs = [("ITEM", 50), ("BANK", 250), ("INVEST", 450)]
    for name, x in tabs:
        color = GOLD if shopTab == name else GRAY
        pygame.draw.rect(temp_surf, color, (x, 20, 180, 50), border_radius=5)
        temp_surf.blit(font_m.render(name, True, BLACK), (x+50, 30))

    # --- 2. 탭별 내용 ---
    if shopTab == "ITEM":
        discount = getDiscountRatio()
        for i, opt in enumerate(shopOptions):
            card_rect = pygame.Rect(30 + i * 215, 150, 200, 320)
            # 할인율이 적용된 실제 가격 계산
            display_price = int(opt["data"]["price"] * discount)
            
            # 카드 렌더링 (기존 로직 유지하되 가격만 변동)
            c = (40, 40, 40) if opt["sold"] else (30, 30, 50)
            pygame.draw.rect(temp_surf, c, card_rect, border_radius=10)
            
            if not opt["sold"]:
                name_text = font_m.render(opt['data']['name'], True, WHITE)
                temp_surf.blit(name_text, (card_rect.x + 20, card_rect.y + 40))
                
                # 지분 상태에 따른 가격 색상 변경
                p_color = GOLD if stats["gold"] >= display_price else RED
                price_text = font_m.render(f"{display_price} G", True, p_color)
                temp_surf.blit(price_text, (card_rect.x + 60, card_rect.y + 260))

    elif shopTab == "BANK":
        # UI 배경
        pygame.draw.rect(temp_surf, (20, 30, 40), (100, 150, 700, 300), border_radius=15)
        
        # 예치 정보
        balance_txt = font_l.render(f"예치 잔액: {bankBalance} G", True, CYAN)
        interest_txt = font_m.render("예상 다음 배당 이율: +10%", True, GREEN)
        temp_surf.blit(balance_txt, (150, 200))
        temp_surf.blit(interest_txt, (150, 280))
        
        # 안내 문구
        guide_txt = font_s.render("[D] 전액 입금  |  [F] 전액 인출 (수수료 5% 발생)", True, WHITE)
        temp_surf.blit(guide_txt, (150, 400))
        
    elif shopTab == "INVEST":
        # camelCase 적용 및 UI 표시를 위한 key 데이터 통합 (DRY 원칙)
        investTargets = [
            {"id": "A", "name": "A구역: 지열 운송", "effect": "이동속도 증가", "cost": 500, "key": "Q"},
            {"id": "B", "name": "B구역: 에너지 연구", "effect": "쿨타임 감소", "cost": 500, "key": "W"},
            {"id": "C", "name": "C구역: 정밀 합금", "effect": "화력 및 할인율", "cost": 500, "key": "E"}
        ]
        
        for i, target in enumerate(investTargets):
            yPos = 150 + (i * 110)
            pygame.draw.rect(tempSurf, (45, 45, 65), (50, yPos, 800, 90), border_radius=10)
            
            # 지분율 바 (Visual Bar)
            barWidth = int(stocks[target["id"]] * 2) 
            pygame.draw.rect(tempSurf, GOLD, (550, yPos + 35, barWidth, 20))
            
            # 텍스트 정보 표기
            tempSurf.blit(fontM.render(f"{target['name']} ({stocks[target['id']]}%)", True, WHITE), (70, yPos + 15))
            tempSurf.blit(fontS.render(f"효과: {target['effect']}", True, GRAY), (70, yPos + 50))
            
            # 버그 해결 지점: i+1 이 아닌, 딕셔너리에 정의된 실제 로직 키(Q, W, E)를 출력하도록 변경
            tempSurf.blit(fontM.render(f"{target['cost']}G [Key:{target['key']}]", True, GOLD), (380, yPos + 30))

    # 지분 하락에 따른 계급 등급 표시 [cite: 15, 16]
    avg_stock = sum(stocks.values()) / 3
    rank = "고등급(Noble)" if avg_stock > 80 else "저등급(Commoner)"
    temp_surf.blit(font_m.render(f"현재 시민 등급: {rank}", True, GOLD), (WIDTH-300, HEIGHT-50))

    if event.type == pygame.MOUSEBUTTONDOWN and gameState == 'SHOP':
        for opt in shopOptions:
            idx = shopOptions.index(opt)
            rect = pygame.Rect(30 + idx * 215, 150, 200, 320)
            if rect.collidepoint(mouse_pos) and not opt["sold"] and stats["gold"] >= opt["data"]["price"]:
                stats["gold"] -= opt["data"]["price"]
                applyUpgrade(opt["data"])
                opt["sold"] = True

    # [2] Logic Update (비즈니스 로직)
    for p in particles[:]:
        p.update()
        if p.life <= 0: particles.remove(p)

    if gameState == 'PLAYING':
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: playerPos.x -= stats["speed"]
        if keys[pygame.K_RIGHT]: playerPos.x += stats["speed"]
        if keys[pygame.K_UP]: playerPos.y -= stats["speed"]
        if keys[pygame.K_DOWN]: playerPos.y += stats["speed"]

        if playerPos.x < -30: playerPos.x = WIDTH
        elif playerPos.x > WIDTH: playerPos.x = -30
        playerPos.y = max(0, min(HEIGHT-40, playerPos.y))

        if keys[pygame.K_q] and shootCooldown <= 0:
            pProjs.append(Projectile(playerPos.x+20, playerPos.y, pygame.Vector2(0,-10), GREEN, stats["damage"]))
            shootCooldown = 10
        shootCooldown = max(0, shootCooldown - 1)
        if invincibleTimer > 0: invincibleTimer -= 1

        if keys[pygame.K_w] and stats["specialAmmo"] > 0 and specialEffectTimer <= 0:
            stats["specialAmmo"] -= 1
            specialEffectTimer = 60  
            shakeTimer = 30         
            if sndExpl: sndExpl.play()
            
            # 1. 화면의 모든 적 투사체(총알) 즉시 삭제
            eProjs.clear() 
            
            # 2. 모든 일반 적에게 강력한 데미지
            for e in enemies[:]:
                # 안전하게 hp 속성 존재 여부 확인 후 데미지 적용
                if hasattr(e, 'hp'):
                    e.hp -= 20
                    if e.hp <= 0:
                        if e in enemies: enemies.remove(e)
                        score += 150
                        # 처치 이펙트 생성 (선택 사항)
                        for _ in range(5): 
                            particles.append(Particle(e.pos.x+15, e.pos.y+15, (255, 255, 255)))
            
            # 3. 보스가 있다면 보스에게도 데미지
            if boss:
                boss.hp -= 30

        if boss is None:
            stageTimer -= 1
            if stageTimer == 120: bossAlertTimer = 120
            if stageTimer <= 0:
                if zeroTicket: boss = BossZero(); zeroTicket = False
                else: boss = BossSwarm()
                enemies.clear()
            
            if len(enemies) < 6:
                # 명확한 Naming Convention 적용 및 통일
                # etype = random.choices(["normal", "bouncer", "sin", "sniper", "elite"], weights=[50, 15, 15, 18.5, 1.5])[0]
                enemyType = random.choices(["type1", "type2", "type3", "type4", "elite"], weights=[50, 15, 15, 18.5, 1.5])[0]
                enemies.append(Enemy(enemyType, random.randint(0, 1000)))

        if boss:
            boss.update(eProjs, playerPos)
            bossRect = getattr(boss, 'rect', pygame.Rect(boss.pos.x, boss.pos.y, 50, 50) if hasattr(boss, 'pos') else None)
            if bossRect and bossRect.colliderect(pygame.Rect(playerPos.x, playerPos.y, 40, 40)) and invincibleTimer <= 0:
                playerHp -= 20; shakeTimer = 20; invincibleTimer = 60
            
            if boss.hp <= 0:
                boss = None
                stats["gold"] += 1500
                score += 5000
                gameState = 'SHOP'
                shopOptions = getShopItems()

        # 적 및 충돌 로직 업데이트
        for e in enemies[:]:
            e.update(eProjs, playerPos) 
            pRect = pygame.Rect(playerPos.x, playerPos.y, 40, 40)
            eRect = pygame.Rect(e.pos.x, e.pos.y, 30, 30)
            
            if pRect.colliderect(eRect) and invincibleTimer <= 0:
                playerHp -= 15; shakeTimer = 15; invincibleTimer = 40
                if e in enemies: enemies.remove(e)
                continue 

            for p in pProjs[:]:
                pBulletRect = pygame.Rect(p.pos.x, p.pos.y, 10, 10)
                if eRect.colliderect(pBulletRect):
                    
                    if not stats["pierce"] and p in pProjs: 
                        pProjs.remove(p)

                    if hasattr(e, 'hp'):
                        e.hp -= stats["damage"]
                    else:
                        e.hp = 5 - stats["damage"]
                    
                    if e.hp <= 0:
                        if e in enemies:
                            if getattr(e, 'eType', None) == "elite": 
                                zeroTicket = True
                                
                            enemies.remove(e)
                            stats["gold"] += 35
                            score += 100 # 점수 누적 확인
                            
                            # 처치 이펙트(파티클) 생성
                            for _ in range(10): 
                                particles.append(Particle(e.pos.x+15, e.pos.y+15, (255, 50, 50)))
                        break

        for p in pProjs[:]:
            p.update()
            hitThisFrame = False
            if boss:
                hit = False
                if boss.type == "CHERNOBOG" and boss.rect.collidepoint(p.pos): hit = True
                elif boss.type == "SWARM":
                    for c in boss.centers:
                        if p.pos.distance_to(c) < 25: hit = True; break
                elif boss.type == "ZERO" and p.pos.distance_to(boss.pos + pygame.Vector2(25,25)) < 40: hit = True
                
                if hit:
                    boss.hp -= p.dmg; hitThisFrame = True
                    if sndHit: sndHit.play() 
                    for _ in range(5): particles.append(Particle(p.pos.x, p.pos.y, (255, 200, 50)))

            if hitThisFrame and not stats["pierce"]:
                if p in pProjs: pProjs.remove(p)
            elif p.pos.y < -10 or p.pos.y > HEIGHT + 10:
                if p in pProjs: pProjs.remove(p)

        for p in eProjs[:]:
            p.update()
            if p.pos.distance_to(playerPos + pygame.Vector2(30,30)) < 22 and invincibleTimer <= 0:
                playerHp -= p.dmg; eProjs.remove(p); shakeTimer = 10; invincibleTimer = 30
            elif p.pos.y > HEIGHT: eProjs.remove(p)
            
        if playerHp <= 0:
            if score > highScore: saveHighscore(score)
            running = False

    # --- 7. 최종 렌더링 부 ---
    # 배경 영상 처리
    screen.fill(BLACK)
    screen.blit(bgImg, (0, 0))

    # 투명도 지원 서피스 (모든 오브젝트는 여기에 그림)
    tempSurf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    tempSurf.fill((0, 0, 0, 0))

    if gameState == 'PLAYING':
        for p in particles: p.draw(tempSurf)
        for e in enemies: e.draw(tempSurf) 
            
        if boss:
            boss.draw(tempSurf)
            pygame.draw.rect(tempSurf, RED, (WIDTH//2-150, 20, 300, 15))
            pygame.draw.rect(tempSurf, GREEN, (WIDTH//2-150, 20, max(0, (boss.hp/boss.maxHp)*300), 15))
            tempSurf.blit(fontS.render(f"BOSS: {boss.type}", True, WHITE), (WIDTH//2-40, 40))
        
        for p in pProjs: p.draw(tempSurf)
        for p in eProjs: p.draw(tempSurf)
        
        # --- 수정된 렌더링 코드 ---
        if invincibleTimer % 4 == 0: 
            tempSurf.blit(playerImg, playerPos)
            
            playerCenter = (int(playerPos.x + 30), int(playerPos.y + 30))
            hitboxRadius = 10 

            # 1. 원형 테두리 (이건 투명도가 필요 없으므로 그대로 유지)
            pygame.draw.circle(tempSurf, CYAN, playerCenter, hitboxRadius, 2)
            fillSurf = pygame.Surface((hitboxRadius * 2, hitboxRadius * 2), pygame.SRCALPHA)
            pygame.draw.circle(fillSurf, (0, 255, 255, 80), (hitboxRadius, hitboxRadius), hitboxRadius - 2)
            tempSurf.blit(fillSurf, (playerCenter[0] - hitboxRadius, playerCenter[1] - hitboxRadius))
            
        if boss is None:
            pygame.draw.rect(tempSurf, GRAY, (WIDTH//2-100, 20, 200, 8))
            pygame.draw.rect(tempSurf, CYAN, (WIDTH//2-100, 20, (stageTimer/STAGE_DURATION)*200, 8))
            if bossAlertTimer > 0:
                tempSurf.blit(fontL.render("-!!! WARNING !!!-", True, RED), (WIDTH//2-250, HEIGHT//2-50))
                bossAlertTimer -= 1

    elif gameState == 'SHOP':
        tempSurf.fill((20, 20, 30))
        tabs = [("ITEM", 50), ("BANK", 250), ("INVEST", 450)]
        for name, x in tabs:
            color = GOLD if shopTab == name else (60, 60, 70)
            pygame.draw.rect(tempSurf, color, (x, 20, 180, 50), border_radius=5)
            tempSurf.blit(fontM.render(name, True, BLACK if shopTab == name else WHITE), (x+50, 30))

        if shopTab == "ITEM":
            discount = getDiscountRatio()
            tempSurf.blit(fontM.render(f"합금 지분 물가 보정: x{discount:.2f}", True, CYAN), (50, 100))
            for i, opt in enumerate(shopOptions):
                cardRect = pygame.Rect(30 + i * 215, 150, 200, 320)
                displayPrice = int(opt["data"]["price"] * discount)
                c = (40, 40, 40) if opt["sold"] else (30, 30, 50)
                pygame.draw.rect(tempSurf, c, cardRect, border_radius=10)
                if not opt["sold"]:
                    tempSurf.blit(fontM.render(opt['data']['name'], True, WHITE), (cardRect.x + 20, cardRect.y + 30))
                    # 버그 3 해결: 아이템 설명 문구(desc) 정상 노출
                    tempSurf.blit(fontS.render(opt['data']['desc'], True, GRAY), (cardRect.x + 20, cardRect.y + 80))
                    pColor = GOLD if stats["gold"] >= displayPrice else RED
                    tempSurf.blit(fontM.render(f"{displayPrice} G", True, pColor), (cardRect.x + 60, cardRect.y + 260))

        elif shopTab == "BANK":
            pygame.draw.rect(tempSurf, (30, 40, 60), (100, 150, 700, 300), border_radius=15)
            tempSurf.blit(fontL.render(f"예치금: {bankBalance} G", True, CYAN), (150, 200))
            tempSurf.blit(fontM.render(f"다음 스테이지 배당금: +10%", True, GREEN), (150, 280))
            tempSurf.blit(fontS.render("[D] 전액 입금  |  [F] 전액 인출 (수수료 5%)", True, WHITE), (150, 400))

        elif shopTab == "INVEST":
            investTargets = [
                {"id": "A", "n": "구역 A: 지열 운송", "y": 150, "k": "1"},
                {"id": "B", "n": "구역 B: 에너지 연구", "y": 260, "k": "2"},
                {"id": "C", "n": "구역 C: 정밀 합금", "y": 370, "k": "3"}
            ]
            for i, inv in enumerate(investTargets):
                y = inv["y"]
                pygame.draw.rect(tempSurf, (45, 45, 65), (50, y, 800, 90), border_radius=10)
                barW = int(stocks[inv["id"]] * 2) 
                pygame.draw.rect(tempSurf, GOLD, (550, y + 35, barW, 20))
                tempSurf.blit(fontM.render(f"{inv['n']} ({stocks[inv['id']]}%)", True, WHITE), (70, y + 15))
                # 번호 키 매핑 안내 수정
                tempSurf.blit(fontM.render(f"500G [Key:{i+1}]", True, GOLD), (380, y + 30))

        avgS = sum(stocks.values()) / 3
        rank = "Noble" if avgS > 85 else "Commoner" 
        tempSurf.blit(fontM.render(f"등급: {rank} | GOLD: {stats['gold']}G", True, WHITE), (300, HEIGHT-50))

        # 하단 상태 정보
        avg_s = sum(stocks.values()) / 3
        rank = "Noble" if avg_s > 85 else "Commoner" 
        temp_surf.blit(font_m.render(f"등급: {rank} | GOLD: {stats['gold']}G", True, WHITE), (300, HEIGHT-50))

    # W 특수기 효과 (화면 반전)
    if specialEffectTimer > 0:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            # 타이머에 따라 투명도가 낮아지며 서서히 사라짐
            alpha = min(255, specialEffectTimer * 10) 
            overlay.fill((255, 255, 255, alpha))
            screen.blit(overlay, (0, 0))
            specialEffectTimer -= 1 # 타이머 감소

    # 배경 그리기
    screen.blit(bgImg, (0, 0))
    # 흔들림이 적용된 도화지(temp_surf)를 실제 화면에 출력
    screen.blit(tempSurf, render_offset)
        
    # --- 배경에 덮이지 않도록 UI를 마지막에 렌더링 ---
    
    # 1. 체력바 배경 현재 체력(초록색)
    # pygame.draw.rect(screen, RED, (10, 10, 200, 20)) 
    pygame.draw.rect(screen, GREEN, (10, 10, max(0, (playerHp/stats['maxHp'])*200), 20))
    # 직관성을 위한 체력 수치 텍스트 표기 추가
    screen.blit(fontS.render(f"{int(playerHp)} / {stats['maxHp']}", True, BLACK), (80, 10))
    
    # 2. 정보 텍스트 (점수, 최고점수, 스테이지 정보 그룹화)
    infoTxt1 = fontS.render(f"SCORE: {score} | HI-SCORE: {highScore} | STAGE: {currentStage}", True, WHITE)
    screen.blit(infoTxt1, (10, 35))
    
    # 3. 재화 및 특수기 개수 표기 (눈에 띄도록 골드 색상 강조)
    infoTxt2 = fontS.render(f"GOLD: {stats['gold']} G | SPECIAL (W): {stats['specialAmmo']} 개", True, GOLD)
    screen.blit(infoTxt2, (10, 55))
    
    # 4. 제로 티켓 활성화 상태 (UI가 겹치지 않게 y좌표 75로 하향 조정)
    if zeroTicket: 
        screen.blit(fontS.render("★ ZERO TICKET ACTIVE ★", True, CYAN), (10, 75))
    # UI 업데이트 및 프레임 제한
    pygame.display.flip()
    clock.tick(60)

pygame.quit()