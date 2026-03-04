import pygame
import random
from constants import *

class Projectile: # 기존 코드 이동 및 네이밍 수정
    def __init__(self, x, y, vel, color, radius, damage):
        self.pos = pygame.Vector2(x, y)
        self.vel = vel
        self.color = color
        self.radius = radius
        self.damage = damage

class BossChernobog: # 요청 사항 4번: 최종 보스 추가
    def __init__(self):
        self.type = "CHERNOBOG"
        self.hp = 5000
        self.maxHp = 5000
        self.pos = pygame.Vector2(WIDTH // 2, -100)
        self.targetY = 150
        self.timer = 0

    def update(self, eProjs):
        if self.pos.y < self.targetY: self.pos.y += 2
        self.timer += 1
        # 최종 보스 패턴: 원형 탄막
        if self.timer % 40 == 0:
            for i in range(0, 360, 20):
                rad = pygame.Vector2(0, 5).rotate(i)
                eProjs.append(Projectile(self.pos.x, self.pos.y, rad, PURPLE, 12, 20))

    def draw(self, surf):
        pygame.draw.circle(surf, PURPLE, (int(self.pos.x), int(self.pos.y)), 60)
        # 보스 체력바
        hpW = (self.hp / self.maxHp) * 400
        pygame.draw.rect(surf, RED, (WIDTH//2 - 200, 20, 400, 10))
        pygame.draw.rect(surf, GREEN, (WIDTH//2 - 200, 20, hpW, 10))