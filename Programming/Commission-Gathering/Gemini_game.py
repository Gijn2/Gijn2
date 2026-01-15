import pygame
import random

# 1. 초기화
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Roguelike: Risk & Reward")
clock = pygame.time.Clock()

# 색상 및 폰트
WHITE, RED, GOLD, BLACK, GREEN, CYAN, PURPLE = (255, 255, 255), (255, 50, 50), (255, 215, 0), (10, 10, 15), (50, 255, 50), (0, 255, 255), (200, 50, 255)
font_s = pygame.font.SysFont("malgungothic", 18)
font_m = pygame.font.SysFont("malgungothic", 28)
font_l = pygame.font.SysFont("malgungothic", 45)

# 2. 게임 상태 및 능력치
stats = {
    "damage": 1, 
    "speed": 5, 
    "gold": 0, 
    "max_hp": 100,
    "pierce": False # 관통 능력 (시너지 예시)
}
score = 0
player_hp = 100
game_state = 'PLAYING'

# 타이머/상태 관리
shotgun_timer = 0
shop_active_timer = 0
shoot_cooldown = 0
shop_options = [] # 현재 상점에 뜬 3가지 카드

# 3. 로그라이크 카드 데이터 (아이디어 1, 2, 3 결합)
# 리스크와 리워드, 특수 능력을 섞은 카드들
UPGRADE_POOL = [
    {"name": "유리 대포", "desc": "데미지 +3, 현재 체력 -30", "effect": "glass", "price": 0},
    {"name": "신속 장화", "desc": "이동속도 +1.5", "effect": "spd", "price": 30},
    {"name": "응급 처치", "desc": "최대 체력 +20 및 풀회복", "effect": "heal", "price": 40},
    {"name": "황금 총알", "desc": "적 처치 시 골드 2배 획득", "effect": "gold_up", "price": 50},
    {"name": "관통 탄환", "desc": "총알이 적을 관통함", "effect": "pierce", "price": 60},
    {"name": "샷건 마스터", "desc": "X키 샷건 지속시간 +5초", "effect": "shotgun_ext", "price": 40},
]

def apply_upgrade(upgrade):
    global player_hp, shotgun_timer
    if upgrade['effect'] == "glass":
        stats["damage"] += 3
        player_hp = max(1, player_hp - 30)
    elif upgrade['effect'] == "spd":
        stats["speed"] += 1.5
    elif upgrade['effect'] == "heal":
        stats["max_hp"] += 20
        player_hp = stats["max_hp"]
    elif upgrade['effect'] == "pierce":
        stats["pierce"] = True
    elif upgrade['effect'] == "shotgun_ext":
        # 상점에서 바로 효과를 주는 게 아니라 능력치 저장 후 나중에 X 사용 시 적용도 가능
        pass 

# 4. 클래스 정의 (투사체, 적, 보스)
class Projectile:
    def __init__(self, x, y, velocity, color, damage):
        self.pos = pygame.Vector2(x, y)
        self.vel = velocity
        self.color = color
        self.damage = damage
        self.hit_list = [] # 관통 시 중복 피격 방지

    def update(self):
        self.pos += self.vel

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), 5)

class Enemy:
    def __init__(self):
        self.pos = pygame.Vector2(random.randint(50, WIDTH-50), random.randint(-100, 0))
        self.hp = 2 + (score // 500) # 점수에 따른 난이도 상승

    def update(self):
        self.pos.y += 1.5

class Boss:
    def __init__(self):
        self.pos = pygame.Vector2(WIDTH//2 - 50, -100)
        self.hp = 50 + (score // 10); self.max_hp = self.hp
        self.shoot_timer = 0

    def update(self, projectiles):
        if self.pos.y < 60: self.pos.y += 2
        self.shoot_timer += 1
        if self.shoot_timer > 60:
            for i in range(10):
                dir_vec = pygame.Vector2(0, 1).rotate(i * 36) * 4
                projectiles.append(Projectile(self.pos.x+50, self.pos.y+50, dir_vec, PURPLE, 10))
            self.shoot_timer = 0

# 5. 초기 객체 설정
player_pos = pygame.Vector2(WIDTH//2, HEIGHT - 80)
enemies = [Enemy() for _ in range(5)]
player_projectiles, enemy_projectiles = [], []
boss = None

# 6. 메인 루프
running = True
while running:
    screen.fill(BLACK)
    
    # --- 이벤트 처리 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            # 보스 잡고 5초 이내에 S 누르면 상점 진입
            if game_state == 'PLAYING' and shop_active_timer > 0 and event.key == pygame.K_s:
                game_state = 'SHOP'
                shop_options = random.sample(UPGRADE_POOL, 3) # 무작위 3개 선정
            
            # 상점에서 선택 (1, 2, 3번 키)
            if game_state == 'SHOP':
                idx = -1
                if event.key == pygame.K_1: idx = 0
                if event.key == pygame.K_2: idx = 1
                if event.key == pygame.K_3: idx = 2
                
                if idx != -1:
                    choice = shop_options[idx]
                    if stats["gold"] >= choice["price"]:
                        stats["gold"] -= choice["price"]
                        apply_upgrade(choice)
                        game_state = 'PLAYING'
                        shop_active_timer = 0 # 구매 후 상점 닫힘

            # X키 샷건 사용 (골드 소모)
            if game_state == 'PLAYING' and event.key == pygame.K_x and stats["gold"] >= 30:
                stats["gold"] -= 30
                shotgun_timer = 600

    # --- 게임 로직 ---
    if game_state == 'PLAYING':
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player_pos.x -= stats["speed"]
        if keys[pygame.K_RIGHT]: player_pos.x += stats["speed"]
        if keys[pygame.K_UP]: player_pos.y -= stats["speed"]
        if keys[pygame.K_DOWN]: player_pos.y += stats["speed"]
        
        # 화면 제한 (좌우 통과, 상하 막힘)
        player_pos.x %= WIDTH
        player_pos.y = max(0, min(HEIGHT-40, player_pos.y))

        # 공격 로직
        if keys[pygame.K_z] and shoot_cooldown <= 0:
            p_center = player_pos + pygame.Vector2(20, 0)
            if shotgun_timer > 0:
                for a in [-25, 0, 25]:
                    player_projectiles.append(Projectile(p_center.x, p_center.y, pygame.Vector2(0, -7).rotate(a), GREEN, stats["damage"]))
            else:
                player_projectiles.append(Projectile(p_center.x, p_center.y, pygame.Vector2(0, -8), GREEN, stats["damage"]))
            shoot_cooldown = 12
        
        if shoot_cooldown > 0: shoot_cooldown -= 1
        if shotgun_timer > 0: shotgun_timer -= 1
        if shop_active_timer > 0: shop_active_timer -= 1

        # 보스 스폰
        if score > 0 and score % 1000 == 0 and boss is None and shop_active_timer <= 0:
            boss = Boss()

        # 적/보스 업데이트 및 충돌
        if boss:
            boss.update(enemy_projectiles)
            if boss.hp <= 0:
                boss = None; score += 500; stats["gold"] += 100
                shop_active_timer = 300 # 5초 활성화

        for e in enemies[:]:
            e.update()
            if e.pos.y > HEIGHT: enemies.remove(e); enemies.append(Enemy())
            
        for p in player_projectiles[:]:
            p.update()
            # 적 충돌
            for e in enemies[:]:
                if p.pos.distance_to(e.pos + pygame.Vector2(15,15)) < 20 and e not in p.hit_list:
                    e.hp -= p.damage
                    if stats["pierce"]: p.hit_list.append(e) # 관통 시 목록 추가
                    else: 
                        if p in player_projectiles: player_projectiles.remove(p)
                    
                    if e.hp <= 0:
                        enemies.remove(e); enemies.append(Enemy()); score += 50; stats["gold"] += 5
                    break
            # 보스 충돌
            if boss and p.pos.distance_to(boss.pos + pygame.Vector2(50,50)) < 50:
                boss.hp -= p.damage
                if not stats["pierce"] and p in player_projectiles: player_projectiles.remove(p)

        for p in enemy_projectiles[:]:
            p.update()
            if p.pos.distance_to(player_pos + pygame.Vector2(20,20)) < 25:
                player_hp -= p.damage
                enemy_projectiles.remove(p)
            elif p.pos.y > HEIGHT: enemy_projectiles.remove(p)

        if player_hp <= 0: running = False

    # --- 그리기 ---
    if game_state == 'PLAYING':
        for p in player_projectiles: p.draw(screen)
        for p in enemy_projectiles: p.draw(screen)
        for e in enemies: screen.blit(pygame.Surface((30,30), pygame.SRCALPHA), e.pos); pygame.draw.rect(screen, RED, (*e.pos, 30, 30))
        if boss: boss.draw(screen)
        screen.blit(player_img, player_pos)
        
        # UI
        pygame.draw.rect(screen, RED, (10, 10, 200, 15))
        pygame.draw.rect(screen, GREEN, (10, 10, (player_hp/stats["max_hp"])*200, 15))
        screen.blit(font_s.render(f"Gold: {stats['gold']} | Score: {score}", True, WHITE), (10, 30))
        if shop_active_timer > 0:
            txt = font_m.render("보급 상점 이용 가능! [S]", True, GOLD)
            screen.blit(txt, (WIDTH//2 - 150, HEIGHT//2))
            pygame.draw.rect(screen, GOLD, (WIDTH//2-150, HEIGHT//2+40, shop_active_timer, 5))

    elif game_state == 'SHOP':
        screen.fill((20, 20, 30))
        screen.blit(font_l.render("UPGRADE SELECT", True, GOLD), (WIDTH//2-180, 50))
        for i, opt in enumerate(shop_options):
            # 카드 배경
            rect = pygame.Rect(50 + i*250, 150, 200, 300)
            pygame.draw.rect(screen, (40, 40, 60), rect, border_radius=10)
            pygame.draw.rect(screen, GOLD, rect, 2, border_radius=10)
            
            # 카드 텍스트
            name_t = font_m.render(opt['name'], True, WHITE)
            desc_t = font_s.render(opt['desc'], True, CYAN)
            price_t = font_m.render(f"{opt['price']} G", True, GOLD)
            num_t = font_l.render(str(i+1), True, (60, 60, 80))
            
            screen.blit(num_t, (rect.centerx-15, rect.top+20))
            screen.blit(name_t, (rect.x+20, rect.y+80))
            screen.blit(desc_t, (rect.x+20, rect.y+130))
            screen.blit(price_t, (rect.x+70, rect.bottom-50))

        screen.blit(font_s.render("숫자 키 [1, 2, 3]을 눌러 선택하세요", True, WHITE), (WIDTH//2-120, 500))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()