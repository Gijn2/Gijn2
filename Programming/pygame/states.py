import pygame
import json

from constants import *
from entities import *
from utils import *
from main import GameContext

class GameState:
    def __init__(self, ctx: GameContext):
        self.ctx = ctx
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
    

class GameContext:
    """게임 전역 데이터 공유 객체"""
    def __init__(self):
        self.data = loadGameData()
        self.stats = {"damage": 10, "speed": 5, "gold": 1000, "maxHp": 100, "pierce": False, "specialAmmo": 3}
        self.playerHp = 100
        self.score = 0
        self.highScore = 0
        self.currentStage = 1
        self.bankBalance = 0
        self.stocks = {"A": 100, "B": 100, "C": 100}
        
    def getDiscountRatio(self):
        ratio = 2.0 - (self.stocks["C"] / 100.0)
        return max(0.5, min(2.0, ratio))

class GameState:
    def __init__(self, ctx: GameContext):
        self.ctx = ctx
    def handleEvents(self, events): pass
    def update(self): pass
    def draw(self, screen): pass

class ShopState(GameState):
    def __init__(self, ctx: GameContext):
        super().__init__(ctx)
        self.shopTab = "ITEM"
        self.fontM = pygame.font.SysFont("malgungothic", 24)
        pool = self.ctx.data.get("upgradePool", [])
        self.shopOptions = [{"data": item, "sold": False} for item in random.sample(pool, min(4, len(pool)))]

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.ctx.bankBalance = int(self.ctx.bankBalance * 1.1)
                self.ctx.currentStage += 1
                from states import PlayingState # 지연 임포트
                return PlayingState(self.ctx)
        return None

    def update(self): pass

    def draw(self, screen):
        screen.fill((20, 20, 30))
        # 상점 UI 렌더링 코드 (기존 shopTab 로직 간소화 적용)
        txt = self.fontM.render(f"SHOP MODE - Press 'S' to next stage | GOLD: {self.ctx.stats['gold']}", True, WHITE)
        screen.blit(txt, (50, 50))

class PlayingState(GameState):
    def __init__(self, ctx: GameContext):
        super().__init__(ctx)
        self.playerPos = pygame.Vector2(WIDTH//2, HEIGHT-80)
        self.pProjs, self.eProjs, self.enemies, self.particles = [], [], [], []
        self.boss = None
        self.stageTimer = 50
        self.shootCooldown = 0
        self.tempSurf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    def handleEvents(self, events):
        # 플레이어 사망 시 상점이나 메인으로 전환 판정
        if self.ctx.playerHp <= 0:
            if self.ctx.score > self.ctx.highScore:
                saveHighscoreSecure(self.ctx.score)
            # 게임 오버 화면 혹은 종료 처리
        return None

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.playerPos.x -= self.ctx.stats["speed"]
        if keys[pygame.K_RIGHT]: self.playerPos.x += self.ctx.stats["speed"]
        if keys[pygame.K_q] and self.shootCooldown <= 0:
            self.pProjs.append(Projectile(self.playerPos.x+20, self.playerPos.y, pygame.Vector2(0,-10), GREEN, self.ctx.stats["damage"]))
            self.shootCooldown = 10
        self.shootCooldown = max(0, self.shootCooldown - 1)

        # 투사체 업데이트 및 보스 로직 (기존 while 루프 내 내용 유지)
        for p in self.pProjs[:]:
            p.update()
            
        if not self.boss:
            self.stageTimer -= 1
            if self.stageTimer <= 0:
                self.boss = BossChernobog() # 테스트용 보스 소환

        if self.boss:
            self.boss.update(self.eProjs, self.playerPos, self.ctx)
            if self.boss.hp <= 0:
                self.ctx.stats["gold"] += 1500
                return ShopState(self.ctx) # 보스 격파 시 상점으로 전이

        return None # 전이 없음

    def draw(self, screen):
        self.tempSurf.fill((0, 0, 0, 0))
        pygame.draw.circle(self.tempSurf, CYAN, self.playerPos + pygame.Vector2(30, 30), 10, 2)
        
        for p in self.pProjs: p.draw(self.tempSurf)
        if self.boss: self.boss.draw(self.tempSurf)
            
        screen.blit(self.tempSurf, (0, 0))