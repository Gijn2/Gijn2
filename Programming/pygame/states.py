import pygame
import json
import hashlib

from constants import *
from entities import *

class GameState:
    def handleEvents(self, events): pass
    def update(self): pass
    def draw(self, surface): pass

class PlayingState(GameState):
    # 기존 PLAYING 관련 입력, 업데이트, 렌더링 로직 이동
    pass

class ShopState(GameState):
    # 기존 SHOP 관련 상점 UI 로직 이동
    pass

class MainMenuState(GameState):
    def update(self):
        pass
        
    def draw(self, surf):
        titleText = fontL.render("Topdown Shooting: Limited Edition", True, WHITE)
        startText = fontM.render("Press ENTER to Start | 'L' to Load", True, CYAN)
        surf.blit(titleText, (WIDTH//2 - 200, HEIGHT//2 - 50))
        surf.blit(startText, (WIDTH//2 - 150, HEIGHT//2 + 20))
        
    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return PlayingState() # 게임 시작
                elif event.key == pygame.K_l:
                    # 세이브 파일 로드 로직
                    try:
                        with open("save.dat", "r") as f:
                            savedData = json.load(f)
                            # stats 등에 데이터 덮어씌우기
                    except Exception:
                        pass
        return None