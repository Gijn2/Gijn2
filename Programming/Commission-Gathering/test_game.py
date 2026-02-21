import pygame
import random
import math
import os
import cv2
import numpy as np
import time
import sys
import json
import threading

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
bgImg = pygame.image.load(os.path.join(IMGS_PATH, "background.png")).convert()
playerImg = pygame.image.load(os.path.join(IMGS_PATH, "player.png")).convert_alpha()
playerImg = pygame.transform.scale(playerImg, (60, 60))

ENEMY_IMGS = {}
for i in range(1, 5):
    ENEMY_IMGS[f"type_{i}"] = {
        "STAND": pygame.transform.scale(pygame.image.load(os.path.join(IMGS_PATH, f"normalEnemy_{i}_stand.png")).convert_alpha(), (50, 50)),
        "ATTACK": pygame.transform.scale(pygame.image.load(os.path.join(IMGS_PATH, f"normalEnemy_{i}_attack.png")).convert_alpha(), (50, 50))
    }

bossSwarmImg = pygame.image.load(os.path.join(IMGS_PATH, "boss_swarm.png")).convert_alpha()
bossSwarmImg = pygame.transform.scale(bossSwarmImg, (100, 100))
bossZeroImg = pygame.image.load(os.path.join(IMGS_PATH, "boss_zero.png")).convert_alpha()
bossZeroImg = pygame.transform.scale(bossZeroImg, (50, 50))

try:
    snd_hit = pygame.mixer.Sound(os.path.join(IMGS_PATH, "hit.wav"))
    snd_expl = pygame.mixer.Sound(os.path.join(IMGS_PATH, "explosion.wav"))
except:
    snd_hit = None
    snd_expl = None


# 색상 및 폰트
WHITE, RED, GOLD, BLACK, GREEN, CYAN, PURPLE, GRAY = (255, 255, 255), (255, 50, 50), (255, 215, 0), (10, 10, 15), (50, 255, 50), (0, 255, 255), (200, 50, 255), (50, 50, 50)
font_s = pygame.font.SysFont("malgungothic", 16)
font_m = pygame.font.SysFont("malgungothic", 24)
font_l = pygame.font.SysFont("malgungothic", 40)

try:
    sndHit = pygame.mixer.Sound(os.path.join(IMGS_PATH, "hit.wav"))
    sndExpl = pygame.mixer.Sound(os.path.join(IMGS_PATH, "explosion.wav"))
except Exception as e:
    sndHit = None
    sndExpl = None

# 바로 이 위치에 폰트 정의를 넣으세요!
try:
    fontS = pygame.font.SysFont("malgungothic", 16)
    fontM = pygame.font.SysFont("malgungothic", 24)
    fontL = pygame.font.SysFont("malgungothic", 40)
except:
    fontS = pygame.font.Font(None, 20)
    fontM = pygame.font.Font(None, 32)
    fontL = pygame.font.Font(None, 50)

# --- 3. 게임 상태 관리 변수 (camelCase 반영) ---
stats = {"damage": 1, "speed": 5, "gold": 1000, "maxHp": 100, "pierce": False, "specialAmmo": 3}
playerHp = 100
score = 0
gameState = 'PLAYING'
shootCooldown = 0
specialEffectTimer = 0
shakeTimer = 0
zeroTicket = False 
STAGE_DURATION = 1800 
stageTimer = STAGE_DURATION
bossAlertTimer = 0
currentStage = 1
invincibleTimer = 0
particles = []    
highScore = 0    

shopTab = "ITEM"
stocks = {"A": 100, "B": 100, "C": 100}
bankBalance = 0

# 지분에 따른 할인율 계산 함수 (C구역: 정밀 합금 기업이 물가 담당)
# 기능 분리: 함수는 camelCase 사용 (KISS & DRY)
def getDiscountRatio():
    ratio = 2.0 - (stocks["C"] / 100.0)
    return max(0.5, min(2.0, ratio))

# 예외 처리 반영
def loadHighscore():
    if os.path.exists("highscore.txt"):
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read())
        except Exception:
            return 0
    return 0

highScore = loadHighscore()
    
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
        self.hp = 62.5; self.maxHp = 62.5; self.timer = 0; self.visible = True
    def update(self, eProjs, pPos):
        self.timer += 1
        self.visible = False if (self.timer // 30) % 2 == 0 else True
        if self.timer % 80 == 0:
            targetX = pPos.x - 25
            self.pos.x = max(0, min(WIDTH - 50, targetX))
    def draw(self, surf):
        if self.visible:
            surf.blit(bossZeroImg, self.pos)

class BossCrusher:
    def __init__(self):
        self.type = "CHERNOBOG"
        self.hp = 500; self.maxHp = 500
        self.rect = pygame.Rect(0, -100, WIDTH, 150)
        self.pos = pygame.Vector2(0, -100)
        self.mode = "MOVE"
        self.timer = 0
        self.beamAlpha = 0

    def update(self, eProjs, pPos): 
        self.timer += 1
        self.pos.x += math.sin(self.timer/20) * 5
        self.rect.topleft = self.pos

        if self.mode == "MOVE":
            if self.timer % 120 == 0: 
                self.mode = random.choice(["BEAM_READY", "HOMING"])
                self.timer = 0 
        elif self.mode == "BEAM_FIRE":
            if abs(pPos.x - (self.pos.x + WIDTH//2)) < 60:
                global playerHp 
                playerHp -= 2

class BossSwarm:
    def __init__(self):
        self.type = "SWARM"; self.hp = 125; self.maxHp = 125; self.timer = 0
        self.centers = [pygame.Vector2(random.randint(100,800), random.randint(50,200)) for _ in range(8)]
    def update(self, eProjs, pPos):
        self.timer += 1
        for i, c in enumerate(self.centers):
            c.x += math.sin(self.timer/25 + i)*3
            if self.timer % 100 == 0:
                diff = pPos - c
                if diff.length() > 0: 
                    eProjs.append(Projectile(c.x, c.y, diff.normalize()*4, PURPLE, 6))
                else:
                    eProjs.append(Projectile(c.x, c.y, pygame.Vector2(0, 4), PURPLE, 6))
    def draw(self, surf):
        for c in self.centers:
            surf.blit(bossSwarmImg, (c.x - 50, c.y - 50))

class Enemy:
    def __init__(self, etype="normal", offset=0):
        self.etype = etype
        self.pos = pygame.Vector2(random.randint(50, WIDTH-50), -50)
        self.offset = offset
        self.vx = 0
        self.vy = 1.5  
        
        if etype == "bouncer": self.vx, self.vy = random.choice([-3, 3]), 2
        elif etype == "sniper": self.vx, self.vy = 2, 0; self.pos.y = random.randint(50, 150)
        elif etype == "sin": self.vx, self.vy = 0, 1.8
        elif etype == "elite": self.vy = 1.0 

        baseHp = (2 + (score // 5000)) * 0.25 
        self.hp = baseHp * 8 if etype == "elite" else baseHp
        self.imgType = f"type_{random.randint(1, 4)}"
        self.state = "STAND"
        self.shootDelay = random.randint(80, 160)

    def shoot(self, eProjs, pPos):
        dist = (pPos - self.pos).length()
        direction = (pPos - self.pos).normalize() * 4 if dist > 0 else pygame.Vector2(0, 1)
        eProjs.append(Projectile(self.pos.x + 15, self.pos.y + 15, direction, GOLD, 5))

    def update(self, eProjs, pPos):
        if self.etype == "sin":
            self.pos.y += self.vy
            self.pos.x += math.sin((pygame.time.get_ticks() + self.offset) / 200) * 5
        else:
            self.pos.y += self.vy
            self.pos.x += self.vx
            if self.pos.x <= 0 or self.pos.x >= WIDTH-30: self.vx *= -1

        self.shootDelay -= 1
        if self.shootDelay < 30: self.state = "ATTACK"
            
        if self.shootDelay <= 0:
            self.shoot(eProjs, pPos)
            self.state = "STAND" 
            self.shootDelay = 180

    def draw(self, surf):
        currentImg = ENEMY_IMGS[self.imgType][self.state]
        surf.blit(currentImg, self.pos)
        if self.etype == "elite":
            pygame.draw.circle(surf, PURPLE, (int(self.pos.x+25), int(self.pos.y+25)), 35, 2)
            surf.blit(fontM.render("!", True, PURPLE), (self.pos.x+10, self.pos.y-35))

# --- 5. 유틸리티 함수 ---
def saveHighscore(s):
    try:
        with open("highscore.txt", "w") as f:
            f.write(str(s))
    except Exception: pass

def getShopItems():
    return [{"data": item, "sold": False} for item in random.sample(UPGRADE_POOL, 4)]

def applyUpgrade(itemData):
    global playerHp, boss
    eff = itemData['effect']
    if eff == "dmg": stats["damage"] += 1.5
    elif eff == "speed": stats["speed"] += 2
    elif eff == "heal": playerHp = min(stats["maxHp"], playerHp + 50)
    elif eff == "pierce": stats["pierce"] = True
    elif eff == "maxhp": stats["maxHp"] += 40; playerHp += 40
    elif eff == "ammo": stats["specialAmmo"] += 2

# --- 6. 메인 게임 루프 ---
playerPos = pygame.Vector2(WIDTH//2, HEIGHT-80)
enemies, pProjs, eProjs, boss = [], [], [], None
shopOptions = []
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    clock.tick(60)
    
    # 화면 흔들림 계산
    render_offset = pygame.Vector2(0, 0)
    if shakeTimer > 0:
        render_offset = pygame.Vector2(random.randint(-7, 7), random.randint(-7, 7))
        shakeTimer -= 1

    # 투명도를 지원하는 도화지 생성
    temp_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    temp_surf.fill((0, 0, 0, 0)) # 투명하게 초기화

    # [1] Input & Event Handling (책임 분리)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        
        if event.type == pygame.KEYDOWN:
            if gameState == 'SHOP':
                if event.key == pygame.K_F1: shopTab = "ITEM"
                if event.key == pygame.K_F2: shopTab = "BANK"
                if event.key == pygame.K_F3: shopTab = "INVEST"
                
                if shopTab == "BANK":
                    if event.key == pygame.K_d: 
                        bankBalance += stats["gold"]; stats["gold"] = 0
                    if event.key == pygame.K_f: 
                        stats["gold"] += int(bankBalance * 0.95); bankBalance = 0
                
                if shopTab == "INVEST":
                    keys = {pygame.K_1: "A", pygame.K_2: "B", pygame.K_3: "C"}
                    if event.key in keys:
                        sid = keys[event.key]
                        if stats["gold"] >= 500:
                            stats["gold"] -= 500
                            stocks[sid] += 10 
                            if sid == "A": stats["speed"] += 0.5
                            if sid == "C": stats["damage"] += 1

                if event.key == pygame.K_s:
                    bankBalance = int(bankBalance * 1.1) 
                    gameState = 'PLAYING'
                    currentStage += 1
                    stageTimer = STAGE_DURATION

        # 마우스 클릭 처리 (UI 분리 및 로직 통합)
        if event.type == pygame.MOUSEBUTTONDOWN and gameState == 'SHOP' and shopTab == "ITEM":
            for i, opt in enumerate(shopOptions):
                rect = pygame.Rect(30 + i * 215, 150, 200, 320)
                discount = getDiscountRatio()
                displayPrice = int(opt["data"]["price"] * discount)
                if rect.collidepoint(mouse_pos) and not opt["sold"] and stats["gold"] >= displayPrice:
                    stats["gold"] -= displayPrice
                    applyUpgrade(opt["data"])
                    opt["sold"] = True
                    
    # --- 1. 배경 및 탭 UI ---
    temp_surf.fill((20, 20, 30))
    # 탭 버튼 (A: 아이템, B: 은행, C: 투자)
    tabs = [("ITEM", 50), ("BANK", 250), ("INVEST", 450)]
    for name, x in tabs:
        color = GOLD if shopTab == name else GRAY
        pygame.draw.rect(temp_surf, color, (x, 20, 180, 50), border_radius=5)
        temp_surf.blit(font_m.render(name, True, BLACK), (x+50, 30))

    # --- 2. 탭별 내용 ---
    if shopTab == "ITEM":
        discount = getDiscountRatio()
        for i, opt in enumerate(shopOptions):
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

    elif shopTab == "BANK":
        # UI 배경
        pygame.draw.rect(temp_surf, (20, 30, 40), (100, 150, 700, 300), border_radius=15)
        
        # 예치 정보
        balance_txt = font_l.render(f"예치 잔액: {bankBalance} G", True, CYAN)
        interest_txt = font_m.render("예상 다음 배당 이율: +10%", True, GREEN)
        temp_surf.blit(balance_txt, (150, 200))
        temp_surf.blit(interest_txt, (150, 280))
        
        # 안내 문구
        guide_txt = font_s.render("[D] 전액 입금  |  [F] 전액 인출 (수수료 5% 발생)", True, WHITE)
        temp_surf.blit(guide_txt, (150, 400))
        
    elif shopTab == "INVEST":
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

    if event.type == pygame.MOUSEBUTTONDOWN and gameState == 'SHOP':
        for opt in shopOptions:
            idx = shopOptions.index(opt)
            rect = pygame.Rect(30 + idx * 215, 150, 200, 320)
            if rect.collidepoint(mouse_pos) and not opt["sold"] and stats["gold"] >= opt["data"]["price"]:
                stats["gold"] -= opt["data"]["price"]
                applyUpgrade(opt["data"])
                opt["sold"] = True

    # [2] Logic Update (비즈니스 로직)
    for p in particles[:]:
        p.update()
        if p.life <= 0: particles.remove(p)

    if gameState == 'PLAYING':
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: playerPos.x -= stats["speed"]
        if keys[pygame.K_RIGHT]: playerPos.x += stats["speed"]
        if keys[pygame.K_UP]: playerPos.y -= stats["speed"]
        if keys[pygame.K_DOWN]: playerPos.y += stats["speed"]

        if playerPos.x < -30: playerPos.x = WIDTH
        elif playerPos.x > WIDTH: playerPos.x = -30
        playerPos.y = max(0, min(HEIGHT-40, playerPos.y))

        if keys[pygame.K_q] and shootCooldown <= 0:
            pProjs.append(Projectile(playerPos.x+20, playerPos.y, pygame.Vector2(0,-10), GREEN, stats["damage"]))
            shootCooldown = 10
        shootCooldown = max(0, shootCooldown - 1)
        if invincibleTimer > 0: invincibleTimer -= 1

        if keys[pygame.K_w] and stats["specialAmmo"] > 0 and specialEffectTimer <= 0:
            stats["specialAmmo"] -= 1
            specialEffectTimer = 60  
            shakeTimer = 30         
            if sndExpl: sndExpl.play()
            
            # 1. 화면의 모든 적 투사체(총알) 즉시 삭제
            eProjs.clear() 
            
            # 2. 모든 일반 적에게 강력한 데미지
            for e in enemies[:]:
                e.hp -= 20  
                if e.hp <= 0:
                    if e in enemies: enemies.remove(e)
                    score += 150
            
            # 3. 보스가 있다면 보스에게도 데미지
            if boss:
                boss.hp -= 30

        if boss is None:
            stageTimer -= 1
            if stageTimer == 120: bossAlertTimer = 120
            if stageTimer <= 0:
                if zeroTicket: boss = BossZero(); zeroTicket = False
                else: boss = BossSwarm()
                enemies.clear()
            
            if len(enemies) < 6:
                etype = random.choices(["normal", "bouncer", "sin", "sniper", "elite"], weights=[50, 15, 15, 18.5, 1.5])[0]
                enemies.append(Enemy(etype, random.randint(0, 1000)))

        if boss:
            boss.update(eProjs, playerPos)
            bossRect = getattr(boss, 'rect', pygame.Rect(boss.pos.x, boss.pos.y, 50, 50) if hasattr(boss, 'pos') else None)
            if bossRect and bossRect.colliderect(pygame.Rect(playerPos.x, playerPos.y, 40, 40)) and invincibleTimer <= 0:
                playerHp -= 20; shakeTimer = 20; invincibleTimer = 60
            
            if boss.hp <= 0:
                stats["gold"] += 1500; boss = None; gameState = 'SHOP'; shopOptions = getShopItems()

        # 적 및 충돌 로직 업데이트
        for e in enemies[:]:
            e.update(eProjs, playerPos) 
            pRect = pygame.Rect(playerPos.x, playerPos.y, 40, 40)
            eRect = pygame.Rect(e.pos.x, e.pos.y, 30, 30)
            
            if pRect.colliderect(eRect) and invincibleTimer <= 0:
                playerHp -= 15; shakeTimer = 15; invincibleTimer = 40
                if e in enemies: enemies.remove(e)
                continue 

            elif e.pos.y > HEIGHT:
                if e in enemies:
                    enemies.remove(e)
                    targetSector = random.choice(["A", "B", "C"]) 
                    stocks[targetSector] -= 5 
                    shakeTimer = 10
                continue

            for p in pProjs[:]:
                pBulletRect = pygame.Rect(p.pos.x, p.pos.y, 10, 10)
                if eRect.colliderect(pBulletRect):
                    e.hp -= stats["damage"]
                    if not stats["pierce"] and p in pProjs: pProjs.remove(p)
                    
                    if e.hp <= 0:
                        if e in enemies:
                            if getattr(e, 'etype', None) == "elite": zeroTicket = True
                            enemies.remove(e); stats["gold"] += 35; score += 100
                            for _ in range(10): particles.append(Particle(e.pos.x+15, e.pos.y+15, (255, 50, 50)))
                        break 

        for p in pProjs[:]:
            p.update()
            hitThisFrame = False
            if boss:
                hit = False
                if boss.type == "CHERNOBOG" and boss.rect.collidepoint(p.pos): hit = True
                elif boss.type == "SWARM":
                    for c in boss.centers:
                        if p.pos.distance_to(c) < 25: hit = True; break
                elif boss.type == "ZERO" and p.pos.distance_to(boss.pos + pygame.Vector2(25,25)) < 40: hit = True
                
                if hit:
                    boss.hp -= p.dmg; hitThisFrame = True
                    if sndHit: sndHit.play() 
                    for _ in range(5): particles.append(Particle(p.pos.x, p.pos.y, (255, 200, 50)))

            if hitThisFrame and not stats["pierce"]:
                if p in pProjs: pProjs.remove(p)
            elif p.pos.y < -10 or p.pos.y > HEIGHT + 10:
                if p in pProjs: pProjs.remove(p)

        for p in eProjs[:]:
            p.update()
            if p.pos.distance_to(playerPos + pygame.Vector2(20,20)) < 22 and invincibleTimer <= 0:
                playerHp -= p.dmg; eProjs.remove(p); shakeTimer = 10; invincibleTimer = 30
            elif p.pos.y > HEIGHT: eProjs.remove(p)
            
        if playerHp <= 0:
            if score > highScore: saveHighscore(score)
            running = False

    # --- 7. 최종 렌더링 부 ---
    # 배경 영상 처리
    screen.fill(BLACK)
    screen.blit(bgImg, (0, 0))

    # 투명도 지원 서피스 (모든 오브젝트는 여기에 그림)
    tempSurf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    tempSurf.fill((0, 0, 0, 0))

    if gameState == 'PLAYING':
        for p in particles: p.draw(tempSurf)
        for e in enemies: e.draw(tempSurf) 
            
        if boss:
            boss.draw(tempSurf)
            pygame.draw.rect(tempSurf, RED, (WIDTH//2-150, 20, 300, 15))
            pygame.draw.rect(tempSurf, GREEN, (WIDTH//2-150, 20, max(0, (boss.hp/boss.maxHp)*300), 15))
            tempSurf.blit(fontS.render(f"BOSS: {boss.type}", True, WHITE), (WIDTH//2-40, 40))
        
        for p in pProjs: p.draw(tempSurf)
        for p in eProjs: p.draw(tempSurf)
        
        if invincibleTimer % 4 == 0: 
            tempSurf.blit(playerImg, playerPos)
        
        if boss is None:
            pygame.draw.rect(tempSurf, GRAY, (WIDTH//2-100, 20, 200, 8))
            pygame.draw.rect(tempSurf, CYAN, (WIDTH//2-100, 20, (stageTimer/STAGE_DURATION)*200, 8))
            if bossAlertTimer > 0:
                tempSurf.blit(fontL.render("-!!! WARNING !!!-", True, RED), (WIDTH//2-250, HEIGHT//2-50))
                bossAlertTimer -= 1

    elif gameState == 'SHOP':
        tempSurf.fill((20, 20, 30))
        tabs = [("ITEM", 50), ("BANK", 250), ("INVEST", 450)]
        for name, x in tabs:
            color = GOLD if shopTab == name else (60, 60, 70)
            pygame.draw.rect(tempSurf, color, (x, 20, 180, 50), border_radius=5)
            tempSurf.blit(fontM.render(name, True, BLACK if shopTab == name else WHITE), (x+50, 30))

        if shopTab == "ITEM":
            discount = getDiscountRatio()
            tempSurf.blit(fontM.render(f"합금 지분 물가 보정: x{discount:.2f}", True, CYAN), (50, 100))
            for i, opt in enumerate(shopOptions):
                cardRect = pygame.Rect(30 + i * 215, 150, 200, 320)
                displayPrice = int(opt["data"]["price"] * discount)
                c = (40, 40, 40) if opt["sold"] else (30, 30, 50)
                pygame.draw.rect(tempSurf, c, cardRect, border_radius=10)
                if not opt["sold"]:
                    tempSurf.blit(fontM.render(opt['data']['name'], True, WHITE), (cardRect.x + 20, cardRect.y + 30))
                    # 버그 3 해결: 아이템 설명 문구(desc) 정상 노출
                    tempSurf.blit(fontS.render(opt['data']['desc'], True, GRAY), (cardRect.x + 20, cardRect.y + 80))
                    pColor = GOLD if stats["gold"] >= displayPrice else RED
                    tempSurf.blit(fontM.render(f"{displayPrice} G", True, pColor), (cardRect.x + 60, cardRect.y + 260))

        elif shopTab == "BANK":
            pygame.draw.rect(tempSurf, (30, 40, 60), (100, 150, 700, 300), border_radius=15)
            tempSurf.blit(fontL.render(f"예치금: {bankBalance} G", True, CYAN), (150, 200))
            tempSurf.blit(fontM.render(f"다음 스테이지 배당금: +10%", True, GREEN), (150, 280))
            tempSurf.blit(fontS.render("[D] 전액 입금  |  [F] 전액 인출 (수수료 5%)", True, WHITE), (150, 400))

        elif shopTab == "INVEST":
            investTargets = [
                {"id": "A", "n": "구역 A: 지열 운송", "y": 150},
                {"id": "B", "n": "구역 B: 에너지 연구", "y": 260},
                {"id": "C", "n": "구역 C: 정밀 합금", "y": 370}
            ]
            for i, inv in enumerate(investTargets):
                y = inv["y"]
                pygame.draw.rect(tempSurf, (45, 45, 65), (50, y, 800, 90), border_radius=10)
                barW = int(stocks[inv["id"]] * 2) 
                pygame.draw.rect(tempSurf, GOLD, (550, y + 35, barW, 20))
                tempSurf.blit(fontM.render(f"{inv['n']} ({stocks[inv['id']]}%)", True, WHITE), (70, y + 15))
                # 번호 키 매핑 안내 수정
                tempSurf.blit(fontM.render(f"500G [Key:{i+1}]", True, GOLD), (380, y + 30))

        avgS = sum(stocks.values()) / 3
        rank = "Noble" if avgS > 85 else "Commoner" 
        tempSurf.blit(fontM.render(f"등급: {rank} | GOLD: {stats['gold']}G", True, WHITE), (300, HEIGHT-50))

        # 하단 상태 정보
        avg_s = sum(stocks.values()) / 3
        rank = "Noble" if avg_s > 85 else "Commoner" 
        temp_surf.blit(font_m.render(f"등급: {rank} | GOLD: {stats['gold']}G", True, WHITE), (300, HEIGHT-50))

    # W 특수기 효과 (화면 반전)
    if specialEffectTimer > 0:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            # 타이머에 따라 투명도가 낮아지며 서서히 사라짐
            alpha = min(255, specialEffectTimer * 10) 
            overlay.fill((255, 255, 255, alpha))
            screen.blit(overlay, (0, 0))
            specialEffectTimer -= 1 # 타이머 감소

    # 배경 그리기
    screen.blit(bgImg, (0, 0))
    # 흔들림이 적용된 도화지(temp_surf)를 실제 화면에 출력
    screen.blit(tempSurf, render_offset)
        
    # 배경에 덮이지 않도록 UI를 마지막에 렌더링
    pygame.draw.rect(screen, GREEN, (10, 10, max(0, (playerHp/stats['maxHp'])*200), 20))
    scoreTxt = fontS.render(f"SCORE: {score} | HI-SCORE: {highScore}", True, WHITE)
    screen.blit(scoreTxt, (10, 40))
    if zeroTicket: screen.blit(fontS.render("★ ZERO TICKET ACTIVE ★", True, CYAN), (10, 60))

    # UI 업데이트 및 프레임 제한
    pygame.display.flip()
    clock.tick(60)

pygame.quit()