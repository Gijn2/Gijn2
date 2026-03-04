import json
import hashlib
import os
from constants import SECRET_SALT

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