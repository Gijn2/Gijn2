import pygame
import random
import math
import json
import hashlib
from constants import *
from Zgame import *

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


class BossZero:
    def __init__(self):
        self.type = "ZERO"
        self.pos = pygame.Vector2(WIDTH//2, 100)
        self.hp = 150; self.maxHp = 150
        self.timer = 0
        self.state = "TELEPORT" # 11. 통합된 콤보 로직
        self.comboStep = 0
        self.hitboxRadius = 30
        self.coneDir = pygame.Vector2(0, 1)
        self.images = BossAssetManager.get_images("bossZero")
        self.currentImg = self.images["STAND"]
        
    def update(self, eProjs, pPos):
        self.timer += 1
        global particles # 사신 이펙트를 위한 파티클 전역변수
        
        if self.state == "TELEPORT":
            if self.comboStep == 0: # 텔레포트 대기
                if self.timer > 60:
                    self.pos.x = max(50, min(WIDTH-50, pPos.x))
                    self.pos.y = max(50, min(HEIGHT-200, pPos.y - 150))
                    self.timer = 0
                    self.comboStep = 1
                    self.coneDir = (pPos - self.pos).normalize() if (pPos - self.pos).length() > 0 else pygame.Vector2(0, 1)

            elif self.comboStep == 1: # 낫 부채꼴 경고
                # 11. 텔레포트 후 사신 이펙트 (검보라색 파티클)
                for _ in range(2):
                    particles.append(Particle(self.pos.x + random.randint(-30, 30), self.pos.y + random.randint(-30, 30), (150, 0, 255)))
                    
                if self.timer > 37:
                    self.comboStep = 2
                    self.timer = 0
                    
            elif self.comboStep == 2:
                # 11. 부채꼴 테두리에서 SOULS 로직 구현
                if self.timer == 1:
                    # 양쪽 테두리 끝 위치 계산
                    leftEdge = self.pos + self.coneDir.rotate(-45) * 200
                    rightEdge = self.pos + self.coneDir.rotate(45) * 200
                    for _ in range(8):
                        eProjs.append(HomingProjectile(leftEdge.x, leftEdge.y, pygame.Vector2(random.uniform(-2, 2), 2), CYAN, 5, 8))
                        eProjs.append(HomingProjectile(rightEdge.x, rightEdge.y, pygame.Vector2(random.uniform(-2, 2), 2), CYAN, 5, 8))
                
                if self.timer > 60:
                    self.comboStep = 0
                    self.timer = 0

    def draw(self, surf):
        surf.blit(self.currentImg, (self.pos.x - 25, self.pos.y - 25))
        if self.state == "TELEPORT_COMBO" and self.comboStep == 1:
            # 11. 플레이어가 완전히 갇히는 거대한 부채꼴 (폴리곤)
            leftVec = self.coneDir.rotate(-45) * 400
            rightVec = self.coneDir.rotate(45) * 400
            points = [self.pos, self.pos + leftVec, self.pos + rightVec]
            pygame.draw.polygon(surf, (255, 0, 0, 80), points)
        
        hpRatio = max(0, self.hp / self.maxHp)
        pygame.draw.rect(surf, GREEN, (self.pos.x - 30, self.pos.y + 40, 60 * hpRatio, 5))

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

    def draw(self, surf):
        # 개별 체력바 표기
        hpRatio = max(0, self.hp / self.maxHp)
        pygame.draw.rect(surf, RED, (self.pos.x - 30, self.pos.y + 60, 60, 6))
        pygame.draw.rect(surf, GREEN, (self.pos.x - 30, self.pos.y + 60, 60 * hpRatio, 6))

        # 보스 본체
        surf.blit(self.currentImg, (self.pos.x - 150, self.pos.y - 150))
        for meteor in self.meteors:
            meteor.draw(surf)

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
