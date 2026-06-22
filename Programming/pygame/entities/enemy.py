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
        self.vy = config["vy"]
        self.imgType = config["img_key"]

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
        elif eType == "type5":
            self.hp = 25
            self.vy = 1.2  # 천천히 전진 배치하며 내려옴
            self.imgType = "type_2" # 기존 로드된 에셋 키 활용 (필요시 교체 가능)
            
            # 대열 내에서의 순번(0, 1, 2, 3...)을 offset 매개변수로 받아 배치 구조 설계
            self.formation_idx = offset
            # 순번에 따라 가로 간격을 벌리고 위쪽 화면 밖 사선 배치 형태(V자 혹은 대각선)로 스폰
            self.pos.x = 180 + (offset * 140) 
            self.pos.y = -60 - (offset * 40)   
            
            self.spawn_center_x = self.pos.x   # 지그재그 운동의 중심이 될 가로 축 기억
            self.movement_timer = 0
            self.shootDelay = 40 + (offset * 15) # 순차적 발사를 위한 딜레이 스태거링

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
                self.movement_timer += 0.04 # 지그재그 진동 속도 제어
                
                # 1. 이동: 중심축을 기준으로 사인파를 돌려 부드러운 S자 지그재그 횡이동 구현
                # 진동 너비 폭을 90픽셀 정도로 지정
                self.pos.x = self.spawn_center_x + math.sin(self.movement_timer) * 90
                self.pos.y += self.vy 
                
                # 2. 공격: 플레이어를 향해 조준 및 유도형 투사체 발사 패턴
                self.shootDelay -= 1
                if self.shootDelay <= 0:
                    # 플레이어의 중심점을 직접적으로 쫓아가는 기존 HomingProjectile 클래스를 사용해 투사체 추가
                    eProjs.append(HomingProjectile(self.pos.x + 15, self.pos.y + 15, pygame.Vector2(0, 4.5), RED, 5, 7))
                    self.shootDelay = 140 # 다음 발사 주기 재장전

    def draw(self, surf):
        currentImg = assets.enemyImgs.get(self.imgType, assets.enemyImgs["type_1"])[self.state]
        surf.blit(currentImg, self.pos)
        
        # type3의 회전하는 투사체 시각화
        if self.state == "ATTACK" and self.eType == "type3":
            for angle in getattr(self, 'orbitAngles', []):
                offset = pygame.Vector2(0, 25).rotate(angle)
                pygame.draw.circle(surf, GOLD, (int(self.pos.x+25 + offset.x), int(self.pos.y+25 + offset.y)), 5)