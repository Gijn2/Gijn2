# 시너지 계산 및 스탯 재계산 로직 (calculateStats)
from constants import baseStats, SYNERGY_DATA
from systems.SharedState import state, stats

SYNERGY_DATA = {
    "WEAPON": {
        2: {"name": "무기(2): 데미지 +5", "effect": {"damage": 5}},
        4: {"name": "무기(4): 데미지 +10, 관통", "effect": {"damage": 10, "pierce": True}},
        6: {"name": "무기(6): 데미지 +20, 관통", "effect": {"damage": 20, "pierce": True}},
        8: {"name": "무기(8): 데미지 +30, 관통", "effect": {"damage": 30, "pierce": True}},
    },
    "TECH": {
        3: {"name": "기술(2): 이동속도 +3", "effect": {"speed": 3}},
        5: {"name": "기술(4): 특수기 +3", "effect": {"specialAmmo": 3}},
        7: {"name": "기술(6): 이동속도 +5, 특수기 +5", "effect": {"speed": 5, "specialAmmo": 5}}
    },
    "ARMOR": {
        2: {"name": "장갑(2): 최대체력 +50", "effect": {"maxHp": 50}},
        3: {"name": "장갑(4): 최대체력 +100", "effect": {"maxHp": 100}},
        4: {"name": "장갑(6): 최대체력 +200", "effect": {"maxHp": 200}},
        5: {"name": "장갑(8): 최대체력 +400", "effect": {"maxHp": 400}},
    },
    "SPEED": {2: {"name": "속도(2): 이속 +5", "effect": {"speed": 5}}},
    "GOLD": {2: {"name": "황금(2): 스테이지 클리어 보너스 +200", "effect": {}}},
    "LIFE": {2: {"name": "생명(2): 최대체력 +100", "effect": {"maxHp": 100}}},
    "ALLOY": {
        2: {"name": "반응형 합금(2): 피격 시 1초 무적", "effect": {"invincibility_bonus": 30}},
        4: {"name": "나노 프로그래머블(4): 피격 시 주변 폭발", "effect": {"nano_explosion": True}}
    }
}


# 스탯 재계산 로직 (DRY 원칙 적용)
def calculate_stats():
    global stats, playerHp
    current_gold = stats.get("gold", 0)
    
    # 기본 스탯으로 초기화
    stats.clear()
    stats.update(baseStats)
    stats["gold"] = current_gold
    
    # 시너지 태그 카운트
    synergy_counts = {}
    active_tags = []
    for item in state["inventory"]:
        for tag in item.get('tags', []):
            active_tags.append(tag)
            synergy_counts[tag] = synergy_counts.get(tag, 0) + 1

    # 중복을 제거한 고유 태그 목록 생성
    # unique_active_tags = sorted(list(set(active_tags)))
        
    # 시너지 효과 적용
    for tag, count in synergy_counts.items():
        if tag in SYNERGY_DATA:
            for req, data in sorted(SYNERGY_DATA[tag].items()):
                if count >= req:
                    for k, v in data["effect"].items():
                        if type(v) == bool:
                            stats[k] = v
                        else:
                            stats[k] += v

    # 최대 체력 변동에 따른 현재 체력 보정
    if state["playerHp"] > stats["maxHp"]:
        state["playerHp"] = stats["maxHp"]