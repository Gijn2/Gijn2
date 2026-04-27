import pygame
import random
import math
import os
import hashlib

# --- 경로 설정 ---
IMGS_PATH = os.path.join(os.path.dirname(__file__), "imgs")

# --- 초기화 및 화면 설정 ---
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Topdown Shooting Pygame: Limited Edition")

clock = pygame.time.Clock()

# --- 에셋 로드 ---
secretSalt = "MyPyGameTest2026"

# 플레이어 및 적 이미지 로드
bgImg = pygame.image.load(os.path.join(IMGS_PATH, "background.png")).convert()
playerImg = pygame.image.load(os.path.join(IMGS_PATH, "player.png")).convert_alpha()
playerImg = pygame.transform.scale(playerImg, (60, 60))

MAX_ENEMY_TYPES = 10 # 몬스터 종류 수
ENEMY_IMGS = {}
for i in range(1, MAX_ENEMY_TYPES + 1):
    type_key = f"type_{i}"
    try:
        ENEMY_IMGS[type_key] = {
            "STAND": pygame.transform.scale(pygame.image.load(os.path.join(IMGS_PATH, f"normalEnemy_{i}_stand.png")).convert_alpha(), (50, 50)),
            "ATTACK": pygame.transform.scale(pygame.image.load(os.path.join(IMGS_PATH, f"normalEnemy_{i}_attack.png")).convert_alpha(), (50, 50)),
        }
    except FileNotFoundError:
        ENEMY_IMGS[type_key] = ENEMY_IMGS.get("type_1")

# 색상 및 폰트
WHITE, RED, GOLD, BLACK, GREEN, CYAN, PURPLE, GRAY = (255, 255, 255), (255, 50, 50), (255, 215, 0), (10, 10, 15), (50, 255, 50), (0, 255, 255), (200, 50, 255), (50, 50, 50)

try:
    meteorImg = pygame.image.load(os.path.join(IMGS_PATH, "meteor.png")).convert_alpha()
    meteorImg = pygame.transform.scale(meteorImg, (60, 60))
except:
    meteorImg = pygame.Surface((60, 60), pygame.SRCALPHA)
    pygame.draw.circle(meteorImg, (100, 100, 100), (30, 30), 30)

try:
    sndHit = pygame.mixer.Sound(os.path.join(IMGS_PATH, "hit.wav"))
    sndExpl = pygame.mixer.Sound(os.path.join(IMGS_PATH, "explosion.wav"))
except Exception as e:
    sndHit = None
    sndExpl = None

try:
    fontS = pygame.font.SysFont("malgungothic", 16)
    fontM = pygame.font.SysFont("malgungothic", 24)
    fontL = pygame.font.SysFont("malgungothic", 40)
except:
    fontS = pygame.font.Font(None, 20)
    fontM = pygame.font.Font(None, 32)
    fontL = pygame.font.Font(None, 50)

# --- 게임 상태 관리 변수 ---
base_stats = {"damage": 10, "speed": 5, "maxHp": 100, "pierce": False, "specialAmmo": 3}
stats = base_stats.copy()
stats['gold'] = 1000
STAGE_DURATION = 50 
stageTimer = STAGE_DURATION

bankBalance = 0         # 은행 잔고
bossAlertTimer = 0
currentStage = 1
freeRefreshAvailable = False
gameState = 'PLAYING'
highScore = 0    
hitboxRadius = 10
inventory = []          # 시너지 인벤토리
particles = []
pendingItem = None      # 인벤토리가 꽉 찼을 때 교체 대기 중인 아이템
score = 0
screenShakeTimer = 0    # 화면 흔들림 카운터
shootCooldown = 0
specialEffectTimer = 0
shopTab = "MARKET"      # 기본 상점 설정
shopOptions = []
shopRefreshCount = 0
shopSubState = "NORMAL"
zeroTicket = False 

global playerHp
playerHp = 100
global shakeTimer
shakeTimer = 0
global invincibleTimer
invincibleTimer = 0

SYNERGY_DATA = {
    "WEAPON": {
        2: {"name": "무기(2): 데미지 +5", "effect": {"damage": 5}},
        4: {"name": "무기(4): 데미지 +10, 관통", "effect": {"damage": 10, "pierce": True}},
        6: {"name": "무기(6): 데미지 +20, 관통", "effect": {"damage": 20, "pierce": True}},
        8: {"name": "무기(8): 데미지 +30, 관통", "effect": {"damage": 30, "pierce": True}},
    },
    "TECH": {
        3: {"name": "기술(2): 이동속도 +3", "effect": {"speed": 3}},
        5: {"name": "기술(4): 특수기 +3", "effect": {"specialAmmo": 3}},
        7: {"name": "기술(6): 이동속도 +5, 특수기 +5", "effect": {"speed": 5, "specialAmmo": 5}}
    },
    "ARMOR": {
        2: {"name": "장갑(2): 최대체력 +50", "effect": {"maxHp": 50}},
        3: {"name": "장갑(4): 최대체력 +100", "effect": {"maxHp": 100}},
        4: {"name": "장갑(6): 최대체력 +200", "effect": {"maxHp": 200}},
        5: {"name": "장갑(8): 최대체력 +400", "effect": {"maxHp": 400}},
    },
    "SPEED": {2: {"name": "속도(2): 이속 +5", "effect": {"speed": 5}}},
    "GOLD": {2: {"name": "황금(2): 스테이지 클리어 보너스 +200", "effect": {}}},
    "LIFE": {2: {"name": "생명(2): 최대체력 +100", "effect": {"maxHp": 100}}}
}

ITEM_POOL = [
    {"id": "cons_1", "name": "수리 키트", "type": "CONSUMABLE", "price": 300, "desc": "체력 50 회복"},
    {"id": "cons_2", "name": "에너지 셀", "type": "CONSUMABLE", "price": 500, "desc": "특수기 1회 충전"},
    {"id": "w1", "name": "화염 방사기", "tags": ["WEAPON", "TECH"], "price": 500, "desc": "무기, 기술"},
    {"id": "w2", "name": "초합금 검", "tags": ["WEAPON"], "price": 300, "desc": "무기"},
    {"id": "a1", "name": "나노 슈트", "tags": ["TECH", "ARMOR"], "price": 600, "desc": "기술, 장갑"},
    {"id": "a2", "name": "강철 방패", "tags": ["ARMOR"], "price": 400, "desc": "장갑"},
    {"id": "w3", "name": "플라즈마 캐논", "tags": ["WEAPON", "TECH"], "price": 700, "desc": "무기, 기술"},
    {"id": "a3", "name": "반응형 장갑", "tags": ["ARMOR", "WEAPON"], "price": 500, "desc": "장갑, 무기"},
    {"id": "w4", "name": "레일건", "tags": ["WEAPON", "TECH"], "price": 800, "desc": "강력한 단일 데미지"},
    {"id": "s1", "name": "초소형 엔진", "tags": ["TECH", "SPEED"], "price": 400, "desc": "이동속도 대폭 상승"},
    {"id": "g1", "name": "마이다스 코어", "tags": ["MAGIC", "GOLD"], "price": 900, "desc": "적 처치 시 골드 +5"},
    {"id": "l1", "name": "재생의 갑옷", "tags": ["ARMOR", "LIFE"], "price": 700, "desc": "피격 시 10% 확률로 무적"},
    {"id": "m1", "name": "마법 지팡이", "tags": ["MAGIC", "WEAPON"], "price": 550, "desc": "투사체 크기 증가"},
    {"id": "v1", "name": "흡혈귀의 이빨", "tags": ["WEAPON", "LIFE"], "price": 1000, "desc": "적 처치 시 체력 1 회복(고유)"},
]

ENEMY_CONFIG = {
    "type1": {"hp": 5,  "vy": 1.5, "img": "type_1"},
    "type2": {"hp": 8,  "vy": 1.5, "img": "type_2"},
    "type3": {"hp": 6,  "vy": 1.0, "img": "type_3"},
    "type4": {"hp": 5,  "vy": 0.0, "img": "type_4"},
    # 추후 여기에 type5 ~ type10까지 한 줄씩만 추가하면 됩니다.
    "type5": {"hp": 10, "vy": 1.2, "img": "type_5"}, 
    "elite": {"hp": 50, "vy": 0.5, "img": "type_1"}, # 예외 케이스

}

ENEMY_SPAWN_POOL = [
    {"type": "type1", "weight": 50.0, "minStage": 1},
    {"type": "type2", "weight": 15.0, "minStage": 2},
    {"type": "type3", "weight": 15.0, "minStage": 3},
    {"type": "type4", "weight": 18.5, "minStage": 5}, 
    {"type": "elite", "weight": 1.5, "minStage": 5},
]

# --- 유틸리티 함수 ---
# 현재 스테이지보다 진입 조건이 같거나 낮은 몬스터만 필터링
def getRandomEnemy(current_stage):
    available = [e for e in ENEMY_SPAWN_POOL if current_stage >= e["minStage"]]
    if not available: return "type1"
    types = [e["type"] for e in available]
    weights = [e["weight"] for e in available]
    return random.choices(types, weights=weights)[0]

def loadHighscore():
    if os.path.exists("highscore.txt"):
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read())
        except Exception:
            return 0
    return 0
highScore = loadHighscore()

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

def take_damage(amount, shake, invinc):
    global playerHp, shakeTimer, invincibleTimer
    if invincibleTimer <= 0:
        playerHp -= amount
        shakeTimer = max(shakeTimer, shake)
        invincibleTimer = invinc
        return True
    return False

# 스탯 재계산 로직 (DRY 원칙 적용)
def calculate_stats():
    global stats, playerHp
    current_gold = stats.get("gold", 0)
    
    # 기본 스탯으로 초기화
    stats.clear()
    stats.update(base_stats)
    stats["gold"] = current_gold
    
    # 시너지 태그 카운트
    synergy_counts = {}
    active_tags = []
    for item in inventory:
        for tag in item.get('tags', []):
            active_tags.append(tag)
            synergy_counts[tag] = synergy_counts.get(tag, 0) + 1

    # 중복을 제거한 고유 태그 목록 생성
    unique_active_tags = sorted(list(set(active_tags)))
        
    # 시너지 효과 적용
    for tag, count in synergy_counts.items():
        if tag in SYNERGY_DATA:
            # 요구 조건을 오름차순으로 정렬하여 모두 적용
            for req, data in sorted(SYNERGY_DATA[tag].items()):
                if count >= req:
                    for k, v in data["effect"].items():
                        if type(v) == bool:
                            stats[k] = v
                        else:
                            stats[k] += v

    # 최대 체력 변동에 따른 현재 체력 보정
    if playerHp > stats["maxHp"]:
        playerHp = stats["maxHp"]

def refresh_shop():
    global shopOptions, inventory
    
    # 1. 현재 인벤토리에 있는 아이템 ID 목록 추출
    equipped_ids = [item['id'] for item in inventory]
    
    # 2. 인벤토리에 없는 아이템만 후보군으로 필터링
    # 소모품(CONSUMABLE)은 항상 등장 가능하게 설정
    available_pool = [
        item for item in ITEM_POOL 
        if item['id'] not in equipped_ids or item.get('type') == 'CONSUMABLE'
    ]
    
    # 3. 랜덤으로 3개 선택 (후보가 3개보다 적으면 전체 선택)
    selected = random.sample(available_pool, min(3, len(available_pool)))
    
    # 4. 상점 옵션 객체 생성
    shopOptions = []
    for item in selected:
        shopOptions.append({"data": item, "sold": False})
        
# 스테이지 클리어 시 이자 계산
def apply_interest():
    if bankBalance > 0:
        interest = int(bankBalance * 0.15)
        stats["gold"] += interest

# --- 클래스 정의 ---   
class BossAssetManager:
    _cache = {}

    # 1. 보스별 개별 설정
    BOSS_CONFIG = {
        "bossSwarm": {"size": (100, 100), "ext": ".png"},
        "bossZero": {"size": (100, 150), "ext": ".png"},
        "bossCrusher": {"size": (300, 300), "ext": ".png"}
    }

    @staticmethod
    def get_images(boss_name):
        # 캐시 확인
        if boss_name in BossAssetManager._cache:
            return BossAssetManager._cache[boss_name]

        # 설정 가져오기 (설정이 없으면 기본값 적용)
        config = BossAssetManager.BOSS_CONFIG.get(boss_name, {"size": (100, 100), "ext": ".png"})
        size = config["size"]
        ext = config["ext"]

        images = {}
        for motion in ["stand", "attack"]:
            file_name = f"{boss_name}_{motion}{ext}"
            path = os.path.join(IMGS_PATH, file_name)
            key = motion.upper()

            try:
                # 0. 동적 파일 형식 지원
                img = pygame.image.load(path).convert_alpha()
                images[key] = pygame.transform.scale(img, size)
            except Exception as e:
                print(f"Asset Error [{file_name}]: {e}")
                # 대체 이미지 생성
                placeholder = pygame.Surface(size, pygame.SRCALPHA)
                color = (255, 0, 0) if key == "ATTACK" else (100, 100, 100)
                pygame.draw.rect(placeholder, color, (0, 0, size[0], size[1]), 2)
                images[key] = placeholder

        BossAssetManager._cache[boss_name] = images
        return images
        
class Particle:
    def __init__(self, x, y, color):
        self.pos = [x, y]
        self.vel = [random.uniform(-3, 3), random.uniform(-3, 3)]
        self.life = 255  # 탄막 유지 시간
        self.color = color
        self.isHoming = False

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.life -= 8 

    def draw(self, surf):
        if self.life > 0:
            p_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(p_surf, (*self.color, self.life), (3, 3), 3)
            surf.blit(p_surf, (self.pos[0]-3, self.pos[1]-3))

class Projectile:
    def __init__(self, x, y, vel, color, dmg, radius=5, isHoming=False):
        self.pos = pygame.Vector2(x, y)
        self.vel = vel
        self.color = color
        self.dmg = dmg
        self.radius = radius
        self.isHoming = isHoming

    def update(self): 
        self.pos += self.vel

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
        pygame.draw.circle(surf, WHITE, (int(self.pos.x), int(self.pos.y)), self.radius - 2)

class HomingProjectile(Projectile):
    def __init__(self, x, y, vel, color, dmg, radius=5, turnSpeed=0.03):
        super().__init__(x, y, vel, color, dmg, radius)
        self.turnSpeed = turnSpeed
        self.maxLife = 360 
        self.timer = 0  # 폭발 타이머
        
    def updateTarget(self, targetPos, eProjs):
        self.timer += 1
        # 6초가 지나면 폭발 및 분열
        if self.timer >= self.maxLife:
            self.explode(eProjs)
            return True # 삭제 신호 반환
        
        desiredDir = targetPos - self.pos
        if desiredDir.length() > 0:
            desiredDir = desiredDir.normalize() * self.vel.length()
            self.vel = self.vel.lerp(desiredDir, self.turnSpeed)
        super().update()
        return False
    
    def explode(self, eProjs):
        for i in range(10):
            angle = i * 36
            # 전방향으로 퍼지는 속도 벡터 계산
            splitVel = pygame.Vector2(0, 4).rotate(angle)
            # 분열된 탄환은 일반 탄막으로 생성
            eProjs.append(Projectile(self.pos.x, self.pos.y, splitVel, self.color, self.dmg, 4))    

class Meteor:
    def __init__(self, target):
        self.target = pygame.Vector2(target)
        self.pos = pygame.Vector2(target.x, -100)
        self.speed = 0
        self.radius = random.randint(20, 55)
        self.alive = True
        self.img = pygame.transform.scale(meteorImg, (self.radius * 2, self.radius * 2))

    def update(self, playerPos):
        # 가속 낙하
        self.speed = min(14, self.speed + 0.6)
        direction = (self.target - self.pos)
        
        if direction.length() > 0:
            direction = direction.normalize()
        self.pos += direction * self.speed
        
        # 플레이어와 메테오 본체의 직접 충돌 판정
        if self.pos.distance_to(playerPos + pygame.Vector2(30, 30)) < self.radius + 10:
            return True # 충돌 발생 신호
            
        # 목표 지점에 도달하거나 화면을 완전히 벗어나면 폭발 및 소멸 처리
        if (self.target - self.pos).length() < 10 or self.pos.y > HEIGHT + 100:
            self.alive = False
        return False

    def draw(self, surf):
        shadow_surf = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)
        for r in range(self.radius, 0, -5):
            alpha = int(150 * (1 - r/self.radius)) 
            pygame.draw.circle(shadow_surf, (0, 0, 0, alpha), (self.radius * 2, self.radius * 2), r)
        surf.blit(shadow_surf, (self.target.x - self.radius * 2, self.target.y - self.radius * 2))
        surf.blit(self.img, (self.pos.x - self.radius, self.pos.y - self.radius))

class BossCrusher:
    def __init__(self):
        self.type = "Crusher"
        self.hp = 80
        self.maxHp = 80
        self.pos = pygame.Vector2(WIDTH // 2, 100)
        self.homePos = pygame.Vector2(WIDTH // 2, 100)
        self.mode = "IDLE"
        self.timer = 0
        self.hitboxRadius = 50 
        self.targetPos = None
        self.trapAngle = 0
        self.spinAngle = 0
        self.images = BossAssetManager.get_images("bossCrusher")
        self.currentImg = self.images["STAND"]

    def update(self, eProjs, pPos): 
        self.timer += 1
        
        if self.mode == "IDLE":
            if self.timer > 90:
                self.mode = "TRAP_SHOOT"
                self.timer = 0

        elif self.mode == "TRAP_SHOOT":
            self.currentImg = self.images["ATTACK"]
            self.trapAngle += 0.05
            if self.timer % 15 == 0:
                for i in range(12):
                    angle = (i * (2 * math.pi / 12)) + self.trapAngle
                    dirVec = pygame.Vector2(math.cos(angle), math.sin(angle)) * 3.5
                    eProjs.append(Projectile(self.pos.x, self.pos.y, dirVec, CYAN, 8, 6))
            if self.timer > 120:
                self.mode = "DASH"
                self.targetPos = pygame.Vector2(pPos.x, pPos.y)
                self.timer = 0

        elif self.mode == "DASH":
            self.currentImg = self.images["ATTACK"]
            dirVec = self.targetPos - self.pos
            if dirVec.length() > 20:
                self.pos += dirVec.normalize() * 20
            else:
                self.mode = "SPIN_SHOOT"
                self.timer = 0
                self.spinAngle = 0

        elif self.mode == "SPIN_SHOOT":
            self.currentImg = self.images["ATTACK"]
            self.spinAngle += 0.1

            if self.timer % 6 == 0:
                for i in range(4): 
                    angle = (i * (math.pi / 2)) + self.spinAngle
                    dirVec = pygame.Vector2(math.cos(angle), math.sin(angle)) * 2.0
                    eProjs.append(Projectile(self.pos.x, self.pos.y, dirVec, GOLD, 10, 8))
                    
                    dirVecRev = pygame.Vector2(math.cos(-angle), math.sin(-angle)) * 2.0
                    eProjs.append(Projectile(self.pos.x, self.pos.y, dirVecRev, RED, 10, 8))
            if self.timer > 150:
                self.mode = "RETURN"
                self.timer = 0
    
        elif self.mode == "RETURN":
            dirVec = self.homePos - self.pos
            self.currentImg = self.images["STAND"]
            if dirVec.length() > 8:
                self.pos += dirVec.normalize() * 8
            else:
                self.mode = "IDLE"
                self.timer = 0

    def draw(self, surf):
        surf.blit(self.currentImg, (self.pos.x - 75, self.pos.y - 75))
        hpRatio = max(0, self.hp / self.maxHp)
        pygame.draw.rect(surf, RED, (self.pos.x - 30, self.pos.y + 60, 60, 6))
        pygame.draw.rect(surf, GREEN, (self.pos.x - 30, self.pos.y + 60, 60 * hpRatio, 6))

class BossChernobog:
    def __init__(self):
        self.type = "CHERNOBOG"
        self.pos = pygame.Vector2(WIDTH // 2, 150)
        self.hp = 3000
        self.maxHp = 3000
        self.timer = 0
        self.hitboxRadius = 60
        self.rect = pygame.Rect(self.pos.x - 60, self.pos.y - 60, 120, 120)
        self.images = BossAssetManager.get_images("bossChernobog")
        self.currentImg = self.images["STAND"]
        
        self.orbitBullets = []
        self.orbitAngle = 0

    def update(self, eProjs):
        global shakeTimer
        self.timer += 1
        self.rect.topleft = (self.pos.x - 60, self.pos.y - 60)
        self.orbitBullets = [b for b in self.orbitBullets if b in eProjs]
        self.orbitAngle += 0.08
        
        # 1페이즈: 궤도 탄막 응집 시간을 3배로 증가 (200 -> 600 프레임)
        if self.timer % 900 < 600:
            self.currentImg = self.images["STAND"]
            if self.timer % 5 == 0 and len(self.orbitBullets) < 120:
                newBullet = Projectile(self.pos.x, self.pos.y, pygame.Vector2(0, 0), PURPLE, 15, 8)
                self.orbitBullets.append(newBullet)
                eProjs.append(newBullet)
                
            for i, bullet in enumerate(self.orbitBullets):
                angle = self.orbitAngle + (i * 0.15)
                radius = 70 + (i * 1.5)
                bullet.pos.x = self.pos.x + math.cos(angle) * radius
                bullet.pos.y = self.pos.y + math.sin(angle) * radius
                bullet.vel = pygame.Vector2(0, 0)
                
        # 2페이즈: 혼돈 분열 시 일부 호밍 투사체 섞기
        elif self.timer % 900 == 600:
            self.currentImg = self.images["ATTACK"]
            shakeTimer = 25 
            for bullet in self.orbitBullets:
                chaoticAngle = random.uniform(0, math.pi * 2)
                speed = random.uniform(3.0, 8.0)
                bulletVel = pygame.Vector2(math.cos(chaoticAngle), math.sin(chaoticAngle)) * speed
                
                # 15% 확률로 기존 탄막 대신 호밍 탄막 발사
                if random.random() < 0.15:
                    eProjs.append(HomingProjectile(bullet.pos.x, bullet.pos.y, bulletVel, GOLD, 15, 8))
                    if bullet in eProjs: eProjs.remove(bullet)
                else:
                    bullet.vel = bulletVel
                    bullet.color = RED 
            self.orbitBullets.clear()

    def draw(self, surf):
        surf.blit(self.currentImg, (self.pos.x - 75, self.pos.y - 75))
        hpRatio = max(0, self.hp / self.maxHp)
        pygame.draw.rect(surf, GREEN, (self.pos.x - 50, self.pos.y + 80, 100 * hpRatio, 8))

class BossRock:
    def __init__(self):
        self.type = "ROCK"
        self.pos = pygame.Vector2(WIDTH // 2, 120)
        self.hp = 18000
        self.maxHp = 18000
        self.timer = 0
        self.meteors = []
        self.images = BossAssetManager.get_images("bossRock")
        self.currentImg = self.images["STAND"]
        self.phase = 1

    def _spawn_meteor(self, targetPos):
        self.meteors.append(Meteor(targetPos))

    def _explode_meteor(self, meteor, eProjs, piece_count=12, homing_count=0):
        # 메테오 폭발 시 파편 사방으로 방출
        for angle in range(0, 360, int(360/piece_count)):
            dirVec = pygame.Vector2(0, random.uniform(3, 6)).rotate(angle)
            eProjs.append(Projectile(meteor.target.x, meteor.target.y, dirVec, RED, 8, 6))
        # 특정 페이즈에서는 폭발 시 유도 파편 추가 발생
        for _ in range(homing_count):
            eProjs.append(HomingProjectile(meteor.target.x, meteor.target.y, pygame.Vector2(random.uniform(-3,3), -3), GOLD, 10, 8))

    def update(self, eProjs, playerPos):
        self.timer += 1
        global playerHp, shakeTimer, invincibleTimer

        if self.timer < 1125: self.phase = 1
        elif self.timer < 2250: self.phase = 2
        elif self.timer < 3375: self.phase = 3
        else: self.phase = 4

        self.pos.x = WIDTH // 2 + math.sin(self.timer * 0.01) * 200 

        if self.phase == 1:
            # 무차별 낙하: 운석우 + 보스의 기본 산탄
            # 패턴 1: 무작위 지역에 끊임없는 메테오
            if self.timer % 25 == 0:
                self._spawn_meteor(pygame.Vector2(random.randint(50, WIDTH-50), random.randint(100, HEIGHT-50)))
            # 패턴 2: 보스 본체에서 발사되는 묵직한 5갈래 부채꼴 산탄
            if self.timer % 40 == 0:
                for angle in [-40, -20, 0, 20, 40]:
                    dirVec = pygame.Vector2(0, 5).rotate(angle)
                    eProjs.append(Projectile(self.pos.x, self.pos.y, dirVec, GOLD, 15, 6))
            
        elif self.phase == 2:
            # 정밀 타격과 화산 폭발
            # 패턴 1: 플레이어를 끈질기게 노리는 메테오
            if self.timer % 30 == 0:
                self._spawn_meteor(pygame.Vector2(playerPos.x, playerPos.y))
            # 패턴 2: 보스를 중심으로 회전하며 떨어지는 화산재 (나선탄)
            if self.timer % 5 == 0:
                angle = self.timer * 0.1
                eProjs.append(Projectile(self.pos.x, self.pos.y, pygame.Vector2(math.cos(angle), math.sin(angle)) * 4, PURPLE, 10, 5))
            # 패턴 3: 십자형 파편을 남기는 대형 폭발탄 (본체에서 발사)
            if self.timer % 80 == 0:
                eProjs.append(Projectile(self.pos.x, self.pos.y, (playerPos - self.pos).normalize() * 7, CYAN, 20, 8))

        elif self.phase == 3:
            # 패턴 1: 플레이어 주변을 포위하듯 떨어지는 3개의 메테오
            if self.timer % 50 == 0:
                for angle in [0, 120, 240]:
                    offset = pygame.Vector2(0, 120).rotate(angle + self.timer)
                    target = playerPos + offset
                    target.x = max(50, min(WIDTH-50, target.x))
                    target.y = max(50, min(HEIGHT-50, target.y))
                    self._spawn_meteor(target)
            # 패턴 2: 보스의 거대한 산탄 총 (일직선 융단 폭격)
            if self.timer % 60 == 0:
                for x_offset in range(-100, 101, 25):
                    eProjs.append(Projectile(self.pos.x + x_offset, self.pos.y, pygame.Vector2(0, 6), RED, 8, 6))
            
        elif self.phase == 4:
            self.currentImg = self.images["ATTACK"]
            # 패턴 1: 초고속 랜덤 메테오 폭격
            if self.timer % 15 == 0:
                self._spawn_meteor(pygame.Vector2(random.randint(20, WIDTH-20), random.randint(50, HEIGHT-20)))
            # 패턴 2: 보스 본체의 16방향 지속 발사
            if self.timer % 15 == 0:
                for i in range(16):
                    angle = i * (math.pi / 8) + (self.timer * 0.05)
                    eProjs.append(Projectile(self.pos.x, self.pos.y, pygame.Vector2(math.cos(angle), math.sin(angle)) * 5, CYAN, 7, 5))
            # 패턴 3: 초대형 메테오 덩어리 (같은 자리에 여러 개 동시 투하하여 폭발 파편 극대화)
            if self.timer % 90 == 0:
                target = playerPos + pygame.Vector2(random.randint(-50,50), random.randint(-50,50))
                for _ in range(3): # 3연속 낙하
                    self._spawn_meteor(target)

        # 공통 메테오 충돌 및 폭발 로직
        for meteor in self.meteors[:]:
            hitPlayer = meteor.update(playerPos)
            if hitPlayer and invincibleTimer <= 0:
                playerHp -= 25
                invincibleTimer = 40
                shakeTimer = 25
                meteor.alive = False

            if not meteor.alive:
                # 페이즈가 오를수록 파편 개수가 증가하고 유도 파편이 추가됨
                frag_count = 12 + (self.phase * 4) # 4페이즈: 폭발당 28개의 파편
                homing = 2 if self.phase >= 3 else 0 # 3, 4페이즈엔 유도 파편 발생
                self._explode_meteor(meteor, eProjs, piece_count=frag_count, homing_count=homing)
                self.meteors.remove(meteor)

    def draw(self, surf):
        for meteor in self.meteors:
            meteor.draw(surf)
        surf.blit(self.currentImg, (self.pos.x - 50, self.pos.y - 50))
        
        hpRatio = max(0, self.hp / self.maxHp)
        pygame.draw.rect(surf, RED, (self.pos.x - 60, self.pos.y + 65, 120, 8))
        pygame.draw.rect(surf, GREEN, (self.pos.x - 60, self.pos.y + 65, 120 * hpRatio, 8))

class BossRoll:
    def __init__(self):
        self.type = "ZERO"
        self.pos = pygame.Vector2(WIDTH // 2, 200)
        self.hp = 14000
        self.maxHp = 14000
        self.timer = 0
        self.rect = pygame.Rect(self.pos.x - 40, self.pos.y - 40, 80, 80)
        self.orbitAngle = 0
        self.phase = 1

    def update(self, eProjs, pPos, ctx=None):
        self.timer += 1
        
        if self.timer < 1125: self.phase = 1
        elif self.timer < 2250: self.phase = 2
        elif self.timer < 3375: self.phase = 3
        else: self.phase = 4

        self.pos.x = WIDTH // 2 + math.sin(self.timer * 0.02) * 100
        self.pos.y = 150 + math.cos(self.timer * 0.03) * 50
        self.rect.center = (self.pos.x, self.pos.y)
        self.orbitAngle += 0.05

        if self.phase == 1:
            # 패턴 1: 3중 나선 교차 (시계/반시계 동시 회전)
            if self.timer % 4 == 0:
                for i in range(3):
                    angle1 = self.orbitAngle * 2 + (i * 2 * math.pi / 3)
                    angle2 = -self.orbitAngle * 2 + (i * 2 * math.pi / 3)
                    eProjs.append(Projectile(self.pos.x, self.pos.y, pygame.Vector2(math.cos(angle1), math.sin(angle1)) * 5, CYAN, 8, 5))
                    eProjs.append(Projectile(self.pos.x, self.pos.y, pygame.Vector2(math.cos(angle2), math.sin(angle2)) * 5, WHITE, 8, 5))
            # 패턴 2: 주기적인 12방향 확산탄
            if self.timer % 60 == 0:
                for i in range(12):
                    angle = i * (math.pi / 6)
                    eProjs.append(Projectile(self.pos.x, self.pos.y, pygame.Vector2(math.cos(angle), math.sin(angle)) * 3, PURPLE, 12, 6))
            # 패턴 3: 빠른 직선 저격탄
            if self.timer % 45 == 0:
                dirVec = (pPos - self.pos).normalize() * 8
                eProjs.append(Projectile(self.pos.x, self.pos.y, dirVec, RED, 10, 5))

        elif self.phase == 2:
            # 패턴 1: 4가닥의 촘촘한 회전 빔 (풍차)
            if self.timer % 3 == 0:
                for i in range(4):
                    angle = self.orbitAngle + (i * math.pi / 2)
                    eProjs.append(Projectile(self.pos.x, self.pos.y, pygame.Vector2(math.cos(angle), math.sin(angle)) * 6, GOLD, 10, 5))
            # 패턴 2: 바깥에서 안으로 좁혀오는 역방향 탄막 (압박용)
            if self.timer % 90 == 0:
                for i in range(16):
                    angle = i * (math.pi / 8)
                    spawn_pos = self.pos + pygame.Vector2(math.cos(angle), math.sin(angle)) * 400
                    eProjs.append(Projectile(spawn_pos.x, spawn_pos.y, (self.pos - spawn_pos).normalize() * 3, CYAN, 8, 6))
            # 패턴 3: 플레이어 위치를 향한 샷건 
            if self.timer % 70 == 0:
                base_dir = (pPos - self.pos).normalize()
                for a in [-15, -5, 5, 15]:
                    eProjs.append(Projectile(self.pos.x, self.pos.y, base_dir.rotate(a) * 7, RED, 7, 5))

        elif self.phase == 3:
            # 패턴 1: 상하좌우로 이동하며 쏘는 격자형 탄막
            if self.timer % 15 == 0:
                eProjs.append(Projectile(self.pos.x - 100, self.pos.y, pygame.Vector2(0, 5), WHITE, 10, 6))
                eProjs.append(Projectile(self.pos.x + 100, self.pos.y, pygame.Vector2(0, 5), WHITE, 10, 6))
                eProjs.append(Projectile(self.pos.x, self.pos.y - 100, pygame.Vector2(-5, 0), WHITE, 10, 6))
                eProjs.append(Projectile(self.pos.x, self.pos.y + 100, pygame.Vector2(5, 0), WHITE, 10, 6))
            # 패턴 2: S자 곡선을 그리며 떨어지는 탄막
            if self.timer % 10 == 0:
                wave_x = math.sin(self.timer * 0.1) * 3
                eProjs.append(Projectile(self.pos.x, self.pos.y, pygame.Vector2(wave_x, 4), PURPLE, 8, 5))
            # 패턴 3: 강력한 양방향 유도탄
            if self.timer % 100 == 0:
                eProjs.append(HomingProjectile(self.pos.x - 50, self.pos.y, pygame.Vector2(-2, 2), CYAN, 15, 8))
                eProjs.append(HomingProjectile(self.pos.x + 50, self.pos.y, pygame.Vector2(2, 2), CYAN, 15, 8))

        elif self.phase == 4:
            # 패턴 1: 7방향 초고속 회전 나선 (일정 주기마다 회전 방향 반전)
            direction = 1 if (self.timer // 150) % 2 == 0 else -1
            if self.timer % 3 == 0:
                for i in range(7):
                    angle = self.orbitAngle * 3 * direction + (i * 2 * math.pi / 7)
                    eProjs.append(Projectile(self.pos.x, self.pos.y, pygame.Vector2(math.cos(angle), math.sin(angle)) * 5, RED, 9, 5))
            # 패턴 2: 조밀하게 팽창하는 링
            if self.timer % 40 == 0:
                for i in range(24):
                    angle = i * (math.pi / 12) + (self.orbitAngle)
                    eProjs.append(Projectile(self.pos.x, self.pos.y, pygame.Vector2(math.cos(angle), math.sin(angle)) * 4, GOLD, 10, 6))
            # 패턴 3: 최후의 유도탄 쇄도
            if self.timer % 45 == 0:
                eProjs.append(HomingProjectile(self.pos.x, self.pos.y, pygame.Vector2(0, 0), WHITE, 12, 10))

    def draw(self, surf):
        hpRatio = max(0, self.hp / self.maxHp)
        pygame.draw.rect(surf, (50, 50, 50), (self.pos.x - 60, self.pos.y + 60, 120, 8))
        pygame.draw.rect(surf, (200, 0, 255), (self.pos.x - 60, self.pos.y + 60, 120 * hpRatio, 8))
        # Zero 코어 이펙트 (회전하는 사각형)
        core_surf = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.rect(core_surf, WHITE, (0,0,40,40), 4)
        rotated_core = pygame.transform.rotate(core_surf, math.degrees(self.orbitAngle * 10))
        surf.blit(rotated_core, rotated_core.get_rect(center=(self.pos.x, self.pos.y)))

class BossSwarm:
    def __init__(self):
        self.type = "SWARM"
        self.hp = 12000 
        self.maxHp = 12000
        self.pos = pygame.Vector2(WIDTH // 2, 120)
        self.timer = 0
        self.images = BossAssetManager.get_images("bossSwarm")
        self.currentImg = self.images["STAND"]
        self.phase = 1

    def update(self, eProjs, pPos):
        self.timer += 1
        if self.timer < 1000: self.phase = 1
        elif self.timer < 2000: self.phase = 2
        elif self.timer < 3000: self.phase = 3
        else: self.phase = 4

        # 하이브(군락)처럼 불규칙하게 진동하는 움직임
        self.pos.x = WIDTH // 2 + math.sin(self.timer * 0.05) * 150 + random.randint(-2, 2)
        self.pos.y = 150 + math.cos(self.timer * 0.03) * 50

        if self.phase == 1:
            # 패턴 1: 벌떼 방출 (느리고 회전 반경이 큰 유도탄)
            if self.timer % 30 == 0:
                for _ in range(3):
                    vel = pygame.Vector2(random.uniform(-4, 4), random.uniform(-2, 4))
                    eProjs.append(HomingProjectile(self.pos.x, self.pos.y, vel, PURPLE, 8, 4, 0.015))
        elif self.phase == 2:
            # 패턴 2: 산성 고리 (확장되는 원형 탄막)
            if self.timer % 60 == 0:
                for i in range(16):
                    angle = i * (math.pi / 8) + (self.timer * 0.1)
                    eProjs.append(Projectile(self.pos.x, self.pos.y, pygame.Vector2(math.cos(angle), math.sin(angle)) * 3.5, GREEN, 10, 6))
            if self.timer % 20 == 0:
                eProjs.append(HomingProjectile(self.pos.x, self.pos.y, pygame.Vector2(0, 3), RED, 10, 5, 0.02))
        elif self.phase == 3:
            # 패턴 3: 군락의 폭주 (무작위 흩뿌리기)
            self.currentImg = self.images["ATTACK"]
            if self.timer % 4 == 0:
                randDir = pygame.Vector2(random.uniform(-5, 5), random.uniform(1, 6))
                eProjs.append(Projectile(self.pos.x, self.pos.y, randDir, CYAN, 5, 4))
        elif self.phase == 4:
            # 패턴 4: 완전 포위망 (모든 패턴 융합)
            if self.timer % 40 == 0:
                for _ in range(5):
                    vel = pygame.Vector2(random.uniform(-5, 5), -2)
                    eProjs.append(HomingProjectile(self.pos.x, self.pos.y, vel, GOLD, 12, 5, 0.025))
            if self.timer % 15 == 0:
                for i in range(8):
                    angle = i * (math.pi / 4) + (self.timer * 0.05)
                    eProjs.append(Projectile(self.pos.x, self.pos.y, pygame.Vector2(math.cos(angle), math.sin(angle)) * 4, RED, 8, 5))

    def draw(self, surf):
        surf.blit(self.currentImg, (self.pos.x - 50, self.pos.y - 50))
        hpRatio = max(0, self.hp / self.maxHp)
        pygame.draw.rect(surf, GREEN, (self.pos.x - 60, self.pos.y + 60, 120 * hpRatio, 8))

class BossZero:
    def __init__(self):
        self.type = "CRAZY"
        self.pos = pygame.Vector2(WIDTH // 2, 200)
        self.hp = 122
        self.maxHp = 18000
        self.timer = 0
        self.orbitBullets = []
        self.orbitAngle = 0
        self.phase = 1
        self.swarmCenters = [pygame.Vector2(self.pos.x, self.pos.y) for _ in range(6)]

    def update(self, eProjs, pPos, ctx=None):
        self.timer += 1
        # 6단계 페이즈 (페이즈당 약 600프레임)
        if self.timer < 600: self.phase = 1
        elif self.timer < 1200: self.phase = 2
        elif self.timer < 1800: self.phase = 3
        elif self.timer < 2400: self.phase = 4
        elif self.timer < 3000: self.phase = 5
        else: self.phase = 6

        self.pos.x = WIDTH // 2 + math.sin(self.timer * 0.02) * 100
        self.pos.y = 150 + math.cos(self.timer * 0.03) * 50
        self.orbitAngle += 0.05

        if self.phase <= 3:
            # 전반부: Swarm의 다중 코어를 활용한 융합 패턴
            for i in range(6):
                targetAngle = (i * (2 * math.pi / 6)) + (self.timer * 0.02)
                radius = 120 + math.sin(self.timer * 0.05) * 40
                targetPos = self.pos + pygame.Vector2(math.cos(targetAngle), math.sin(targetAngle)) * radius
                self.swarmCenters[i] = self.swarmCenters[i].lerp(targetPos, 0.1)

            if self.phase == 1:
                # 6개의 코어에서 동시 조준 사격
                if self.timer % 80 == 0:
                    for center in self.swarmCenters:
                        dirVec = (pPos - center).normalize() * 5
                        eProjs.append(Projectile(center.x, center.y, dirVec, CYAN, 10, 5))
            elif self.phase == 2:
                # 코어에서 회전하는 나선탄 방출
                if self.timer % 15 == 0:
                    for i, center in enumerate(self.swarmCenters):
                        angle = self.orbitAngle + (i * math.pi / 3)
                        eProjs.append(Projectile(center.x, center.y, pygame.Vector2(math.cos(angle), math.sin(angle)) * 4, PURPLE, 8, 4))
            elif self.phase == 3:
                # 코어 수축 및 유도탄 쇄도
                if self.timer % 60 == 0:
                    for center in self.swarmCenters:
                        eProjs.append(HomingProjectile(center.x, center.y, pygame.Vector2(0, -3), RED, 12, 6))

        else:
            if self.phase == 4:
                # 거대 궤도 조준 발사
                self.orbitBullets = [b for b in self.orbitBullets if b in eProjs]
                if len(self.orbitBullets) < 12 and self.timer % 10 == 0:
                    newBullet = Projectile(self.pos.x, self.pos.y, pygame.Vector2(0, 0), GOLD, 15, 6)
                    self.orbitBullets.append(newBullet)
                    eProjs.append(newBullet)
                for i, bullet in enumerate(self.orbitBullets):
                    angle = self.orbitAngle + (i * (2 * math.pi / 12))
                    bullet.pos.x = self.pos.x + math.cos(angle) * 200
                    bullet.pos.y = self.pos.y + math.sin(angle) * 200
                    bullet.vel = pygame.Vector2(0, 0)
                if self.timer % 45 == 0 and self.orbitBullets:
                    firedBullet = self.orbitBullets.pop(0)
                    firedBullet.vel = (pPos - firedBullet.pos).normalize() * 10
                    firedBullet.color = RED

            elif self.phase == 5:
                # 화면 전체를 덮는 무작위 탄막망
                if self.timer % 5 == 0:
                    spawnX = random.randint(0, WIDTH)
                    eProjs.append(Projectile(spawnX, -20, pygame.Vector2(0, random.uniform(4, 7)), WHITE, 10, 4))
                if self.timer % 60 == 0:
                    for i in range(12):
                        angle = i * (math.pi / 6)
                        eProjs.append(Projectile(self.pos.x, self.pos.y, pygame.Vector2(math.cos(angle), math.sin(angle)) * 6, CYAN, 12, 5))

            elif self.phase == 6:
                # 발악 패턴: 궤도 코어 + 양방향 나선 + 유도 폭격
                if self.timer % 8 == 0:
                    for i in range(4):
                        angle = (i * (math.pi / 2)) + self.orbitAngle * 2
                        eProjs.append(Projectile(self.pos.x, self.pos.y, pygame.Vector2(math.cos(angle), math.sin(angle)) * 5, PURPLE, 15, 6))
                        eProjs.append(Projectile(self.pos.x, self.pos.y, pygame.Vector2(math.cos(-angle), math.sin(-angle)) * 5, RED, 15, 6))
                if self.timer % 100 == 0:
                    eProjs.append(HomingProjectile(self.pos.x, self.pos.y, pygame.Vector2(0, -5), GOLD, 20, 8))

    def draw(self, surf):
        hpRatio = max(0, self.hp / self.maxHp)
        pygame.draw.rect(surf, (200, 50, 50), (self.pos.x - 60, self.pos.y + 60, 120 * hpRatio, 10))
        
        # 본체 렌더링
        pygame.draw.circle(surf, RED, (int(self.pos.x), int(self.pos.y)), 30, 0)
        pygame.draw.circle(surf, WHITE, (int(self.pos.x), int(self.pos.y)), 10)
        
        # 코어 렌더링
        if self.phase <= 3:
            for center in self.swarmCenters:
                pygame.draw.circle(surf, CYAN, (int(center.x), int(center.y)), 10)
        
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
        
        # 타입별 초기화 로직 분리
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
        # 1. 이동 로직
        if self.eType == "type3":
            self.pos.y += self.vy
            self.pos.x += math.sin(pygame.time.get_ticks() / 200) * 4 
        else:
            self.pos.y += self.vy
            self.pos.x += self.vx
            if self.pos.x <= 0 or self.pos.x >= WIDTH-30: 
                self.vx *= -1

        # 2. 공격 상태 전환
        if self.state == "STAND":
            self.shootDelay -= 1
            if self.shootDelay <= 0:
                self.state = "ATTACK"
                self.attackTimer = 0 
                if self.eType == "type3":
                    self.orbitAngles = [i * 40 for i in range(9)]
                
        # 3. 공격 패턴 실행
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
                    
            elif self.eType == "type2":
                if self.attackTimer % 6 == 0 and self.attackTimer <= 30:
                    angles = [-0.2, 0, 0.2]
                    for angle in angles:
                        dirVec = pygame.Vector2(0, 4).rotate(math.degrees(angle))
                        eProjs.append(Projectile(self.pos.x+25, self.pos.y+15, dirVec, PURPLE, 4, 5))
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
                    eProjs.append(HomingProjectile(self.pos.x+15, self.pos.y+15, pygame.Vector2(0, 5), RED, 5, 7))
                if self.attackTimer > 30:
                    self.state = "STAND"; self.shootDelay = 90

    def draw(self, surf):
        currentImg = ENEMY_IMGS.get(self.imgType, ENEMY_IMGS["type_1"])[self.state]
        surf.blit(currentImg, self.pos)
        
        # type3의 회전하는 투사체 시각화
        if self.state == "ATTACK" and self.eType == "type3":
            for angle in getattr(self, 'orbitAngles', []):
                offset = pygame.Vector2(0, 25).rotate(angle)
                pygame.draw.circle(surf, GOLD, (int(self.pos.x+25 + offset.x), int(self.pos.y+25 + offset.y)), 5)

# --- 0. 메인 게임 루프 ---
playerPos = pygame.Vector2(WIDTH//2, HEIGHT-80)
enemies, pProjs, eProjs, boss = [], [], [], None
shopOptions = []
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    clock.tick(37.5)
    
    # 화면 흔들림 계산
    render_offset = pygame.Vector2(0, 0)
    if shakeTimer > 0:
        render_offset = pygame.Vector2(random.randint(-7, 7), random.randint(-7, 7))
        shakeTimer -= 1

    # 투명도를 지원하는 도화지 생성
    tempSurf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    tempSurf.fill((0, 0, 0, 0)) # 투명하게 초기화

    # [1] Input & Event Handling (책임 분리)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        
        if event.type == pygame.KEYDOWN:

            if gameState == 'SHOP':
                
                # 은행 입출금 기능 (은행 탭일 때만 작동)
                if shopTab == "BANK":
                    if event.key == pygame.K_a and stats["gold"] >= 100:
                        stats["gold"] -= 100
                        bankBalance += 100
                    elif event.key == pygame.K_d and bankBalance >= 100:
                        stats["gold"] += 100
                        bankBalance -= 100

                if event.key == pygame.K_z:
                    shopTab = "BANK" if shopTab == "MARKET" else "MARKET"
                
                # S키로 스테이지 시작
                elif event.key == pygame.K_s:
                    apply_interest()
                    gameState = 'PLAYING'
                    currentStage += 1
                
                # R키: 상점 새로고침
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    cost = 0 if freeRefreshAvailable else (200 + 100 * shopRefreshCount)
                    if stats['gold'] >= cost:
                        stats['gold'] -= cost
                        if not freeRefreshAvailable:
                            shopRefreshCount += 1
                        freeRefreshAvailable = False
                        refresh_shop()  # 아이템 교체 실행

                # 숫자키 1, 2, 3으로 아이템 구매
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    if shopTab == "MARKET" and shopSubState == "NORMAL":
                        idx = event.key - pygame.K_1 # K_1은 0, K_2는 1, K_3은 2로 매핑
                        if idx < len(shopOptions):
                            opt = shopOptions[idx]
                            if not opt["sold"]:
                                item = opt["data"]
                                if stats['gold'] >= item['price']:
                                    if item.get("type") == "CONSUMABLE":
                                        stats['gold'] -= item['price']
                                        if item["id"] == "cons_1": playerHp = min(stats['maxHp'], playerHp + 50)
                                        elif item["id"] == "cons_2": stats['specialAmmo'] += 1
                                        opt["sold"] = True
                                    else:
                                        if len(inventory) < 9:
                                            stats['gold'] -= item['price']
                                            inventory.append(item)
                                            opt["sold"] = True
                                            calculate_stats()
                                        else:
                                            pendingItem = opt
                                            shopSubState = "CONFIRM_REPLACE"

        # 마우스 클릭: 아이템 구매 및 인벤토리 관리
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if gameState == 'SHOP':
                mousePos = pygame.mouse.get_pos()
                        
                # 1. 일반 상점 아이템 구매
                if shopSubState == "NORMAL" and shopTab == "MARKET":
                    for i, opt in enumerate(shopOptions):
                        # (수정됨) UI 화면 그리기 코드와 완벽히 일치하도록 좌표 수정
                        card_rect = pygame.Rect(30 + i * 135, 170, 125, 180)

                        if card_rect.collidepoint(mousePos) and not opt["sold"]:
                            item = opt["data"]
                            if stats['gold'] >= item['price']:
                                        
                                # 소모품 처리
                                if item.get("type") == "CONSUMABLE":
                                    stats['gold'] -= item['price']
                                    if item["id"] == "cons_1": playerHp = min(stats['maxHp'], playerHp + 50)
                                    elif item["id"] == "cons_2": stats['specialAmmo'] += 1
                                    opt["sold"] = True
                                            
                                    # 인벤토리 장착 처리
                                else:
                                    if len(inventory) < 9:
                                        stats['gold'] -= item['price']
                                        inventory.append(item)
                                        opt["sold"] = True
                                        calculate_stats()
                                    else:
                                        pendingItem = opt
                                        shopSubState = "CONFIRM_REPLACE"

            # 교체 확인 모드 처리
            elif shopSubState == "CONFIRM_REPLACE":
                # UI 렌더링 부와 동일한 좌표의 Rect 생성
                btn_yes = pygame.Rect(330, HEIGHT//2 + 50, 100, 40)
                btn_no = pygame.Rect(470, HEIGHT//2 + 50, 100, 40)

                if btn_yes.collidepoint(mousePos):
                    shopSubState = "SELECT_REMOVE"
                elif btn_no.collidepoint(mousePos):
                    shopSubState = "NORMAL"
                    pendingItem = None

            # 제거할 아이템 선택 모드 처리
            elif shopSubState == "SELECT_REMOVE":
                CENTER_X = WIDTH // 2
                # 인벤토리 순회하며 클릭된 슬롯 확인
                for i in range(len(inventory)):
                    row, col = i // 3, i % 3
                    slotRect = pygame.Rect(CENTER_X + 50 + col * 110, 160 + row * 110, 100, 100)

                    if slotRect.collidepoint(mousePos):
                        # 돈 차감 및 아이템 교체 및 상점 내 품절 처리
                        stats['gold'] -= pendingItem["data"]["price"]
                        inventory.pop(i)
                        inventory.append(pendingItem["data"])
                        pendingItem["sold"] = True

                        # 상태 초기화 및 스탯 재적용
                        shopSubState = "NORMAL"
                        pendingItem = None
                        calculate_stats()
                        break                
                    
    # --- 게임 상태별 업데이트 및 렌더링 ---
    for p in particles[:]:
        p.update()
        if p.life <= 0: particles.remove(p)
    
    if gameState == 'PLAYING':
        playerCenter = playerPos + pygame.Vector2(30, 30)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: playerPos.x -= stats["speed"]
        if keys[pygame.K_RIGHT]: playerPos.x += stats["speed"]
        if keys[pygame.K_UP]: playerPos.y -= stats["speed"]
        if keys[pygame.K_DOWN]: playerPos.y += stats["speed"]

        if playerPos.x < -30: playerPos.x = WIDTH
        elif playerPos.x > WIDTH: playerPos.x = -30
        playerPos.y = max(0, min(HEIGHT-40, playerPos.y))
        
        current_homing = keys[pygame.K_LSHIFT]  
        if keys[pygame.K_q] and shootCooldown <= 0:
            base_dir = pygame.Vector2(0, -10)  # 기본 위쪽 발사
            is_homing = keys[pygame.K_LSHIFT]

            new_proj = Projectile(
                    playerPos.x + 30, 
                    playerPos.y + 30, 
                    pygame.Vector2(0, -10), 
                    GREEN, 
                    stats['damage'],
                    isHoming=keys[pygame.K_LSHIFT] # 이제 정상적으로 인식됩니다.
                )
            pProjs.append(new_proj)
            shootCooldown = 15 # 발사 간격 조절
        shootCooldown = max(0, shootCooldown - 1)
        if invincibleTimer > 0: invincibleTimer -= 1

        if keys[pygame.K_w] and stats["specialAmmo"] > 0 and specialEffectTimer <= 0:
            stats["specialAmmo"] -= 1
            specialEffectTimer = 40  
            shakeTimer = 10         
            if sndExpl: sndExpl.play()
            
            # 1. 화면의 모든 적 투사체(총알) 즉시 삭제
            eProjs.clear() 
            
            # 2. 모든 일반 적에게 강력한 데미지
            for e in enemies[:]:
                # 안전하게 hp 속성 존재 여부 확인 후 데미지 적용
                if hasattr(e, 'hp'):
                    e.hp -= 30
                    if e.hp <= 0:
                        if e in enemies: enemies.remove(e)
                        score += 150
                        # 처치 이펙트 생성 (선택 사항)
                        for _ in range(5): 
                            particles.append(Particle(e.pos.x+15, e.pos.y+15, (255, 255, 255)))
            
            # 3. 보스가 있다면 보스에게도 데미지
            if boss:
                boss.hp -= 100

        if boss is None:
            stageTimer -= 1
            if stageTimer == 120: bossAlertTimer = 120
            if stageTimer <= 0:
                if zeroTicket: boss = BossZero(); zeroTicket = False
                elif currentStage == 1:
                    # boss = BossSwarm()
                    # boss = BossZero()
                    # boss = BossChernobog()
                    boss = BossCrusher()
                elif currentStage == 2:
                    boss = BossCrusher()
                elif currentStage == 3:
                    boss = BossCrusher()
                else:
                    # 모든 지정된 스테이지 이후에는 무작위 혹은 기본 보스
                    boss = random.choice([BossCrusher()])

            if len(enemies) < 10:
                enemyType = getRandomEnemy(currentStage)
                enemies.append(Enemy(enemyType, random.randint(0, 1000)))
        else:
            if boss.type == "SWARM":
                if len(enemies) < 5: 
                    # 너무 자주 스폰되지 않도록 낮은 확률 부여
                    if random.random() < 0.25:
                        enemies.append(Enemy("type4", random.randint(0, 1000)))
            pass


        if boss:
            boss.update(eProjs, playerPos)
            bossRect = getattr(boss, 'rect', pygame.Rect(boss.pos.x, boss.pos.y, 50, 50) if hasattr(boss, 'pos') else None)
            hit_by_boss = False
            if bossRect and bossRect.collidepoint(playerCenter.x, playerCenter.y): 
                hit_by_boss = True
            elif hasattr(boss, 'pos') and boss.pos.distance_to(playerCenter) < hitboxRadius + 25: # 반경 25로 보스 둥근 몸체 가정
                hit_by_boss = True

            if hit_by_boss and invincibleTimer <= 0:
                playerHp -= 20; shakeTimer = 20; invincibleTimer = 60

            if boss.hp <= 0:
                boss = None
                stats["gold"] += 1500
                score += 5000
                gameState = 'SHOP'
                refresh_shop()

# --- [준비 단계] 공통 변수 계산 (DRY 원칙) ---

        # --- 1. 적(Enemies) 업데이트 및 플레이어 충돌 판정 ---
        for e in enemies[:]:
            e.update(eProjs, playerPos) 
            eCenter = pygame.Vector2(e.pos.x + 15, e.pos.y + 15)

            # type4 좌우 반사 로직 (화면 밖 제거 대신 반사)
            if getattr(e, 'eType', "") == "type4":
                if e.pos.x <= 0 or e.pos.x >= WIDTH - 10:
                    e.vx *= -1
            
            # 플레이어 본체와 적 충돌 (원형 판정)
            if playerCenter.distance_to(eCenter) < hitboxRadius + 15 and invincibleTimer <= 0:
                if take_damage(15, 15, 40):
                    if e in enemies: enemies.remove(e)

            # 화면 하단 이탈 시 제거 (리스폰을 위함)
            if e.pos.y > HEIGHT + 50:
                if e in enemies: enemies.remove(e)
                continue

        # --- 2. 적 투사체(eProjs) 업데이트 및 플레이어 피격 판정 ---
        for p in eProjs[:]:
            shouldRemove = False
            if isinstance(p, HomingProjectile):
                shouldRemove = p.updateTarget(playerPos, eProjs)
            else:
                p.update()
            
            # 화면 밖 제거 판정
            offScreen = p.pos.x < -100 or p.pos.x > WIDTH+100 or p.pos.y < -100 or p.pos.y > HEIGHT+100
            if shouldRemove or offScreen:
                if p in eProjs: eProjs.remove(p)
                continue

            # 플레이어 피격 판정
            p_radius = getattr(p, 'radius', 5)
            if p.pos.distance_to(playerCenter) < hitboxRadius + p_radius and invincibleTimer <= 0:
                playerHp -= p.dmg
                if p in eProjs: eProjs.remove(p)
                shakeTimer = 10; invincibleTimer = 30
            elif p.pos.y > HEIGHT: 
                if p in eProjs: eProjs.remove(p)

        # --- 플레이어 투사체(pProjs) 업데이트 및 적/보스 피격 판정 ---
        for p in pProjs[:]:
            if getattr(p, 'isHoming', False):
                valid_targets = []
                
                # 1. 몬스터 타겟 추가
                for e in enemies:
                    valid_targets.append(pygame.Vector2(e.pos.x + 15, e.pos.y + 15))
                
                # 2. 보스 타겟 추가
                if boss and hasattr(boss, 'pos'):
                    # 보스의 중심점 (보스 종류에 따라 세밀한 조정이 필요하다면 offset 추가 가능)
                    valid_targets.append(pygame.Vector2(boss.pos.x, boss.pos.y))
                
                # 3. 가장 가까운 타겟 계산 및 속도 보정 (lerp)
                if valid_targets:
                    closest_target = min(valid_targets, key=lambda pos: p.pos.distance_to(pos))
                    target_dir = closest_target - p.pos
                    if target_dir.length() > 0:
                        # 0.15의 가중치로 부드러운 유도 미사일 궤적 생성
                        p.vel = p.vel.lerp(target_dir.normalize() * 12, 0.15)
            p.update()
            hitThisFrame = False
            
            # 보스 피격 판정
            if boss:
                hit_radius = getattr(boss, 'hitboxRadius', 40) # 보스 클래스에 정의된 피격 반경 우선 사용
                hitThisFrame = False

                # BossZero의 다중 코어(swarmCenters) 판정
                if boss.type == "CRAZY" and boss.phase <= 3:
                    for center in boss.swarmCenters:
                        if p.pos.distance_to(center) < 20: # 코어 피격 반경
                            boss.hp -= p.dmg # p.damage가 아니라 p.dmg 여야 합니다!
                            hitThisFrame = True
                            break
                
                # 일반적인 보스 본체 피격 판정
                if not hitThisFrame and p.pos.distance_to(boss.pos) < hit_radius:
                    boss.hp -= p.dmg
                    hitThisFrame = True
                
            # 일반 적 피격 판정 (보스를 맞추지 않았을 때만 체크하거나 관통 시 체크)
            if not hitThisFrame:
                for e in enemies[:]:
                    eCenter = pygame.Vector2(e.pos.x + 15, e.pos.y + 15)
                    if p.pos.distance_to(eCenter) < 20: # 적 피격 판정 범위 20
                        e.hp -= stats["damage"]
                        hitThisFrame = True
                        
                        if e.hp <= 0:
                            if getattr(e, 'eType', None) == "elite": zeroTicket = True
                            if e in enemies: enemies.remove(e)
                            stats["gold"] += 35
                            
                            earned_score = 40 if getattr(p, 'isHoming', False) else 100
                            score += earned_score
                            
                            for _ in range(10): particles.append(Particle(eCenter.x, eCenter.y, (255, 50, 50)))
                        break

            # 투사체 소멸 처리 (관통 업그레이드 여부 확인)
            if hitThisFrame and not stats.get("pierce", False):
                if p in pProjs: pProjs.remove(p)
            elif p.pos.y < -50 or p.pos.y > HEIGHT + 50 or p.pos.x < -50 or p.pos.x > WIDTH + 50:
                if p in pProjs: pProjs.remove(p)

        # --- 게임 오버 체크 ---
        if playerHp <= 0:
            if score > highScore: 
                try:
                    saveHighscoreSecure(score) # 보안 저장 함수로 변경
                except Exception as e:
                    print(f"점수 저장 실패: {e}") # try-catch 예외 처리 규칙 반영
            running = False

    # --- 최종 렌더링 부 ---
    # 배경 영상 처리
    screen.fill(BLACK)

    # 투명도 지원 서피스 (모든 오브젝트는 여기에 그림)
    tempSurf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    tempSurf.fill((0, 0, 0, 0))

    if gameState == 'PLAYING':
        for p in particles: p.draw(tempSurf)
        for e in enemies: e.draw(tempSurf) 
            
        if boss:
            boss.draw(tempSurf)
        
        for p in pProjs: p.draw(tempSurf)
        for p in eProjs: p.draw(tempSurf)
        
        # --- 수정된 렌더링 코드 ---
        if invincibleTimer % 4 == 0: 
            tempSurf.blit(playerImg, playerPos)
            hitboxRadius = 5

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

    # --- 메인 루프 내부 그리기 영역 ---

    if gameState == 'SHOP':
        tempSurf.fill((15, 15, 25)) 
        CENTER_X = WIDTH // 2  # 450px

        # 0. 상단 공통 타이틀 및 안내
        tempSurf.blit(fontM.render(f"보유 골드: {stats['gold']}G", True, GOLD), (30, 30))
        tempSurf.blit(fontS.render("[Z] 전환 | [S] 시작", True, WHITE), (30, 70))

        # --- [좌측 영역: 상점 및 시너지 (0 ~ 450px)] ---
        if shopTab == "MARKET":
            tempSurf.blit(fontM.render("MARKET ITEMS", True, CYAN), (30, 120))
            for i, opt in enumerate(shopOptions):
                cardRect = pygame.Rect(30 + i * 135, 170, 125, 180)
                color = (40, 40, 50) if not opt["sold"] else (20, 20, 20)
                pygame.draw.rect(tempSurf, color, cardRect, border_radius=10)
                if not opt["sold"]:
                    tempSurf.blit(fontS.render(opt['data']['name'][:8], True, WHITE), (cardRect.x+10, cardRect.y+15))
                    tempSurf.blit(fontS.render(f"{opt['data']['price']}G", True, GOLD), (cardRect.x+10, cardRect.y+150))
        elif shopTab == "BANK":
            # 은행 전용 인터페이스 추가
            tempSurf.blit(fontM.render("GALACTIC BANK", True, GOLD), (30, 120))
            # 은행 잔고 및 조작 안내
            bank_info = f"은행 잔고: {bankBalance}G"
            tempSurf.blit(fontM.render(bank_info, True, WHITE), (60, 180))
            tempSurf.blit(fontS.render("[A] 100G 예금 | [D] 100G 출금", True, CYAN), (60, 230))
            tempSurf.blit(fontS.render("이자는 라운드 종료 시 15% 지급됩니다.", True, GREEN), (60, 270))
            
        # [좌측 하단: 시너지 이원화 표시]
        pygame.draw.line(tempSurf, GRAY, (20, 350), (CENTER_X - 20, 350), 2)
        # 왼쪽 칸: 보유 현황
        tempSurf.blit(fontS.render("[ 보유 시너지 ]", True, GOLD), (30, 365))
        # 오른쪽 칸: 발동 효과
        tempSurf.blit(fontS.render("[ 발동 효과 ]", True, GREEN), (CENTER_X // 2 + 30, 365))
        
        synergy_counts = {}
        for item in inventory:
            for tag in item["tags"]:
                synergy_counts[tag] = synergy_counts.get(tag, 0) + 1
        
        y_pos = 400
        for tag, count in synergy_counts.items():
            # 왼쪽 출력 (보유 태그 개수)
            tempSurf.blit(fontS.render(f"{tag}: {count}개", True, WHITE), (30, y_pos))
            
            # 오른쪽 출력 (발동된 효과)
            if tag in SYNERGY_DATA:
                valid_effects = [
                    (req, data) for req, data in SYNERGY_DATA[tag].items()
                    if count >= req
                ]
                if valid_effects:
                    req, data = max(valid_effects, key=lambda x: x[0])  # 최고 단계만 출력
                    eff_txt = f"{data['name']}"
                    tempSurf.blit(fontS.render(eff_txt, True, CYAN), (CENTER_X // 2 + 30, y_pos))
            y_pos += 25

        # --- [우측 영역: 인벤토리 9칸 (450 ~ 900px)] ---
        tempSurf.blit(fontM.render("INVENTORY", True, WHITE), (CENTER_X + 40, 120))
        for i in range(9):
            row, col = i // 3, i % 3
            slotRect = pygame.Rect(CENTER_X + 50 + col * 110, 160 + row * 110, 100, 100)
            pygame.draw.rect(tempSurf, (25, 25, 35), slotRect, border_radius=5)
            pygame.draw.rect(tempSurf, GRAY, slotRect, 2, border_radius=5)
            
            if i < len(inventory):
                # 아이템 장착 시 표시
                item_txt = fontS.render(inventory[i]["name"][:6], True, CYAN)
                tempSurf.blit(item_txt, (slotRect.x + 10, slotRect.y + 40))

        if shopSubState == "CONFIRM_REPLACE":
            # 화면 중앙 팝업창 배경
            popup_rect = pygame.Rect(300, HEIGHT//2 - 50, 300, 160)
            pygame.draw.rect(tempSurf, (40, 40, 50), popup_rect, border_radius=10)
            pygame.draw.rect(tempSurf, GOLD, popup_rect, 2, border_radius=10)
            
            # 안내 문구
            tempSurf.blit(fontS.render("인벤토리가 꽉 찼습니다.", True, WHITE), (355, HEIGHT//2 - 30))
            tempSurf.blit(fontS.render("기존 아이템을 버리고 장착하시겠습니까?", True, GOLD), (315, HEIGHT//2 - 5))
            
            # YES 버튼 (x=330, y=HEIGHT//2+50)
            pygame.draw.rect(tempSurf, GREEN, (330, HEIGHT//2 + 50, 100, 40), border_radius=5)
            tempSurf.blit(fontM.render("YES", True, BLACK), (355, HEIGHT//2 + 55))
            
            # NO 버튼 (x=470, y=HEIGHT//2+50)
            pygame.draw.rect(tempSurf, RED, (470, HEIGHT//2 + 50, 100, 40), border_radius=5)
            tempSurf.blit(fontM.render("NO", True, WHITE), (500, HEIGHT//2 + 55))
            
        elif shopSubState == "SELECT_REMOVE":
            # 인벤토리 영역 위에 붉은색 경고/안내 문구 표시
            tempSurf.blit(fontM.render("버릴 아이템을 클릭하세요!", True, RED), (CENTER_X + 50, 90))
        # 스탯 렌더링
        stat_text = f"DMG: {stats['damage']} | SPD: {stats['speed']} | MAX_HP: {stats['maxHp']} | 관통: {'ON' if stats['pierce'] else 'OFF'} | W: {stats['specialAmmo']}"
        tempSurf.blit(fontS.render(stat_text, True, WHITE), (300, HEIGHT - 30))

    # 1. 가장 밑바닥에 배경 먼저 그리기
    screen.blit(bgImg, (0, 0))
    screen.blit(tempSurf, (0, 0))
        
    # W 특수기 효과
    if specialEffectTimer > 0:
        # 1. 화면 전체를 어둡게 (섬광 대신 몰입감)
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))
        
        # 2. 개성 있는 '절단선' 이펙트 (화면을 가로지르는 날카로운 선)
        line_y = HEIGHT // 2
        line_width = specialEffectTimer * 2 # 시간이 갈수록 얇아짐
        pygame.draw.line(screen, CYAN, (0, line_y), (WIDTH, line_y), line_width)
        pygame.draw.line(screen, WHITE, (0, line_y), (WIDTH, line_y), max(1, line_width // 3))
        
        specialEffectTimer -= 1
    
    # 4. 전투 시에만 보이는 UI
    if gameState != 'SHOP':
        # 체력바 배경 현재 체력(초록색)
        pygame.draw.rect(screen, GREEN, (10, 10, max(0, (playerHp/stats['maxHp'])*200), 20))    
        screen.blit(fontS.render(f"{int(playerHp)} / {stats['maxHp']}", True, BLACK), (80, 10))
        
        # 정보 텍스트 (점수, 최고점수, 스테이지 정보 그룹화)
        infoTxt1 = fontS.render(f"SCORE: {score} | HI-SCORE: {highScore} | STAGE: {currentStage}", True, WHITE)
        screen.blit(infoTxt1, (10, 35))
        
        # 재화 및 특수기 개수 표기 (눈에 띄도록 골드 색상 강조)
        infoTxt2 = fontS.render(f"GOLD: {stats['gold']} G | SPECIAL (W): {stats['specialAmmo']} 개", True, GOLD)
        screen.blit(infoTxt2, (10, 55))
        
        # 제로 티켓 활성화 상태
        if zeroTicket: 
            screen.blit(fontS.render("★ ZERO TICKET ACTIVE ★", True, CYAN), (10, 75))
            
    # UI 업데이트 및 프레임 제한
    pygame.display.flip()
pygame.quit()