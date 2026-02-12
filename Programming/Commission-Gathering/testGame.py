import pygame
import random
import math
import os

# --- 1. 초기화 및 설정 ---
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Legendary Bosses: Final Edition (Optimized)")
clock = pygame.time.Clock()

# 색상 및 폰트
WHITE, RED, GOLD, BLACK, GREEN, CYAN, PURPLE, GRAY = (255, 255, 255), (255, 50, 50), (255, 215, 0), (10, 10, 15), (50, 255, 50), (0, 255, 255), (200, 50, 255), (50, 50, 50)
font_s = pygame.font.SysFont("malgungothic", 16)
font_m = pygame.font.SysFont("malgungothic", 24)
font_l = pygame.font.SysFont("malgungothic", 40)

# --- 2. 게임 상태 관리 ---
stats = {"damage": 1, "speed": 5, "gold": 100, "max_hp": 100, "pierce": False, "special_ammo": 3, "shoot_delay": 10}
player_hp = 100
score, game_state = 0, 'PLAYING'
shoot_cooldown = 0
special_effect_timer = 0
shake_timer = 0
zero_ticket = False 
STAGE_DURATION = 1800 
stage_timer = STAGE_DURATION
current_stage = 1
invincible_timer = 0
particles, enemies, p_projs, e_projs, boss = [], [], [], [], None
stocks = {"A": 100, "B": 100, "C": 100}
bank_balance = 0
shop_tab = "ITEM"

zero_ticket = False
boss = None
boss_alert_timer = 0

# 최고 점수 로드
high_score = 0
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        try: high_score = int(f.read())
        except: high_score = 0

# --- 3. 클래스 정의 ---
class Particle:
    def __init__(self, x, y, color):
        self.pos = [x, y]
        self.vel = [random.uniform(-3, 3), random.uniform(-3, 3)]
        self.life = 255
        self.color = color
    def update(self):
        self.pos[0] += self.vel[0]; self.pos[1] += self.vel[1]; self.life -= 8
    def draw(self, surf):
        if self.life > 0:
            p_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(p_surf, (*self.color, self.life), (3, 3), 3)
            surf.blit(p_surf, (self.pos[0]-3, self.pos[1]-3))

class Projectile:
    def __init__(self, x, y, vel, color, dmg):
        self.pos, self.vel, self.color, self.dmg = pygame.Vector2(x, y), vel, color, dmg
    def update(self): self.pos += self.vel
    def draw(self, surf): pygame.draw.circle(surf, self.color, (int(self.pos.x), int(self.pos.y)), 5)

class Enemy:
    def __init__(self, etype="normal"):
        self.etype = etype
        self.pos = pygame.Vector2(random.randint(50, WIDTH-50), -50)
        self.vx, self.vy = 0, 1.5
        if etype == "bouncer": self.vx, self.vy = random.choice([-3, 3]), 2
        elif etype == "sniper": self.vx, self.vy, self.pos.y = 2, 0, random.randint(50, 150)
        
        base_hp = (2 + (score // 5000)) * 0.25
        self.hp = base_hp * 8 if etype == "elite" else base_hp
        self.shoot_delay = random.randint(80, 160)
        self.rect = pygame.Rect(self.pos.x, self.pos.y, 40, 40)

    def shoot(self, e_projs, p_pos):
        diff = p_pos - self.pos
        direction = diff.normalize() * 4 if diff.length() > 0 else pygame.Vector2(0, 1)
        e_projs.append(Projectile(self.pos.x+20, self.pos.y+20, direction, GOLD, 5))

    def update(self, e_projs, p_pos):
        self.pos.y += self.vy; self.pos.x += self.vx
        if self.pos.x <= 0 or self.pos.x >= WIDTH-40: self.vx *= -1
        self.rect.topleft = self.pos
        self.shoot_delay -= 1
        if self.shoot_delay <= 0:
            self.shoot(e_projs, p_pos)
            self.shoot_delay = 180

class BossZero:
    def __init__(self):
        self.type = "ZERO"; self.pos = pygame.Vector2(WIDTH//2-25, 60)
        self.hp = 62.5; self.max_hp = 62.5; self.timer = 0; self.visible = True
    def update(self, e_projs, p_pos):
        self.timer += 1
        self.visible = False if (self.timer // 30) % 2 == 0 else True
        if self.timer % 80 == 0:
            # 보스가 화면 좌우 끝을 벗어나지 않도록 제한 (Testability)
            target_x = p_pos.x - 25
            self.pos.x = max(0, min(WIDTH - 50, target_x))
    def draw(self, surf):
        if self.visible:
            # 사각형 대신 로드한 boss_zero_img 사용
            surf.blit(boss_zero_img, self.pos)

class BossCrusher:
    def __init__(self):
        self.type = "CHERNOBOG"
        self.hp = 500; self.max_hp = 500
        # 보스의 실제 충돌 박스 (KISS: Rect를 속성으로 관리)
        self.rect = pygame.Rect(0, -100, WIDTH, 150)
        self.pos = pygame.Vector2(0, -100)
        self.mode = "MOVE"
        self.timer = 0
        self.beam_alpha = 0

    def update(self, e_projs, p_pos, player_obj=None): # player_obj를 인자로 받음
        self.timer += 1
        # 이동 시 rect도 함께 업데이트
        self.pos.x += math.sin(self.timer/20) * 5
        self.rect.topleft = self.pos

        if self.mode == "MOVE":
            if self.timer % 120 == 0: 
                self.mode = random.choice(["BEAM_READY", "HOMING"])
                self.timer = 0 # 타이머 리셋으로 다음 패턴 시간 확보

        elif self.mode == "BEAM_FIRE":
            if abs(p_pos.x - (self.pos.x + WIDTH//2)) < 60:
                # global을 선언해야 외부의 player_hp 변수를 수정할 수 있습니다.
                global player_hp 
                player_hp -= 2
                
class BossSwarm:
    def __init__(self):
        self.type = "SWARM"; self.hp = 125; self.max_hp = 125; self.timer = 0
        self.centers = [pygame.Vector2(random.randint(100,800), random.randint(50,200)) for _ in range(8)]
    def update(self, e_projs, p_pos):
        self.timer += 1
        for i, c in enumerate(self.centers):
            c.x += math.sin(self.timer/25 + i)*3
            if self.timer % 100 == 0:
                diff = p_pos - c
                if diff.length() > 0: # 에러 방지 (Safe Coding)
                    e_projs.append(Projectile(c.x, c.y, diff.normalize()*4, PURPLE, 6))
                else:
                    e_projs.append(Projectile(c.x, c.y, pygame.Vector2(0, 4), PURPLE, 6))
    def draw(self, surf):
            for c in self.centers:
                # 원 대신 boss_swarm_img 사용 (중심점 계산을 위해 이미지 크기의 절반인 50을 뺌)
                surf.blit(boss_swarm_img, (c.x - 50, c.y - 50))

# --- 4. 유틸리티 함수 ---
def get_discount_ratio():
    ratio = 2.0 - (stocks["C"] / 100.0)
    return max(0.5, min(2.0, ratio))

def apply_upgrade(item_data):
    global player_hp, boss
    eff = item_data['effect']
    if eff == "dmg": stats["damage"] += 1.5
    elif eff == "speed": stats["speed"] += 2
    elif eff == "heal": player_hp = min(stats["max_hp"], player_hp + 50)
    elif eff == "pierce": stats["pierce"] = True
    elif eff == "maxhp": stats["max_hp"] += 40; player_hp += 40
    elif eff == "ammo": stats["special_ammo"] += 2

# --- 5. 메인 루프 ---
running = True
player_pos = pygame.Vector2(WIDTH//2, HEIGHT-80)
UPGRADE_POOL = [
    {"name": "공격력 강화", "desc": "데미지 +1.5", "effect": "dmg", "price": 1200},
    {"name": "기동성 강화", "desc": "이동속도 +2", "effect": "speed", "price": 720},
    {"name": "긴급 수리", "desc": "체력 50 회복", "effect": "heal", "price": 960},
    {"name": "레일건", "desc": "탄환 관통 부여", "effect": "pierce", "price": 1920},
    {"name": "장갑 강화", "desc": "최대 체력 +40", "effect": "maxhp", "price": 1440},
    {"name": "특수기 보급", "desc": "W 횟수 +2회", "effect": "ammo", "price": 1080},
]

while running:
    clock.tick(60)
    temp_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if game_state == 'PLAYING':
                # [W 특수기 복구] 화면 정화 및 반전 효과
                if event.key == pygame.K_w and stats["special_ammo"] > 0:
                    stats["special_ammo"] -= 1
                    e_projs.clear() # 적 투사체 제거
                    special_effect_timer = 10 # 화면 반전
                    shake_timer = 20
            
            elif game_state == 'SHOP':
                if event.key == pygame.K_F1: shop_tab = "ITEM"
                if event.key == pygame.K_F2: shop_tab = "BANK"
                if event.key == pygame.K_F3: shop_tab = "INVEST"
                if event.key == pygame.K_s: game_state = 'PLAYING'; stage_timer = STAGE_DURATION; bank_balance = int(bank_balance * 1.1)
                
                if shop_tab == "INVEST":
                    keys = {pygame.K_1: "A", pygame.K_2: "B", pygame.K_3: "C"}
                    if event.key in keys:
                        sid = keys[event.key]
                        if stats["gold"] >= 500:
                            stats["gold"] -= 500; stocks[sid] += 10
                            if sid == "A": stats["speed"] += 0.5
                            if sid == "B": stats["shoot_delay"] = max(5, stats["shoot_delay"] - 1) # 쿨타임 감소 반영
                            
    # --- 상점 UI 렌더링 섹션 ---
    if game_state == 'SHOP':
        # 배경 상자
        pygame.draw.rect(screen, (30, 30, 50), (100, 50, 700, 500), border_radius=15)
        discount = get_discount_ratio() # C구역 지분 반영 할인율
        
        if shop_tab == "ITEM":
            screen.blit(font_m.render("--- ITEM SHOP (F1) ---", True, GOLD), (330, 70))
            for i, opt in enumerate(shop_options):
                item = opt["data"]
                price = int(item["price"] * discount) # 실시간 할인 적용
                color = GOLD if stats["gold"] >= price else GRAY
                
                y_pos = 150 + (i * 100)
                pygame.draw.rect(screen, (45, 45, 65), (150, y_pos, 600, 80), border_radius=10)
                screen.blit(font_m.render(f"{item['name']} - {price}G", True, color), (170, y_pos + 15))
                screen.blit(font_s.render(item["desc"], True, WHITE), (170, y_pos + 50))

        elif shop_tab == "BANK":
            screen.blit(font_m.render("--- CELESTE BANK (F2) ---", True, CYAN), (320, 70))
            bank_info = f"현재 예금: {bank_balance}G (다음 스테이지 이자 +10%)"
            screen.blit(font_m.render(bank_info, True, WHITE), (230, 250))
            
        elif shop_tab == "INVEST":
            screen.blit(font_m.render("--- INDUSTRIAL INVEST (F3) ---", True, GREEN), (300, 70))
            # 지분 투자용 UI (구역별 바 그래프 등) 추가 가능
            for i, area in enumerate(["A", "B", "C"]):
                y_pos = 200 + (i * 100)
                screen.blit(font_m.render(f"구역 {area} 지분: {stocks[area]}%", True, WHITE), (250, y_pos))
                pygame.draw.rect(screen, GREEN, (450, y_pos + 10, stocks[area] * 2, 20))
                pygame.draw.rect(screen, WHITE, (450, y_pos + 10, 200, 20), 2)
                screen.blit(font_s.render(f"투자 비용: 500G (지분 +10%)", True, WHITE), (250, y_pos + 40))
            # --- 게임 플레이 섹션 ---

    if game_state == 'PLAYING':
        # 플레이어 이동
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player_pos.x -= stats["speed"]
        if keys[pygame.K_RIGHT]: player_pos.x += stats["speed"]
        if keys[pygame.K_UP]: player_pos.y -= stats["speed"]
        if keys[pygame.K_DOWN]: player_pos.y += stats["speed"]
        player_pos.x = max(0, min(WIDTH-40, player_pos.x))
        player_pos.y = max(0, min(HEIGHT-40, player_pos.y))

        # 공격
        if keys[pygame.K_q] and shoot_cooldown <= 0:
            p_projs.append(Projectile(player_pos.x+20, player_pos.y, pygame.Vector2(0,-10), GREEN, stats["damage"]))
            shoot_cooldown = stats["shoot_delay"]
        shoot_cooldown = max(0, shoot_cooldown - 1)
        if invincible_timer > 0: invincible_timer -= 1

        # 적 생성 및 업데이트 루프
        if len(enemies) < 6 and stage_timer > 0:
            etype = random.choice(["normal", "bouncer", "sniper"])
            enemies.append(Enemy(etype))
        stage_timer -= 1
        if boss is None:
            stage_timer -= 1

            if stage_timer <= 0:
                if zero_ticket:
                    boss = BossZero()
                    zero_ticket = False
                else:
                    boss = BossSwarm()
                enemies.clear()
        if boss:
            boss.update(e_projs, player_pos)

            if boss.hp <= 0:
                stats["gold"] += 1500
                boss = None
                game_state = 'SHOP'
                
        # 통합 적 관리 루프 (ValueError 방지를 위해 복사본 순회)
        for e in enemies[:]:
            e.update(e_projs, player_pos)
            
            # [A] 플레이어 충돌
            p_rect = pygame.Rect(player_pos.x, player_pos.y, 40, 40)
            if p_rect.colliderect(e.rect) and invincible_timer <= 0:
                player_hp -= 15
                invincible_timer = 40
                if e in enemies: enemies.remove(e)
                continue

            # [B] 적 유출 (지분 하락 페널티)
            if e.pos.y > HEIGHT:
                if e in enemies:
                    enemies.remove(e)
                    # 랜덤 구역 지분 감소 (KISS)
                    target = random.choice(["A", "B", "C"])
                    stocks[target] -= 5
                continue

            # [C] 탄환 충돌 (관통 로직 포함)
            for p in p_projs[:]:
                if e.rect.collidepoint(p.pos):
                    e.hp -= stats["damage"]
                    if not stats["pierce"]: 
                        if p in p_projs: p_projs.remove(p)
                    if e.hp <= 0:
                        if e in enemies:
                            enemies.remove(e)
                            stats["gold"] += 35
                        break

        for p in e_projs[:]:
            p.update()
            if p.pos.distance_to(player_pos+pygame.Vector2(20,20)) < 25 and invincible_timer <= 0:
                player_hp -= p.dmg; e_projs.remove(p); shake_timer = 10; invincible_timer = 30
            elif p.pos.y > HEIGHT: e_projs.remove(p)
        for p in p_projs[:]:
            p.update()
            if p.pos.y < 0: p_projs.remove(p)
        for p in particles[:]:
            p.update()
            if p.life <= 0: particles.remove(p)

    # --- 렌더링 ---
    screen.fill(BLACK)
    if special_effect_timer > 0: screen.fill(WHITE); special_effect_timer -= 1
    
    # 오브젝트 그리기
    for e in enemies: pygame.draw.rect(screen, RED, e.rect)
    for p in p_projs: p.draw(screen)
    for p in e_projs: p.draw(screen)
    for p in particles: p.draw(screen)
    if invincible_timer % 4 == 0: pygame.draw.rect(screen, CYAN, (player_pos.x, player_pos.y, 40, 40))

    # UI 렌더링 (지분 및 상태)
    avg_s = sum(stocks.values()) / 3
    rank = "Noble" if avg_s > 85 else "Commoner"
    screen.blit(font_s.render(f"HP: {player_hp} | GOLD: {stats['gold']} | AMMO: {stats['special_ammo']} | RANK: {rank}", True, WHITE), (10, 10))
    
    if game_state == 'SHOP':
        pygame.draw.rect(screen, (30, 30, 50), (100, 100, 700, 400))
        screen.blit(font_m.render(f"--- SHOP ({shop_tab}) - Press S to Next Stage ---", True, GOLD), (250, 120))
        # 상점 내용물은 shop_tab에 따라 조건부 렌더링 (기본 구조 유지)

    pygame.display.flip()

pygame.quit()