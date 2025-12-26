import pygame
import random
import math

# 1. 초기화 및 설정
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# 색상 및 상점(메타 프로그레션) 데이터
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GOLD = (255, 215, 0)
BLACK = (10, 10, 15)

# 영구 능력치 (메타 프로그레션 예시)
permanent_stats = {"damage": 1, "speed": 5, "gold": 0}

class Particle:
    """ [요소 2: 주스 - 파티클 효과] """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)
        self.lifetime = 20

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

class Player:
    def __init__(self):
        self.pos = pygame.Vector2(WIDTH//2, HEIGHT//2)
        self.speed = permanent_stats["speed"]
        self.hp = 100
        self.shake_intensity = 0

    def move(self, keys):
        vel = pygame.Vector2(0, 0)
        if keys[pygame.K_LEFT]: vel.x = -1
        if keys[pygame.K_RIGHT]: vel.x = 1
        if keys[pygame.K_UP]: vel.y = -1
        if keys[pygame.K_DOWN]: vel.y = 1
        if vel.length() > 0:
            self.pos += vel.normalize() * self.speed

class Enemy:
    def __init__(self):
        self.pos = pygame.Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.hp = 3

# 게임 루프 변수
player = Player()
enemies = [Enemy() for _ in range(5)]
particles = []
screen_shake = 0
score = 0

running = True
while running:
    # 화면 흔들림 계산 [요소 2: 주스]
    offset = pygame.Vector2(0, 0)
    if screen_shake > 0:
        offset = pygame.Vector2(random.uniform(-screen_shake, screen_shake), 
                                random.uniform(-screen_shake, screen_shake))
        screen_shake -= 1

    screen.fill(BLACK)
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # 공격 및 충돌 (간략화된 로직)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            for e in enemies[:]:
                dist = player.pos.distance_to(e.pos)
                if dist < 100: # 공격 범위
                    e.hp -= permanent_stats["damage"]
                    # [요소 2: 주스 - 피격 효과]
                    screen_shake = 10 
                    for _ in range(10): particles.append(Particle(e.pos.x, e.pos.y))
                    
                    if e.hp <= 0:
                        enemies.remove(e)
                        enemies.append(Enemy()) # [요소 1: 무작위성 - 새로운 적 생성]
                        permanent_stats["gold"] += 10
                        score += 1

    # 업데이트 및 그리기
    player.move(keys)
    
    # 파티클 업데이트
    for p in particles[:]:
        p.update()
        if p.lifetime <= 0: particles.remove(p)
        pygame.draw.circle(screen, RED, (int(p.x + offset.x), int(p.y + offset.y)), 3)

    # 플레이어 및 적 그리기
    pygame.draw.rect(screen, WHITE, (player.pos.x + offset.x, player.pos.y + offset.y, 30, 30))
    for e in enemies:
        pygame.draw.circle(screen, RED, (int(e.pos.x + offset.x), int(e.pos.y + offset.y)), 15)

    # UI (메타 프로그레션 확인)
    font = pygame.font.SysFont(None, 36)
    gold_text = font.render(f"GOLD: {permanent_stats['gold']} (Press Z to Attack)", True, GOLD)
    screen.blit(gold_text, (20, 20))

    pygame.display.flip()
    clock.tick(60)


pygame.quit()