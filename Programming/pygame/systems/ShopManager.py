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

# 스테이지 클리어 시 이자 계산
def applyInterest():
    if state.get("bankBalance", 0) > 0:
        interest = int(state["bankBalance"] * 0.15)
        stats["gold"] += interest
