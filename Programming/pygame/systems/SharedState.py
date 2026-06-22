# 전역에서 공유할 게임 상태 딕셔너리
from constants import baseStats

state = {
    "playerHp": 125,
    "shakeTimer": 0,
    "invincibleTimer": 0,
    "zeroTicket": False,
    "bossAlertTimer": 0,
    "currentStage": 1,
    "freeRefreshAvailable": False,
    "gameState": 'PLAYING',
    
    "hitboxRadius": 10,   
    "particles": [],
    "pendingItem": None,
    "screenShakeTimer": 0,
    "shootCooldown": 0,
    "specialEffectTimer": 0,
    "regenCounter": 0,
    # 상점 관련 상태
    "bankBalance": 0,
    "inventory": [],
    "shopTab": "MARKET",
    "shopOptions": [],
    "shopRefreshCount": 0,
    "shopSubState": "NORMAL",
    # 점수, 콤보 관련 상태
    "score": 0,
    "combo": 0,
    "comboTimer": 0,
    "highScoreItems": [],
    "highScore": 0,
    "unlockedStories": [],
    # 슬롯에 등록된 무기 리스트와 현재 장착 중인 무기 인덱스
    "weapons": [
        {"name": "기본 빔", "color": (50, 255, 50), "dmg": 0, "cooldown": 15, "speed": 10, "isHoming": False},
        {"name": "유도 로켓", "color": (0, 255, 255), "dmg": -5, "cooldown": 25, "speed": 8, "isHoming": True}
    ],
    "currentWeaponIdx": 0,
}

stats = baseStats.copy()
stats['gold'] = 1000