# 투사체 및 엔티티 간의 충돌 판정 분리
from systems.SharedState import state, stats

def take_damage(amount, shake, invinc):
    invinc_frames = invinc + stats.get("invincibility_bonus", 0)
    
    if state["invincibleTimer"] <= 0:
        state["playerHp"] -= amount
        state["shakeTimer"] = max(state["shakeTimer"], shake)
        state["invincibleTimer"] = invinc_frames
        
        if stats.get("nano_explosion", False):
            pass 
        return True
    return False