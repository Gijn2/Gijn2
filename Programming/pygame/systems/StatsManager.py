# 시너지 계산 및 스탯 재계산 로직 (calculateStats)
from constants import baseStats, SYNERGY_DATA
from systems.SharedState import state, stats

def calculateStats():
    global stats
    current_gold = stats.get("gold", 0)
    
    stats.clear()
    stats.update(baseStats)
    stats["gold"] = current_gold
    
    synergy_counts = {}
    active_tags = []
    for item in state["inventory"]:
        for tag in item.get('tags', []):
            active_tags.append(tag)
            synergy_counts[tag] = synergy_counts.get(tag, 0) + 1
        
    for tag, count in synergy_counts.items():
            if tag in SYNERGY_DATA:
                # 현재 활성화 조건 조건을 만족하는 req(개수) 목록 필터링
                valid_reqs = [req for req in SYNERGY_DATA[tag].keys() if count >= req]
                if valid_reqs:
                    # 활성화된 단계 중 가장 높은 단계(가장 큰 값)의 데이터만 추출
                    max_req = max(valid_reqs)
                    data = SYNERGY_DATA[tag][max_req]
                    
                    for k, v in data["effect"].items():
                        if type(v) == bool:
                            stats[k] = v
                        else:
                            stats[k] += v

    if state["playerHp"] > stats["maxHp"]:
        state["playerHp"] = stats["maxHp"]