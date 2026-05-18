# 상점 생성, 새로고침, 구매 로직 (refresh_shop 등)

import random
from constants import ITEM_POOL
from systems.SharedState import state, stats 

def refresh_shop():
    
    # 1. 현재 인벤토리에 있는 아이템 ID 목록 추출
    equipped_ids = [item['id'] for item in state["inventory"]]
    
    # 2. 인벤토리에 없는 아이템만 후보군으로 필터링
    available_pool = [
        item for item in ITEM_POOL 
        if item['id'] not in equipped_ids or item.get('type') == 'CONSUMABLE'
    ]
    
    # 3. 랜덤으로 3개 선택 (후보가 3개보다 적으면 전체 선택)
    selected = random.sample(available_pool, min(3, len(available_pool)))
    
    # 4. 상점 옵션 객체 생성
    shopOptions = []
    for item in selected:
        shopOptions.append({"data": item, "sold": False})
        
# 스테이지 클리어 시 이자 계산
def apply_interest():
    pass
    # if state["bankBalance"] > 0:
    #     interest = int(state["bankBalance"] * 0.15)
    #     stats["gold"] += interest
