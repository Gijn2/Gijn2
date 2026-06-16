# UIManager.py
import pygame
from constants import WIDTH, HEIGHT, GOLD, WHITE, CYAN, GREEN, GRAY, RED, BLACK, SYNERGY_DATA
from assetManager import assets
from systems.SharedState import state, stats

def drawShopUI(screen):
    if state["gameState"] != 'SHOP':
        return
        
    tempSurf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    tempSurf.fill((15, 15, 25)) 
    centerX = WIDTH // 2  

    tempSurf.blit(assets.fonts['medium'].render(f"보유 골드: {stats['gold']}G", True, GOLD), (30, 30))
    tempSurf.blit(assets.fonts['small'].render("[Z] 전환 | [S] 시작", True, WHITE), (30, 70))

    if state["shopTab"] == "MARKET":
        tempSurf.blit(assets.fonts['medium'].render("MARKET ITEMS", True, CYAN), (30, 120))
        for i, opt in enumerate(state["shopOptions"]):
            cardRect = pygame.Rect(30 + i * 135, 170, 125, 180)
            color = (40, 40, 50) if not opt["sold"] else (20, 20, 20)
            pygame.draw.rect(tempSurf, color, cardRect, border_radius=10)
            if not opt["sold"]:
                tempSurf.blit(assets.fonts['small'].render(opt['data']['name'][:8], True, WHITE), (cardRect.x+10, cardRect.y+15))
                tempSurf.blit(assets.fonts['small'].render(f"{opt['data']['price']}G", True, GOLD), (cardRect.x+10, cardRect.y+150))
                
    elif state["shopTab"] == "BANK":
        tempSurf.blit(assets.fonts['medium'].render("GALACTIC BANK", True, GOLD), (30, 120))
        bankInfo = f"은행 잔고: {state['bankBalance']}G"
        tempSurf.blit(assets.fonts['medium'].render(bankInfo, True, WHITE), (60, 180))
        tempSurf.blit(assets.fonts['small'].render("[A] 100G 예금 | [D] 100G 출금", True, CYAN), (60, 230))
        tempSurf.blit(assets.fonts['small'].render("이자는 라운드 종료 시 5% 지급됩니다.", True, GREEN), (60, 270))
        
    pygame.draw.line(tempSurf, GRAY, (20, 350), (centerX - 20, 350), 2)
    tempSurf.blit(assets.fonts['small'].render("[ 보유 시너지 ]", True, GOLD), (30, 365))
    tempSurf.blit(assets.fonts['small'].render("[ 발동 효과 ]", True, GREEN), (centerX // 2 + 30, 365))
    
    synergyCounts = {}
    for item in state["inventory"]:
        for tag in item["tags"]:
            synergyCounts[tag] = synergyCounts.get(tag, 0) + 1
    
    yPos = 400
    for tag, count in synergyCounts.items():
        tempSurf.blit(assets.fonts['small'].render(f"{tag}: {count}개", True, WHITE), (30, yPos))
        if tag in SYNERGY_DATA:
            validEffects = [(req, data) for req, data in SYNERGY_DATA[tag].items() if count >= req]
            if validEffects:
                req, data = max(validEffects, key=lambda x: x[0])
                tempSurf.blit(assets.fonts['small'].render(data['name'], True, CYAN), (centerX // 2 + 30, yPos))
        yPos += 25

    tempSurf.blit(assets.fonts['medium'].render("INVENTORY", True, WHITE), (centerX + 40, 120))
    for i in range(9):
        row, col = i // 3, i % 3
        slotRect = pygame.Rect(centerX + 50 + col * 110, 160 + row * 110, 100, 100)
        pygame.draw.rect(tempSurf, (25, 25, 35), slotRect, border_radius=5)
        pygame.draw.rect(tempSurf, GRAY, slotRect, 2, border_radius=5)
        
        if i < len(state["inventory"]):
            itemTxt = assets.fonts['small'].render(state["inventory"][i]["name"][:6], True, CYAN)
            tempSurf.blit(itemTxt, (slotRect.x + 10, slotRect.y + 40))

    if state["shopSubState"] == "CONFIRM_REPLACE":
        popupRect = pygame.Rect(300, HEIGHT//2 - 50, 300, 160)
        pygame.draw.rect(tempSurf, (40, 40, 50), popupRect, border_radius=10)
        pygame.draw.rect(tempSurf, GOLD, popupRect, 2, border_radius=10)
        
        tempSurf.blit(assets.fonts['small'].render("인벤토리가 꽉 찼습니다.", True, WHITE), (355, HEIGHT//2 - 30))
        tempSurf.blit(assets.fonts['small'].render("기존 아이템을 버리고 장착하시겠습니까?", True, GOLD), (315, HEIGHT//2 - 5))
        
        pygame.draw.rect(tempSurf, GREEN, (330, HEIGHT//2 + 50, 100, 40), border_radius=5)
        tempSurf.blit(assets.fonts['medium'].render("YES", True, BLACK), (355, HEIGHT//2 + 55))
        
        pygame.draw.rect(tempSurf, RED, (470, HEIGHT//2 + 50, 100, 40), border_radius=5)
        tempSurf.blit(assets.fonts['medium'].render("NO", True, WHITE), (500, HEIGHT//2 + 55))
        
    elif state["shopSubState"] == "SELECT_REMOVE":
        tempSurf.blit(assets.fonts['medium'].render("버릴 아이템을 클릭하세요!", True, RED), (centerX + 50, 90))

    statText = f"DMG: {stats['damage']} | SPD: {stats['speed']} | MAX_HP: {stats['maxHp']} | 관통: {'ON' if stats['pierce'] else 'OFF'} | W: {stats['specialAmmo']}"
    tempSurf.blit(assets.fonts['small'].render(statText, True, WHITE), (300, HEIGHT - 30))
    
    screen.blit(tempSurf, (0, 0))

def drawCombatUI(screen):
    if state["gameState"] == 'SHOP':
        return
        
    pygame.draw.rect(screen, GREEN, (10, 10, max(0, (state['playerHp']/stats['maxHp'])*200), 20))    
    screen.blit(assets.fonts['small'].render(f"{int(state['playerHp'])} / {stats['maxHp']}", True, BLACK), (80, 10))
    
    infoTxt1 = assets.fonts['small'].render(f"SCORE: {state['score']} | HI-SCORE: {state['highScore']} | STAGE: {state['currentStage']}", True, WHITE)
    screen.blit(infoTxt1, (10, 35))
    
    infoTxt2 = assets.fonts['small'].render(f"GOLD: {stats['gold']} G | SPECIAL (W): {stats['specialAmmo']} 개", True, GOLD)
    screen.blit(infoTxt2, (10, 55))
    
    if state['zeroTicket']: 
        screen.blit(assets.fonts['small'].render("★ ZERO TICKET ACTIVE ★", True, CYAN), (10, 75))

def drawSpecialEffect(screen):
    if state["specialEffectTimer"] <= 0:
        return
        
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    screen.blit(overlay, (0, 0))
    
    lineY = HEIGHT // 2
    lineWidth = state["specialEffectTimer"] * 2 
    pygame.draw.line(screen, CYAN, (0, lineY), (WIDTH, lineY), lineWidth)
    pygame.draw.line(screen, WHITE, (0, lineY), (WIDTH, lineY), max(1, lineWidth // 3))
    
    state["specialEffectTimer"] -= 1