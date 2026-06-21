# 전역에서 공유할 게임 상태 딕셔너리
from constants import baseStats

state = {
    "playerHp": 125,
    "shakeTimer": 0,
    "invincibleTimer": 0,
    "score": 0,
    "zeroTicket": False,
    
    "bankBalance": 0,
    "inventory": [],
    "shopTab": "MARKET",
    "shopOptions": [],
    "shopRefreshCount": 0,
    "shopSubState": "NORMAL",

    "bossAlertTimer": 0,
    "currentStage": 1,
    "freeRefreshAvailable": False,
    "gameState": 'PLAYING',
    "highScore": 0, # 추후 loadHighscoreSecure() 사용   
    "hitboxRadius": 10,   
    "particles": [],
    "pendingItem": None,
    "screenShakeTimer": 0,
    "shootCooldown": 0,
    "specialEffectTimer": 0,
    "regenCounter": 0,
    "combo": 0,
    "comboTimer": 0,
    "highScoreItems": [],
    "unlockedStories": [],
}

stats = baseStats.copy()
stats['gold'] = 1000