# 일반 몬스터 로직
import pygame
import math
import random
from entities.Projectiles import Projectile, HomingProjectile
from constants import *
from assetManager import assets


def getRandomEnemy(current_stage):
    available = [e for e in ENEMY_SPAWN_POOL if current_stage >= e["minStage"]]
    if not available: return "type1"
    types = [e["type"] for e in available]
    weights = [e["weight"] for e in available]
    return random.choices(types, weights=weights)[0]


class Enemy:
    def __init__(self, eType="type1", offset=0):
        self.eType = eType

        config = ENEMY_CONFIG.get(eType, ENEMY_CONFIG["type1"])
        self.hp = config["hp"]
        self.imgType = config["img_key"]

        # 공통 로직
        self.pos = pygame.Vector2(random.randint(50, WIDTH-50), -50)
        self.offset = offset
        self.vx = 0
        self.vy = config["vy"] 
        self.state = "STAND"
        self.shootDelay = random.randint(80, 160)
        self.attackTimer = 0
        self.orbitBullets = [] # type3를 위한 회전 총알 저장소
        
        # 타입별 초기화 로직 분리
        if eType == "type1":
            self.hp = 5
            self.imgType = "type_1"
        elif eType == "type2":
            self.hp = 8
            self.imgType = "type_2"
        elif eType == "type3":
            self.hp = 6
            self.vy = 1.0
            self.imgType = "type_3"
            self.orbitAngles = [0, 90, 180, 270]
        elif eType == "type5":
            self.hp = 10
            self.vy = 1.2
            self.imgType = "type_2"
            self.formation_idx = offset
            self.pos.x = 180 + (offset * 140) 
            self.pos.y = -60 - (offset * 40)   
            self.spawn_center_x = self.pos.x 
            self.movement_timer = 0
            self.shootDelay = 40 + (offset * 15)
            
        elif eType == "type6":
            self.hp = 15
            self.vy = 1.0
            self.imgType = "type_3"
            self.angle = offset * (math.pi / 2) 
            self.radius = 100 
            self.turn_speed = 0.04
            shared_center_x = WIDTH // 2 + math.sin(pygame.time.get_ticks() / 1000) * 200
            self.center_x = max(100, min(WIDTH - 100, shared_center_x))
            self.center_y = -100 
            self.pos.x = self.center_x + math.cos(self.angle) * self.radius
            self.pos.y = self.center_y + math.sin(self.angle) * self.radius
            self.shootDelay = 60 + (offset * 15)
        
        elif eType == "type6":
            self.hp = 15
            self.vy = 1.0  # 나선 하강 속도
            self.imgType = "type_3" # 보라색 계열 이미지 활용
            
            # 4마리가 십자 형태(90도 = math.pi/2 간격)로 대열을 이루도록 각도 분산
            self.angle = offset * (math.pi / 2) 
            self.radius = 100 # 회전 반경
            self.turn_speed = 0.04 # 회전 속도
            
            # 4마리가 완벽히 같은 중심점을 갖게 하기 위한 시간 기반 난수 트릭
            shared_center_x = WIDTH // 2 + math.sin(pygame.time.get_ticks() / 1000) * 200
            self.center_x = max(100, min(WIDTH - 100, shared_center_x))
            self.center_y = -100 # 화면 위에서 시작
            
            self.pos.x = self.center_x + math.cos(self.angle) * self.radius
            self.pos.y = self.center_y + math.sin(self.angle) * self.radius
            
            self.shootDelay = 60 + (offset * 15) # 발사 타이밍을 엇갈리게 설정

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
            
            elif self.eType == "type5":
                self.movement_timer += 0.04
                self.pos.x = self.spawn_center_x + math.sin(self.movement_timer) * 90
                self.pos.y += self.vy 
                if 0 <= self.pos.y <= HEIGHT:
                    self.shootDelay -= 1
                    if self.shootDelay <= 0:
                        eProjs.append(HomingProjectile(self.pos.x + 15, self.pos.y + 15, pygame.Vector2(0, 4.5), RED, 5, 7))
                        self.shootDelay = 140
                    
            # 나선형 원형 궤도 비행 (type6)
            elif self.eType == "type6":
                self.center_y += self.vy
                self.angle += self.turn_speed
                self.pos.x = self.center_x + math.cos(self.angle) * self.radius
                self.pos.y = self.center_y + math.sin(self.angle) * self.radius
                if 0 <= self.pos.y <= HEIGHT:
                    self.shootDelay -= 1
                    if self.shootDelay <= 0:
                        dirVec = pygame.Vector2(math.cos(self.angle), math.sin(self.angle)) * 5
                        eProjs.append(Projectile(self.pos.x + 15, self.pos.y + 15, dirVec, PURPLE, 5, 6))
                        self.shootDelay = 80

    def draw(self, surf):
        currentImg = assets.enemyImgs.get(self.imgType, assets.enemyImgs["type_1"])[self.state]
        surf.blit(currentImg, self.pos)
        
        # type3의 회전하는 투사체 시각화
        if self.state == "ATTACK" and self.eType == "type3":
            for angle in getattr(self, 'orbitAngles', []):
                offset = pygame.Vector2(0, 25).rotate(angle)
                pygame.draw.circle(surf, GOLD, (int(self.pos.x+25 + offset.x), int(self.pos.y+25 + offset.y)), 5)