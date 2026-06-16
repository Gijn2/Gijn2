import os
import hashlib
import json
from constants import SECRET_SALT
from systems.SharedState import state

def saveGameDataSecure():
    """최고기록, 당시 아이템 목록, 해금된 스토리 진행 상황을 묶어서 암호화 저장합니다."""
    # 1. 저장할 데이터 구조화
    save_data = {
        "highScore": state["highScore"],
        "highScoreItems": state["highScoreItems"],
        "unlockedStories": state["unlockedStories"]
    }
    # 2. JSON 문자열로 직렬화
    data_str = json.dumps(save_data, ensure_ascii=False)
    
    # 3. 데이터 변조 방지용 체크섬 생성
    checksum = hashlib.sha256((data_str + SECRET_SALT).encode('utf-8')).hexdigest()
    
    # 4. 파일에 기록
    with open("gamedata.dat", "w", encoding="utf-8") as f:
        f.write(f"{data_str}\n{checksum}")

def loadGameDataSecure():
    """보안 데이터 파일을 불러와 검증 후 게임 상태에 적용합니다."""
    try:
        if not os.path.exists("gamedata.dat"): 
            return
        with open("gamedata.dat", "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            if len(lines) < 2: return
            
            data_str = lines[0]
            saved_checksum = lines[1]
            
            # 체크섬 검증
            calc_checksum = hashlib.sha256((data_str + SECRET_SALT).encode('utf-8')).hexdigest()
            if saved_checksum == calc_checksum:
                loaded_data = json.loads(data_str)
                state["highScore"] = loaded_data.get("highScore", 0)
                state["highScoreItems"] = loaded_data.get("highScoreItems", [])
                state["unlockedStories"] = loaded_data.get("unlockedStories", ["intro"])
            else:
                print("⚠️ 경고: 세이브 파일이 변조되었거나 훼손되어 불러올 수 없습니다.")
    except Exception as e:
        print(f"데이터 파일 로드 오류: {e}")