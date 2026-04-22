import pygame
import random
import math
import os
import hashlib
import json

# --- 0. 경로 설정 ---
IMGS_PATH = os.path.join(os.path.dirname(__file__), "imgs")

# --- 1. 초기화 및 화면 설정 ---
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Topdown Shooting Pygame: Limited Edition")

clock = pygame.time.Clock()

# --- 2. 에셋 로드 (화면 설정 후 로드해야 함) --
# 해킹을 막기 위한 비밀 키
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
stats["gold"] = 1000
playerHp = 100
score = 0
gameState = 'PLAYING'
shootCooldown = 0
specialEffectTimer = 0
shakeTimer = 0
zeroTicket = False 
STAGE_DURATION = 50 
stageTimer = STAGE_DURATION
bossAlertTimer = 0
currentStage = 1
invincibleTimer = 0
particles = []    
highScore = 0    
hitboxRadius = 10
bankBalance = 0
shopTab = "MARKET" # 현재 상점 탭 ("MARKET" 또는 "BANK")

# --- 덱 빌딩 & 시너지 시스템 변수 ---
inventory = []       # 최대 9개 장착 가능
pendingItem = None   # 인벤토리가 꽉 찼을 때 교체 대기 중인 아이템
shopOptions = []

SYNERGY_DATA = {
    "WEAPON": {
        2: {"name": "무기(2): 데미지 +5", "effect": {"damage": 5}},
        4: {"name": "무기(4): 데미지 +10, 관통", "effect": {"damage": 10, "pierce": True}}
    },
    "TECH": {
        2: {"name": "기술(2): 이동속도 +3", "effect": {"speed": 3}},
        4: {"name": "기술(4): 특수기 +3", "effect": {"specialAmmo": 3}}
    },
    "ARMOR": {
        2: {"name": "장갑(2): 최대체력 +50", "effect": {"maxHp": 50}},
        4: {"name": "장갑(4): 최대체력 +100", "effect": {"maxHp": 100}}
    }
}

ITEM_POOL = [
    {"id": "w1", "name": "화염 방사기", "tags": ["WEAPON", "TECH"], "price": 500, "desc": "무기, 기술"},
    {"id": "w2", "name": "초합금 검", "tags": ["WEAPON"], "price": 300, "desc": "무기"},
    {"id": "a1", "name": "나노 슈트", "tags": ["TECH", "ARMOR"], "price": 600, "desc": "기술, 장갑"},
    {"id": "a2", "name": "강철 방패", "tags": ["ARMOR"], "price": 400, "desc": "장갑"},
    {"id": "w3", "name": "플라즈마 캐논", "tags": ["WEAPON", "TECH"], "price": 700, "desc": "무기, 기술"},
    {"id": "a3", "name": "반응형 장갑", "tags": ["ARMOR", "WEAPON"], "price": 500, "desc": "장갑, 무기"},
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
    for item in inventory:
        for tag in item["tags"]:
            synergy_counts[tag] = synergy_counts.get(tag, 0) + 1
            
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

def getShopItems():
    return [{"data": item, "sold": False} for item in random.sample(ITEM_POOL, 3)]

# 스테이지 클리어 시 이자 계산 (기존 gameState = 'SHOP' 변경 직전에 배치)
def apply_interest():
    global bankBalance
    interest = int(bankBalance * 0.15)
    bankBalance += interest

# --- 5. 클래스 정의 ---
class BossAssetManager:
    _cache = {}

    # 1. 보스별 개별 설정 (이름: (가로, 세로, 확장자)) / 여기에 새 보스를 추가하기만 하면 자동으로 로드됩니다.
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
                # 0. 동적 파일 형식 지원 (png, gif 등 ext 설정에 따름)
                img = pygame.image.load(path).convert_alpha()
                images[key] = pygame.transform.scale(img, size)
            except Exception as e:
                print(f"Asset Error [{file_name}]: {e}")
                # 대체 이미지 생성 (설정된 사이즈에 맞게)
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
    def __init__(self, x, y, vel, color, dmg, radius=5):
        self.pos = pygame.Vector2(x, y)
        self.vel = vel
        self.color = color
        self.dmg = dmg
        self.radius = radius

    def update(self): 
        self.pos += self.vel

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
        pygame.draw.circle(surf, WHITE, (int(self.pos.x), int(self.pos.y)), self.radius - 2)

class HomingProjectile(Projectile):
    def __init__(self, x, y, vel, color, dmg, radius=5, turnSpeed=0.03):
        super().__init__(x, y, vel, color, dmg, radius)
        self.turnSpeed = turnSpeed
        self.timer = 0  # 폭발 타이머 추가
        self.maxLife = 360 
        
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
            # 전방향(360도)으로 퍼지는 속도 벡터 계산
            splitVel = pygame.Vector2(0, 4).rotate(angle)
            # 분열된 탄환은 일반 Projectile로 생성 (무한 분열 방지)
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
        # 가속 낙하 로직
        self.speed = min(14, self.speed + 0.6)
        direction = (self.target - self.pos)
        
        if direction.length() > 0:
            direction = direction.normalize()
        self.pos += direction * self.speed
        
        # 플레이어와 메테오 본체의 직접 충돌 판정
        if self.pos.distance_to(playerPos + pygame.Vector2(30, 30)) < self.radius + 10:
            return True # 충돌 발생 신호
            
        # 목표 지점에 도달하거나 화면을 완전히 벗어나면 폭발 및 소멸 처리 (안전장치 추가)
        if (self.target - self.pos).length() < 10 or self.pos.y > HEIGHT + 100:
            self.alive = False
        return False

    def draw(self, surf):
        shadow_surf = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)
        for r in range(self.radius, 0, -5):
            # r이 작아질수록(중심으로 갈수록) 알파값(진하기) 증가
            alpha = int(150 * (1 - r/self.radius)) 
            pygame.draw.circle(shadow_surf, (0, 0, 0, alpha), (self.radius * 2, self.radius * 2), r)
        surf.blit(shadow_surf, (self.target.x - self.radius * 2, self.target.y - self.radius * 2))
        surf.blit(self.img, (self.pos.x - self.radius, self.pos.y - self.radius))

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

    def update(self, eProjs, pPos):
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

class BossCrusher:
    def __init__(self):
        self.type = "Crusher"
        self.hp = 800
        self.maxHp = 800
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
            # 화면을 가득 채우지만 매우 느리고 틈이 넓은 양방향 나선 탄막 아트
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

class BossRock:
    def __init__(self):
        self.type = "ROCK"
        self.pos = pygame.Vector2(WIDTH // 2, 120)
        self.hp = 18
        self.maxHp = 18000
        self.timer = 0
        self.meteors = []
        self.images = BossAssetManager.get_images("bossRock")
        self.currentImg = self.images["STAND"]
        self.phase = 1

    def _spawn_meteor(self, targetPos):
        self.meteors.append(Meteor(targetPos))

    def _explode_meteor(self, meteor, eProjs, piece_count=12, homing_count=0):
        # 메테오 폭발 시 파편(탄막) 사방으로 방출 (Danmaku 스타일)
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

        # 대지의 중압감을 표현하는 묵직한 좌우 이동
        self.pos.x = WIDTH // 2 + math.sin(self.timer * 0.01) * 200 

        if self.phase == 1:
            # [기] 무차별 낙하: 운석우 + 보스의 기본 산탄
            # 패턴 1: 무작위 지역에 끊임없는 메테오
            if self.timer % 25 == 0:
                self._spawn_meteor(pygame.Vector2(random.randint(50, WIDTH-50), random.randint(100, HEIGHT-50)))
            # 패턴 2: 보스 본체에서 발사되는 묵직한 5갈래 부채꼴 산탄
            if self.timer % 40 == 0:
                for angle in [-40, -20, 0, 20, 40]:
                    dirVec = pygame.Vector2(0, 5).rotate(angle)
                    eProjs.append(Projectile(self.pos.x, self.pos.y, dirVec, GOLD, 15, 6))
            
        elif self.phase == 2:
            # [승] 정밀 타격과 화산 폭발
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
            # [전] 메테오 트랩: 갇힌 공간에서의 회피
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
            # [결] 카타클리즘(대재앙): 화면 전체를 뒤덮는 메테오와 파편, 유도탄의 축제
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
                frag_count = 12 + (self.phase * 4) # 4페이즈엔 폭발당 28개의 파편
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

class BossSwarm:
    def __init__(self):
        self.type = "SWARM"
        self.hp = 10000 # 탄막이 화려해진 만큼 체력 소폭 상향
        self.maxHp = 10000
        self.centers = [pygame.Vector2(random.randint(100,800), random.randint(50,200)) for _ in range(8)]
        self.timer = 0
        self.spinAngle = 0
        self.images = BossAssetManager.get_images("bossSwarm")
        self.currentImg = self.images["STAND"]
        self.phase = 1

    def update(self, eProjs, pPos):
        self.timer += 1
        
        # 기승전결 2분 컷 (페이즈당 약 30초 = 1125프레임)
        if self.timer < 1125: self.phase = 1      
        elif self.timer < 2250: self.phase = 2    
        elif self.timer < 3375: self.phase = 3    
        else: self.phase = 4                      

        self.currentImg = self.images["ATTACK"] if self.timer % 20 < 10 else self.images["STAND"]
        self.spinAngle += 2

        if self.phase == 1:
            # [기] 군단의 개화: 8각 진형 회전 + 다중 나선탄 + 정밀 저격
            targetCenter = pygame.Vector2(WIDTH//2, 150)
            for i in range(8):
                rad = math.radians(self.spinAngle * 0.5 + i * 45)
                self.centers[i] = self.centers[i].lerp(targetCenter + pygame.Vector2(math.cos(rad)*150, math.sin(rad)*150), 0.1)
                
                # 패턴 1: 끊임없이 피어나는 나선 탄막
                if self.timer % 10 == 0:
                    dirVec = pygame.Vector2(math.cos(rad*2), math.sin(rad*2)) * 4
                    eProjs.append(Projectile(self.centers[i].x, self.centers[i].y, dirVec, PURPLE, 6, 5))
                # 패턴 2: 엇박자 플레이어 조준탄
                if self.timer % 90 == i * 11:
                    dirVec = (pPos - self.centers[i]).normalize() * 6
                    eProjs.append(Projectile(self.centers[i].x, self.centers[i].y, dirVec, RED, 8, 5))
                # 패턴 3: 중앙 집중 폭발탄
                if self.timer % 150 == 0:
                    eProjs.append(Projectile(self.centers[i].x, self.centers[i].y, (targetCenter - self.centers[i]).normalize() * 3, CYAN, 12, 6))

        elif self.phase == 2:
            # [승] 분단과 교차: 좌우 4기씩 분열하여 X자 교차 탄막 형성
            for i in range(8):
                side_x = 100 if i < 4 else WIDTH - 100
                targetY = 100 + (i % 4) * 100 + math.sin(self.timer * 0.1) * 30
                self.centers[i] = self.centers[i].lerp(pygame.Vector2(side_x, targetY), 0.05)

                # 패턴 1: 화면을 가로지르는 격자형 탄막망
                if self.timer % 15 == 0:
                    dir_x = 5 if i < 4 else -5
                    eProjs.append(Projectile(self.centers[i].x, self.centers[i].y, pygame.Vector2(dir_x, 0), CYAN, 7, 5))
                # 패턴 2: 대각선 교차 지향탄
                if self.timer % 40 == 0:
                    dirVec = pygame.Vector2(1 if i < 4 else -1, 1).normalize() * 4
                    eProjs.append(Projectile(self.centers[i].x, self.centers[i].y, dirVec, GOLD, 9, 6))
                # 패턴 3: 주기적인 유도탄 압박
                if self.timer % 120 == i * 15:
                    eProjs.append(HomingProjectile(self.centers[i].x, self.centers[i].y, pygame.Vector2(0, 3), PURPLE, 10, 7))

        elif self.phase == 3:
            # [전] 춤추는 탄막의 강: 위아래로 물결치며 쏟아지는 탄막의 비
            for i in range(8):
                targetX = 100 + i * (WIDTH - 200) / 7
                targetY = 150 + math.sin(self.timer * 0.05 + i) * 100
                self.centers[i] = self.centers[i].lerp(pygame.Vector2(targetX, targetY), 0.1)
                
                # 패턴 1: 물결 형태의 곡선 궤적 탄막
                if self.timer % 8 == 0:
                    eProjs.append(Projectile(self.centers[i].x, self.centers[i].y, pygame.Vector2(math.sin(self.timer*0.1), 5), WHITE, 6, 5))
                # 패턴 2: 부채꼴 확산탄
                if self.timer % 60 == 0 and i % 2 == 0:
                    for angle in [-20, 0, 20]:
                        dirVec = pygame.Vector2(0, 6).rotate(angle)
                        eProjs.append(Projectile(self.centers[i].x, self.centers[i].y, dirVec, RED, 8, 6))
                # 패턴 3: 무작위 산탄
                if self.timer % 20 == 0:
                    rand_dir = pygame.Vector2(random.uniform(-3, 3), random.uniform(2, 6))
                    eProjs.append(Projectile(self.centers[i].x, self.centers[i].y, rand_dir, CYAN, 5, 5))

        elif self.phase == 4:
            # [결] 군단 오버드라이브: 초고속 기동과 함께 만개하는 탄막의 꽃
            for i in range(8):
                self.centers[i].x += math.sin(self.timer * 0.3 + i) * 12
                self.centers[i].y += math.cos(self.timer * 0.2 + i) * 8
                self.centers[i].x = max(50, min(WIDTH-50, self.centers[i].x))
                self.centers[i].y = max(50, min(HEIGHT//2, self.centers[i].y))

                # 패턴 1: 탄막의 꽃 (초고속 전방위 발사)
                if self.timer % 6 == 0:
                    fire_rad = math.radians(self.spinAngle * 3 + i * 45)
                    eProjs.append(Projectile(self.centers[i].x, self.centers[i].y, pygame.Vector2(math.cos(fire_rad), math.sin(fire_rad)) * 6, GOLD, 8, 5))
                # 패턴 2: 플레이어 포위형 링 생성
                if self.timer % 90 == 0 and i == 0:
                    for a in range(0, 360, 30):
                        dirVec = pygame.Vector2(0, 4).rotate(a)
                        eProjs.append(Projectile(self.centers[i].x, self.centers[i].y, dirVec, PURPLE, 10, 6))
                # 패턴 3: 끝없는 유도탄
                if self.timer % 60 == i * 7:
                    eProjs.append(HomingProjectile(self.centers[i].x, self.centers[i].y, pygame.Vector2(0, -2), RED, 12, 7))

    def draw(self, surf):
        for p in self.centers:
            surf.blit(self.currentImg, (p.x - 25, p.y - 25))
        if self.centers:
            avg_x = sum(c.x for c in self.centers) / len(self.centers)
            avg_y = sum(c.y for c in self.centers) / len(self.centers)
            hpRatio = max(0, self.hp / self.maxHp)
            pygame.draw.rect(surf, RED, (avg_x - 60, avg_y - 70, 120, 8))
            pygame.draw.rect(surf, GREEN, (avg_x - 60, avg_y - 70, 120 * hpRatio, 8))

class BossZero:
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
            # [기] 육각성(Hexagram) 펄스
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
            # [승] 통제된 회전: 풍차 모양의 거대한 레이저 탄막
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
            # [전] 체크보드와 파도: 플레이어의 무빙을 강제하는 체스판 패턴
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
            # [결] 절대 영도 만다라: 극한의 밀도와 아름다움을 지닌 최종 패턴
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
        
class BossZombie:
    def __init__(self):
        self.type = "CRAZY"
        self.pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
        self.hp = 15000
        self.maxHp = 15000
        self.timer = 0
        self.rect = pygame.Rect(self.pos.x - 40, self.pos.y - 40, 80, 80)
        self.orbitBullets = []
        self.orbitAngle = 0
        self.phase = 1

    def update(self, eProjs, pPos, ctx=None):
        self.timer += 1
        
        # 600프레임(약 16초) 주기로 Zero 1 -> 2 -> 3 -> 4 -> 최종 병합 페이즈로 전환
        if self.timer < 600: self.phase = 1
        elif self.timer < 1200: self.phase = 2
        elif self.timer < 1800: self.phase = 3
        elif self.timer < 2400: self.phase = 4
        else: self.phase = 5

        self.pos.x = WIDTH // 2 + math.sin(self.timer * 0.03) * 150
        self.pos.y = 150 + math.cos(self.timer * 0.02) * 50
        self.rect.center = (self.pos.x, self.pos.y)

        if self.phase == 1:
            # 패턴 1: 화면 밖에서 수축하는 원형 탄막
            progress = (self.timer % 600) / 600.0
            currentRadius = 600 - (480 * progress)
            if self.timer % 6 == 0:
                for i in range(10):
                    angle = (i * (2 * math.pi / 10)) + (self.timer * 0.1)
                    spawnX = self.pos.x + math.cos(angle) * currentRadius
                    spawnY = self.pos.y + math.sin(angle) * currentRadius
                    dirVec = (self.pos - pygame.Vector2(spawnX, spawnY)).normalize() * 1.5
                    eProjs.append(Projectile(spawnX, spawnY, dirVec, CYAN, 10, 5))

        elif self.phase == 2:
            # 패턴 2: 궤도 고정 후 조준 사격
            self.orbitAngle += 0.05
            self.orbitBullets = [b for b in self.orbitBullets if b in eProjs]
            if len(self.orbitBullets) < 12 and self.timer % 10 == 0:
                newBullet = Projectile(self.pos.x, self.pos.y, pygame.Vector2(0, 0), CYAN, 10, 6)
                self.orbitBullets.append(newBullet)
                eProjs.append(newBullet)
            for i, bullet in enumerate(self.orbitBullets):
                angle = self.orbitAngle + (i * (2 * math.pi / 12))
                bullet.pos.x = self.pos.x + math.cos(angle) * 150
                bullet.pos.y = self.pos.y + math.sin(angle) * 150
                bullet.vel = pygame.Vector2(0, 0)
            if self.timer % 50 == 0 and self.orbitBullets:
                firedBullet = self.orbitBullets.pop(0)
                targetDir = (pPos - firedBullet.pos).normalize()
                firedBullet.vel = targetDir * 8
                firedBullet.color = RED

        elif self.phase == 3:
            # 패턴 3: 거대한 궤도에서 작아지는 탄막 소환
            progress = (self.timer % 600) / 600.0
            currentRadius = 2100 - (2075 * progress) 
            if self.timer % 4 == 0:
                for i in range(8):
                    angle = (i * (2 * math.pi / 8)) + (self.timer * 0.15)
                    spawnX = self.pos.x + math.cos(angle) * currentRadius
                    spawnY = self.pos.y + math.sin(angle) * currentRadius
                    dirVec = (self.pos - pygame.Vector2(spawnX, spawnY)).normalize() * 3.0
                    eProjs.append(Projectile(spawnX, spawnY, dirVec, PURPLE, 10, 5))

        elif self.phase == 4:
            # 패턴 4: 거대한 궤도를 그리며 회전, 점점 좁혀지다 발사
            self.orbitAngle += 0.05
            progress = (self.timer % 600) / 600.0
            currentRadius = 525 - (450 * progress) 
            self.orbitBullets = [b for b in self.orbitBullets if b in eProjs]
            if len(self.orbitBullets) < 16 and self.timer % 8 == 0:
                newBullet = Projectile(self.pos.x, self.pos.y, pygame.Vector2(0, 0), CYAN, 10, 6)
                self.orbitBullets.append(newBullet)
                eProjs.append(newBullet)
            for i, bullet in enumerate(self.orbitBullets):
                angle = self.orbitAngle + (i * (2 * math.pi / 16))
                bullet.pos.x = self.pos.x + math.cos(angle) * currentRadius
                bullet.pos.y = self.pos.y + math.sin(angle) * currentRadius
                bullet.vel = pygame.Vector2(0, 0)
            if self.timer % 40 == 0 and self.orbitBullets:
                firedBullet = self.orbitBullets.pop(0)
                targetDir = (pPos - firedBullet.pos).normalize()
                firedBullet.vel = targetDir * 9
                firedBullet.color = RED

        elif self.phase == 5:
            # 패턴 5: 모든 속성을 합친 지옥의 탄막 아트
            self.orbitAngle += 0.08
            if self.timer % 12 == 0:
                for i in range(6):
                    angle = (i * (2 * math.pi / 6)) + self.orbitAngle
                    spawnX = self.pos.x + math.cos(angle) * 200
                    spawnY = self.pos.y + math.sin(angle) * 200
                    dirVec = (self.pos - pygame.Vector2(spawnX, spawnY)).normalize() * 2.5
                    eProjs.append(Projectile(spawnX, spawnY, dirVec, PURPLE, 10, 5))
            if self.timer % 30 == 0:
                for xGate in range(0, WIDTH + 1, 180):
                    zigzagX = math.sin(self.timer * 0.15 + xGate) * 5
                    vel = pygame.Vector2(zigzagX, 6)
                    eProjs.append(Projectile(xGate, -20, vel, WHITE, 8, 4))
            if self.timer % 90 == 0: 
                eProjs.append(HomingProjectile(self.pos.x, self.pos.y, pygame.Vector2(0, -4), GOLD, 15, 8))

    def draw(self, surf):
        hpRatio = max(0, self.hp / self.maxHp)
        pygame.draw.rect(surf, (100, 100, 100), (self.pos.x - 60, self.pos.y + 80, 120, 10))
        pygame.draw.rect(surf, (255, 50, 50), (self.pos.x - 60, self.pos.y + 80, 120 * hpRatio, 10))
        
        color = [WHITE, CYAN, PURPLE, GOLD, RED, BLACK][min(self.phase, 5)]
        pygame.draw.circle(surf, color, (int(self.pos.x), int(self.pos.y)), 25, 3)
        pygame.draw.circle(surf, WHITE, (int(self.pos.x), int(self.pos.y)), 10)

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
        
        # type3의 회전하는 투사체 시각화 (STAND 전환 전까지)
        if self.state == "ATTACK" and self.eType == "type3":
            for angle in getattr(self, 'orbitAngles', []):
                offset = pygame.Vector2(0, 25).rotate(angle)
                pygame.draw.circle(surf, GOLD, (int(self.pos.x+25 + offset.x), int(self.pos.y+25 + offset.y)), 5)

# --- 6. 메인 게임 루프 ---
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
                if event.key == pygame.K_s:
                    apply_interest()
                    gameState = 'PLAYING'
                    currentStage += 1
                    stageTimer = STAGE_DURATION

        # 마우스 클릭 처리 (UI 분리 및 로직 통합)
        if event.type == pygame.MOUSEBUTTONDOWN and gameState == 'SHOP':
            mousePos = pygame.mouse.get_pos()
            
            # 1. 인벤토리가 꽉 차서 교체 대기 중일 때 인벤토리 클릭 처리
            if pendingItem is not None:
                for i in range(len(inventory)):
                    row = i // 3
                    col = i % 3
                    slotRect = pygame.Rect(550 + col * 100, 100 + row * 100, 90, 90)
                    if slotRect.collidepoint(mousePos):
                        inventory[i] = pendingItem["data"] # 기존 아이템 대체
                        pendingItem["sold"] = True
                        pendingItem = None
                        calculate_stats()
                        break
            else:
                # 2. 상점 아이템 구매 클릭 처리
                for i, opt in enumerate(shopOptions):
                    card_rect = pygame.Rect(50 + i * 160, 100, 150, 200)
                    if card_rect.collidepoint(mousePos) and not opt["sold"] and stats["gold"] >= opt["data"]["price"]:
                        stats["gold"] -= opt["data"]["price"]
                        
                        if len(inventory) < 9:
                            # 자리 여유 시 즉시 장착
                            inventory.append(opt["data"])
                            opt["sold"] = True
                            calculate_stats()
                        else:
                            # 9칸 꽉 찼을 경우 교체 대기 상태 진입
                            pendingItem = opt
                    
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
                elif currentStage == 1:
                    # boss = BossSwarm()
                    # boss = BossZero()
                    boss = BossRock()
                    # boss = BossChernobog()
                    # boss = BossCrusher()
                    # boss = BossZombie()
                elif currentStage == 2:
                    boss = BossSwarm()
                elif currentStage == 3:
                    boss = BossChernobog()
                else:
                    # 모든 지정된 스테이지 이후에는 무작위 혹은 기본 보스
                    boss = random.choice([BossRock(), BossSwarm()])

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
                shopOptions = getShopItems()

# --- [준비 단계] 공통 변수 계산 (DRY 원칙) ---

        # --- 1. 적(Enemies) 업데이트 및 플레이어 충돌 판정 ---
        for e in enemies[:]:
            e.update(eProjs, playerPos) 
            eCenter = pygame.Vector2(e.pos.x + 15, e.pos.y + 15)

            # [수정 5] type4 좌우 반사 로직 (화면 밖 제거 대신 반사)
            if getattr(e, 'eType', "") == "type4":
                if e.pos.x <= 0 or e.pos.x >= WIDTH - 10:
                    e.vx *= -1
            
            # 플레이어 본체와 적 충돌 (원형 판정)
            if playerCenter.distance_to(eCenter) < hitboxRadius + 15 and invincibleTimer <= 0:
                playerHp -= 15; shakeTimer = 15; invincibleTimer = 40
                if e in enemies: enemies.remove(e)
                continue

            # 화면 하단 이탈 시 제거 (리스폰을 위함)
            if e.pos.y > HEIGHT + 50:
                if e in enemies: enemies.remove(e)
                continue

        # --- 2. 적 투사체(eProjs) 업데이트 및 플레이어 피격 판정 ---
        # 중복 루프를 하나로 합쳐 속도 문제를 해결했습니다.
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

            # 플레이어 피격 판정 (원형 10px 기준)
            p_radius = getattr(p, 'radius', 5)
            if p.pos.distance_to(playerCenter) < hitboxRadius + p_radius and invincibleTimer <= 0:
                playerHp -= p.dmg
                if p in eProjs: eProjs.remove(p)
                shakeTimer = 10; invincibleTimer = 30
            elif p.pos.y > HEIGHT: 
                if p in eProjs: eProjs.remove(p)

        # --- 플레이어 투사체(pProjs) 업데이트 및 적/보스 피격 판정 ---
        for p in pProjs[:]:
            p.update()
            hitThisFrame = False

            # 보스 피격 판정
            if boss:
                hit = False
                hitSwarmWeak = False 
                
                if boss.type == "CHERNOBOG" and boss.rect.collidepoint(p.pos): hit = True
                elif boss.type == "SWARM":
                    for i, c in enumerate(boss.centers):
                        if p.pos.distance_to(c) < 25: 
                            hit = True
                            if i == getattr(boss, 'weakIndex', -1): hitSwarmWeak = True
                            break
                elif boss.type == "ZERO" and p.pos.distance_to(boss.pos + pygame.Vector2(25,25)) < 40: hit = True
                elif boss.type == "ROCK" and p.pos.distance_to(boss.pos) < 60: hit = True # 판정 범위 상향
                elif boss.type == "Crusher" and p.pos.distance_to(boss.pos) < 60: hit = True

                if hit:
                    actualDmg = p.dmg
                    if boss.type == "SWARM":
                        actualDmg = p.dmg if hitSwarmWeak else p.dmg * 0.0001
                    
                    boss.hp -= actualDmg
                    hitThisFrame = True
                    if sndHit: sndHit.play() 
                    for _ in range(5): particles.append(Particle(p.pos.x, p.pos.y, (255, 200, 50)))

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
                            stats["gold"] += 35; score += 100
                            for _ in range(10): particles.append(Particle(eCenter.x, eCenter.y, (255, 50, 50)))
                        break # 한 발당 적 하나(관통 없을 시)

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
        tempSurf.fill((15, 15, 25)) # 배경색 변경
        
        # 상단 정보 (이름 변경 및 특수 스킬 횟수 추가)
        tempSurf.blit(fontL.render("SUPPLY MARKET", True, GOLD), (50, 20))
        info_text = f"보유 골드: {stats['gold']} G | 예금: {bankBalance} G | 특수기: {stats['specialAmmo']}회"
        tempSurf.blit(fontM.render(info_text, True, WHITE), (50, 65))

        # 탭 메뉴 (MARKET / BANK)
        # [M] Market, [B] Bank 키 입력 등으로 전환 가능하게 구현

        if shopTab == "MARKET":
            # 1. 왼쪽: 시너지 창 (크기 축소 및 왼쪽 배치)
            syn_rect = pygame.Rect(30, 120, 220, 350)
            pygame.draw.rect(tempSurf, (30, 30, 45), syn_rect, border_radius=10)
            tempSurf.blit(fontS.render("활성 시너지", True, GOLD), (45, 130))
            # 시너지 아이콘/텍스트 출력 로직 (생략)

            # 2. 중앙: 판매 아이템
            for i, opt in enumerate(shopOptions):
                card_rect = pygame.Rect(270 + i * 160, 120, 140, 220)
                # 아이템 카드 그리기...

            # 3. 오른쪽: 인벤토리 (위치 고정)
            inv_start_x = 760
            tempSurf.blit(fontS.render(f"INV ({len(inventory)}/9)", True, WHITE), (inv_start_x, 100))
            for i in range(9):
                r, c = i // 3, i % 3
                slot = pygame.Rect(inv_start_x + c * 45, 120 + r * 45, 40, 40)
                pygame.draw.rect(tempSurf, (50, 50, 70), slot)

        elif shopTab == "BANK":
            # 은행 UI: 입금/출금 버튼 및 이율 정보 표시
            tempSurf.blit(fontM.render("중앙 은행 (이율 15%)", True, CYAN), (350, 200))
            tempSurf.blit(fontS.render(f"현재 예금: {bankBalance} G", True, WHITE), (380, 250))
            tempSurf.blit(fontS.render("[D] 100G 입금 | [W] 전액 출금", True, GRAY), (350, 300))


            if pendingItem:
                tempSurf.blit(fontM.render("교체할 인벤토리 아이템을 클릭하세요!", True, RED), (500, 50))

            # 1. 상점 판매 슬롯 (좌측)
            for i, opt in enumerate(shopOptions):
                cardRect = pygame.Rect(50 + i * 160, 100, 150, 200)
                c = (40, 40, 40) if opt["sold"] else (30, 30, 50)
                borderColor = RED if pendingItem == opt else GRAY
                
                pygame.draw.rect(tempSurf, c, cardRect, border_radius=10)
                pygame.draw.rect(tempSurf, borderColor, cardRect, 2, border_radius=10)
                
                if not opt["sold"]:
                    tempSurf.blit(fontM.render(opt['data']['name'], True, WHITE), (cardRect.x + 10, cardRect.y + 20))
                    tempSurf.blit(fontS.render(opt['data']['desc'], True, CYAN), (cardRect.x + 10, cardRect.y + 60))
                    pColor = GOLD if stats["gold"] >= opt['data']['price'] else RED
                    tempSurf.blit(fontM.render(f"{opt['data']['price']} G", True, pColor), (cardRect.x + 10, cardRect.y + 160))

            # 2. 인벤토리 3x3 그리드 (우측 상단)
            tempSurf.blit(fontM.render(f"인벤토리 ({len(inventory)}/9)", True, WHITE), (550, 60))
            for i in range(9):
                row = i // 3
                col = i % 3
                slotRect = pygame.Rect(550 + col * 100, 100 + row * 100, 90, 90)
                pygame.draw.rect(tempSurf, (45, 45, 65), slotRect, border_radius=5)
                pygame.draw.rect(tempSurf, GRAY, slotRect, 2, border_radius=5)
                
                if i < len(inventory):
                    item = inventory[i]
                    # 아이템 이름 출력 (너무 길면 잘림 방지)
                    name_txt = fontS.render(item["name"][:5], True, WHITE)
                    tempSurf.blit(name_txt, (slotRect.x + 10, slotRect.y + 35))

            # 3. 활성화된 시너지 및 현재 스탯 요약 (하단)
            pygame.draw.rect(tempSurf, (30, 30, 40), (50, 330, 800, 150), border_radius=10)
            tempSurf.blit(fontM.render("- 활성화된 시너지 효과 -", True, GOLD), (70, 340))
            
            # 현재 태그 개수 계산
            synergy_counts = {}
            for item in inventory:
                for tag in item["tags"]:
                    synergy_counts[tag] = synergy_counts.get(tag, 0) + 1
                    
            syn_y = 380
            syn_x = 70
            for tag, count in synergy_counts.items():
                if tag in SYNERGY_DATA:
                    for req, data in sorted(SYNERGY_DATA[tag].items()):
                        if count >= req:
                            tempSurf.blit(fontS.render(data["name"], True, CYAN), (syn_x, syn_y))
                            syn_y += 25
                            if syn_y > 450:
                                syn_y = 380
                                syn_x += 250

            # 스탯 렌더링
            stat_text = f"DMG: {stats['damage']} | SPD: {stats['speed']} | MAX_HP: {stats['maxHp']} | 관통: {'ON' if stats['pierce'] else 'OFF'} | W: {stats['specialAmmo']}"
            tempSurf.blit(fontS.render(stat_text, True, WHITE), (300, HEIGHT - 30))
    
    # 1. 가장 밑바닥에 배경 먼저 그리기
    screen.blit(bgImg, (0, 0))
    screen.blit(tempSurf, (0, 0))
        
    # 3. W 특수기 효과 (화면 반전) - 배경 위에 그려야 효과가 보임!
    if specialEffectTimer > 0:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        alpha = min(255, specialEffectTimer * 10) 
        overlay.fill((255, 255, 255, alpha))
        screen.blit(overlay, (0, 0))
        specialEffectTimer -= 1 
    
    # 4. 전투 시에만 보이는 UI (상점에서는 숨김 처리)
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