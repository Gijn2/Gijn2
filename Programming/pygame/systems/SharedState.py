# 전역에서 공유할 게임 상태 딕셔너리
from constants import baseStats

state = {
    "playerHp": 125,
    "shakeTimer": 0,
    "invincibleTimer": 0,
    "score": 0,
    "zeroTicket": False
}

stats = baseStats.copy()
stats['gold'] = 1000