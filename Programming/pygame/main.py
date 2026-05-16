# 게임의 진입점 및 메인 루프 (이벤트 처리, 화면 렌더링)

# main.py
import pygame
import os
import random

# 분리된 모듈 임포트
from constants import SYNERGY_DATA, WIDTH, HEIGHT, STAGE_DURATION, BLACK, RED, GREEN, CYAN, GRAY, WHITE, GOLD, MAX_ENEMY_TYPES
from assetManager import assets
from entities.Enemy import Enemy, getRandomEnemy
from systems.ShopManager import apply_interest, shopTab, shopSubState, shopRefreshCount, bankBalance, shopOptions # refresh_shop, 고장
from systems.StatsManager import calculate_stats, stats, inventory
from utils.fileIO import saveHighscoreSecure
from entities.Bosses import *
from entities.Projectiles import *
from systems.SharedState import state, stats

# --- 초기화 및 화면 설정 ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Topdown Shooting Pygame: Limited Edition")
clock = pygame.time.Clock()
assets.loadAllAssets()     # 에셋 로드 함수를 별도의 모듈로 분리하여 관리 (SRP 원칙 반영)

# --- 게임 상태 관리 변수 초기화 ---
stageTimer = STAGE_DURATION

        
bossAlertTimer = 0
currentStage = 1
freeRefreshAvailable = False
gameState = 'PLAYING'
highScore = 0 # 추후 loadHighscoreSecure() 사용   
hitboxRadius = 10   
particles = []
pendingItem = None      
screenShakeTimer = 0 
shootCooldown = 0
specialEffectTimer = 0


playerPos = pygame.Vector2(WIDTH//2, HEIGHT-80)
enemies, pProjs, eProjs, boss = [], [], [], None
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    clock.tick(37.5)
    
    # 화면 흔들림 계산
    render_offset = pygame.Vector2(0, 0)
    if shakeTimer > 0:
        render_offset = pygame.Vector2(random.randint(-7, 7), random.randint(-7, 7))
        shakeTimer -= 1

    # 투명도를 지원하는 도화지 생성
    tempSurf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    tempSurf.fill((0, 0, 0, 0)) # 투명하게 초기화

    # [1] Input & Event Handling (책임 분리)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        
        if event.type == pygame.KEYDOWN:

            if gameState == 'SHOP':
                if shopSubState == "NORMAL":
                    # 은행 입출금 기능 (은행 탭일 때만 작동)
                    if shopTab == "BANK":
                        if event.key == pygame.K_a and stats["gold"] >= 100:
                            stats["gold"] -= 100
                            bankBalance += 100
                        elif event.key == pygame.K_d and bankBalance >= 100:
                            stats["gold"] += 100
                            bankBalance -= 100

                    if event.key == pygame.K_z:
                        shopTab = "BANK" if shopTab == "MARKET" else "MARKET"
                    
                    # S키로 스테이지 시작
                    elif event.key == pygame.K_s:
                        apply_interest()
                        gameState = 'PLAYING'
                        currentStage += 1
                
                    # R키: 상점 새로고침
                    if event.key == pygame.K_r:
                        cost = 0 if freeRefreshAvailable else (200 + 100 * shopRefreshCount)
                        if stats['gold'] >= cost:
                            stats['gold'] -= cost
                            if not freeRefreshAvailable:
                                shopRefreshCount += 1
                            freeRefreshAvailable = False
                            refresh_shop()  # 아이템 교체 실행

                    # 숫자키 1, 2, 3으로 아이템 구매
                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                        if shopTab == "MARKET" and shopSubState == "NORMAL":
                            idx = event.key - pygame.K_1 # K_1은 0, K_2는 1, K_3은 2로 매핑
                            if idx < len(shopOptions):
                                opt = shopOptions[idx]
                                if not opt["sold"]:
                                    item = opt["data"]
                                    if stats['gold'] >= item['price']:
                                        if item.get("type") == "CONSUMABLE":
                                            stats['gold'] -= item['price']
                                            if item["id"] == "cons_1": playerHp = min(stats['maxHp'], playerHp + 50)
                                            elif item["id"] == "cons_2": stats['specialAmmo'] += 1
                                            opt["sold"] = True
                                        else:
                                            if len(inventory) < 9:
                                                stats['gold'] -= item['price']
                                                inventory.append(item)
                                                opt["sold"] = True
                                                calculate_stats()
                                            else:
                                                pendingItem = opt
                                                shopSubState = "CONFIRM_REPLACE"

        # 마우스 클릭: 아이템 구매 및 인벤토리 관리
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if gameState == 'SHOP':
                mousePos = pygame.mouse.get_pos()
                
                # 1. 일반 상점 아이템 구매
                if shopSubState == "NORMAL" and shopTab == "MARKET":
                    for i, opt in enumerate(shopOptions):
                        card_rect = pygame.Rect(30 + i * 135, 170, 125, 180)

                        if card_rect.collidepoint(mousePos) and not opt["sold"]:
                            item = opt["data"]
                            if stats['gold'] >= item['price']:
                                # 소모품 처리
                                if item.get("type") == "CONSUMABLE":
                                    stats['gold'] -= item['price']
                                    if item["id"] == "cons_1": playerHp = min(stats['maxHp'], playerHp + 50)
                                    elif item["id"] == "cons_2": stats['specialAmmo'] += 1
                                    opt["sold"] = True
                                # 인벤토리 장착 처리
                                else:
                                    if len(inventory) < 9:
                                        stats['gold'] -= item['price']
                                        inventory.append(item)
                                        opt["sold"] = True
                                        calculate_stats()
                                    else:
                                        pendingItem = opt
                                        shopSubState = "CONFIRM_REPLACE"

                # 2. 교체 확인 모드 처리 (들여쓰기 수정 완료)
                elif shopSubState == "CONFIRM_REPLACE":
                    btn_yes = pygame.Rect(330, HEIGHT//2 + 50, 100, 40)
                    btn_no = pygame.Rect(470, HEIGHT//2 + 50, 100, 40)

                    if btn_yes.collidepoint(mousePos):
                        shopSubState = "SELECT_REMOVE"
                    elif btn_no.collidepoint(mousePos):
                        shopSubState = "NORMAL"
                        pendingItem = None

                # 3. 제거할 아이템 선택 모드 처리 (들여쓰기 수정 완료)
                elif shopSubState == "SELECT_REMOVE":
                    CENTER_X = WIDTH // 2
                    # 인벤토리 순회하며 클릭된 슬롯 확인
                    for i in range(len(inventory)):
                        row, col = i // 3, i % 3
                        slotRect = pygame.Rect(CENTER_X + 50 + col * 110, 160 + row * 110, 100, 100)

                        if slotRect.collidepoint(mousePos):
                            # 돈 차감 및 아이템 교체 및 상점 내 품절 처리
                            stats['gold'] -= pendingItem["data"]["price"]
                            inventory.pop(i)
                            inventory.append(pendingItem["data"])
                            pendingItem["sold"] = True

                            # 상태 초기화 및 스탯 재적용
                            shopSubState = "NORMAL"
                            pendingItem = None
                            calculate_stats()
                            break     
                    
    # --- 게임 상태별 업데이트 및 렌더링 ---
    for p in particles[:]:
        p.update()
        if p.life <= 0: particles.remove(p)
    
    if gameState == 'PLAYING':
        playerCenter = playerPos + pygame.Vector2(30, 30)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: playerPos.x -= stats["speed"]
        if keys[pygame.K_RIGHT]: playerPos.x += stats["speed"]
        if keys[pygame.K_UP]: playerPos.y -= stats["speed"]
        if keys[pygame.K_DOWN]: playerPos.y += stats["speed"]

        if playerPos.x < -30: playerPos.x = WIDTH
        elif playerPos.x > WIDTH: playerPos.x = -30
        playerPos.y = max(0, min(HEIGHT-40, playerPos.y))
        
        current_homing = keys[pygame.K_LSHIFT]  
        if keys[pygame.K_q] and shootCooldown <= 0:
            base_dir = pygame.Vector2(0, -10)  # 기본 위쪽 발사
            is_homing = keys[pygame.K_LSHIFT]

            new_proj = Projectile(
                    playerPos.x + 30, 
                    playerPos.y + 30, 
                    pygame.Vector2(0, -10), 
                    GREEN, 
                    stats['damage'],
                    isHoming=keys[pygame.K_LSHIFT] # 이제 정상적으로 인식됩니다.
                )
            pProjs.append(new_proj)
            shootCooldown = 15 # 발사 간격 조절
        shootCooldown = max(0, shootCooldown - 1)
        if invincibleTimer > 0: invincibleTimer -= 1

        if keys[pygame.K_w] and stats["specialAmmo"] > 0 and specialEffectTimer <= 0:
            stats["specialAmmo"] -= 1
            specialEffectTimer = 40  
            shakeTimer = 10         
            if assets.sounds['explosion']:
                assets.sounds['explosion'].play()
            
            # 1. 화면의 모든 적 투사체(총알) 즉시 삭제
            eProjs.clear() 
            
            # 2. 모든 일반 적에게 강력한 데미지
            for e in enemies[:]:
                # 안전하게 hp 속성 존재 여부 확인 후 데미지 적용
                if hasattr(e, 'hp'):
                    e.hp -= 30
                    if e.hp <= 0:
                        if e in enemies: enemies.remove(e)
                        score += 150
                        # 처치 이펙트 생성 (선택 사항)
                        for _ in range(5): 
                            particles.append(Particle(e.pos.x+15, e.pos.y+15, (255, 255, 255)))
            
            # 3. 보스가 있다면 보스에게도 데미지
            if boss:
                boss.hp -= 100

        if boss is None:
            stageTimer -= 1
            if stageTimer == 120: bossAlertTimer = 120
            if stageTimer <= 0:
                if zeroTicket: boss = BossZero(); zeroTicket = False
                elif currentStage == 1:
                    # boss = BossSwarm()
                    # boss = BossZero()
                    # boss = BossChernobog()
                    boss = BossCrusher()
                elif currentStage == 2:
                    boss = BossCrusher()
                elif currentStage == 3:
                    boss = BossCrusher()
                else:
                    # 모든 지정된 스테이지 이후에는 무작위 혹은 기본 보스
                    boss = random.choice([BossCrusher()])

            if len(enemies) < 10:
                enemyType = getRandomEnemy(currentStage)
                enemies.append(Enemy(enemyType, random.randint(0, 1000)))
        else:
            if boss.type == "SWARM":
                if len(enemies) < 5: 
                    if random.random() < 0.25:
                        enemies.append(Enemy("type4", random.randint(0, 1000)))

        if boss:
            boss.update(eProjs, playerPos)
            bossRect = getattr(boss, 'rect', pygame.Rect(boss.pos.x, boss.pos.y, 50, 50) if hasattr(boss, 'pos') else None)
            hit_by_boss = False
            if bossRect and bossRect.collidepoint(playerCenter.x, playerCenter.y): 
                hit_by_boss = True
            elif hasattr(boss, 'pos') and boss.pos.distance_to(playerCenter) < hitboxRadius + 25: # 반경 25로 보스 둥근 몸체 가정
                hit_by_boss = True

            if hit_by_boss:
                take_damage(20, 20, 60)

            if boss.hp <= 0:
                boss = None
                stats["gold"] += 1500
                score += 5000
                gameState = 'SHOP'
                refresh_shop()

# --- [준비 단계] 공통 변수 계산 (DRY 원칙) ---

        # --- 1. 적(Enemies) 업데이트 및 플레이어 충돌 판정 ---
        for e in enemies[:]:
            e.update(eProjs, playerPos) 
            eCenter = pygame.Vector2(e.pos.x + 15, e.pos.y + 15)

            # type4 좌우 반사 로직 (화면 밖 제거 대신 반사)
            if getattr(e, 'eType', "") == "type4":
                if e.pos.x <= 0 or e.pos.x >= WIDTH - 10:
                    e.vx *= -1
            
            # 플레이어 본체와 적 충돌 (원형 판정)
            if playerCenter.distance_to(eCenter) < hitboxRadius + 15 and invincibleTimer <= 0:
                if take_damage(15, 15, 40):
                    if e in enemies: enemies.remove(e)

            # 화면 하단 이탈 시 제거 (리스폰을 위함)
            if e.pos.y > HEIGHT + 50:
                if e in enemies: enemies.remove(e)
                continue

        # --- 2. 적 투사체(eProjs) 업데이트 및 플레이어 피격 판정 ---
        for p in eProjs[:]:
            shouldRemove = False
            if isinstance(p, HomingProjectile):
                shouldRemove = p.updateTarget(playerPos, eProjs)
            else:
                p.update()
            
            # 화면 밖 제거 판정
            offScreen = p.pos.x < -100 or p.pos.x > WIDTH+100 or p.pos.y < -100 or p.pos.y > HEIGHT+100
            if shouldRemove or offScreen:
                if p in eProjs: eProjs.remove(p)
                continue

            # 플레이어 피격 판정
            p_radius = getattr(p, 'radius', 5)
            if p.pos.distance_to(playerCenter) < hitboxRadius + p_radius:
                playerHp -= p.dmg
                if p in eProjs: eProjs.remove(p)
            elif p.pos.y > HEIGHT: 
                if p in eProjs: eProjs.remove(p)

        # --- 플레이어 투사체(pProjs) 업데이트 및 적/보스 피격 판정 ---
        for p in pProjs[:]:
            if getattr(p, 'isHoming', False):
                valid_targets = []
                
                # 1. 몬스터 타겟 추가
                for e in enemies:
                    valid_targets.append(pygame.Vector2(e.pos.x + 15, e.pos.y + 15))
                
                # 2. 보스 타겟 추가
                if boss and hasattr(boss, 'pos'):
                    # 보스의 중심점 (보스 종류에 따라 세밀한 조정이 필요하다면 offset 추가 가능)
                    valid_targets.append(pygame.Vector2(boss.pos.x, boss.pos.y))
                
                # 3. 가장 가까운 타겟 계산 및 속도 보정 (lerp)
                if valid_targets:
                    closest_target = min(valid_targets, key=lambda pos: p.pos.distance_to(pos))
                    target_dir = closest_target - p.pos
                    if target_dir.length() > 0:
                        # 0.15의 가중치로 부드러운 유도 미사일 궤적 생성
                        p.vel = p.vel.lerp(target_dir.normalize() * 12, 0.15)
            p.update()
            hitThisFrame = False
            
            # 보스 피격 판정
            if boss:
                hit_radius = getattr(boss, 'hitboxRadius', 40) # 보스 클래스에 정의된 피격 반경 우선 사용
                hitThisFrame = False

                # BossZero의 다중 코어(swarmCenters) 판정
                if boss.type == "CRAZY" and boss.phase <= 3:
                    for center in boss.swarmCenters:
                        if p.pos.distance_to(center) < 20: # 코어 피격 반경
                            boss.hp -= p.dmg # p.damage가 아니라 p.dmg 여야 합니다!
                            hitThisFrame = True
                            break
                
                # 일반적인 보스 본체 피격 판정
                if not hitThisFrame and p.pos.distance_to(boss.pos) < hit_radius:
                    boss.hp -= p.dmg
                    hitThisFrame = True
                
            # 일반 적 피격 판정 (보스를 맞추지 않았을 때만 체크하거나 관통 시 체크)
            if not hitThisFrame:
                for e in enemies[:]:
                    eCenter = pygame.Vector2(e.pos.x + 15, e.pos.y + 15)
                    if p.pos.distance_to(eCenter) < 20: # 적 피격 판정 범위 20
                        e.hp -= stats["damage"]
                        hitThisFrame = True
                        
                        if e.hp <= 0:
                            if getattr(e, 'eType', None) == "elite": zeroTicket = True
                            if e in enemies: enemies.remove(e)
                            stats["gold"] += 35
                            
                            earned_score = 40 if getattr(p, 'isHoming', False) else 100
                            score += earned_score
                            
                            for _ in range(10): particles.append(Particle(eCenter.x, eCenter.y, (255, 50, 50)))
                        break

            # 투사체 소멸 처리 (관통 업그레이드 여부 확인)
            if hitThisFrame and not stats.get("pierce", False):
                if p in pProjs: pProjs.remove(p)
            elif p.pos.y < -50 or p.pos.y > HEIGHT + 50 or p.pos.x < -50 or p.pos.x > WIDTH + 50:
                if p in pProjs: pProjs.remove(p)

        # --- 게임 오버 체크 ---
        if playerHp <= 0:
            if score > highScore: 
                try:
                    saveHighscoreSecure(score) # 보안 저장 함수로 변경
                except Exception as e:
                    print(f"점수 저장 실패: {e}") # try-catch 예외 처리 규칙 반영
            running = False

    # --- 최종 렌더링 부 ---
    # 배경 영상 처리
    screen.fill(BLACK)

    # 투명도 지원 서피스 (모든 오브젝트는 여기에 그림)
    tempSurf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    tempSurf.fill((0, 0, 0, 0))

    if gameState == 'PLAYING':
        for p in particles: p.draw(tempSurf)
        for e in enemies: e.draw(tempSurf) 
            
        if boss:
            boss.draw(tempSurf)
        
        for p in pProjs: p.draw(tempSurf)
        for p in eProjs: p.draw(tempSurf)
        
        # --- 수정된 렌더링 코드 ---
        if invincibleTimer % 4 == 0: 
            tempSurf.blit(assets.images['player'], playerPos)
            hitboxRadius = 5

            # 1. 원형 테두리 (이건 투명도가 필요 없으므로 그대로 유지)
            pygame.draw.circle(tempSurf, CYAN, playerCenter, hitboxRadius, 2)
            fillSurf = pygame.Surface((hitboxRadius * 2, hitboxRadius * 2), pygame.SRCALPHA)
            pygame.draw.circle(fillSurf, (0, 255, 255, 80), (hitboxRadius, hitboxRadius), hitboxRadius - 2)
            tempSurf.blit(fillSurf, (playerCenter[0] - hitboxRadius, playerCenter[1] - hitboxRadius))
            
        if boss is None:
            pygame.draw.rect(tempSurf, GRAY, (WIDTH//2-100, 20, 200, 8))
            pygame.draw.rect(tempSurf, CYAN, (WIDTH//2-100, 20, (stageTimer/STAGE_DURATION)*200, 8))
            if bossAlertTimer > 0:
                tempSurf.blit(assets.fonts['large'].render("-!!! WARNING !!!-", True, assets.colors['red']), (WIDTH//2-250, HEIGHT//2-50))
                bossAlertTimer -= 1

    # --- 메인 루프 내부 그리기 영역 ---

    if gameState == 'SHOP':
        tempSurf.fill((15, 15, 25)) 
        CENTER_X = WIDTH // 2  # 450px

        # 0. 상단 공통 타이틀 및 안내
        tempSurf.blit(assets.fonts['medium'].render(f"보유 골드: {stats['gold']}G", True, assets.colors['gold']), (30, 30))
        tempSurf.blit(assets.fonts['small'].render("[Z] 전환 | [S] 시작", True, assets.colors['white']), (30, 70))

        # --- [좌측 영역: 상점 및 시너지 (0 ~ 450px)] ---
        if shopTab == "MARKET":
            tempSurf.blit(assets.fonts['medium'].render("MARKET ITEMS", True, assets.colors['cyan']), (30, 120))
            for i, opt in enumerate(shopOptions):
                cardRect = pygame.Rect(30 + i * 135, 170, 125, 180)
                color = (40, 40, 50) if not opt["sold"] else (20, 20, 20)
                pygame.draw.rect(tempSurf, color, cardRect, border_radius=10)
                if not opt["sold"]:
                    tempSurf.blit(assets.fonts['small'].render(opt['data']['name'][:8], True, assets.colors['white']), (cardRect.x+10, cardRect.y+15))
                    tempSurf.blit(assets.fonts['small'].render(f"{opt['data']['price']}G", True, assets.colors['gold']), (cardRect.x+10, cardRect.y+150))
        elif shopTab == "BANK":
            # 은행 전용 인터페이스 추가
            tempSurf.blit(assets.fonts['medium'].render("GALACTIC BANK", True, assets.colors['gold']), (30, 120))
            # 은행 잔고 및 조작 안내
            bank_info = f"은행 잔고: {bankBalance}G"
            tempSurf.blit(assets.fonts['medium'].render(bank_info, True, assets.colors['white']), (60, 180))
            tempSurf.blit(assets.fonts['small'].render("[A] 100G 예금 | [D] 100G 출금", True, assets.colors['cyan']), (60, 230))
            tempSurf.blit(assets.fonts['small'].render("이자는 라운드 종료 시 15% 지급됩니다.", True, assets.colors['green']), (60, 270))
            
        # [좌측 하단: 시너지 이원화 표시]
        pygame.draw.line(tempSurf, assets.colors['gray'], (20, 350), (CENTER_X - 20, 350), 2)
        # 왼쪽 칸: 보유 현황
        tempSurf.blit(assets.fonts['small'].render("[ 보유 시너지 ]", True, assets.colors['gold']), (30, 365))
        # 오른쪽 칸: 발동 효과
        tempSurf.blit(assets.fonts['small'].render("[ 발동 효과 ]", True, assets.colors['green']), (CENTER_X // 2 + 30, 365))
        
        synergy_counts = {}
        for item in inventory:
            for tag in item["tags"]:
                synergy_counts[tag] = synergy_counts.get(tag, 0) + 1
        
        y_pos = 400
        for tag, count in synergy_counts.items():
            # 왼쪽 출력 (보유 태그 개수)
            tempSurf.blit(assets.fonts['small'].render(f"{tag}: {count}개", True, assets.colors['white']), (30, y_pos))
            
            # 오른쪽 출력 (발동된 효과)
            if tag in SYNERGY_DATA:
                valid_effects = [
                    (req, data) for req, data in SYNERGY_DATA[tag].items()
                    if count >= req
                ]
                if valid_effects:
                    req, data = max(valid_effects, key=lambda x: x[0])  # 최고 단계만 출력
                    eff_txt = f"{data['name']}"
                    tempSurf.blit(assets.fonts['small'].render(eff_txt, True, assets.colors['cyan']), (CENTER_X // 2 + 30, y_pos))
            y_pos += 25

        # --- [우측 영역: 인벤토리 9칸 (450 ~ 900px)] ---
        tempSurf.blit(assets.fonts['medium'].render("INVENTORY", True, assets.colors['white']), (CENTER_X + 40, 120))
        for i in range(9):
            row, col = i // 3, i % 3
            slotRect = pygame.Rect(CENTER_X + 50 + col * 110, 160 + row * 110, 100, 100)
            pygame.draw.rect(tempSurf, (25, 25, 35), slotRect, border_radius=5)
            pygame.draw.rect(tempSurf, assets.colors['gray'], slotRect, 2, border_radius=5)
            
            if i < len(inventory):
                # 아이템 장착 시 표시
                item_txt = assets.fonts['small'].render(inventory[i]["name"][:6], True, assets.colors['cyan'])
                tempSurf.blit(item_txt, (slotRect.x + 10, slotRect.y + 40))

        if shopSubState == "CONFIRM_REPLACE":
            # 화면 중앙 팝업창 배경
            popup_rect = pygame.Rect(300, HEIGHT//2 - 50, 300, 160)
            pygame.draw.rect(tempSurf, (40, 40, 50), popup_rect, border_radius=10)
            pygame.draw.rect(tempSurf, assets.colors['gold'], popup_rect, 2, border_radius=10)
            
            # 안내 문구
            tempSurf.blit(assets.fonts['small'].render("인벤토리가 꽉 찼습니다.", True, assets.colors['white']), (355, HEIGHT//2 - 30))
            tempSurf.blit(assets.fonts['small'].render("기존 아이템을 버리고 장착하시겠습니까?", True, assets.colors['gold']), (315, HEIGHT//2 - 5))
            
            # YES 버튼 (x=330, y=HEIGHT//2+50)
            pygame.draw.rect(tempSurf, assets.colors['green'], (330, HEIGHT//2 + 50, 100, 40), border_radius=5)
            tempSurf.blit(assets.fonts['medium'].render("YES", True, assets.colors['black']), (355, HEIGHT//2 + 55))
            
            # NO 버튼 (x=470, y=HEIGHT//2+50)
            pygame.draw.rect(tempSurf, assets.colors['red'], (470, HEIGHT//2 + 50, 100, 40), border_radius=5)
            tempSurf.blit(assets.fonts['medium'].render("NO", True, assets.colors['white']), (500, HEIGHT//2 + 55))
            
        elif shopSubState == "SELECT_REMOVE":
            # 인벤토리 영역 위에 붉은색 경고/안내 문구 표시
            tempSurf.blit(assets.fonts['medium'].render("버릴 아이템을 클릭하세요!", True, assets.colors['red']), (CENTER_X + 50, 90))
        # 스탯 렌더링
        stat_text = f"DMG: {stats['damage']} | SPD: {stats['speed']} | MAX_HP: {stats['maxHp']} | 관통: {'ON' if stats['pierce'] else 'OFF'} | W: {stats['specialAmmo']}"
        tempSurf.blit(assets.fonts['small'].render(stat_text, True, assets.colors['white']), (300, HEIGHT - 30))

    # 1. 가장 밑바닥에 배경 먼저 그리기
    screen.blit(assets.images['background'], (0, 0))
    screen.blit(tempSurf, (0, 0))
        
    # W 특수기 효과
    if specialEffectTimer > 0:
        # 1. 화면 전체를 어둡게 (섬광 대신 몰입감)
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))
        
        # 2. 개성 있는 '절단선' 이펙트 (화면을 가로지르는 날카로운 선)
        line_y = HEIGHT // 2
        line_width = specialEffectTimer * 2 # 시간이 갈수록 얇아짐
        pygame.draw.line(screen, CYAN, (0, line_y), (WIDTH, line_y), line_width)
        pygame.draw.line(screen, WHITE, (0, line_y), (WIDTH, line_y), max(1, line_width // 3))
        
        specialEffectTimer -= 1
    
    # 4. 전투 시에만 보이는 UI
    if gameState != 'SHOP':
        # 체력바 배경 현재 체력(초록색)
        pygame.draw.rect(screen, GREEN, (10, 10, max(0, (playerHp/stats['maxHp'])*200), 20))    
        screen.blit(assets.fonts['small'].render(f"{int(playerHp)} / {stats['maxHp']}", True, assets.colors['black']), (80, 10))
        
        # 정보 텍스트 (점수, 최고점수, 스테이지 정보 그룹화)
        infoTxt1 = assets.fonts['small'].render(f"SCORE: {score} | HI-SCORE: {highScore} | STAGE: {currentStage}", True, assets.colors['white'])
        screen.blit(infoTxt1, (10, 35))
        
        # 재화 및 특수기 개수 표기 (눈에 띄도록 골드 색상 강조)
        infoTxt2 = assets.fonts['small'].render(f"GOLD: {stats['gold']} G | SPECIAL (W): {stats['specialAmmo']} 개", True, assets.colors['gold'])
        screen.blit(infoTxt2, (10, 55))
        
        # 제로 티켓 활성화 상태
        if zeroTicket: 
            screen.blit(assets.fonts['small'].render("★ ZERO TICKET ACTIVE ★", True, assets.colors['cyan']), (10, 75))
            
    # UI 업데이트 및 프레임 제한
    pygame.display.flip()
pygame.quit()