import pygame
import random
import math

# 1. 초기화 및 기본 설정
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Roguelike: Auto-Targeting & Auto-Exit")
clock = pygame.time.Clock()

# 색상 정의
WHITE, RED, GOLD, BLACK, GREEN, CYAN, PURPLE = (255, 255, 255), (255, 50, 50), (255, 215, 0), (10, 10, 15), (50, 255, 50), (0, 255, 255), (200, 50, 255)

# 2. 전역 상태 및 메타 데이터
permanent_stats = {
    "damage": 1, 
    "speed": 5, 
    "gold": 0,
    "weapon_type": "NORMAL",
    "dmg_price": 50,
    "spd_price": 50
}
score = 0
player_hp = 100
game_state = 'PLAYING'

# --- 에셋 로드 함수 ---
def get_surf(size, color, alpha=255):
    surf = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(surf, (*color, alpha), (0, 0, size[0], size[1]))
    return surf

player_img = get_surf((40, 40), WHITE)
enemy_img = get_surf((30, 30), RED)
boss_img = get_surf((100, 100), PURPLE)

# 3. 클래스 정의
class Item:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.type = random.choice(['HEAL', 'SPEED'])
        self.color = GREEN if self.type == 'HEAL' else CYAN
        self.lifetime = 600

    def draw(self, surface, offset):
        pygame.draw.rect(surface, self.color, (self.pos.x + offset.x, self.pos.y + offset.y, 15, 15))

class Projectile:
    def __init__(self, x, y, velocity, color, damage):
        self.pos = pygame.Vector2(x, y)
        self.vel = velocity
        self.color = color
        self.damage = damage

    def update(self):
        self.pos += self.vel

    def draw(self, surface, offset):
        pygame.draw.circle(surface, self.color, (int(self.pos.x + offset.x), int(self.pos.y + offset.y)), 5)

class Boss:
    def __init__(self):
        self.pos = pygame.Vector2(WIDTH//2 - 50, -150)
        self.target_y = 80
        self.hp = 150
        self.max_hp = 150
        self.shoot_timer = 0

    def update(self, player_pos, projectiles):
        if self.pos.y < self.target_y: self.pos.y += 2
        self.shoot_timer += 1
        if self.shoot_timer > 50:
            for i in range(12):
                angle = i * (360 / 12)
                dir_vec = pygame.Vector2(1, 0).rotate(angle) * 5
                projectiles.append(Projectile(self.pos.x + 50, self.pos.y + 50, dir_vec, PURPLE, 10))
            self.shoot_timer = 0

    def draw(self, surface, offset):
        surface.blit(boss_img, (self.pos.x + offset.x, self.pos.y + offset.y))
        pygame.draw.rect(surface, RED, (self.pos.x, self.pos.y - 20, 100, 10))
        pygame.draw.rect(surface, GREEN, (self.pos.x, self.pos.y - 20, (self.hp/self.max_hp)*100, 10))

class Enemy:
    def __init__(self):
        self.pos = pygame.Vector2(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50))
        self.hp = 3
        self.shoot_timer = random.randint(60, 150)

    def update(self, player_pos, projectiles):
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            dir_vec = (player_pos - self.pos).normalize() * 4
            projectiles.append(Projectile(self.pos.x, self.pos.y, dir_vec, GOLD, 5))
            self.shoot_timer = random.randint(100, 200)

# 4. 초기 객체 생성
player_pos = pygame.Vector2(WIDTH//2, HEIGHT//2)
enemies = [Enemy() for _ in range(5)]
items = []
player_projectiles = []
enemy_projectiles = []
boss = None
shoot_cooldown = 0
screen_shake = 0

# 5. 메인 루프
running = True
while running:
    # [요청 기능 2] 피가 0 이하가 되면 자동으로 게임 종료
    if player_hp <= 0:
        running = False

    # --- 1) 이벤트 처리 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s: game_state = 'SHOP' if game_state == 'PLAYING' else 'PLAYING'
            if event.key == pygame.K_1: permanent_stats["weapon_type"] = "NORMAL"
            if event.key == pygame.K_2: permanent_stats["weapon_type"] = "SHOTGUN"

    # --- 2) 게임 로직 ---
    if game_state == 'PLAYING':
        # 이동 및 공간 이동
        keys = pygame.key.get_pressed()
        move = pygame.Vector2(0,0)
        if keys[pygame.K_LEFT]: move.x = -1
        if keys[pygame.K_RIGHT]: move.x = 1
        if keys[pygame.K_UP]: move.y = -1
        if keys[pygame.K_DOWN]: move.y = 1
        if move.length() > 0: player_pos += move.normalize() * permanent_stats["speed"]

        player_size = 40
        if player_pos.x > WIDTH: player_pos.x = -player_size
        elif player_pos.x < -player_size: player_pos.x = WIDTH
        if player_pos.y > HEIGHT: player_pos.y = -player_size
        elif player_pos.y < -player_size: player_pos.y = HEIGHT

        # [요청 기능 1] 가장 가까운 대상 자동 조준 사격
        if shoot_cooldown <= 0:
            p_center = player_pos + pygame.Vector2(20, 20)
            target_pos = None
            min_dist = 9999
            
            # 모든 적과 보스 중 가장 가까운 것 찾기
            targets = list(enemies)
            if boss: targets.append(boss)
            
            for t in targets:
                # 보스는 중심점이 다르므로 보정
                t_pos = t.pos + (pygame.Vector2(50,50) if isinstance(t, Boss) else pygame.Vector2(0,0))
                dist = p_center.distance_to(t_pos)
                if dist < min_dist:
                    min_dist = dist
                    target_pos = t_pos
            
            # 타겟이 있으면 발사, 없으면 마우스 방향
            if target_pos:
                base_dir = (target_pos - p_center).normalize()
            else:
                m_pos = pygame.Vector2(pygame.mouse.get_pos())
                base_dir = (m_pos - p_center).normalize() if (m_pos - p_center).length() > 0 else pygame.Vector2(0, -1)

            if permanent_stats["weapon_type"] == "NORMAL":
                player_projectiles.append(Projectile(p_center.x, p_center.y, base_dir * 8, GREEN, permanent_stats["damage"]))
            elif permanent_stats["weapon_type"] == "SHOTGUN":
                for angle in [-20, 0, 20]:
                    player_projectiles.append(Projectile(p_center.x, p_center.y, base_dir.rotate(angle) * 7, (200, 255, 100), permanent_stats["damage"]))
            
            shoot_cooldown = 30 # 0.5초 주기
        
        if shoot_cooldown > 0: shoot_cooldown -= 1

        # 업데이트 및 충돌 체크
        if score >= 200 and boss is None: boss = Boss()
        if boss: boss.update(player_pos + pygame.Vector2(20,20), enemy_projectiles)
        for e in enemies: e.update(player_pos + pygame.Vector2(20,20), enemy_projectiles)
        
        for p in player_projectiles[:]:
            p.update()
            if boss and p.pos.distance_to(boss.pos + pygame.Vector2(50,50)) < 50:
                boss.hp -= p.damage
                player_projectiles.remove(p)
                if boss.hp <= 0: boss = None; score += 1000; permanent_stats["gold"] += 500
            else:
                for e in enemies[:]:
                    if p.pos.distance_to(e.pos) < 20:
                        e.hp -= p.damage
                        if p in player_projectiles: player_projectiles.remove(p)
                        if e.hp <= 0:
                            enemies.remove(e); enemies.append(Enemy())
                            score += 20; permanent_stats["gold"] += 10
                            if random.random() < 0.3: items.append(Item(e.pos.x, e.pos.y))
            if not screen.get_rect().inflate(100, 100).collidepoint(p.pos):
                if p in player_projectiles: player_projectiles.remove(p)

        for p in enemy_projectiles[:]:
            p.update()
            if p.pos.distance_to(player_pos + pygame.Vector2(20,20)) < 25:
                player_hp -= p.damage; enemy_projectiles.remove(p); screen_shake = 10
            elif not screen.get_rect().inflate(100, 100).collidepoint(p.pos): enemy_projectiles.remove(p)

        for i in items[:]:
            if i.pos.distance_to(player_pos + pygame.Vector2(20,20)) < 30:
                if i.type == 'HEAL': player_hp = min(100, player_hp + 25)
                else: permanent_stats["speed"] += 0.2
                items.remove(i)

    # --- 3) 그리기 ---
    screen.fill(BLACK)
    offset = pygame.Vector2(random.uniform(-screen_shake, screen_shake), random.uniform(-screen_shake, screen_shake)) if screen_shake > 0 else pygame.Vector2(0,0)
    if screen_shake > 0: screen_shake -= 1

    if game_state == 'PLAYING':
        for i in items: i.draw(screen, offset)
        for p in player_projectiles: p.draw(screen, offset)
        for p in enemy_projectiles: p.draw(screen, offset)
        for e in enemies: screen.blit(enemy_img, (e.pos.x - 15 + offset.x, e.pos.y - 15 + offset.y))
        if boss: boss.draw(screen, offset)
        screen.blit(player_img, (player_pos.x + offset.x, player_pos.y + offset.y))

        font = pygame.font.SysFont("malgungothic", 20)
        ui_txt = font.render(f"HP: {int(player_hp)} | Target: Auto | Firing: 0.5s", True, GOLD)
        screen.blit(ui_txt, (20, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()