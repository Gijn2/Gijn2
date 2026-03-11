import json
import hashlib
import os
import random
from constants import *


def getRandomEnemy(current_stage):
    available = [e for e in ENEMY_SPAWN_POOL if current_stage >= e["minStage"]]
    if not available: return "type1"
    types = [e["type"] for e in available]
    weights = [e["weight"] for e in available]
    return random.choices(types, weights=weights)[0]

# 지분에 따른 할인율 계산 함수
def getDiscountRatio():
    ratio = 2.0 - (stocks["C"] / 100.0) #(C구역: 정밀 합금 기업이 물가 담당)
    return max(0.5, min(2.0, ratio))

def loadHighscore():
    if os.path.exists("highscore.txt"):
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read())
        except Exception:
            return 0
    return 0

highScore = loadHighscore()

# --- [신규] 보안 및 다국어 시스템 ---
def saveGameSecure(data, filename="save.dat"):
    data_str = json.dumps(data, sort_keys=True)
    signature = hashlib.sha256((data_str + secretSalt).encode()).hexdigest()
    with open(filename, "w") as f:
        json.dump({"payload": data, "signature": signature}, f)

LANG_DB = {
    "ko": {"shop_title": "시스템 업그레이드", "core_warn": "코어 감지됨", "start": "전투 개시"},
    "en": {"shop_title": "SYSTEM UPGRADE", "core_warn": "CORE DETECTED", "start": "START BATTLE"}
}
current_lang = "ko"
def _t(key): return LANG_DB[current_lang].get(key, key)

# 해킹을 막기 위한 함수
def saveHighscoreSecure(scoreValue):
    # 점수와 비밀키를 합쳐 해시값(Checksum) 생성
    dataStr = str(scoreValue) + secretSalt
    checksum = hashlib.sha256(dataStr.encode()).hexdigest()
    
    with open("highscore.dat", "w") as f:
        # 점수와 해시값을 같이 저장
        f.write(f"{scoreValue}\n{checksum}")

def loadHighscoreSecure():
    if os.path.exists("highscore.dat"):
        try:
            with open("highscore.dat", "r") as f:
                lines = f.readlines()
                scoreValue = int(lines[0].strip())
                savedChecksum = lines[1].strip()
                
                # 파일을 읽을 때 동일한 공식으로 해시를 재계산하여 검증
                calcChecksum = hashlib.sha256((str(scoreValue) + secretSalt).encode()).hexdigest()
                
                if savedChecksum == calcChecksum:
                    return scoreValue
                else:
                    print("점수 조작이 감지되었습니다.")
                    return 0 # 조작 감지 시 0점으로 초기화
        except Exception:
            return 0
    return 0

def saveHighscore(s):
    try:
        with open("highscore.txt", "w") as f:
            f.write(str(s))
    except Exception: pass

def getShopItems():
    return [{"data": item, "sold": False} for item in random.sample(UPGRADE_POOL, 4)]

def applyUpgrade(itemData):
    global playerHp, boss
    eff = itemData['effect']
    if eff == "dmg": stats["damage"] += 1.5
    elif eff == "speed": stats["speed"] += 2
    elif eff == "heal": playerHp = min(stats["maxHp"], playerHp + 50)
    elif eff == "pierce": stats["pierce"] = True
    elif eff == "maxhp": stats["maxHp"] += 40; playerHp += 40
    elif eff == "ammo": stats["specialAmmo"] += 2

def saveHighscoreSecure(score, filename="save.dat"):
    data = {"highScore": score}
    dataStr = json.dumps(data, sort_keys=True)
    signature = hashlib.sha256((dataStr + SECRET_SALT).encode()).hexdigest()
    
    with open(filename, "w") as f:
        json.dump({"payload": data, "signature": signature}, f)

def loadHighscoreSecure(filename="save.dat"):
    if not os.path.exists(filename): return 0
    try:
        with open(filename, "r") as f:
            content = json.load(f)
            payload = content["payload"]
            signature = content["signature"]
            # 검증
            checkStr = json.dumps(payload, sort_keys=True)
            expected = hashlib.sha256((checkStr + SECRET_SALT).encode()).hexdigest()
            if signature == expected:
                return payload.get("highScore", 0)
    except:
        return 0
    return 0

def loadGameConfig():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)