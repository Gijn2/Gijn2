# core/idleCalculator.py

class IdleCalculator:
    @staticmethod
    def calculateTickExp(baseExp: float, buffMultiplier: float = 1.0) -> float:
        """1 틱당 획득할 경험치를 계산합니다."""
        return baseExp * buffMultiplier

    @staticmethod
    def checkLevelUp(currentExp: float, currentLevel: int) -> tuple[bool, int, float]:
        """
        경험치가 요구량(E_base * L^1.5)을 충족했는지 검사합니다.
        Returns: (레벨업 여부, 새 레벨, 차감 후 남은 경험치)
        """
        baseReqExp = 100.0
        reqExp = baseReqExp * (currentLevel ** 1.5)
        
        if currentExp >= reqExp:
            newLevel = currentLevel + 1
            remainingExp = currentExp - reqExp
            return True, newLevel, remainingExp
            
        return False, currentLevel, currentExp