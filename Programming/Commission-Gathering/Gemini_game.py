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
bg_img     = pygame.image.load(os.path.join(IMGS_PATH, "background.png")).convert()
player_img = pygame.image.load(os.path.join(IMGS_PATH, "player.png")).convert_alpha()
player_img = pygame.transform.scale(player_img, (60, 60))

ENEMY_IMGS = {}
for i in range(1, 5):
    ENEMY_IMGS[f"type_{i}"] = {
        "STAND": pygame.transform.scale(pygame.image.load(os.path.join(IMGS_PATH, f"normalEnemy_{i}_stand.png")).convert_alpha(), (50, 50)),
        "ATTACK": pygame.transform.scale(pygame.image.load(os.path.join(IMGS_PATH, f"normalEnemy_{i}_attack.png")).convert_alpha(), (50, 50))
    }

boss_swarm_img = pygame.image.load(os.path.join(IMGS_PATH, "boss_swarm.png")).convert_alpha()
boss_swarm_img = pygame.transform.scale(boss_swarm_img, (100, 100))
boss_zero_img = pygame.image.load(os.path.join(IMGS_PATH, "boss_zero.png")).convert_alpha()
boss_zero_img = pygame.transform.scale(boss_zero_img, (50, 50))

try:
    # 사운드 파일이 imgs 폴더 안에 있다고 가정합니다.
    snd_hit = pygame.mixer.Sound(os.path.join(IMGS_PATH, "hit.wav"))
    snd_expl = pygame.mixer.Sound(os.path.join(IMGS_PATH, "explosion.wav"))
except:
    # 파일이 없을 경우 에러 방지를 위해 None으로 설정
    snd_hit = None
    snd_expl = None


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
particles = []    # 파티클 객체들을 담을 리스트
high_score = 0    # 최고 점수를 담을 변수

shop_tab = "ITEM" # "ITEM", "BANK", "INVEST"
# 산업 구역별 지분 (기본 100%) [cite: 9, 10]
stocks = {"A": 100, "B": 100, "C": 100}
bank_balance = 0 # 은행 예치금
shop_tab = "ITEM"

# 지분에 따른 할인율 계산 함수 (C구역: 정밀 합금 기업이 물가 담당)
def get_discount_ratio():
    # 지분이 100%보다 높으면 할인, 낮으면 할증 (최소 0.5배 ~ 최대 2배)
    ratio = 2.0 - (stocks["C"] / 100.0)
    return max(0.5, min(2.0, ratio))

# 여기서 기존 최고 기록을 불러옵니다.
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        try:
            high_score = int(f.read())
        except:
            high_score = 0
else:
    high_score = 0
    
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
            # 수명에 따라 투명도가 변하는 작은 원 그리기
            p_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(p_surf, (*self.color, self.life), (3, 3), 3)
            surf.blit(p_surf, (self.pos[0]-3, self.pos[1]-3))

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

class Enemy:
    def __init__(self, etype="normal", offset=0):
        self.etype = etype
        self.pos = pygame.Vector2(random.randint(50, WIDTH-50), -50)
        self.offset = offset
        
        # 1. 기본 속성 선언 (KISS: 에러 방지를 위해 변수를 미리 생성)
        self.vx = 0
        self.vy = 1.5  # 모든 적의 기본 하강 속도
        
        # 2. 타입별 속성 재정의 (유지보수성 향상)
        if etype == "bouncer": 
            self.vx, self.vy = random.choice([-3, 3]), 2
        elif etype == "sniper": 
            self.vx, self.vy = 2, 0
            self.pos.y = random.randint(50, 150)
        elif etype == "sin": 
            self.vx, self.vy = 0, 1.8
        elif etype == "elite":
            self.vy = 1.0 # 엘리트는 천천히 압박

        # 3. HP 및 기타 설정
        base_hp = (2 + (score // 5000)) * 0.25 
        self.hp = base_hp * 8 if etype == "elite" else base_hp
        
        # 이미지 및 상태 설정
        self.img_type = f"type_{random.randint(1, 4)}"
        self.state = "STAND"
        self.shoot_delay = random.randint(80, 160)

    def shoot(self, e_projs, p_pos):
        """투사체를 생성하고 발사 상태를 관리하는 독립 메서드 (DRY 원칙 적용)"""
        dist = (p_pos - self.pos).length()
        # 플레이어 방향 벡터 계산 (KISS: 명확한 벡터 연산)
        direction = (p_pos - self.pos).normalize() * 4 if dist > 0 else pygame.Vector2(0, 1)
        e_projs.append(Projectile(self.pos.x + 15, self.pos.y + 15, direction, GOLD, 5))        # 투사체 추가 (골드 색상, 데미지 5)


        # # 모든 적이 반드시 hp 속성을 가지도록 초기화
        # base_hp = (2 + (score // 5000)) * 0.25 
        # if etype == "elite":
        #     self.hp = base_hp * 8
        # else:
        #     self.hp = base_hp
            
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
        if self.shoot_delay < 30: # 발사 0.5초 전(30프레임)부터 공격 모션
            self.state = "ATTACK"
            
        if self.shoot_delay <= 0:
            dist = (p_pos - self.pos).length()
            dir = (p_pos - self.pos).normalize() * 4 if dist > 0 else pygame.Vector2(0,1)
            e_projs.append(Projectile(self.pos.x+15, self.pos.y+15, dir, GOLD, 5))
           
            self.shoot(e_projs, p_pos)
            self.state = "STAND" # 발사 후 다시 스탠드로 복귀
            self.shoot_delay = 180

    def draw(self, surf):
        current_img = ENEMY_IMGS[self.img_type][self.state]
        surf.blit(current_img, self.pos)
        
        # 엘리트 전용 시각 효과
        if self.etype == "elite":
            pygame.draw.circle(surf, PURPLE, (int(self.pos.x+25), int(self.pos.y+25)), 35, 2)
            surf.blit(font_m.render("!", True, PURPLE), (self.pos.x+10, self.pos.y-35))

# --- 5. 유틸리티 함수 ---
def save_highscore(score):
    try:
        with open("highscore.txt", "w") as f:
            f.write(str(score))
    except: pass

def load_highscore():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            return int(f.read())
    return 0

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
current_sector = "A"    # 1. 루프 시작 전 변수 확인

while running:
    mouse_pos = pygame.mouse.get_pos()
    clock.tick(60)
    
    # 1. 화면 흔들림 계산
    render_offset = pygame.Vector2(0, 0)
    if shake_timer > 0:
        render_offset = pygame.Vector2(random.randint(-7, 7), random.randint(-7, 7))
        shake_timer -= 1

    # 2. [중요] temp_surf 초기화 - 여기서 정의해야 아래에서 에러가 안 납니다.
    # 투명도를 지원하는 도화지 생성
    temp_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    temp_surf.fill((0, 0, 0, 0)) # 투명하게 초기화

    # 3. 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        
        if event.type == pygame.KEYDOWN:
            if game_state == 'SHOP':
                # 탭 전환 (F1, F2, F3)
                if event.key == pygame.K_F1: shop_tab = "ITEM"
                if event.key == pygame.K_F2: shop_tab = "BANK"
                if event.key == pygame.K_F3: shop_tab = "INVEST"
                
                # 중앙은행 입출금 
                if shop_tab == "BANK":
                    if event.key == pygame.K_d: # 입금
                        bank_balance += stats["gold"]; stats["gold"] = 0
                    if event.key == pygame.K_f: # 출금 (수수료 5% 발생)
                        stats["gold"] += int(bank_balance * 0.95); bank_balance = 0
                
                # 산업 투자 (Key 1, 2, 3) 
                if shop_tab == "INVEST":
                    keys = {pygame.K_1: "A", pygame.K_2: "B", pygame.K_3: "C"}
                    if event.key in keys:
                        sid = keys[event.key]
                        if stats["gold"] >= 500:
                            stats["gold"] -= 500
                            stocks[sid] += 10 # 지분 상승
                            # 능력치 즉시 반영
                            if sid == "A": stats["speed"] += 0.5
                            if sid == "B": stats["shoot_delay"] = max(10, stats["shoot_delay"] - 2)
                            if sid == "C": stats["damage"] += 1

                # 다음 스테이지로 넘어가기 (S 키)
                if event.key == pygame.K_s:
                    bank_balance = int(bank_balance * 1.1) # 복리 이자 10% 
                    game_state = 'PLAYING'
                    current_stage += 1
                    stage_timer = STAGE_DURATION

    # --- 1. 배경 및 탭 UI ---
    temp_surf.fill((20, 20, 30))
    # 탭 버튼 (A: 아이템, B: 은행, C: 투자)
    tabs = [("ITEM", 50), ("BANK", 250), ("INVEST", 450)]
    for name, x in tabs:
        color = GOLD if shop_tab == name else GRAY
        pygame.draw.rect(temp_surf, color, (x, 20, 180, 50), border_radius=5)
        temp_surf.blit(font_m.render(name, True, BLACK), (x+50, 30))

    # --- 2. 탭별 내용 ---
    if shop_tab == "ITEM":
        discount = get_discount_ratio()
        for i, opt in enumerate(shop_options):
            card_rect = pygame.Rect(30 + i * 215, 150, 200, 320)
            # 할인율이 적용된 실제 가격 계산
            display_price = int(opt["data"]["price"] * discount)
            
            # 카드 렌더링 (기존 로직 유지하되 가격만 변동)
            c = (40, 40, 40) if opt["sold"] else (30, 30, 50)
            pygame.draw.rect(temp_surf, c, card_rect, border_radius=10)
            
            if not opt["sold"]:
                name_text = font_m.render(opt['data']['name'], True, WHITE)
                temp_surf.blit(name_text, (card_rect.x + 20, card_rect.y + 40))
                
                # 지분 상태에 따른 가격 색상 변경
                p_color = GOLD if stats["gold"] >= display_price else RED
                price_text = font_m.render(f"{display_price} G", True, p_color)
                temp_surf.blit(price_text, (card_rect.x + 60, card_rect.y + 260))

    elif shop_tab == "BANK":
        # UI 배경
        pygame.draw.rect(temp_surf, (20, 30, 40), (100, 150, 700, 300), border_radius=15)
        
        # 예치 정보
        balance_txt = font_l.render(f"예치 잔액: {bank_balance} G", True, CYAN)
        interest_txt = font_m.render("예상 다음 배당 이율: +10%", True, GREEN)
        temp_surf.blit(balance_txt, (150, 200))
        temp_surf.blit(interest_txt, (150, 280))
        
        # 안내 문구
        guide_txt = font_s.render("[D] 전액 입금  |  [F] 전액 인출 (수수료 5% 발생)", True, WHITE)
        temp_surf.blit(guide_txt, (150, 400))
        
    elif shop_tab == "INVEST":
        invest_targets = [
            {"id": "A", "name": "A구역: 지열 운송", "effect": "이동속도 증가", "cost": 500},
            {"id": "B", "name": "B구역: 에너지 연구", "effect": "쿨타임 감소", "cost": 500},
            {"id": "C", "name": "C구역: 정밀 합금", "effect": "화력 및 할인율", "cost": 500}
        ]
        
        for i, target in enumerate(invest_targets):
            y_pos = 150 + (i * 110)
            pygame.draw.rect(temp_surf, (45, 45, 65), (50, y_pos, 800, 90), border_radius=10)
            
            # 지분율 바 (Visual Bar)
            bar_width = int(stocks[target["id"]] * 2) # 100% = 200px
            pygame.draw.rect(temp_surf, GOLD, (550, y_pos + 35, bar_width, 20))
            
            # 텍스트 정보
            temp_surf.blit(font_m.render(f"{target['name']} ({stocks[target['id']]}%)", True, WHITE), (70, y_pos + 15))
            temp_surf.blit(font_s.render(f"효과: {target['effect']}", True, GRAY), (70, y_pos + 50))
            temp_surf.blit(font_m.render(f"{target['cost']}G [Key:{i+1}]", True, GOLD), (380, y_pos + 30))

    # 지분 하락에 따른 계급 등급 표시 [cite: 15, 16]
    avg_stock = sum(stocks.values()) / 3
    rank = "고등급(Noble)" if avg_stock > 80 else "저등급(Commoner)"
    temp_surf.blit(font_m.render(f"현재 시민 등급: {rank}", True, GOLD), (WIDTH-300, HEIGHT-50))

    if event.type == pygame.MOUSEBUTTONDOWN and game_state == 'SHOP':
        for opt in shop_options:
            idx = shop_options.index(opt)
            rect = pygame.Rect(30 + idx * 215, 150, 200, 320)
            if rect.collidepoint(mouse_pos) and not opt["sold"] and stats["gold"] >= opt["data"]["price"]:
                stats["gold"] -= opt["data"]["price"]
                apply_upgrade(opt["data"])
                opt["sold"] = True

    # [A] 파티클 로직 업데이트 (기존 투사체 업데이트 근처)
    for p in particles[:]:
        p.update()
        if p.life <= 0:
            particles.remove(p)

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
# --- 메인 루프 내부의 충돌 처리 섹션 (264라인 이후 통합본) ---

        # 1. 적 업데이트 및 충돌 처리 (통합된 단일 루프)
        for e in enemies[:]:
            # 이미 상단에서 선언된 e_projs와 player_pos를 사용합니다.
            e.update(e_projs, player_pos) 
            
            # [A] 플레이어와 적의 충돌 (기본 rect 사용)
            p_rect = pygame.Rect(player_pos.x, player_pos.y, 40, 40)
            e_rect = pygame.Rect(e.pos.x, e.pos.y, 30, 30)
            
            if p_rect.colliderect(e_rect) and invincible_timer <= 0:
                player_hp -= 15
                shake_timer = 15
                invincible_timer = 40
                if e in enemies: enemies.remove(e)
                continue # 이미 삭제되었으므로 다음 단계 생략

            # [B] 화면 밖 유출 (세계관 반영: 지분 하락 페널티)
            elif e.pos.y > HEIGHT:
                if e in enemies:
                    enemies.remove(e)
                    # '소모임.txt' 설정에 따라 산업 구역 중 하나를 랜덤하게 감점
                    target_sector = random.choice(["A", "B", "C"]) 
                    stocks[target_sector] -= 5 
                    shake_timer = 10
                continue

            # [C] 플레이어 총알(p_projs)과 적의 충돌
            for p in p_projs[:]:
                # Projectile 객체의 pos를 기준으로 충돌 박스 생성
                p_bullet_rect = pygame.Rect(p.pos.x, p.pos.y, 10, 10)
                if e_rect.colliderect(p_bullet_rect):
                    e.hp -= stats["damage"]
                    if not stats["pierce"]: # 관통 업그레이드가 없을 때만 탄환 제거
                        if p in p_projs: p_projs.remove(p)
                    
                    if e.hp <= 0:
                        if e in enemies:
                            # 엘리트 처치 시 제로 티켓 획득
                            if getattr(e, 'etype', None) == "elite": zero_ticket = True
                            enemies.remove(e)
                            stats["gold"] += 35
                            score += 100
                            # 폭발 파티클 생성
                            for _ in range(10): 
                                particles.append(Particle(e.pos.x+15, e.pos.y+15, (255, 50, 50)))
                        break # 이미 죽은 적에 대한 탄환 충돌 계산 중단

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

                    if snd_hit: snd_hit.play() # 사운드 재생
                    for _ in range(5): # 파티클 생성
                        particles.append(Particle(p.pos.x, p.pos.y, (255, 200, 50)))
                    
                    if e.hp <= 0:
                        if e.etype == "elite": zero_ticket = True
                        enemies.remove(e); stats["gold"] += 35; score += 100
                        # [추가] 적 파괴 시 더 큰 폭발 파티클
                        for _ in range(10): 
                            particles.append(Particle(e.pos.x+15, e.pos.y+15, (255, 50, 50)))
                        
                        if score > high_score:
                            save_highscore(score)
                            running = False

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
            
    # 플레이어 체력 체크 및 게임 오버 처리
        if player_hp <= 0:
            if score > high_score:
                with open("highscore.txt", "w") as f:
                    f.write(str(score))
            running = False

    # --- 7. 최종 렌더링 부 ---
    # 배경 영상 처리
    screen.fill(BLACK)
    screen.blit(bg_img, (0, 0))

    # 투명도 지원 서피스 (모든 오브젝트는 여기에 그림)
    temp_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    temp_surf.fill((0, 0, 0, 0))

    if game_state == 'PLAYING':
        # 파티클 먼저 그리기 (바닥 효과)
        for p in particles:
            p.draw(temp_surf)

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
        # 상점 배경색
        temp_surf.fill((20, 20, 30))
        
        # --- 탭 UI ---
        tabs = [("ITEM", 50), ("BANK", 250), ("INVEST", 450)]
        for name, x in tabs:
            color = GOLD if shop_tab == name else (60, 60, 70)
            pygame.draw.rect(temp_surf, color, (x, 20, 180, 50), border_radius=5)
            temp_surf.blit(font_m.render(name, True, BLACK if shop_tab == name else WHITE), (x+50, 30))

        # --- 탭별 내용 ---
        if shop_tab == "ITEM":
            discount = get_discount_ratio()
            temp_surf.blit(font_m.render(f"합금 지분 물가 보정: x{discount:.2f}", True, CYAN), (50, 100))
            for i, opt in enumerate(shop_options):
                card_rect = pygame.Rect(30 + i * 215, 150, 200, 320)
                display_price = int(opt["data"]["price"] * discount)
                c = (40, 40, 40) if opt["sold"] else (30, 30, 50)
                pygame.draw.rect(temp_surf, c, card_rect, border_radius=10)
                if not opt["sold"]:
                    temp_surf.blit(font_m.render(opt['data']['name'], True, WHITE), (card_rect.x + 20, card_rect.y + 40))
                    p_color = GOLD if stats["gold"] >= display_price else RED
                    temp_surf.blit(font_m.render(f"{display_price} G", True, p_color), (card_rect.x + 60, card_rect.y + 260))

        elif shop_tab == "BANK":
            pygame.draw.rect(temp_surf, (30, 40, 60), (100, 150, 700, 300), border_radius=15)
            temp_surf.blit(font_l.render(f"예치금: {bank_balance} G", True, CYAN), (150, 200))
            temp_surf.blit(font_m.render(f"다음 스테이지 배당금: +10%", True, GREEN), (150, 280))
            temp_surf.blit(font_s.render("[D] 전액 입금  |  [F] 전액 인출 (수수료 5%)", True, WHITE), (150, 400))

        elif shop_tab == "INVEST":
            invest_targets = [
                {"id": "A", "n": "구역 A: 지열 운송", "y": 150},
                {"id": "B", "n": "구역 B: 에너지 연구", "y": 260},
                {"id": "C", "n": "구역 C: 정밀 합금", "y": 370}
            ]
            for inv in invest_targets:
                y = inv["y"]
                pygame.draw.rect(temp_surf, (45, 45, 65), (50, y, 800, 90), border_radius=10)
                bar_w = int(stocks[inv["id"]] * 2) 
                pygame.draw.rect(temp_surf, GOLD, (550, y + 35, bar_w, 20))
                temp_surf.blit(font_m.render(f"{inv['n']} ({stocks[inv['id']]}%)", True, WHITE), (70, y + 15))
                temp_surf.blit(font_m.render(f"500G [Key:{inv['id']}]", True, GOLD), (380, y + 30))

        # 하단 상태 정보
        avg_s = sum(stocks.values()) / 3
        rank = "Noble" if avg_s > 85 else "Commoner" 
        temp_surf.blit(font_m.render(f"등급: {rank} | GOLD: {stats['gold']}G", True, WHITE), (300, HEIGHT-50))

    # UI (고정 위치)
    pygame.draw.rect(screen, GREEN, (10, 10, max(0, (player_hp/stats['max_hp'])*200), 20))
    score_txt = font_s.render(f"SCORE: {score} | HI-SCORE: {high_score}", True, WHITE)
    screen.blit(score_txt, (10, 60))
    if zero_ticket: screen.blit(font_s.render("★ ZERO TICKET ACTIVE ★", True, CYAN), (10, 55))

    # W 특수기 효과 (화면 반전)
    if special_effect_timer > 0:
        screen.fill(WHITE)
        special_effect_timer -= 1

    # 배경 그리기
    screen.blit(bg_img, (0, 0))
    # 흔들림이 적용된 도화지(temp_surf)를 실제 화면에 출력
    screen.blit(temp_surf, render_offset)
    
    # UI 업데이트 및 프레임 제한
    pygame.display.flip()
    clock.tick(60)

pygame.quit()