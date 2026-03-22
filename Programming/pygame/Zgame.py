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

# --- 3. 게임 상태 관리 변수 ---
stats = {"damage": 10, "speed": 5, "gold": 1000, "maxHp": 100, "pierce": False, "specialAmmo": 3}
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

shopTab = "ITEM"
stocks = {"A": 100, "B": 100, "C": 100}
bankBalance = 0
    
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

# 지분에 따른 할인율 계산 함수
def getDiscountRatio():
    ratio = 2.0 - (stocks["C"] / 100.0) #(C구역: 정밀 합금 기업이 물가 담당)
    return max(0.5, min(2.0, ratio))

def loadHighscore():
    if os.path.exists("highscore.txt"):
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read())
        except Exception:
            return 0
    return 0

highScore = loadHighscore()

# --- [신규] 보안 및 다국어 시스템 ---
def saveGameSecure(data, filename="save.dat"):
    data_str = json.dumps(data, sort_keys=True)
    signature = hashlib.sha256((data_str + secretSalt).encode()).hexdigest()
    with open(filename, "w") as f:
        json.dump({"payload": data, "signature": signature}, f)

LANG_DB = {
    "ko": {"shop_title": "시스템 업그레이드", "core_warn": "코어 감지됨", "start": "전투 개시"},
    "en": {"shop_title": "SYSTEM UPGRADE", "core_warn": "CORE DETECTED", "start": "START BATTLE"}
}
current_lang = "ko"
def _t(key): return LANG_DB[current_lang].get(key, key)

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
            
        # 목표 지점에 도달하면 폭발
        if (self.target - self.pos).length() < 10:
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
        # 에셋 매니저에서 이미지 로드 (없을 시 기본 사각형 반환)
        self.images = BossAssetManager.get_images("bossChernobog")
        self.currentImg = self.images["STAND"]

    def update(self, eProjs, pPos):
        self.timer += 1
        self.rect.topleft = (self.pos.x - 60, self.pos.y - 60)
        
        # 거대 십자 탄막 패턴
        if self.timer % 60 == 0:
            for angle in range(0, 360, 45):
                dirVec = pygame.Vector2(0, 6).rotate(angle)
                eProjs.append(Projectile(self.pos.x, self.pos.y, dirVec, PURPLE, 15, 12))

    def draw(self, surf):
        surf.blit(self.currentImg, (self.pos.x - 75, self.pos.y - 75))
        hpRatio = max(0, self.hp / self.maxHp)
        pygame.draw.rect(surf, GREEN, (self.pos.x - 50, self.pos.y + 80, 100 * hpRatio, 8))
        
class BossCounter:
    def __init__(self):
        self.type = "ZERO"
        self.pos = pygame.Vector2(WIDTH // 2, 200) # 중앙 배치
        self.hp = 3500
        self.maxHp = 3500
        self.timer = 0
        self.pattern_cycle = 15 * 37.5  # 15초 주기 (FPS 37.5 기준)
        self.rect = pygame.Rect(self.pos.x - 40, self.pos.y - 40, 80, 80)
        self.angle_offset = 0

    def update(self, eProjs, pPos, ctx=None):
        self.timer += 1
        current_time = self.timer % self.pattern_cycle
        phase_1_end = 10 * 37.5 # 10초 지점
        
        # 보스 위치를 부드럽게 8자 모양으로 이동 (공격 범위 분산)
        self.pos.x = WIDTH // 2 + math.sin(self.timer * 0.05) * 100
        self.pos.y = 150 + math.cos(self.timer * 0.03) * 50
        self.rect.center = (self.pos.x, self.pos.y)

        # --- 패턴 1: 0~10초 - 화면 밖에서 수축하는 원형 탄막 ---
        if current_time < phase_1_end:
            # 15프레임마다 한 번씩 원형 탄막 생성
            if self.timer % 15 == 0:
                num_bullets = 24 # 한 원에 생성될 탄알 수
                radius = 600 - (current_time * 1.2) # 시간에 따라 소환 반경이 줄어듦
                radius = max(200, radius) # 최소 200px 거리 유지
                
                self.angle_offset += 10 # 소환 각도를 틀어 나선형 느낌 부여
                
                for i in range(num_bullets):
                    angle = math.radians(i * (360 / num_bullets) + self.angle_offset)
                    # 화면 밖(반경 radius) 지점에서 위치 계산
                    spawn_x = self.pos.x + math.cos(angle) * radius
                    spawn_y = self.pos.y + math.sin(angle) * radius
                    
                    # 중앙(보스)을 향해 서서히 수축하는 속도 벡터
                    vel = (self.pos - pygame.Vector2(spawn_x, spawn_y)).normalize() * 3.5
                    
                    # 아트 효과: 시간대에 따라 색상 교차 (청록 -> 보라)
                    color = CYAN if self.timer % 30 == 0 else PURPLE
                    eProjs.append(Projectile(spawn_x, spawn_y, vel, color, 12, 6))

        # --- 패턴 2: 10~15초 - 위에서 아래로 지그재그 하강 탄막 ---
        else:
            # 더 촘촘하게 발사 (5프레임 주기)
            if self.timer % 5 == 0:
                # 화면 가로폭을 일정 간격으로 나누어 여러 줄 생성
                for x_gate in range(0, WIDTH + 1, 120):
                    # 지그재그 효과: sin 함수를 사용하여 수평 속도 조절
                    zigzag_x = math.sin(self.timer * 0.2 + x_gate) * 4 
                    vel = pygame.Vector2(zigzag_x, 6) # 아래로 빠른 속도로 하강
                    
                    # 시작 위치는 화면 상단
                    spawn_x = x_gate + math.cos(self.timer * 0.1) * 30
                    eProjs.append(Projectile(spawn_x, -20, vel, WHITE, 10, 5))

        # 보너스: 보스 주변을 보호하는 회전 영혼 (항시 발동)
        if self.timer % 3 == 0:
            rot_vel = pygame.Vector2(5, 0).rotate(self.timer * 8)
            eProjs.append(Projectile(self.pos.x, self.pos.y, rot_vel, BLACK, 8, 4))

    def draw(self, surf):
        # 체력바 드로우
        hpRatio = max(0, self.hp / self.maxHp)
        pygame.draw.rect(surf, GRAY, (self.pos.x - 50, self.pos.y + 60, 100, 8))
        pygame.draw.rect(surf, RED, (self.pos.x - 50, self.pos.y + 60, 100 * hpRatio, 8))
        
        # 보스 본체 연출 (오라 효과)
        pulse = math.sin(pygame.time.get_ticks() * 0.01) * 10
        pygame.draw.circle(surf, (100, 0, 150, 100), (int(self.pos.x), int(self.pos.y)), 40 + int(pulse))
        # 실제 이미지는 메인 루프에서 그릴 수도 있으나, 클래스 내 draw가 있다면 아래 추가 가능
        # surf.blit(이미지, 좌표)
            
class BossCrusher:
    def __init__(self):
        self.type = "Crusher"
        self.hp = 500; self.maxHp = 500
        self.pos = pygame.Vector2(WIDTH//2, 50)
        self.homePos = pygame.Vector2(WIDTH//2, 50)
        self.mode = "IDLE"
        self.timer = 0
        self.hitboxRadius = 50 
        self.targetPos = None
        self.spinAngle = 0
        self.images = BossAssetManager.get_images("bossCrusher")
        self.currentImg = self.images["STAND"]

    def update(self, eProjs, pPos): 
        self.timer += 1
        # 9. 돌진 -> 정지 후 회전 사격 -> 부메랑 복귀 로직
        if self.mode == "IDLE":
            if self.timer > 90:
                self.mode = "DASH"
                self.targetPos = pygame.Vector2(pPos.x, pPos.y)
                self.timer = 0
        elif self.mode == "DASH":
            self.currentImg = self.images["ATTACK"]
            dirVec = self.targetPos - self.pos
            if dirVec.length() > 15:
                self.pos += dirVec.normalize() * 15
            else:
                self.mode = "SPIN_SHOOT"
                self.timer = 0
        elif self.mode == "SPIN_SHOOT":
            self.currentImg = self.images["ATTACK"]
            self.spinAngle += 15
            # 추후 거대한 투사체 이미지로 교체를 위한 Projectile 반경 15 설정
            if self.timer % 8 == 0:
                dirVec = pygame.Vector2(0, 6).rotate(self.spinAngle)
                eProjs.append(Projectile(self.pos.x, self.pos.y, dirVec, RED, 10, 15))
            if self.timer > 120: # 약 3~4초 유지
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
        # 개별 체력바 표기
        hpRatio = max(0, self.hp / self.maxHp)
        pygame.draw.rect(surf, RED, (self.pos.x - 30, self.pos.y + 60, 60, 6))
        pygame.draw.rect(surf, GREEN, (self.pos.x - 30, self.pos.y + 60, 60 * hpRatio, 6))

class BossRock:
    def __init__(self):
        self.type = "ROCK"
        self.pos = pygame.Vector2(WIDTH // 2, 120)
        self.hp = 1350; self.maxHp = 1350
        self.state = "IDLE"
        self.timer = 0
        self.meteors = []
        self.images = BossAssetManager.get_images("bossRock")
        self.currentImg = self.images["STAND"]


    def _spawn_meteor(self, playerPos):
        # 플레이어 근처 무작위 지점을 타겟으로 설정
        offset = pygame.Vector2(random.randint(-150, 150), random.randint(-120, 120))
        target = playerPos + offset
        # 화면 밖으로 나가지 않게 제한
        target.x = max(50, min(WIDTH - 50, target.x))
        target.y = max(50, min(HEIGHT - 50, target.y))
        self.meteors.append(Meteor(target))

    def _explode_meteor(self, meteor, eProjs):
        for angle in range(0, 360, 40):
            dirVec = pygame.Vector2(0, 3).rotate(angle)
            eProjs.append(Projectile(meteor.target.x, meteor.target.y, dirVec, RED, 10, 6))

    def update(self, eProjs, playerPos):
        self.timer += 1
        global playerHp, shakeTimer, invincibleTimer

        if self.state == "IDLE":
            if self.timer > 90:
                self.state = "METEOR_PREP"
                self.timer = 0
        
        elif self.state == "METEOR_PREP":
            if self.timer % 5 == 0 and self.timer <= 80:
                self._spawn_meteor(playerPos)
            if self.timer > 120:
                self.state = "METEOR_RAIN"
                self.timer = 0
        
        elif self.state == "METEOR_RAIN":
            for meteor in self.meteors[:]:
                hitPlayer = meteor.update(playerPos)
                
                # 메테오에 직접 맞았을 때
                if hitPlayer and invincibleTimer <= 0:
                    playerHp -= 20
                    invincibleTimer = 40
                    shakeTimer = 20
                    meteor.alive = False # 맞으면 즉시 터짐

                if not meteor.alive:
                    self._explode_meteor(meteor, eProjs)
                    self.meteors.remove(meteor)
            
            if not self.meteors and self.timer > 60:
                self.state = "IDLE"
                self.timer = 0
                
class BossSwarm:
    def __init__(self):
        self.type = "SWARM"
        self.hp = 250; self.maxHp = 250
        self.centers = [pygame.Vector2(random.randint(100,800), random.randint(50,200)) for _ in range(8)]
        self.fireTimers = [random.randint(60, 150) for _ in range(8)]
        self.maxTimers = list(self.fireTimers) 
        self.weakIndex = random.randint(0, 7)
        self.state = "SCATTER" 
        self.stateTimer = 0
        self.hitboxRadius = 25
        self.spinAngle = 0
        self.images = BossAssetManager.get_images("bossSwarm")
        self.currentImg = self.images["STAND"]

    def update(self, eProjs, pPos):
        self.stateTimer += 1
        
        # 일정 시간마다 패턴 변환
        if self.stateTimer > 300:
            self.state = "GATHER" if self.state == "SCATTER" else "SCATTER"
            self.stateTimer = 0
            if self.state == "SCATTER":
                self.weakIndex = random.randint(0, 7)
                self.currentImg = self.images["STAND"]
        
        if self.state == "SCATTER":
            for i in range(8):
                self.centers[i].x += math.sin(pygame.time.get_ticks() / 500 + i) * 7
                self.fireTimers[i] -= 1
                
                if self.fireTimers[i] <= 0:
                    waitRatio = self.maxTimers[i] / 60.0 
                    pSize = int(4 + (waitRatio * 3))     
                    pDmg = int(5 + (waitRatio * 2))      
                    
                    diff = pPos - self.centers[i]
                    dirVec = diff.normalize() * 4 if diff.length() > 0 else pygame.Vector2(0, 4)
                    
                    eProjs.append(Projectile(self.centers[i].x, self.centers[i].y, dirVec, PURPLE, pDmg, pSize))
                    self.fireTimers[i] = random.randint(60, 150)
                    self.maxTimers[i] = self.fireTimers[i]

        elif self.state == "GATHER":
            targetCenter = pygame.Vector2(WIDTH//2, 150)
            
            # 1. 이동 및 회전 공격 단계 (120~350프레임)
            if 120 <= self.stateTimer < 350:
                # 보스 개체들이 회전하는 속도 (이 값을 키우면 보스들이 더 빨리 돕니다)
                self.spinAngle += 3 
                self.currentImg = self.images["ATTACK"] # 공격 모션 유지
                
                for i in range(8):
                    # 보스 개체들의 위치를 원형으로 회전시킴 (반지름 120의 원)
                    # i * 45는 8개 개체를 360도에 균등 배분 (360/8 = 45)
                    orbitAngle = self.spinAngle + (i * 45)
                    rad = math.radians(orbitAngle)
                    
                    # 새로운 위치 계산 (중앙점 + 회전 좌표)
                    self.centers[i].x = targetCenter.x + math.cos(rad) * 120
                    self.centers[i].y = targetCenter.y + math.sin(rad) * 120
                    self.currentImg = self.images["ATTACK"]
                
                # 탄막 발사 로직 (5프레임 간격)
                if self.stateTimer % 5 == 0:
                    for i in range(8):
                        # 발사 방향: 보스가 바라보는 바깥쪽 방향에 회전 가미
                        # rotate()를 사용해 화려한 스파이럴 효과 연출
                        baseDir = (self.centers[i] - targetCenter).normalize() * 4
                        bulletSpin = self.spinAngle * 2 # 탄막 회전 가속
                        
                        for offset in [-25, 0, 25]:
                            # 보스의 회전 방향과 탄막의 회전 방향을 조합
                            finalDir = baseDir.rotate(offset + bulletSpin)
                            eProjs.append(Projectile(self.centers[i].x, self.centers[i].y, finalDir, RED, 5, 5))
                      
                    
                    
            # 2. 이동 단계 (0~120프레임): 초기 진입 시에는 부드럽게 모임
            elif self.stateTimer < 120:
                for i in range(8):
                    angle = (i / 8) * math.pi * 2
                    targetPos = targetCenter + pygame.Vector2(math.cos(angle)*120, math.sin(angle)*120)
                    self.centers[i] = self.centers[i].lerp(targetPos, 0.05)
                
            
            # 3. 상태 종료
            else:
                self.state = "SCATTER"
                self.stateTimer = 0
                self.weakIndex = random.randint(0, 7)                
                
    def draw(self, surf):
        for i, c in enumerate(self.centers):    
            
            if i == self.weakIndex:
                # (A) 본체 뒤에서 타오르는 플라즈마 불꽃 (이미지보다 뒤에 렌더링)
                time_f = pygame.time.get_ticks() * 0.01
                # 안쪽(흰색) -> 중간(보라) -> 바깥(청록) 순서로 겹쳐서 입체감 부여
                flame_layers = [
                    {"color": (255, 60, 0, 100), "radius": 32.5}, # 외곽 광륜
                    {"color": (255, 140, 0, 160), "radius": 27.5}, # 플라즈마 에너지
                    {"color": (255, 255, 200, 220), "radius": 25}  # 핵심 코어
                ]
                
                for layer in flame_layers:
                    # 숨쉬는 듯한 크기 변화 (Pulse)
                    pulse = math.sin(time_f * 2) * 5
                    # 위아래로 요동치는 움직임
                    y_float = math.sin(time_f * 1.5) * 7
                    
                    # 투명도 적용을 위한 임시 서피스
                    f_size = int((layer["radius"] + pulse) * 2)
                    f_surf = pygame.Surface((f_size, f_size), pygame.SRCALPHA)
                    pygame.draw.circle(f_surf, layer["color"], (f_size//2, f_size//2), f_size//2)
                    
                    # 개체 위치(c)를 기준으로 블릿 (이미지 뒤쪽으로 배치)
                    surf.blit(f_surf, (c.x - f_size//2, c.y - f_size//2 + y_float))
            # --- [핵심] 약점 개체 연출 끝 ---

            # 2. 보스 개체 이미지 출력 (중앙 정렬)
            surf.blit(self.currentImg, (c.x - 50, c.y - 50))
                


    def draw(self, surf):
        # 개별 체력바 표기
        hpRatio = max(0, self.hp / self.maxHp)
        pygame.draw.rect(surf, RED, (self.pos.x - 30, self.pos.y + 60, 60, 6))
        pygame.draw.rect(surf, GREEN, (self.pos.x - 30, self.pos.y + 60, 60 * hpRatio, 6))

        # 보스 본체
        surf.blit(self.currentImg, (self.pos.x - 150, self.pos.y - 150))
        for meteor in self.meteors:
            meteor.draw(surf)

class BossZero:
    def __init__(self):
        self.type = "ZERO"
        self.pos = pygame.Vector2(WIDTH // 2, 200)
        self.hp = 3500
        self.maxHp = 3500
        self.timer = 0
        self.rect = pygame.Rect(self.pos.x - 40, self.pos.y - 40, 80, 80)
        
        # --- 대량 회전 탄막 관련 변수 설정 ---
        self.orbitBullets = []
        self.orbitAngle = 0
        self.numOrbitBullets = 240   # 12개에서 20배 증가 (240개)
        self.rotationSpeed = 0.02    # 탄막이 많으므로 회전 속도를 조금 낮춤 (우아한 연출)
        
        # 반경 로직 (기존 요청 유지)
        self.baseRadius = 150
        self.startRadius = self.baseRadius * 3.5
        self.targetRadius = self.baseRadius * 0.5
        self.currentRadius = self.startRadius
        self.shrinkSpeed = 0.003     # 탄막이 많으므로 수렴 속도를 살짝 늦춤

    def update(self, eProjs, pPos, ctx=None):
        self.timer += 1
        
        # 1. 보스 본체 이동 (8자 기동)
        self.pos.x = WIDTH // 2 + math.sin(self.timer * 0.03) * 150
        self.pos.y = 150 + math.cos(self.timer * 0.02) * 50
        self.rect.center = (self.pos.x, self.pos.y)

        # 2. 회전 및 반경 업데이트
        self.orbitAngle += self.rotationSpeed
        if self.currentRadius > self.targetRadius:
            self.currentRadius -= (self.currentRadius - self.targetRadius) * self.shrinkSpeed

        # 3. 궤도 탄막 관리 (리스트 정리)
        self.orbitBullets = [b for b in self.orbitBullets if b in eProjs]

        # 4. 탄막 순차적 생성 (한 번에 240개를 만들면 끊길 수 있으므로 매 프레임 4개씩 보충)
        if len(self.orbitBullets) < self.numOrbitBullets:
            for _ in range(4): 
                if len(self.orbitBullets) < self.numOrbitBullets:
                    # 초기 위치는 보스 위치, 색상은 화려함을 위해 타이머에 따라 가변
                    newBullet = Projectile(self.pos.x, self.pos.y, pygame.Vector2(0, 0), CYAN, 8, 5)
                    self.orbitBullets.append(newBullet)
                    eProjs.append(newBullet)

        # 5. 대량 탄막 배치 (고밀도 원형/소용돌이 로직)
        for i, bullet in enumerate(self.orbitBullets):
            # i값에 따라 각도를 분배하여 촘촘한 원 생성
            angle = self.orbitAngle + (i * (2 * math.pi / self.numOrbitBullets))
            
            # 중심에서 밖으로 퍼졌다가 다시 안으로 모이는 시각적 효과
            bullet.pos.x = self.pos.x + math.cos(angle) * self.currentRadius
            bullet.pos.y = self.pos.y + math.sin(angle) * self.currentRadius
            bullet.vel = pygame.Vector2(0, 0)

        # 6. 공격 로직: 촘촘한 탄막 중 무작위로 발사 (비처럼 쏟아지는 효과)
        if self.timer % 3 == 0 and self.orbitBullets:
            # 궤도 탄막 중 랜덤하게 하나를 골라 플레이어에게 발사
            target_idx = random.randint(0, len(self.orbitBullets) - 1)
            firedBullet = self.orbitBullets.pop(target_idx)
            
            targetDir = (pPos - firedBullet.pos).normalize()
            firedBullet.vel = targetDir * 7
            firedBullet.color = (255, 100, 100) # 발사되는 탄막은 붉은색 계열로 변경

    def draw(self, surf):
        # 보스 체력바 및 본체 렌더링
        hpRatio = max(0, self.hp / self.maxHp)
        pygame.draw.rect(surf, (50, 50, 50), (self.pos.x - 60, self.pos.y + 80, 120, 10))
        pygame.draw.rect(surf, (200, 0, 255), (self.pos.x - 60, self.pos.y + 80, 120 * hpRatio, 10))
        
        # 보스 코어 연출 (대량 탄막의 중심점)
        pygame.draw.circle(surf, WHITE, (int(self.pos.x), int(self.pos.y)), 15)

class BossZero4:
    def __init__(self):
        self.type = "ZERO"
        self.pos = pygame.Vector2(WIDTH // 2, 200)
        self.hp = 3500
        self.maxHp = 3500
        self.timer = 0
        self.rect = pygame.Rect(self.pos.x - 40, self.pos.y - 40, 80, 80)
        
        # --- 회전 탄막 관련 변수 설정 ---
        self.orbitBullets = []
        self.orbitAngle = 0
        self.numOrbitBullets = 12
        self.rotationSpeed = 0.05
        
        # 반경 관련 설정
        self.baseRadius = 150              # 기준 반경
        self.startRadius = self.baseRadius * 3.5  # 초기 반경 (3.5배)
        self.targetRadius = self.baseRadius * 0.5 # 최종 반경 (0.5배)
        self.currentRadius = self.startRadius     # 현재 적용 중인 반경
        self.shrinkSpeed = 0.005           # 반경이 줄어드는 속도 계수

    def update(self, eProjs, pPos, ctx=None):
        self.timer += 1
        
        # 1. 보스 본체 이동
        self.pos.x = WIDTH // 2 + math.sin(self.timer * 0.03) * 150
        self.pos.y = 150 + math.cos(self.timer * 0.02) * 50
        self.rect.center = (self.pos.x, self.pos.y)

        # 2. 회전 각도 및 반경 업데이트
        self.orbitAngle += self.rotationSpeed
        
        # 반경이 targetRadius(0.5배)에 도달할 때까지 서서히 줄어듦 (지수적 감소)
        # 현재 값에서 목표 값으로 부드럽게 접근하는 보간 로직
        if self.currentRadius > self.targetRadius:
            self.currentRadius -= (self.currentRadius - self.targetRadius) * self.shrinkSpeed

        # 3. 궤도 탄막 리스트 관리
        self.orbitBullets = [b for b in self.orbitBullets if b in eProjs]

        # 4. 탄막 보충
        if len(self.orbitBullets) < self.numOrbitBullets:
            if self.timer % 8 == 0:
                newBullet = Projectile(self.pos.x, self.pos.y, pygame.Vector2(0, 0), CYAN, 10, 6)
                self.orbitBullets.append(newBullet)
                eProjs.append(newBullet)

        # 5. 수렴하는 원형 궤도 계산
        for i, bullet in enumerate(self.orbitBullets):
            # 탄막별 간격 계산
            angle = self.orbitAngle + (i * (2 * math.pi / self.numOrbitBullets))
            
            # 점점 작아지는 currentRadius를 적용하여 위치 결정
            bullet.pos.x = self.pos.x + math.cos(angle) * self.currentRadius
            bullet.pos.y = self.pos.y + math.sin(angle) * self.currentRadius
            bullet.vel = pygame.Vector2(0, 0)

        # 6. 공격 로직 (궤도에서 플레이어에게 발사)
        if self.timer % 50 == 0 and self.orbitBullets:
            firedBullet = self.orbitBullets.pop(0)
            targetDir = (pPos - firedBullet.pos).normalize()
            firedBullet.vel = targetDir * 9
            firedBullet.color = RED

    def draw(self, surf):
        # 체력바 등 기본 그리기 로직 (생략 가능, 기존 유지)
        hpRatio = max(0, self.hp / self.maxHp)
        pygame.draw.rect(surf, (100, 100, 100), (self.pos.x - 50, self.pos.y + 70, 100, 8))
        pygame.draw.rect(surf, (255, 0, 0), (self.pos.x - 50, self.pos.y + 70, 100 * hpRatio, 8))
        pygame.draw.circle(surf, (0, 255, 255), (int(self.pos.x), int(self.pos.y)), 20, 2)

class BossZero3:
    def __init__(self):
        self.type = "ZERO"
        self.pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
        self.hp = 3500
        self.maxHp = 3500
        self.timer = 0
        self.rect = pygame.Rect(self.pos.x - 40, self.pos.y - 40, 80, 80)
        
        # 패턴 설정 변수
        self.angleOffset = 0
        self.cycleFrames = 10 * 37.5  # 10초 주기 수축
        
        # [수정] 초기 중심 거리 3.5배(600 * 3.5 = 2100) 및 최종 반경 0.5배(50 * 0.5 = 25) 설정
        self.startRadius = 600 * 3.5 
        self.targetRadius = 50 * 0.5 

    def update(self, eProjs, pPos, ctx=None):
        self.timer += 1
        self.angleOffset += 0.15 # 회전 속도
        
        # 선형 보간(Lerp)을 위한 진행률 계산 (0.0 ~ 1.0)
        progress = (self.timer % self.cycleFrames) / self.cycleFrames
        
        # 시작 지점(startRadius)에서 목표 지점(targetRadius)까지 서서히 줄어드는 반지름 계산
        currentRadius = self.startRadius - (self.startRadius - self.targetRadius) * progress
        
        # 3프레임마다 탄막 생성
        if self.timer % 3 == 0:
            numBullets = 8
            for i in range(numBullets):
                # 원의 테두리 좌표 계산
                angle = (i * (2 * math.pi / numBullets)) + self.angleOffset
                spawnX = self.pos.x + math.cos(angle) * currentRadius
                spawnY = self.pos.y + math.sin(angle) * currentRadius
                
                # 보스 중심을 향해 파고드는 속도 벡터 설정
                direction = (self.pos - pygame.Vector2(spawnX, spawnY)).normalize()
                vel = direction * 2.5
                
                # 진행도에 따른 색상 변화 연출 (Cyan -> Purple)
                color = CYAN if progress < 0.6 else PURPLE
                eProjs.append(Projectile(spawnX, spawnY, vel, color, 10, 5))

    def draw(self, surf):
        # 체력바 드로우
        hpRatio = max(0, self.hp / self.maxHp)
        pygame.draw.rect(surf, GRAY, (self.pos.x - 50, self.pos.y + 60, 100, 8))
        pygame.draw.rect(surf, RED, (self.pos.x - 50, self.pos.y + 60, 100 * hpRatio, 8))
        
        # 보스 코어 연출
        pulse = math.sin(self.timer * 0.1) * 10
        pygame.draw.circle(surf, WHITE, (int(self.pos.x), int(self.pos.y)), 20 + int(pulse), 2)
        pygame.draw.circle(surf, CYAN, (int(self.pos.x), int(self.pos.y)), 5)

class BossZero2:
    def __init__(self):
        self.type = "ZERO"
        self.pos = pygame.Vector2(WIDTH // 2, 200) # 보스의 초기 위치 설정
        self.hp = 3500 # 보스의 최대 체력 설정
        self.maxHp = 3500
        self.timer = 0
        self.rect = pygame.Rect(self.pos.x - 40, self.pos.y - 40, 80, 80) # 충돌 판정용 사각형
        
        # --- 회전 탄막 관련 변수 (유지보수를 위해 camelCase 적용) ---
        self.orbitBullets = []      # 현재 보스 주변을 도는 탄막 리스트
        self.orbitAngle = 0         # 기준 회전 각도
        self.orbitRadius = 150      # 보스와 탄막 사이의 거리
        self.numOrbitBullets = 12   # 원형 궤도를 구성할 탄막의 개수
        self.rotationSpeed = 0.05   # 프레임당 회전 속도

    def update(self, eProjs, pPos, ctx=None):
        self.timer += 1
        
        # 1. 보스 본체의 부드러운 이동 (8자 곡선 형태)
        self.pos.x = WIDTH // 2 + math.sin(self.timer * 0.03) * 150
        self.pos.y = 150 + math.cos(self.timer * 0.02) * 50
        self.rect.center = (self.pos.x, self.pos.y)

        # 2. 전체 회전 각도 업데이트
        self.orbitAngle += self.rotationSpeed

        # 3. 궤도 탄막 상태 관리: 파괴되거나 발사된 탄막은 리스트에서 제외
        self.orbitBullets = [b for b in self.orbitBullets if b in eProjs]

        # 4. 탄막 보충: 궤도 탄막이 부족할 경우 일정 주기마다 생성
        if len(self.orbitBullets) < self.numOrbitBullets:
            if self.timer % 10 == 0: # 생성 간격을 두어 자연스럽게 배치
                # 초기 위치는 보스로 설정하며, 궤도에 고정하기 위해 vel은 0으로 시작
                newBullet = Projectile(self.pos.x, self.pos.y, pygame.Vector2(0, 0), CYAN, 10, 6)
                self.orbitBullets.append(newBullet)
                eProjs.append(newBullet)

        # 5. 원형 궤도 유지 로직: 각 탄막의 위치를 보스 중심으로 강제 업데이트
        for i, bullet in enumerate(self.orbitBullets):
            # i번째 탄막이 원 위에 균등하게 위치하도록 개별 각도 계산
            angle = self.orbitAngle + (i * (2 * math.pi / self.numOrbitBullets))
            
            # 삼각함수를 이용한 원형 좌표(x, y) 계산
            bullet.pos.x = self.pos.x + math.cos(angle) * self.orbitRadius
            bullet.pos.y = self.pos.y + math.sin(angle) * self.orbitRadius
            
            # 궤도 이동 중에는 Projectile의 자체 이동 로직이 작동하지 않도록 vel을 0으로 고정
            bullet.vel = pygame.Vector2(0, 0)

        # 6. 추가 공격: 약 1.5초마다 궤도 탄막 하나를 플레이어에게 조준 사격
        if self.timer % 60 == 0 and self.orbitBullets:
            firedBullet = self.orbitBullets.pop(0) # 궤도 리스트에서 제거하여 독립된 탄막으로 전환
            
            # 플레이어 방향으로 가속도 부여
            targetDir = (pPos - firedBullet.pos).normalize()
            firedBullet.vel = targetDir * 8
            firedBullet.color = RED # 공격 상태임을 알리기 위해 색상 변경

    def draw(self, surf):
        # 체력바 렌더링
        hpRatio = max(0, self.hp / self.maxHp)
        pygame.draw.rect(surf, GRAY, (self.pos.x - 50, self.pos.y + 70, 100, 8))
        pygame.draw.rect(surf, RED, (self.pos.x - 50, self.pos.y + 70, 100 * hpRatio, 8))
        
        # 보스 본체 중심부 연출
        pulse = math.sin(pygame.time.get_ticks() * 0.01) * 10
        pygame.draw.circle(surf, CYAN, (int(self.pos.x), int(self.pos.y)), 20 + int(pulse), 2)
        pygame.draw.circle(surf, WHITE, (int(self.pos.x), int(self.pos.y)), 10)

class BossZero1:
    def __init__(self):
        self.type = "ZERO"
        self.pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
        self.hp = 3500
        self.maxHp = 3500
        self.timer = 0
        self.rect = pygame.Rect(self.pos.x - 40, self.pos.y - 40, 80, 80)
        
        # 패턴 설정 변수
        self.angleOffset = 0
        self.cycleFrames = 10 * 37.5  # 10초 주기 수축

    def update(self, eProjs, pPos, ctx=None):
        self.timer += 1
        self.angleOffset += 0.15  # 회전 속도 (높을수록 빠르게 회전)
        
        # 10초 주기로 반지름이 600에서 50까지 줄어듦
        progress = (self.timer % self.cycleFrames) / self.cycleFrames
        currentRadius = 600 - (550 * progress)
        
        # 3프레임마다 탄막 생성 (탄막 밀도 조절)
        if self.timer % 3 == 0:
            numBullets = 8  # 한 번에 생성되는 탄알 수
            for i in range(numBullets):
                # 원의 테두리 좌표 계산
                angle = (i * (2 * math.pi / numBullets)) + self.angleOffset
                spawnX = self.pos.x + math.cos(angle) * currentRadius
                spawnY = self.pos.y + math.sin(angle) * currentRadius
                
                # 탄막이 생성된 지점에서 보스(중심)를 향해 이동하는 벡터 계산
                direction = (self.pos - pygame.Vector2(spawnX, spawnY)).normalize()
                vel = direction * 2.5  # 탄막이 중심으로 파고드는 속도
                
                # 시각 효과: 수축 정도에 따라 색상 변화 (Cyan -> Purple)
                color = CYAN if progress < 0.6 else PURPLE
                eProjs.append(Projectile(spawnX, spawnY, vel, color, 10, 5))

    def draw(self, surf):
        # 체력바 표시
        hpRatio = max(0, self.hp / self.maxHp)
        pygame.draw.rect(surf, GRAY, (self.pos.x - 50, self.pos.y + 60, 100, 8))
        pygame.draw.rect(surf, RED, (self.pos.x - 50, self.pos.y + 60, 100 * hpRatio, 8))
        
        # 보스 중심부 연출
        pulse = math.sin(self.timer * 0.1) * 10
        pygame.draw.circle(surf, WHITE, (int(self.pos.x), int(self.pos.y)), 20 + int(pulse), 2)
        pygame.draw.circle(surf, CYAN, (int(self.pos.x), int(self.pos.y)), 5)

class BossZero0:
    def __init__(self):
        self.type = "ZERO"
        self.pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2) # 중앙에 위치하여 패턴 전개
        self.hp = 3500
        self.maxHp = 3500
        self.timer = 0
        self.patternCycle = 15 * 37.5 # 15초 주기 (FPS 37.5 기준)
        self.rect = pygame.Rect(self.pos.x - 40, self.pos.y - 40, 80, 80)
        self.angleOffset = 0 # 회전 효과를 위한 오프셋

    def update(self, eProjs, pPos, ctx=None):
        self.timer += 1
        currentTime = self.timer % self.patternCycle
        phase1End = 10 * 37.5 # 10초 지점
        
        # 보스 위치: 부드럽게 중앙 주변을 배회
        self.pos.x = WIDTH // 2 + math.sin(self.timer * 0.02) * 50
        self.pos.y = HEIGHT // 2 + math.cos(self.timer * 0.02) * 50
        self.rect.center = (self.pos.x, self.pos.y)

        # --- 패턴 1: 0~10초 - 회전하며 수축하는 원형 감옥 ---
        if currentTime < phase1End:
            # 반지름 계산: 600(화면 밖)에서 시작하여 120(플레이어 근처)까지 줄어듦
            progress = currentTime / phase1End
            currentRadius = 600 - (480 * progress)
            
            # 매 프레임마다 회전각 증가
            self.angleOffset += 0.08 
            
            # 일정 간격으로 탄막 생성 (회전하는 원의 테두리)
            if self.timer % 8 == 0:
                numBullets = 10 # 한 번에 생성할 탄막 개수
                for i in range(numBullets):
                    # 원의 테두리 좌표 계산
                    angle = (i * (2 * math.pi / numBullets)) + self.angleOffset
                    spawnX = self.pos.x + math.cos(angle) * currentRadius
                    spawnY = self.pos.y + math.sin(angle) * currentRadius
                    
                    # 탄막의 이동: 원의 형태를 유지하며 아주 천천히 중앙으로 수축
                    # (완전히 멈춰있으면 피하기 너무 쉬우므로 약간의 속도를 부여)
                    direction = (self.pos - pygame.Vector2(spawnX, spawnY)).normalize()
                    vel = direction * 1.2 
                    
                    # 색상 연출: 수축할수록 붉은색에 가깝게 변함 (청록 -> 보라 -> 빨강)
                    bulletColor = CYAN if progress < 0.5 else PURPLE
                    eProjs.append(Projectile(spawnX, spawnY, vel, bulletColor, 10, 5))

        # --- 패턴 2: 10~15초 - 지그재그 하강 탄막 (감옥 해제 후 기습) ---
        else:
            if self.timer % 4 == 0:
                # 화면 상단 여러 지점에서 지그재그로 내려오는 탄막
                for xGate in range(0, WIDTH + 1, 150):
                    # sin 함수를 이용한 수평 흔들림
                    zigzagX = math.sin(self.timer * 0.15 + xGate) * 5
                    vel = pygame.Vector2(zigzagX, 7) # 빠른 하강 속도
                    
                    spawnX = xGate + math.cos(self.timer * 0.1) * 20
                    eProjs.append(Projectile(spawnX, -20, vel, WHITE, 8, 4))

        # 상시 방어 패턴: 보스 주변을 빠르게 회전하는 보호 탄막
        if self.timer % 5 == 0:
            rotVel = pygame.Vector2(6, 0).rotate(self.timer * 12)
            eProjs.append(Projectile(self.pos.x, self.pos.y, rotVel, BLACK, 6, 3))

    def draw(self, surf):
        # 체력바 렌더링
        hpRatio = max(0, self.hp / self.maxHp)
        pygame.draw.rect(surf, GRAY, (self.pos.x - 50, self.pos.y + 60, 100, 8))
        pygame.draw.rect(surf, RED, (self.pos.x - 50, self.pos.y + 60, 100 * hpRatio, 8))
        
        # 보스 본체 연출 (수축하는 에너지 구체 느낌)
        pulse = math.sin(pygame.time.get_ticks() * 0.01) * 15
        innerRadius = 30 + int(pulse * 0.5)
        pygame.draw.circle(surf, PURPLE, (int(self.pos.x), int(self.pos.y)), innerRadius, 2)
        pygame.draw.circle(surf, CYAN, (int(self.pos.x), int(self.pos.y)), 10)

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
    tempSurf.fill((20, 20, 30))
    # 탭 버튼 (A: 아이템, B: 은행, C: 투자)
    tabs = [("ITEM", 50), ("BANK", 250), ("INVEST", 450)]
    for name, x in tabs:
        color = GOLD if shopTab == name else GRAY
        pygame.draw.rect(tempSurf, color, (x, 20, 180, 50), border_radius=5)
        tempSurf.blit(fontM.render(name, True, BLACK), (x+50, 30))

    # --- 2. 탭별 내용 ---
    if shopTab == "ITEM":
        discount = getDiscountRatio()
        for i, opt in enumerate(shopOptions):
            card_rect = pygame.Rect(30 + i * 215, 150, 200, 320)
            # 할인율이 적용된 실제 가격 계산
            display_price = int(opt["data"]["price"] * discount)
            
            # 카드 렌더링 (기존 로직 유지하되 가격만 변동)
            c = (40, 40, 40) if opt["sold"] else (30, 30, 50)
            pygame.draw.rect(tempSurf, c, card_rect, border_radius=10)
            
            if not opt["sold"]:
                name_text = fontM.render(opt['data']['name'], True, WHITE)
                tempSurf.blit(name_text, (card_rect.x + 20, card_rect.y + 40))
                
                # 지분 상태에 따른 가격 색상 변경
                p_color = GOLD if stats["gold"] >= display_price else RED
                price_text = fontM.render(f"{display_price} G", True, p_color)
                tempSurf.blit(price_text, (card_rect.x + 60, card_rect.y + 260))

    elif shopTab == "BANK":
        # UI 배경
        pygame.draw.rect(tempSurf, (20, 30, 40), (100, 150, 700, 300), border_radius=15)
        
        # 예치 정보
        balance_txt = fontL.render(f"예치 잔액: {bankBalance} G", True, CYAN)
        interest_txt = fontM.render("예상 다음 배당 이율: +10%", True, GREEN)
        tempSurf.blit(balance_txt, (150, 200))
        tempSurf.blit(interest_txt, (150, 280))
        
        # 안내 문구
        guide_txt = fontS.render("[D] 전액 입금  |  [F] 전액 인출 (수수료 5% 발생)", True, WHITE)
        tempSurf.blit(guide_txt, (150, 400))
        
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
    tempSurf.blit(fontM.render(f"현재 시민 등급: {rank}", True, GOLD), (WIDTH-300, HEIGHT-50))

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
                elif currentStage == 1:
                    # boss = BossSwarm()
                    boss = BossZero1()
                    # boss = BossRock()
                    # boss = BossChernobog()
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
            if boss.type == "swarm":
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
        playerCenter = playerPos + pygame.Vector2(30, 30)
        # hitboxRadius는 코드 상단에 10으로 정의되어 있어야 합니다.

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

        # --- 3. 플레이어 투사체(pProjs) 업데이트 및 적/보스 피격 판정 ---
        for p in pProjs[:]:
            p.update()
            hitThisFrame = False

            # 3-1. 보스 피격 판정
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

            # 3-2. 일반 적 피격 판정 (보스를 맞추지 않았을 때만 체크하거나 관통 시 체크)
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
    screen.blit(bgImg, (0, 0))

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
            
            playerCenter = playerPos + pygame.Vector2(30, 30)
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
        tempSurf.blit(fontM.render(f"등급: {rank} | GOLD: {stats['gold']}G", True, WHITE), (300, HEIGHT-50))

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
    # 흔들림이 적용된 도화지(tempSurf)를 실제 화면에 출력
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

pygame.quit()