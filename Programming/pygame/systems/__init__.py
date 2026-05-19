# # 2026-05-19 코드 짬통

# main.py에서 게임 루프와 이벤트 처리를 담당하는 부분을 시스템별로 나누어 관리하기 위해, 시스템별로 함수를 정의하여 호출하는 구조로 리팩토링할 수 있습니다. 아래는 시스템별로 함수를 정의하고, main.py에서 이를 호출하는 예시입니다.
# --- 메인 루프 내부 그리기 영역 ---

#     if state["gameState"] == 'SHOP':
#         tempSurf.fill((15, 15, 25)) 
#         CENTER_X = WIDTH // 2  # 450px

#         # 0. 상단 공통 타이틀 및 안내
#         tempSurf.blit(assets.fonts['medium'].render(f"보유 골드: {state['gold']}G", True, GOLD), (30, 30))
#         tempSurf.blit(assets.fonts['small'].render("[Z] 전환 | [S] 시작", True, WHITE), (30, 70))

#         # --- [좌측 영역: 상점 및 시너지 (0 ~ 450px)] ---
#         if state["shopTab"] == "MARKET":
#             tempSurf.blit(assets.fonts['medium'].render("MARKET ITEMS", True, CYAN), (30, 120))
#             for i, opt in enumerate(state["shopOptions"]):
#                 cardRect = pygame.Rect(30 + i * 135, 170, 125, 180)
#                 color = (40, 40, 50) if not opt["sold"] else (20, 20, 20)
#                 pygame.draw.rect(tempSurf, color, cardRect, border_radius=10)
#                 if not opt["sold"]:
#                     tempSurf.blit(assets.fonts['small'].render(opt['data']['name'][:8], True, WHITE), (cardRect.x+10, cardRect.y+15))
#                     tempSurf.blit(assets.fonts['small'].render(f"{opt['data']['price']}G", True, GOLD), (cardRect.x+10, cardRect.y+150))
#         elif state["shopTab"] == "BANK":
#             # 은행 전용 인터페이스 추가
#             tempSurf.blit(assets.fonts['medium'].render("GALACTIC BANK", True, GOLD), (30, 120))
#             # 은행 잔고 및 조작 안내
#             bank_info = f"은행 잔고: {state['bankBalance']}G"
#             tempSurf.blit(assets.fonts['medium'].render(bank_info, True, WHITE), (60, 180))
#             tempSurf.blit(assets.fonts['small'].render("[A] 100G 예금 | [D] 100G 출금", True, CYAN), (60, 230))
#             tempSurf.blit(assets.fonts['small'].render("이자는 라운드 종료 시 15% 지급됩니다.", True, GREEN), (60, 270))
            
#         # [좌측 하단: 시너지 이원화 표시]
#         pygame.draw.line(tempSurf, GRAY, (20, 350), (CENTER_X - 20, 350), 2)
#         # 왼쪽 칸: 보유 현황
#         tempSurf.blit(assets.fonts['small'].render("[ 보유 시너지 ]", True, GOLD), (30, 365))
#         # 오른쪽 칸: 발동 효과
#         tempSurf.blit(assets.fonts['small'].render("[ 발동 효과 ]", True, GREEN), (CENTER_X // 2 + 30, 365))
        
#         synergy_counts = {}
#         for item in state["inventory"]:
#             for tag in item["tags"]:
#                 synergy_counts[tag] = synergy_counts.get(tag, 0) + 1
        
#         y_pos = 400
#         for tag, count in synergy_counts.items():
#             # 왼쪽 출력 (보유 태그 개수)
#             tempSurf.blit(assets.fonts['small'].render(f"{tag}: {count}개", True, WHITE), (30, y_pos))
            
#             # 오른쪽 출력 (발동된 효과)
#             if tag in SYNERGY_DATA:
#                 valid_effects = [
#                     (req, data) for req, data in SYNERGY_DATA[tag].items()
#                     if count >= req
#                 ]
#                 if valid_effects:
#                     req, data = max(valid_effects, key=lambda x: x[0])  # 최고 단계만 출력
#                     eff_txt = f"{data['name']}"
#                     tempSurf.blit(assets.fonts['small'].render(eff_txt, True, CYAN), (CENTER_X // 2 + 30, y_pos))
#             y_pos += 25

#         # --- [우측 영역: 인벤토리 9칸 (450 ~ 900px)] ---
#         tempSurf.blit(assets.fonts['medium'].render("INVENTORY", True, WHITE), (CENTER_X + 40, 120))
#         for i in range(9):
#             row, col = i // 3, i % 3
#             slotRect = pygame.Rect(CENTER_X + 50 + col * 110, 160 + row * 110, 100, 100)
#             pygame.draw.rect(tempSurf, (25, 25, 35), slotRect, border_radius=5)
#             pygame.draw.rect(tempSurf, GRAY, slotRect, 2, border_radius=5)
            
#             if i < len(state["inventory"]):
#                 # 아이템 장착 시 표시
#                 item_txt = assets.fonts['small'].render(state["inventory"][i]["name"][:6], True, CYAN)
#                 tempSurf.blit(item_txt, (slotRect.x + 10, slotRect.y + 40))

#         if state["shopSubState"] == "CONFIRM_REPLACE":
#             # 화면 중앙 팝업창 배경
#             popup_rect = pygame.Rect(300, HEIGHT//2 - 50, 300, 160)
#             pygame.draw.rect(tempSurf, (40, 40, 50), popup_rect, border_radius=10)
#             pygame.draw.rect(tempSurf, GOLD, popup_rect, 2, border_radius=10)
            
#             # 안내 문구
#             tempSurf.blit(assets.fonts['small'].render("인벤토리가 꽉 찼습니다.", True, WHITE), (355, HEIGHT//2 - 30))
#             tempSurf.blit(assets.fonts['small'].render("기존 아이템을 버리고 장착하시겠습니까?", True, GOLD), (315, HEIGHT//2 - 5))
            
#             # YES 버튼 (x=330, y=HEIGHT//2+50)
#             pygame.draw.rect(tempSurf, GREEN, (330, HEIGHT//2 + 50, 100, 40), border_radius=5)
#             tempSurf.blit(assets.fonts['medium'].render("YES", True, BLACK), (355, HEIGHT//2 + 55))
            
#             # NO 버튼 (x=470, y=HEIGHT//2+50)
#             pygame.draw.rect(tempSurf, RED, (470, HEIGHT//2 + 50, 100, 40), border_radius=5)
#             tempSurf.blit(assets.fonts['medium'].render("NO", True, WHITE), (500, HEIGHT//2 + 55))
            
#         elif state["shopSubState"] == "SELECT_REMOVE":
#             # 인벤토리 영역 위에 붉은색 경고/안내 문구 표시
#             tempSurf.blit(assets.fonts['medium'].render("버릴 아이템을 클릭하세요!", True, RED), (CENTER_X + 50, 90))
#         # 스탯 렌더링
#         stat_text = f"DMG: {stats['damage']} | SPD: {stats['speed']} | MAX_HP: {stats['maxHp']} | 관통: {'ON' if stats['pierce'] else 'OFF'} | W: {stats['specialAmmo']}"
#         tempSurf.blit(assets.fonts['small'].render(stat_text, True, WHITE), (300, HEIGHT - 30))

#     # 1. 가장 밑바닥에 배경 먼저 그리기
#     screen.blit(assets.images['background'], (0, 0))
#     screen.blit(tempSurf, (0, 0))
        
#     # W 특수기 효과
#     if state["specialEffectTimer"] > 0:
#         # 1. 화면 전체를 어둡게 (섬광 대신 몰입감)
#         overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
#         overlay.fill((0, 0, 0, 100))
#         screen.blit(overlay, (0, 0))
        
#         # 2. 개성 있는 '절단선' 이펙트 (화면을 가로지르는 날카로운 선)
#         line_y = HEIGHT // 2
#         line_width = state["specialEffectTimer"] * 2 # 시간이 갈수록 얇아짐
#         pygame.draw.line(screen, CYAN, (0, line_y), (WIDTH, line_y), line_width)
#         pygame.draw.line(screen, WHITE, (0, line_y), (WIDTH, line_y), max(1, line_width // 3))
        
#         state["specialEffectTimer"] -= 1
    
#     # 4. 전투 시에만 보이는 UI
#     if state["gameState"] != 'SHOP':
#         pygame.draw.rect(screen, GREEN, (10, 10, max(0, (state['playerHp']/stats['maxHp'])*200), 20))    
#         screen.blit(assets.fonts['small'].render(f"{int(state['playerHp'])} / {stats['maxHp']}", True, BLACK), (80, 10))
        
#         # 정보 텍스트 (점수, 최고점수, 스테이지 정보 그룹화)
#         infoTxt1 = assets.fonts['small'].render(f"SCORE: {state['score']} | HI-SCORE: {state['highScore']} | STAGE: {state['currentStage']}", True, WHITE)
#         screen.blit(infoTxt1, (10, 35))
        
#         # 재화 및 특수기 개수 표기 (눈에 띄도록 골드 색상 강조)
#         infoTxt2 = assets.fonts['small'].render(f"GOLD: {stats['gold']} G | SPECIAL (W): {stats['specialAmmo']} 개", True, GOLD)
#         screen.blit(infoTxt2, (10, 55))
        
#         # 제로 티켓 활성화 상태 
#         if state['zeroTicket']: 
#             screen.blit(assets.fonts['small'].render("★ ZERO TICKET ACTIVE ★", True, CYAN), (10, 75))
            
#     # UI 업데이트 및 프레임 제한
#     pygame.display.flip()
# pygame.quit()