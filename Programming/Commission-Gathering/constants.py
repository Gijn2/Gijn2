import pygame
import os

# 화면 설정
WIDTH, HEIGHT = 900, 600
FPS = 60

# 색상 정의 (상수는 대문자)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
CYAN = (0, 255, 255)
PURPLE = (160, 32, 240)

# 보안 키
SECRET_SALT = "MyPyGameTest2026"

# 경로 설정
BASE_PATH = os.path.dirname(__file__)
IMGS_PATH = os.path.join(BASE_PATH, "imgs")

try:
    fontS = pygame.font.SysFont("malgungothic", 16)
    fontM = pygame.font.SysFont("malgungothic", 24)
    fontL = pygame.font.SysFont("malgungothic", 40)
except:
    fontS = pygame.font.Font(None, 20)
    fontM = pygame.font.Font(None, 32)
    fontL = pygame.font.Font(None, 50)