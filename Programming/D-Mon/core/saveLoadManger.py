# core/saveLoadManager.py
import json
import os

class SaveLoadManager:
    def __init__(self, savePath: str = "saveData.json"):
        self.savePath = savePath

    def loadData(self) -> dict:
        """저장된 데이터를 불러옵니다. 실패 시 Fallback 로직을 실행합니다."""
        if not os.path.exists(self.savePath):
            return self._getDefaultData()
            
        try:
            with open(self.savePath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError, Exception) as e:
            # 예외 발생 시 게임이 멈추지 않고 초기 데이터로 안전 복구
            print(f"Data load failed, recovering with default data. Error: {e}")
            return self._getDefaultData()

    def saveData(self, data: dict) -> bool:
        """현재 상태를 JSON으로 저장합니다."""
        try:
            with open(self.savePath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Data save failed. Error: {e}")
            return False

    def _getDefaultData(self) -> dict:
        return {
            "partnerName": "Koromon",
            "level": 1,
            "currentExp": 0.0,
            "affinity": 0,
            "buffMultiplier": 1.0
        }