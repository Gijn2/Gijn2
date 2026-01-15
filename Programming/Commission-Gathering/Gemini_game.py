import pygame
import random
import math

# 1. 초기화
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Roguelike Shooting: Advanced Enemies")
clock = pygame.time.Clock()

# 색상 및 폰트
WHITE, RED, GOLD, BLACK, GREEN, CYAN, PURPLE, GRAY = (255, 255, 255), (255, 50, 50), (255, 215, 0), (10, 10, 15), (50, 255, 50), (0, 255, 255), (200, 50, 255), (50, 50, 50)
font_s = pygame.font.SysFont("malgungothic", 16)
font_m = pygame.font.SysFont("malgungothic", 24)
font_l = pygame.font.SysFont("malgungothic", 40)

# 2. 게임 상태
stats = {"damage": 1, "speed": 5, "gold": 100, "max_hp": 100, "pierce": False, "special_ammo": 3}
player_hp = 100
score, game_state = 0, 'PLAYING'
shop_active_timer, shoot_cooldown = 0, 0
special_effect_timer = 0
shop_options = []

# [수정] 상점 옵션 및 가격 개별 책정
UPGRADE_POOL = [
    {"name": "공격력 강화", "desc": "데미지 +1.5", "effect": "dmg", "price": 50},
    {"name": "기동성 강화", "desc": "이동속도 +2", "effect": "speed", "price": 30},
    {"name": "긴급 수리", "desc": "체력 50 회복", "effect": "heal", "price": 40},
    {"name": "레일건", "desc": "탄환 관통 부여", "effect": "pierce", "price": 80},
    {"name": "장갑 강화", "desc": "최대 체력 +40", "effect": "maxhp", "price": 60},
    {"name": "특수기 보급", "desc": "W 횟수 +2회", "effect": "ammo", "price": 45},
    {"name": "보물 상자", "desc": "즉시 120골드 획득", "effect": "gold", "price": 20},
]

# 3. 클래스 정의
class Projectile:
    def __init__(self, x, y, vel, color, dmg):
        self.pos, self.vel, self.color, self.dmg = pygame.Vector2(x, y), vel, color, dmg
        self.hit_enemies = []
    def update(self): self.pos += self.vel
    def draw(self, surf): pygame.draw.circle(surf, self.color, (int(self.pos.x), int(self.pos.y)), 5)

class Enemy:
    def __init__(self, etype="normal", offset=0):
        self.etype = etype
        self.pos = pygame.Vector2(random.randint(50, WIDTH-50), random.randint(-150, -50))
        self.hp = 2 + (score // 5000)
        self.shoot_delay = random.randint(60, 120)
        self.spawn_time = pygame.time.get_ticks()
        self.offset = offset # SinWave 등을 위한 오프셋
        
        # 타입별 설정
        if etype == "bouncer":
            self.vx = random.choice([-3, 3]); self.vy = 2
        elif etype == "sniper":
            self.vx = 2; self.vy = 0; self.pos.y = random.randint(50, 150)
        else:
            self.vx = 0; self.vy = 1.5

    def update(self, e_projs, p_pos):
        if self.etype == "normal":
            self.pos.y += self.vy
        elif self.etype == "bouncer":
            self.pos += pygame.Vector2(self.vx, self.vy)
            if self.pos.x <= 0 or self.pos.x >= WIDTH - 30: self.vx *= -1
        elif self.etype == "sin":
            self.pos.y += 2
            self.pos.x += math.sin((pygame.time.get_ticks() + self.offset) / 200) * 5
        elif self.etype == "sniper":
            self.pos.x += self.vx
            if self.pos.x <= 0 or self.pos.x >= WIDTH - 30: self.vx *= -1

        # 조준 사격 (공통)
        self.shoot_delay -= 1
        if self.shoot_delay <= 0:
            direction = (p_pos + pygame.Vector2(20, 20)) - (self.pos + pygame.Vector2(15, 15))
            if direction.length() > 0:
                e_projs.append(Projectile(self.pos.x + 15, self.pos.y + 15, direction.normalize() * 4, GOLD, 5))
            self.shoot_delay = random.randint(120, 200)

class Boss:
    def __init__(self):
        self.pos, self.hp = pygame.Vector2(WIDTH//2 - 50, -120), 100 + (score//5)
        self.max_hp, self.timer = self.hp, 0
    def update(self, e_projs):
        if self.pos.y < 60: self.pos.y += 1.5
        self.timer += 1
        if self.timer > 40:
            for a in range(0, 360, 24):
                e_projs.append(Projectile(self.pos.x+50, self.pos.y+50, pygame.Vector2(0,1).rotate(a)*5, PURPLE, 10))
            self.timer = 0
    def draw(self, surf):
        pygame.draw.rect(surf, PURPLE, (*self.pos, 100, 100))
        pygame.draw.rect(surf, RED, (self.pos.x, self.pos.y-15, 100, 8))
        pygame.draw.rect(surf, GREEN, (self.pos.x, self.pos.y-15, (self.hp/self.max_hp)*100, 8))

# 4. 함수
def apply_upgrade(item):
    global player_hp
    if item['effect'] == "dmg": stats["damage"] += 1.5
    elif item['effect'] == "speed": stats["speed"] += 2
    elif item['effect'] == "heal": player_hp = min(stats["max_hp"], player_hp + 50)
    elif item['effect'] == "pierce": stats["pierce"] = True
    elif item['effect'] == "maxhp": stats["max_hp"] += 40; player_hp += 40
    elif item['effect'] == "ammo": stats["special_ammo"] += 2
    elif item['effect'] == "gold": stats["gold"] += 120

# 5. 게임 엔진
player_pos = pygame.Vector2(WIDTH//2, HEIGHT-80)
enemies = [Enemy() for _ in range(5)]
p_projs, e_projs, boss = [], [], None

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        
        if event.type == pygame.KEYDOWN:
            if game_state == 'PLAYING':
                if shop_active_timer > 0 and event.key == pygame.K_s:
                    game_state = 'SHOP'
                    shop_options = random.sample(UPGRADE_POOL, 4)
                if event.key == pygame.K_w and stats["special_ammo"] > 0:
                    stats["special_ammo"] -= 1; e_projs.clear(); special_effect_timer = 5
            
            elif game_state == 'SHOP':
                idx = {pygame.K_1:0, pygame.K_2:1, pygame.K_3:2, pygame.K_4:3}.get(event.key, -1)
                if idx != -1 and idx < len(shop_options):
                    item = shop_options[idx]
                    if stats["gold"] >= item["price"]:
                        stats["gold"] -= item["price"]; apply_upgrade(item); game_state, shop_active_timer = 'PLAYING', 0

        if event.type == pygame.MOUSEBUTTONDOWN and game_state == 'SHOP':
            for i in range(4):
                if pygame.Rect(30 + i * 215, 150, 200, 320).collidepoint(mouse_pos):
                    item = shop_options[i]
                    if stats["gold"] >= item["price"]:
                        stats["gold"] -= item["price"]; apply_upgrade(item); game_state, shop_active_timer = 'PLAYING', 0

    if game_state == 'PLAYING':
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player_pos.x -= stats["speed"]
        if keys[pygame.K_RIGHT]: player_pos.x += stats["speed"]
        if keys[pygame.K_UP]: player_pos.y -= stats["speed"]
        if keys[pygame.K_DOWN]: player_pos.y += stats["speed"]
        player_pos.x %= WIDTH
        player_pos.y = max(0, min(HEIGHT-40, player_pos.y))

        if keys[pygame.K_q] and shoot_cooldown <= 0:
            p_projs.append(Projectile(player_pos.x+20, player_pos.y, pygame.Vector2(0,-10), GREEN, stats["damage"]))
            shoot_cooldown = 8
        shoot_cooldown = max(0, shoot_cooldown - 1)
        shop_active_timer = max(0, shop_active_timer - 1)
        if special_effect_timer > 0: special_effect_timer -= 1

        # 보스 스폰 및 일반 몬스터 스폰 제어
        if score >= 1500 and score % 1500 < 100 and boss is None and shop_active_timer <= 0:
            boss = Boss()

        # [수정] 보스가 없을 때만 일반 몬스터 스폰
        if boss is None and len(enemies) < 6:
            etype = random.choices(["normal", "bouncer", "sin", "sniper"], weights=[40, 30, 20, 10])[0]
            if etype == "sin": # 사인파는 3마리씩 줄지어 나옴
                spawn_x = random.randint(100, WIDTH-100)
                for i in range(3):
                    e = Enemy("sin", i * 500); e.pos.x = spawn_x; enemies.append(e)
            else:
                enemies.append(Enemy(etype))

        if boss: boss.update(e_projs)
        if boss and boss.hp <= 0: boss = None; score += 1000; stats["gold"] += 200; shop_active_timer = 300

        for e in enemies[:]:
            e.update(e_projs, player_pos)
            if e.pos.distance_to(player_pos) < 35: player_hp -= 10; enemies.remove(e)
            elif e.pos.y > HEIGHT + 50: enemies.remove(e)

        for p in p_projs[:]:
            p.update()
            if boss and p.pos.distance_to(boss.pos + pygame.Vector2(50,50)) < 55:
                boss.hp -= p.dmg
                if not stats["pierce"]: p_projs.remove(p)
            for e in enemies[:]:
                if p.pos.distance_to(e.pos + pygame.Vector2(15,15)) < 25:
                    if e not in p.hit_enemies:
                        e.hp -= p.dmg
                        if stats["pierce"]: p.hit_enemies.append(e)
                        else: (p_projs.remove(p) if p in p_projs else None)
                        if e.hp <= 0: (enemies.remove(e) if e in enemies else None); score += 100; stats["gold"] += 15
            if p.pos.y < -10: (p_projs.remove(p) if p in p_projs else None)

        for p in e_projs[:]:
            p.update()
            if p.pos.distance_to(player_pos + pygame.Vector2(20,20)) < 22: player_hp -= p.dmg; e_projs.remove(p)
            elif p.pos.y > HEIGHT or p.pos.x < -50 or p.pos.x > WIDTH + 50: e_projs.remove(p)

        if player_hp <= 0: running = False

    # --- 그리기 ---
    screen.fill(BLACK)
    if game_state == 'PLAYING':
        for e in enemies:
            color = RED if e.etype == "normal" else CYAN if e.etype == "bouncer" else PURPLE if e.etype == "sin" else WHITE
            pygame.draw.rect(screen, color, (*e.pos, 30, 30))
        if boss: boss.draw(screen)
        for p in p_projs: p.draw(screen)
        for p in e_projs: p.draw(screen)
        pygame.draw.rect(screen, WHITE, (*player_pos, 40, 40), 2) # 플레이어
        
        pygame.draw.rect(screen, GRAY, (10, 10, 200, 20))
        pygame.draw.rect(screen, GREEN, (10, 10, max(0, (player_hp/stats["max_hp"])*200), 20))
        screen.blit(font_s.render(f"GOLD: {stats['gold']}  SCORE: {score}  W: {stats['special_ammo']}", True, WHITE), (10, 35))
        if shop_active_timer > 0:
            msg = font_m.render(f"보급 상점 이용 가능! [S] ({shop_active_timer//60}s)", True, GOLD)
            screen.blit(msg, (WIDTH//2 - 130, HEIGHT//2))
        if special_effect_timer > 0: screen.fill(WHITE)

    elif game_state == 'SHOP':
        for i, opt in enumerate(shop_options):
            card_rect = pygame.Rect(30 + i * 215, 150, 200, 320)
            color = (60, 60, 90) if card_rect.collidepoint(mouse_pos) else (30, 30, 50)
            pygame.draw.rect(screen, color, card_rect, border_radius=10)
            pygame.draw.rect(screen, GOLD, card_rect, 2, border_radius=10)
            screen.blit(font_l.render(f"{i+1}", True, GRAY), (card_rect.x + 85, card_rect.y + 20))
            screen.blit(font_m.render(opt['name'], True, WHITE), (card_rect.x + 20, card_rect.y + 100))
            screen.blit(font_s.render(opt['desc'], True, CYAN), (card_rect.x + 15, card_rect.y + 160))
            # [수정] 가격 표시 및 색상 피드백
            p_color = GOLD if stats["gold"] >= opt["price"] else RED
            screen.blit(font_m.render(f"{opt['price']} G", True, p_color), (card_rect.x + 60, card_rect.y + 260))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()