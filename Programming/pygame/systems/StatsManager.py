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
            for req, data in sorted(SYNERGY_DATA[tag].items()):
                if count >= req:
                    for k, v in data["effect"].items():
                        if type(v) == bool:
                            stats[k] = v
                        else:
                            stats[k] += v

    if state["playerHp"] > stats["maxHp"]:
        state["playerHp"] = stats["maxHp"]