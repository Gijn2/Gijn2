# 이미지, 사운드, 폰트 로드 및 캐싱 (싱글톤 패턴 추천)

import pygame
import os
from constants import MAX_ENEMY_TYPES

# --- 에셋 로드 ---
secretSalt = "MyPyGameTest2026"

# --- 경로 설정 ---
IMGS_PATH = os.path.join(os.path.dirname(__file__), "imgs")

class AssetManager:
    def __init__(self):
        self.imgsPath = os.path.join(os.path.dirname(__file__), "imgs")
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        self.enemyImgs = {}
        self.itemImgs = {}
        self.bossAttackImgs = {}

    def loadAllAssets(self):
        # 1. 이미지 로드
        try:
            self.images['background'] = pygame.image.load(os.path.join(self.imgsPath, "background.png")).convert()
            playerImg = pygame.image.load(os.path.join(self.imgsPath, "player.png")).convert_alpha()
            self.images['player'] = pygame.transform.scale(playerImg, (60, 60))
        except FileNotFoundError as e:
            print(f"기본 이미지 로드 실패: {e}")

        # 적 이미지 로드 (반복문 분리)
        for i in range(1, MAX_ENEMY_TYPES + 1):
            typeKey = f"type_{i}"
            try:
                self.enemyImgs[typeKey] = {
                    "STAND": pygame.transform.scale(pygame.image.load(os.path.join(self.imgsPath, f"normalEnemy_{i}_stand.png")).convert_alpha(), (50, 50)),
                    "ATTACK": pygame.transform.scale(pygame.image.load(os.path.join(self.imgsPath, f"normalEnemy_{i}_attack.png")).convert_alpha(), (50, 50)),
                }
            except FileNotFoundError:
                # 1번 타입 이미지가 이미 안전하게 로드되어 있다면 그것으로 대체
                if "type_1" in self.enemyImgs and self.enemyImgs["type_1"] is not None:
                    self.enemyImgs[typeKey] = self.enemyImgs["type_1"]
                else:
                    # 1번 이미지마저 없다면 튕기지 않도록 에러 예방용 임시 색상 상자 생성
                    fallback_stand = pygame.Surface((50, 50))
                    fallback_stand.fill((255, 50, 50))    # 빨간 사각형
                    fallback_attack = pygame.Surface((50, 50))
                    fallback_attack.fill((255, 150, 50))  # 주황 사각형
                    self.enemyImgs[typeKey] = {"STAND": fallback_stand, "ATTACK": fallback_attack}
                    
        # 메테오 이미지 예외 처리
        try:
            meteorImg = pygame.image.load(os.path.join(self.imgsPath, "meteor.png")).convert_alpha()
            self.images['meteor'] = pygame.transform.scale(meteorImg, (60, 60))
        except FileNotFoundError:
            meteorImg = pygame.Surface((60, 60), pygame.SRCALPHA)
            pygame.draw.circle(meteorImg, (100, 100, 100), (30, 30), 30)
            self.images['meteor'] = meteorImg

        # 2. 사운드 로드
        try:
            self.sounds['hit'] = pygame.mixer.Sound(os.path.join(self.imgsPath, "hit.wav"))
            self.sounds['explosion'] = pygame.mixer.Sound(os.path.join(self.imgsPath, "explosion.wav"))
        except Exception as e:
            print(f"사운드 파일 로드 실패: {e}")
            self.sounds['hit'] = None
            self.sounds['explosion'] = None

        # 3. 폰트 로드 (Windows, Mac, Linux 호환성을 위한 한글 폰트 우선순위 리스트 설정)
        ko_fonts = ["malgungothic", "applesgothic", "nanumgothic", "notosanscjkkr", "sans"]
        try:
            self.fonts['small'] = pygame.font.SysFont(ko_fonts, 16)
            self.fonts['medium'] = pygame.font.SysFont(ko_fonts, 24)
            self.fonts['large'] = pygame.font.SysFont(ko_fonts, 40)
        except Exception:
            self.fonts['small'] = pygame.font.Font(None, 20)
            self.fonts['medium'] = pygame.font.Font(None, 32)
            self.fonts['large'] = pygame.font.Font(None, 50)
            
# 싱글톤 인스턴스 생성
assets = AssetManager()