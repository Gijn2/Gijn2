# 상점 생성, 새로고침, 구매 로직 (refresh_shop 등)

import random
from constants import ITEM_POOL
from systems.SharedState import state, stats 

def refreshShop():
    equipped_ids = [item['id'] for item in state["inventory"]]
    
    available_pool = [
        item for item in ITEM_POOL 
        if item['id'] not in equipped_ids or item.get('type') == 'CONSUMABLE'
    ]
    
    selected = random.sample(available_pool, min(3, len(available_pool)))
    
    shopOptions = []
    for item in selected:
        shopOptions.append({"data": item, "sold": False})
        
    state["shopOptions"] = shopOptions
    pass

# 스테이지 클리어 시 이자 계산
def applyInterest():
    # stats["gold"] 대신 state["bankBalance"]를 기준으로 변경
    current_bank = state.get("bankBalance", 0)
    if current_bank > 0:
        interest = int(current_bank * 0.15)
        MAX_INTEREST = 50 
        interest = min(interest, MAX_INTEREST)

        # 이자를 은행 잔고에 추가할지, 소지금에 바로 줄지 선택하여 반영
        state["bankBalance"] += interest  # 은행 잔고에 이자 누적 예시
