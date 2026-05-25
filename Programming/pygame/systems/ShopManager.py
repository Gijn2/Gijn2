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
    current_gold = stats.get("gold", 0)
    if current_gold > 0:
        # 2. 보유 골드의 15%를 이자로 계산
        interest = int(current_gold * 0.15)
        
        # 3. 게임 밸런스 붕괴 방지를 위한 최대 이자 제한 (예: 최대 50G)
        # (이 값은 필요에 따라 constants.py로 분리하여 관리하면 유지보수에 좋습니다.)
        MAX_INTEREST = 50 
        interest = min(interest, MAX_INTEREST)
        
        # 4. 플레이어의 골드에 이자 추가
        stats["gold"] += interest
