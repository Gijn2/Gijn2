# 투사체 및 엔티티 간의 충돌 판정 분리
from main import playerHp, shakeTimer, invincibleTimer, stats
from entities.Bosses import *



def take_damage(amount, shake, invinc):
    global playerHp, shakeTimer, invincibleTimer
    invinc_frames = invinc + stats.get("invincibility_bonus", 0)
    
    if invincibleTimer <= 0:
        playerHp -= amount
        shakeTimer = max(shakeTimer, shake)
        invincibleTimer = invinc_frames
        
        # 나노 프로그래머블 시너지: 피격 시 적에게 반사 폭발 데미지
        if stats.get("nano_explosion", False):
            # pProjs 리스트에 전방향 파편 투사체 생성 로직 추가 (추후 메인 루프 연동 필요)
            pass 
        return True
    return False