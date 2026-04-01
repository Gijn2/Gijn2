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

import math

class BossArc:
    def __init__(self):
        self.pos = [WIDTH // 2, 150]
        self.angle = 0
        self.phase = 1
        self.timer = 0

    def update(self, player_pos, bullets):
        self.timer += 1
        self.angle += 2  # 회전 속도 제어
        
        # 1프레임마다 발사하는 것이 아니라 간격을 둠
        if self.timer % 5 == 0:
            if self.phase == 1:
                self.pattern_spiral(bullets)
            elif self.phase == 2:
                self.pattern_flower(bullets)

    def pattern_spiral(self, bullets):
        # 정석적인 나선형 탄막 (N-way 스파이럴)
        num_streams = 6
        for i in range(num_streams):
            # 기본 각도에 스트림별 간격과 시간에 따른 회전각을 더함
            rad = math.radians(self.angle + (i * (360 / num_streams)))
            dx = math.cos(rad) * 3
            dy = math.sin(rad) * 3
            bullets.append({"pos": list(self.pos), "vel": [dx, dy], "color": (0, 255, 255)})

    def pattern_flower(self, bullets):
        # 시계 방향과 반시계 방향이 교차하는 패턴
        for i in range(12):
            rad = math.radians(i * 30 + self.angle)
            inv_rad = math.radians(i * 30 - self.angle)
            # 바깥으로 퍼지는 속도 조절
            bullets.append({"pos": list(self.pos), "vel": [math.cos(rad)*2, math.sin(rad)*2]})
            bullets.append({"pos": list(self.pos), "vel": [math.cos(inv_rad)*2, math.sin(inv_rad)*2]})

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

class BossCrazy:
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
        self.hp = 600 
        self.maxHp = 600
        self.centers = [pygame.Vector2(random.randint(100,800), random.randint(50,200)) for _ in range(8)]
        self.fireTimers = [random.randint(60, 150) for _ in range(8)]
        self.weakIndex = random.randint(0, 7)
        self.state = "SCATTER" 
        self.stateTimer = 0
        self.hitboxRadius = 25
        self.spinAngle = 0
        self.images = BossAssetManager.get_images("bossSwarm")
        self.currentImg = self.images["STAND"]

    def update(self, eProjs, pPos):
        self.stateTimer += 1
        
        if self.state == "SCATTER" and self.stateTimer > 200:
            self.state = "GATHER"
            self.stateTimer = 0
        elif self.state == "GATHER" and self.stateTimer > 150:
            self.state = "CONVERGE_SHOOT"
            self.stateTimer = 0
            self.currentImg = self.images["ATTACK"]
        elif self.state == "CONVERGE_SHOOT" and self.stateTimer > 120:
            self.state = "SCATTER"
            self.stateTimer = 0
            self.weakIndex = random.randint(0, 7)
            self.currentImg = self.images["STAND"]
        
        if self.state == "SCATTER":
            for i in range(8):
                self.centers[i].x += math.sin(pygame.time.get_ticks() / 500 + i) * 7
                self.fireTimers[i] -= 1
                if self.fireTimers[i] <= 0:
                    diff = pPos - self.centers[i]
                    dirVec = diff.normalize() * 4 if diff.length() > 0 else pygame.Vector2(0, 4)
                    eProjs.append(Projectile(self.centers[i].x, self.centers[i].y, dirVec, PURPLE, 7, 5))
                    self.fireTimers[i] = random.randint(60, 150)

        elif self.state == "GATHER":
            targetCenter = pygame.Vector2(WIDTH//2, 150)
            self.spinAngle += 4 
            for i in range(8):
                orbitAngle = self.spinAngle + (i * 45)
                rad = math.radians(orbitAngle)
                targetPos = targetCenter + pygame.Vector2(math.cos(rad) * 120, math.sin(rad) * 120)
                self.centers[i] = self.centers[i].lerp(targetPos, 0.05)
                
            # 회전하며 십자 형태로 전방향 탄막 발사
            if self.stateTimer % 15 == 0:
                for i in range(8):
                    for j in range(4): 
                        angle = math.radians(self.spinAngle + (j * 90))
                        dirVec = pygame.Vector2(math.cos(angle), math.sin(angle)) * 3.0
                        eProjs.append(Projectile(self.centers[i].x, self.centers[i].y, dirVec, CYAN, 5, 4))
                
        elif self.state == "CONVERGE_SHOOT":
            # 화려하게 겹치는 넓은 부채꼴 교차 탄막 (빈틈을 파고드는 난이도)
            if self.stateTimer % 20 == 0:
                for i in range(8):
                    diff = pPos - self.centers[i]
                    baseDir = diff.normalize() * 5 if diff.length() > 0 else pygame.Vector2(0, 5)
                    for offset in [-40, 0, 40]: 
                        dirVec = baseDir.rotate(offset)
                        eProjs.append(Projectile(self.centers[i].x, self.centers[i].y, dirVec, RED, 10, 6))

    def draw(self, surf):
        for i, c in enumerate(self.centers):    
            if i == self.weakIndex:
                pulse = math.sin(pygame.time.get_ticks() * 0.01) * 5
                pygame.draw.circle(surf, (255, 140, 0, 150), (int(c.x), int(c.y)), int(30 + pulse))
            surf.blit(self.currentImg, (c.x - 50, c.y - 50))

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
            # 단축키(k)를 실제 입력 이벤트와 일치하도록 Q, W, E로 수정
            investTargets = [
                {"id": "A", "n": "구역 A: 지열 운송", "y": 150, "k": "Q"},
                {"id": "B", "n": "구역 B: 에너지 연구", "y": 260, "k": "W"},
                {"id": "C", "n": "구역 C: 정밀 합금", "y": 370, "k": "E"}
            ]
            for i, inv in enumerate(investTargets):
                y = inv["y"]
                pygame.draw.rect(tempSurf, (45, 45, 65), (50, y, 800, 90), border_radius=10)
                barW = int(stocks[inv["id"]] * 2) 
                pygame.draw.rect(tempSurf, GOLD, (550, y + 35, barW, 20))
                tempSurf.blit(fontM.render(f"{inv['n']} ({stocks[inv['id']]}%)", True, WHITE), (70, y + 15))
                # 수정: 배열 인덱스가 아닌 실제 할당된 'k' 값 출력
                tempSurf.blit(fontM.render(f"500G [Key:{inv['k']}]", True, GOLD), (380, y + 30))
                
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
                    # boss = BossRock()
                    # boss = BossChernobog()
                    boss = BossCrusher()
                    # boss = BossCrazy()
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
    # W 특수기 효과 (화면 반전)
    if specialEffectTimer > 0:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            alpha = min(255, specialEffectTimer * 10) 
            overlay.fill((255, 255, 255, alpha))
            screen.blit(overlay, (0, 0))
            specialEffectTimer -= 1 
    
    # 배경 그리기
    screen.blit(bgImg, (0, 0))
        
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