# loadHighscoreSecure, saveHighscoreSecure (try-catch 포함)
import os
import hashlib
from constants import SECRET_SALT


def loadHighscore():
    if os.path.exists("highscore.txt"):
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read())
        except Exception:
            return 0
    return 0
highScore = loadHighscore()

def saveHighscoreSecure(scoreValue):
    # 점수와 비밀키를 합쳐 해시값(Checksum) 생성
    dataStr = str(scoreValue) + SECRET_SALT
    checksum = hashlib.sha256(dataStr.encode()).hexdigest()
    
    with open("highscore.dat", "w") as f:
        # 점수와 해시값을 같이 저장
        f.write(f"{scoreValue}\n{checksum}")

def loadHighscoreSecure():
    try:
        if not os.path.exists("highscore.dat"): return 0
        with open("highscore.dat", "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            if len(lines) < 2: return 0
            scoreValue = int(lines[0].strip())
            savedChecksum = lines[1].strip()
            calcChecksum = hashlib.sha256((str(scoreValue) + SECRET_SALT).encode()).hexdigest()
                
            if savedChecksum == calcChecksum:
                return scoreValue
            else:
                print("점수 조작이 감지되었습니다.")
                return 0 # 조작 감지 시 0점으로 초기화
    except (IOError, ValueError, IndexError):
        return 0
    return 0
