# 이미지, 사운드, 폰트 로드 및 캐싱 (싱글톤 패턴 추천)

import pygame
import os
from constants import MAX_ENEMY_TYPES

# --- 경로 설정 ---
IMGS_PATH = os.path.join(os.path.dirname(__file__), "imgs")

class AssetManager:
    def __init__(self):
        self.imgsPath = os.path.join(os.path.dirname(__file__), "imgs")
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        self.enemyImgs = {}

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
                self.enemyImgs[typeKey] = self.enemyImgs.get("type_1", None)

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

        # 3. 폰트 로드
        try:
            self.fonts['small'] = pygame.font.SysFont("malgungothic", 16)
            self.fonts['medium'] = pygame.font.SysFont("malgungothic", 24)
            self.fonts['large'] = pygame.font.SysFont("malgungothic", 40)
        except Exception:
            self.fonts['small'] = pygame.font.Font(None, 20)
            self.fonts['medium'] = pygame.font.Font(None, 32)
            self.fonts['large'] = pygame.font.Font(None, 50)

# 싱글톤 인스턴스 생성
assets = AssetManager()