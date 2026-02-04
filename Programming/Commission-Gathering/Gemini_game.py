import pygame
import random
import math
import os


# --- 0. 경로 설정 ---
IMGS_PATH = os.path.join(os.path.dirname(__file__), "imgs")

# --- 1. 초기화 및 화면 설정 ---
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Legendary Bosses: Final Edition (Visual Enhanced)")
clock = pygame.time.Clock()

# --- 2. 에셋 로드 (화면 설정 후 로드해야 함) --

# 플레이어 및 적 이미지 로드
bg_img = pygame.image.load(os.path.join(IMGS_PATH, "background.png")).convert()
player_img = pygame.image.load(os.path.join(IMGS_PATH, "player.png")).convert_alpha()
player_img = pygame.transform.scale(player_img, (60, 60))

enemy1_img = pygame.image.load(os.path.join(IMGS_PATH, "enemy_1.png")).convert_alpha()
enemy1_img = pygame.transform.scale(enemy1_img, (50, 50))
enemy2_img = pygame.image.load(os.path.join(IMGS_PATH, "enemy_2.png")).convert_alpha()
enemy2_img = pygame.transform.scale(enemy2_img, (50, 50))
enemy3_img = pygame.image.load(os.path.join(IMGS_PATH, "enemy_3.png")).convert_alpha()
enemy3_img = pygame.transform.scale(enemy3_img, (50, 50))
enemy4_img = pygame.image.load(os.path.join(IMGS_PATH, "enemy_4.png")).convert_alpha()
enemy4_img = pygame.transform.scale(enemy4_img, (50, 50))

boss_swarm_img = pygame.image.load(os.path.join(IMGS_PATH, "boss_swarm.png")).convert_alpha()
boss_swarm_img = pygame.transform.scale(boss_swarm_img, (100, 100))
boss_zero_img = pygame.image.load(os.path.join(IMGS_PATH, "boss_zero.png")).convert_alpha()
boss_zero_img = pygame.transform.scale(boss_zero_img, (50, 50))

# [추가] 보스용 이미지 (파일이 없다면 기본 도형으로 대체되도록 예외처리 가능)
# 현재는 기존 도형 렌더링 유지하며 이미지 출력 로직만 준비

# 색상 및 폰트
WHITE, RED, GOLD, BLACK, GREEN, CYAN, PURPLE, GRAY = (255, 255, 255), (255, 50, 50), (255, 215, 0), (10, 10, 15), (50, 255, 50), (0, 255, 255), (200, 50, 255), (50, 50, 50)
font_s = pygame.font.SysFont("malgungothic", 16)
font_m = pygame.font.SysFont("malgungothic", 24)
font_l = pygame.font.SysFont("malgungothic", 40)

# --- 3. 게임 상태 관리 변수 ---
stats = {"damage": 1, "speed": 5, "gold": 100, "max_hp": 100, "pierce": False, "special_ammo": 3}
player_hp = 100
score, game_state = 0, 'PLAYING'
shoot_cooldown = 0
special_effect_timer = 0
shake_timer = 0
zero_ticket = False 
STAGE_DURATION = 1800 # 30초
stage_timer = STAGE_DURATION
boss_alert_timer = 0
current_stage = 1
invincible_timer = 0

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

# --- 4. 클래스 정의 ---

class Projectile:
    def __init__(self, x, y, vel, color, dmg):
        self.pos, self.vel, self.color, self.dmg = pygame.Vector2(x, y), vel, color, dmg
    def update(self): self.pos += self.vel
    def draw(self, surf): pygame.draw.circle(surf, self.color, (int(self.pos.x), int(self.pos.y)), 5)

class BossZero:
    def __init__(self):
        self.type = "ZERO"; self.pos = pygame.Vector2(WIDTH//2-25, 60)
        self.hp = 62.5; self.max_hp = 62.5; self.timer = 0; self.visible = True
    def update(self, e_projs, p_pos):
        self.timer += 1
        self.visible = False if (self.timer // 30) % 2 == 0 else True
        if self.timer % 80 == 0:
            self.pos.x = p_pos.x - 25
            for i in range(5): e_projs.append(Projectile(self.pos.x+25, self.pos.y+50+i*20, pygame.Vector2(0, 8), CYAN, 15))
    def draw(self, surf):
        if self.visible:
            # 사각형 대신 로드한 boss_zero_img 사용
            surf.blit(boss_zero_img, self.pos)

class BossCrusher:
    def __init__(self):
        self.type = "CRUSHER"; self.hp = 300; self.max_hp = 300; self.timer = 0
        self.mode = "READY"; self.rect = pygame.Rect(0, -600, WIDTH, 150)
        self.warning_timer = 45 
        self.target_mode = "TOP"

    def update(self, e_projs, p_pos):
        self.timer += 1
        if self.mode == "READY":
            self.warning_timer -= 1
            if self.warning_timer <= 0:
                self.mode = "ATTACK"
                self.warning_timer = 45
        else:
            if self.target_mode == "TOP":
                attack_range = 600 
                offset = math.sin(self.timer/8) * attack_range
                self.rect = pygame.Rect(0, -350 + offset, WIDTH, 150)
            else:
                attack_range = 1200
                offset = math.sin(self.timer/8) * attack_range
                if self.target_mode == "LEFT": self.rect = pygame.Rect(-500 + offset, 0, 150, HEIGHT)
                elif self.target_mode == "RIGHT": self.rect = pygame.Rect(WIDTH + 500 - offset, 0, 150, HEIGHT)
            
            if self.timer % 140 == 0: 
                self.mode = "READY"
                self.target_mode = random.choice(["TOP", "LEFT", "RIGHT"])

    def draw(self, surf):
        if self.mode == "READY":
            if self.target_mode == "TOP": pygame.draw.rect(surf, (150, 0, 0), (0, 0, WIDTH, 150), 2)
            elif self.target_mode == "LEFT": pygame.draw.rect(surf, (150, 0, 0), (0, 0, 150, HEIGHT), 2)
            elif self.target_mode == "RIGHT": pygame.draw.rect(surf, (150, 0, 0), (WIDTH-150, 0, 150, HEIGHT), 2)
        
        pygame.draw.rect(surf, GRAY, self.rect)
        if self.mode == "ATTACK": pygame.draw.rect(surf, RED, self.rect, 4)

class BossSwarm:
    def __init__(self):
        self.type = "SWARM"; self.hp = 125; self.max_hp = 125; self.timer = 0
        self.centers = [pygame.Vector2(random.randint(100,800), random.randint(50,200)) for _ in range(8)]
    def update(self, e_projs, p_pos):
        self.timer += 1
        for i, c in enumerate(self.centers):
            c.x += math.sin(self.timer/25 + i)*3
            if self.timer % 100 == 0: e_projs.append(Projectile(c.x, c.y, (p_pos-c).normalize()*4, PURPLE, 6))
    def draw(self, surf):
            for c in self.centers:
                # 원 대신 boss_swarm_img 사용 (중심점 계산을 위해 이미지 크기의 절반인 50을 뺌)
                surf.blit(boss_swarm_img, (c.x - 50, c.y - 50))

class Enemy:
    def __init__(self, etype="normal", offset=0):
        self.etype = etype
        self.pos = pygame.Vector2(random.randint(50, WIDTH-50), -50)
        self.offset = offset
        self.shoot_delay = random.randint(80, 160)
        
        # 모든 적이 반드시 hp 속성을 가지도록 초기화
        base_hp = (2 + (score // 5000)) * 0.25 
        if etype == "elite":
            self.hp = base_hp * 8
        else:
            self.hp = base_hp
            
        # 속도 설정
        if etype == "bouncer": self.vx, self.vy = random.choice([-3, 3]), 2
        elif etype == "sniper": self.vx, self.vy = 2, 0; self.pos.y = random.randint(50, 150)
        elif etype == "sin": self.vx, self.vy = 0, 1.8
        else: self.vx, self.vy = 0, 1.5

    def update(self, e_projs, p_pos):
        if self.etype == "sin":
            self.pos.y += self.vy
            self.pos.x += math.sin((pygame.time.get_ticks() + self.offset) / 200) * 5
        else:
            self.pos.y += self.vy
            self.pos.x += self.vx
            if self.pos.x <= 0 or self.pos.x >= WIDTH-30: self.vx *= -1

        self.shoot_delay -= 1
        if self.shoot_delay <= 0:
            dist = (p_pos - self.pos).length()
            dir = (p_pos - self.pos).normalize() * 4 if dist > 0 else pygame.Vector2(0,1)
            e_projs.append(Projectile(self.pos.x+15, self.pos.y+15, dir, GOLD, 5))
            self.shoot_delay = 180

    def draw(self, surf):
        img = enemy1_img  # 기본
        if self.etype == "bouncer": img = enemy2_img
        elif self.etype == "sin": img = enemy3_img
        elif self.etype == "sniper": img = enemy4_img
        
        surf.blit(img, self.pos)
        
        # 엘리트 전용 시각 효과
        if self.etype == "elite":
            pygame.draw.circle(surf, PURPLE, (int(self.pos.x+25), int(self.pos.y+25)), 35, 2)
            surf.blit(font_m.render("!", True, PURPLE), (self.pos.x+10, self.pos.y-35))

    

# --- 5. 유틸리티 함수 ---

def get_shop_items():
    return [{"data": item, "sold": False} for item in random.sample(UPGRADE_POOL, 4)]

def apply_upgrade(item_data):
    global player_hp, boss
    eff = item_data['effect']
    if eff == "dmg": stats["damage"] += 1.5
    elif eff == "speed": stats["speed"] += 2
    elif eff == "heal": player_hp = min(stats["max_hp"], player_hp + 50)
    elif eff == "pierce": stats["pierce"] = True
    elif eff == "maxhp": stats["max_hp"] += 40; player_hp += 40
    elif eff == "ammo": stats["special_ammo"] += 2
    elif eff == "call_crusher": boss = BossCrusher()

# --- 6. 메인 게임 루프 ---

player_pos = pygame.Vector2(WIDTH//2, HEIGHT-80)
enemies, p_projs, e_projs, boss = [], [], [], None
shop_options = []

running = True


while running:
   
    # 화면 흔들림 효과 계산
    render_offset = pygame.Vector2(0, 0)
    if shake_timer > 0:
        render_offset = pygame.Vector2(random.randint(-7, 7), random.randint(-7, 7))
        shake_timer -= 1

    mouse_pos = pygame.mouse.get_pos()
    
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        
        if event.type == pygame.KEYDOWN:
            if game_state == 'PLAYING':
                if event.key == pygame.K_w and stats["special_ammo"] > 0:
                    stats["special_ammo"] -= 1
                    e_projs.clear()
                    special_effect_timer = 5
            elif game_state == 'SHOP' and event.key == pygame.K_s:
                game_state = 'PLAYING'; stage_timer = STAGE_DURATION; current_stage += 1

        if event.type == pygame.MOUSEBUTTONDOWN and game_state == 'SHOP':
            for opt in shop_options:
                idx = shop_options.index(opt)
                rect = pygame.Rect(30 + idx * 215, 150, 200, 320)
                if rect.collidepoint(mouse_pos) and not opt["sold"] and stats["gold"] >= opt["data"]["price"]:
                    stats["gold"] -= opt["data"]["price"]
                    apply_upgrade(opt["data"])
                    opt["sold"] = True

    if game_state == 'PLAYING':
        # 이동 로직
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player_pos.x -= stats["speed"]
        if keys[pygame.K_RIGHT]: player_pos.x += stats["speed"]
        if keys[pygame.K_UP]: player_pos.y -= stats["speed"]
        if keys[pygame.K_DOWN]: player_pos.y += stats["speed"]

        # 워프 및 경계 제한
        if player_pos.x < -30: player_pos.x = WIDTH
        elif player_pos.x > WIDTH: player_pos.x = -30
        player_pos.y = max(0, min(HEIGHT-40, player_pos.y))

        # 공격 로직
        if keys[pygame.K_q] and shoot_cooldown <= 0:
            p_projs.append(Projectile(player_pos.x+20, player_pos.y, pygame.Vector2(0,-10), GREEN, stats["damage"]))
            shoot_cooldown = 10
        shoot_cooldown = max(0, shoot_cooldown - 1)
        if invincible_timer > 0: invincible_timer -= 1

        # 적 생성 및 보스 체크
        if boss is None:
            stage_timer -= 1
            if stage_timer == 120: boss_alert_timer = 120
            if stage_timer <= 0:
                if zero_ticket: boss = BossZero(); zero_ticket = False
                else: boss = BossSwarm()
                enemies.clear()
            
            if len(enemies) < 6:
                etype = random.choices(["normal", "bouncer", "sin", "sniper", "elite"], weights=[50, 15, 15, 18.5, 1.5])[0]
                enemies.append(Enemy(etype, random.randint(0, 1000)))

        # 보스 업데이트
        if boss:
            boss.update(e_projs, player_pos)
            boss_rect = getattr(boss, 'rect', pygame.Rect(boss.pos.x, boss.pos.y, 50, 50) if hasattr(boss, 'pos') else None)
            if boss_rect and boss_rect.colliderect(pygame.Rect(player_pos.x, player_pos.y, 40, 40)) and invincible_timer <= 0:
                player_hp -= 20; shake_timer = 20; invincible_timer = 60
            
            if boss.hp <= 0:
                stats["gold"] += 1500; boss = None; game_state = 'SHOP'; shop_options = get_shop_items()

        # 충돌 처리
        p_rect = pygame.Rect(player_pos.x, player_pos.y, 40, 40)
        for e in enemies[:]:
            e.update(e_projs, player_pos)
            if p_rect.colliderect(pygame.Rect(e.pos.x, e.pos.y, 30, 30)) and invincible_timer <= 0:
                player_hp -= 15; shake_timer = 15; invincible_timer = 40; enemies.remove(e)
            elif e.pos.y > HEIGHT: enemies.remove(e)

        # 투사체 충돌 (플레이어 탄환)
        for p in p_projs[:]:
            p.update()
            hit_this_frame = False
            if boss:
                hit = False
                if boss.type == "CRUSHER" and boss.rect.collidepoint(p.pos): hit = True
                elif boss.type == "SWARM":
                    for c in boss.centers:
                        if p.pos.distance_to(c) < 25: hit = True; break
                elif boss.type == "ZERO" and p.pos.distance_to(boss.pos + pygame.Vector2(25,25)) < 40: hit = True
                if hit:
                    boss.hp -= p.dmg
                    hit_this_frame = True

            for e in enemies[:]:
                if p.pos.distance_to(e.pos + pygame.Vector2(15,15)) < 25:
                    e.hp -= p.dmg
                    hit_this_frame = True
                    if e.hp <= 0:
                        if e.etype == "elite": zero_ticket = True
                        enemies.remove(e); stats["gold"] += 35; score += 100

            if hit_this_frame and not stats["pierce"]:
                if p in p_projs: p_projs.remove(p)
            elif p.pos.y < -10 or p.pos.y > HEIGHT + 10:
                if p in p_projs: p_projs.remove(p)

        # 투사체 충돌 (적군 탄환)
        for p in e_projs[:]:
            p.update()
            if p.pos.distance_to(player_pos + pygame.Vector2(20,20)) < 22 and invincible_timer <= 0:
                player_hp -= p.dmg; e_projs.remove(p); shake_timer = 10; invincible_timer = 30
            elif p.pos.y > HEIGHT: e_projs.remove(p)

        if player_hp <= 0: running = False

    # --- 7. 최종 렌더링 부 ---
    # 배경 영상 처리
    screen.fill(BLACK)
    screen.blit(bg_img, (0, 0))

    # 투명도 지원 서피스 (모든 오브젝트는 여기에 그림)
    temp_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    temp_surf.fill((0, 0, 0, 0))

    if game_state == 'PLAYING':

        for e in enemies:
            # Enemy 클래스의 draw 내부에서 처리하거나 여기서 직접 처리
            e.draw(temp_surf) 
            
        if boss:
            boss.draw(temp_surf)
            # 보스 체력바
            pygame.draw.rect(temp_surf, RED, (WIDTH//2-150, 20, 300, 15))
            pygame.draw.rect(temp_surf, GREEN, (WIDTH//2-150, 20, max(0, (boss.hp/boss.max_hp)*300), 15))
            temp_surf.blit(font_s.render(f"BOSS: {boss.type}", True, WHITE), (WIDTH//2-40, 40))
        
        for p in p_projs: p.draw(temp_surf)
        for p in e_projs: p.draw(temp_surf)
        
        # 플레이어 이미지 출력 (무적 시 깜빡임 포함)
        if invincible_timer % 4 == 0: 
            temp_surf.blit(player_img, player_pos)
        
        # 스테이지 타이머
        if boss is None:
            pygame.draw.rect(temp_surf, GRAY, (WIDTH//2-100, 20, 200, 8))
            pygame.draw.rect(temp_surf, CYAN, (WIDTH//2-100, 20, (stage_timer/STAGE_DURATION)*200, 8))
            if boss_alert_timer > 0:
                alert_txt = font_l.render("-!!! WARNING !!!-", True, RED)
                temp_surf.blit(alert_txt, (WIDTH//2-250, HEIGHT//2-50))
                boss_alert_timer -= 1

    elif game_state == 'SHOP':
        temp_surf.blit(font_l.render(f"STAGE {current_stage} COMPLETE", True, GOLD), (WIDTH//2-180, 50))
        for i, opt in enumerate(shop_options):
            card_rect = pygame.Rect(30 + i * 215, 150, 200, 320)
            c = (40, 40, 40) if opt["sold"] else (30, 30, 50)
            pygame.draw.rect(temp_surf, c, card_rect, border_radius=10)
            if not opt["sold"]:
                temp_surf.blit(font_m.render(opt['data']['name'], True, WHITE), (card_rect.x + 20, card_rect.y + 80))
                price_color = GOLD if stats["gold"] >= opt["data"]["price"] else RED
                temp_surf.blit(font_m.render(f"{opt['data']['price']} G", True, price_color), (card_rect.x + 60, card_rect.y + 260))
            else:
                temp_surf.blit(font_m.render("SOLD OUT", True, GRAY), (card_rect.x + 50, card_rect.y + 150))
        temp_surf.blit(font_m.render(f"GOLD: {stats['gold']}G  |  Press [S] for Next Stage", True, WHITE), (WIDTH//2-200, HEIGHT-50))

    # 흔들림 효과를 적용하여 화면에 출력
    screen.blit(temp_surf, render_offset)
    
    # UI (고정 위치)
    pygame.draw.rect(screen, GREEN, (10, 10, max(0, (player_hp/stats['max_hp'])*200), 20))
    screen.blit(font_s.render(f"HP: {int(player_hp)}  GOLD: {stats['gold']}  W: {stats['special_ammo']}", True, WHITE), (10, 35))
    if zero_ticket: screen.blit(font_s.render("★ ZERO TICKET ACTIVE ★", True, CYAN), (10, 55))

    # W 특수기 효과 (화면 반전)
    if special_effect_timer > 0:
        screen.fill(WHITE)
        special_effect_timer -= 1

    pygame.display.flip()
    clock.tick(60)

pygame.quit()