# 게임의 진입점 및 메인 루프 (이벤트 처리, 화면 렌더링)

# main.py
import pygame
import os
import random

# 분리된 모듈 임포트
from constants import *
from assetManager import assets
from entities.Enemy import Enemy, getRandomEnemy
from systems.ShopManager import refreshShop, applyInterest
from systems.SharedState import state, stats
from systems.StatsManager import calculateStats
from systems.CollisionManager import takeDamage
from systems.UIManager import drawShopUI, drawCombatUI, drawSpecialEffect
from utils.fileIO import saveHighscoreSecure
from entities.Bosses import *
from entities.Projectiles import *

# --- 초기화 및 화면 설정 ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Topdown Shooting Pygame: Limited Edition")
clock = pygame.time.Clock()
assets.loadAllAssets()

# --- 게임 상태 관리 변수 초기화 ---
stageTimer = STAGE_DURATION

playerPos = pygame.Vector2(WIDTH//2, HEIGHT-80)
enemies, pProjs, eProjs, boss = [], [], [], None
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    clock.tick(37.5)
    
    # 화면 흔들림 계산
    render_offset = pygame.Vector2(0, 0)
    if state["shakeTimer"] > 0:
        render_offset = (random.randint(-state["shakeTimer"], state["shakeTimer"]), 
                        random.randint(-state["shakeTimer"], state["shakeTimer"]))
        state["shakeTimer"] -= 1
    else:
        render_offset = (0, 0)

    # 투명도를 지원하는 도화지 생성
    tempSurf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    tempSurf.fill((0, 0, 0, 0)) # 투명하게 초기화

    # [1] Input & Event Handling (책임 분리)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        
        if event.type == pygame.KEYDOWN:

            if state["gameState"] == 'SHOP':
                if state["shopSubState"] == "NORMAL":
                    # 은행 입출금 기능 (은행 탭일 때만 작동)
                    if state["shopTab"] == "BANK":
                        if event.key == pygame.K_a and stats["gold"] >= 100:
                            stats["gold"] -= 100
                            state["bankBalance"] += 100
                        elif event.key == pygame.K_d and state["bankBalance"] >= 100:
                            stats["gold"] += 100
                            state["bankBalance"] -= 100

                    if event.key == pygame.K_z:
                        state["shopTab"] = "BANK" if state["shopTab"] == "MARKET" else "MARKET"
                    
                    # S키로 스테이지 시작
                    elif event.key == pygame.K_s:
                        applyInterest()
                        state["gameState"] = 'PLAYING'
                        state["currentStage"] += 1
                        stageTimer = STAGE_DURATION
                
                    # R키: 상점 새로고침
                    if event.key == pygame.K_r:
                        cost = 0 if state["freeRefreshAvailable"] else (200 + 100 * state["shopRefreshCount"])
                        if stats['gold'] >= cost:
                            stats['gold'] -= cost
                            if not state["freeRefreshAvailable"]:
                                state["shopRefreshCount"] += 1
                            state["freeRefreshAvailable"] = False
                            refreshShop()  # 아이템 교체 실행

                    # 숫자키 1, 2, 3으로 아이템 구매
                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                        if state["shopTab"] == "MARKET" and state["shopSubState"] == "NORMAL":
                            idx = event.key - pygame.K_1 # K_1은 0, K_2는 1, K_3은 2로 매핑
                            if idx < len(state["shopOptions"]):
                                opt = state["shopOptions"][idx]
                                if not opt["sold"]:
                                    item = opt["data"]
                                    if stats['gold'] >= item['price']:
                                        if item.get("type") == "CONSUMABLE":
                                            stats['gold'] -= item['price']
                                            if item["id"] == "cons_1": state["playerHp"] = min(stats['maxHp'], state["playerHp"] + 50)
                                            elif item["id"] == "cons_2": stats['specialAmmo'] += 1
                                            opt["sold"] = True
                                        else:
                                            if len(state["inventory"]) < 9:
                                                stats['gold'] -= item['price']
                                                state["inventory"].append(item)
                                                opt["sold"] = True
                                                calculateStats()
                                            else:
                                                state["pendingItem"] = opt
                                                state["shopSubState"] = "CONFIRM_REPLACE"

        # 마우스 클릭: 아이템 구매 및 인벤토리 관리
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state["gameState"] == 'SHOP':
                mousePos = pygame.mouse.get_pos()
                
                # 1. 일반 상점 아이템 구매
                if state["shopSubState"] == "NORMAL" and state["shopTab"] == "MARKET":
                    for i, opt in enumerate(state["shopOptions"]):
                        card_rect = pygame.Rect(30 + i * 135, 170, 125, 180)

                        if card_rect.collidepoint(mousePos) and not opt["sold"]:
                            item = opt["data"]
                            if stats['gold'] >= item['price']:
                                # 소모품 처리
                                if item.get("type") == "CONSUMABLE":
                                    stats['gold'] -= item['price']
                                    if item["id"] == "cons_1": state["playerHp"] = min(stats['maxHp'], state["playerHp"] + 50)
                                    elif item["id"] == "cons_2": stats['specialAmmo'] += 1
                                    opt["sold"] = True
                                # 인벤토리 장착 처리
                                else:
                                    if len(state["inventory"]) < 9:
                                        stats['gold'] -= item['price']
                                        state["inventory"].append(item)
                                        opt["sold"] = True
                                        calculateStats()
                                    else:
                                        state["pendingItem"] = opt
                                        state["shopSubState"] = "CONFIRM_REPLACE"

                # 2. 교체 확인 모드 처리 (들여쓰기 수정 완료)
                elif state["shopSubState"] == "CONFIRM_REPLACE":
                    btn_yes = pygame.Rect(330, HEIGHT//2 + 50, 100, 40)
                    btn_no = pygame.Rect(470, HEIGHT//2 + 50, 100, 40)

                    if btn_yes.collidepoint(mousePos):
                        state["shopSubState"] = "SELECT_REMOVE"
                    elif btn_no.collidepoint(mousePos):
                        state["shopSubState"] = "NORMAL"
                        state["pendingItem"] = None

                # 3. 제거할 아이템 선택 모드 처리 (들여쓰기 수정 완료)
                elif state["shopSubState"] == "SELECT_REMOVE":
                    CENTER_X = WIDTH // 2
                    # 인벤토리 순회하며 클릭된 슬롯 확인
                    for i in range(len(state["inventory"])):
                        row, col = i // 3, i % 3
                        slotRect = pygame.Rect(CENTER_X + 50 + col * 110, 160 + row * 110, 100, 100)

                        if slotRect.collidepoint(mousePos):
                            # 돈 차감 및 아이템 교체 및 상점 내 품절 처리
                            stats["gold"] -= state["pendingItem"]["data"]["price"]
                            state["inventory"].pop(i)
                            state["inventory"].append(state["pendingItem"]["data"])
                            state["pendingItem"]["sold"] = True

                            # 상태 초기화 및 스탯 재적용
                            state["shopSubState"] = "NORMAL"
                            state["pendingItem"] = None
                            calculateStats()
                            break
                    
    # --- 게임 상태별 업데이트 및 렌더링 ---
    for p in state["particles"][:]:
        p.update()
        if p.life <= 0: state["particles"].remove(p)

    if state["gameState"] == 'PLAYING':
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
        if keys[pygame.K_q] and state["shootCooldown"] <= 0:
            base_dir = pygame.Vector2(0, -10)  # 기본 위쪽 발사
            is_homing = keys[pygame.K_LSHIFT]

            new_proj = Projectile(
                    playerPos.x + 30, 
                    playerPos.y + 30, 
                    pygame.Vector2(0, -10), 
                    GREEN, 
                    stats["damage"],
                    isHoming=keys[pygame.K_LSHIFT]
                )
            pProjs.append(new_proj)
            state["shootCooldown"] = 15 # 발사 간격 조절
        state["shootCooldown"] = max(0, state["shootCooldown"] - 1)
        if state["invincibleTimer"] > 0: state["invincibleTimer"] -= 1

        if keys[pygame.K_w] and stats["specialAmmo"] > 0 and state["specialEffectTimer"] <= 0:
            stats["specialAmmo"] -= 1
            state["specialEffectTimer"] = 40  
            state["shakeTimer"] = 10         
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
                        state["score"] += 150
                        # 처치 이펙트 생성 (선택 사항)
                        for _ in range(5): 
                            state["particles"].append(Particle(e.pos.x+15, e.pos.y+15, (255, 255, 255)))
            
            # 3. 보스가 있다면 보스에게도 데미지
            if boss:
                boss.hp -= 100

        if boss is None:
            stageTimer -= 1
            if stageTimer == 120: state["bossAlertTimer"] = 120
            if stageTimer <= 0:
                if state['zeroTicket']: boss = BossZero(); state['zeroTicket'] = False
                elif state['currentStage'] == 1:
                    # boss = BossSwarm()
                    # boss = BossZero()
                    boss = BossCrusher()
                elif state['currentStage'] == 2:
                    boss = BossCrusher()
                elif state['currentStage'] == 3:
                    boss = BossCrusher()
                else:
                    # 모든 지정된 스테이지 이후에는 무작위 혹은 기본 보스
                    boss = random.choice([BossCrusher()])

            if len(enemies) < 10:
                enemyType = getRandomEnemy(state['currentStage'])
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
            elif hasattr(boss, 'pos') and boss.pos.distance_to(playerCenter) < state["hitboxRadius"] + 25: # 반경 25로 보스 둥근 몸체 가정
                hit_by_boss = True

            if hit_by_boss:
                takeDamage(20, 20, 60)

            if boss.hp <= 0:
                boss = None
                stats["gold"] += 1500
                state["score"] += 5000
                state["gameState"] = 'SHOP'

                stageTimer = STAGE_DURATION 
                
                state["freeRefreshAvailable"] = True
                state["shopRefreshCount"] = 0
                refreshShop()
    
    # 2026-05-19: 시너지 효과 처리 (기본 스탯 확장에 따른 업데이트)
    # [신규] 마녀회(2) 시너지: 틱당 체력 재생 (약 1초마다 1씩 회복)
        if stats.get("hp_regen", 0) > 0 and state["playerHp"] > 0:
            # 60프레임 기준으로 대략 1초에 한 번 발동되도록 설정
            if pygame.time.get_ticks() % 1000 < 37: 
                state["playerHp"] = min(stats["maxHp"], state["playerHp"] + stats["hp_regen"])

    # [신규] 여신교(2) 시너지: 이동 시 화염 잔상 파티클 생성
        if stats.get("burn_damage"):
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                if random.random() < 0.4: # 입자 생성 빈도 조절
                    # 주황/빨강 계열의 파티클 생성
                    state["particles"].append(Particle(playerCenter.x + random.randint(-10, 10), playerCenter.y + 15, (255, 100, 20)))

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
            if playerCenter.distance_to(eCenter) < state["hitboxRadius"] + 15 and state["invincibleTimer"] <= 0:
                if takeDamage(15, 15, 40):
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
            if p.pos.distance_to(playerCenter) < state["hitboxRadius"] + p_radius:
                state["playerHp"] -= p.dmg
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
                            if getattr(e, 'eType', None) == "elite": state["zeroTicket"] = True
                            if e in enemies: enemies.remove(e)
                            stats["gold"] += 35
                            
                            earned_score = 40 if getattr(p, 'isHoming', False) else 100
                            state["score"] += earned_score
                            
                            for _ in range(10): state["particles"].append(Particle(eCenter.x, eCenter.y, (255, 50, 50)))
                        break

            # 투사체 소멸 처리 (관통 업그레이드 여부 확인)
            if hitThisFrame and not stats.get("pierce", False):
                if p in pProjs: pProjs.remove(p)
            elif p.pos.y < -50 or p.pos.y > HEIGHT + 50 or p.pos.x < -50 or p.pos.x > WIDTH + 50:
                if p in pProjs: pProjs.remove(p)

        # --- 게임 오버 체크 ---
        if state["playerHp"] <= 0:
            if state["score"] > state["highScore"]:
                try:
                    saveHighscoreSecure(state["score"]) # 보안 저장 함수로 변경
                except Exception as e:
                    print(f"점수 저장 실패: {e}") # try-catch 예외 처리 규칙 반영
            running = False

    # --- 최종 렌더링 부 ---
    # 배경 영상 처리
    screen.fill(BLACK)

    # 투명도 지원 서피스 (모든 오브젝트는 여기에 그림)
    tempSurf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    tempSurf.fill((0, 0, 0, 0))

    if state["gameState"] == 'PLAYING':

        for p in state["particles"]: p.draw(tempSurf)
        for e in enemies: e.draw(tempSurf) 
            
        if boss:
            boss.draw(tempSurf)
        
        for p in pProjs: p.draw(tempSurf)
        for p in eProjs: p.draw(tempSurf)
        
        # --- 수정된 렌더링 코드 ---
        if state["invincibleTimer"] % 4 == 0: 
            tempSurf.blit(assets.images['player'], playerPos)
            state["hitboxRadius"] = 5

            # 1. 원형 테두리 (이건 투명도가 필요 없으므로 그대로 유지)
            pygame.draw.circle(tempSurf, CYAN, playerCenter, state["hitboxRadius"], 2)
            fillSurf = pygame.Surface((state["hitboxRadius"] * 2, state["hitboxRadius"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(fillSurf, (0, 255, 255, 80), (state["hitboxRadius"], state["hitboxRadius"]), state["hitboxRadius"] - 2)
            tempSurf.blit(fillSurf, (playerCenter[0] - state["hitboxRadius"], playerCenter[1] - state["hitboxRadius"]))
            
            # 2026-05-19: 시너지 효과 처리 (기본 스탯 확장에 따른 업데이트)
            # [신규] 셀레스트(4) 시너지: 고정 보호막 시각화
            if stats.get("celest_shield"):
                shield_radius = state["hitboxRadius"] + 25
                # 외곽선
                pygame.draw.circle(tempSurf, (100, 200, 255), playerCenter, shield_radius, 2)
                # 반투명 내부 채우기
                shieldSurf = pygame.Surface((shield_radius * 2, shield_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(shieldSurf, (100, 200, 255, 40), (shield_radius, shield_radius), shield_radius)
                tempSurf.blit(shieldSurf, (playerCenter[0] - shield_radius, playerCenter[1] - shield_radius))

        if boss is None:
            pygame.draw.rect(tempSurf, GRAY, (WIDTH//2-100, 20, 200, 8))
            pygame.draw.rect(tempSurf, CYAN, (WIDTH//2-100, 20, (stageTimer/STAGE_DURATION)*200, 8))
            if state["bossAlertTimer"] > 0:
                tempSurf.blit(assets.fonts['large'].render("-!!! WARNING !!!-", True, RED), (WIDTH//2-250, HEIGHT//2-50))
                state["bossAlertTimer"] -= 1
        drawCombatUI(screen)
    elif state["gameState"] == 'SHOP':
        drawShopUI(screen)
    drawSpecialEffect(screen)

    # 1. 가장 밑바닥에 배경 먼저 그리기
    screen.blit(assets.images['background'], (0, 0))
    
    # 2. 플레이어, 적, 파티클 등이 그려진 tempSurf 덮어씌우기
    screen.blit(tempSurf, (0, 0))
            
    # UI 업데이트 및 프레임 제한
    pygame.display.flip()

pygame.quit()