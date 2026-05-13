# 투사체 관리: Projectile, HomingProjectile, Meteor, Particle
import pygame
import random
from constants import *
from main import meteorImg
from assetManager import *

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
