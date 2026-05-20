# 하드코딩된 색상, 화면 크기, ITEM_POOL, SYNERGY_DATA 등 상수

# --- 화면 및 기본 설정 ---
WIDTH, HEIGHT = 900, 600
STAGE_DURATION = 50 
SECRET_SALT = "MyPyGameTest2026"
MAX_ENEMY_TYPES = 10

# --- 색상 설정 ---
WHITE  = (255, 255, 255)
RED    = (255, 50, 50)
GOLD   = (255, 215, 0)
BLACK  = (10, 10, 15)
GREEN  = (50, 255, 50)
CYAN   = (0, 255, 255)
PURPLE = (200, 50, 255)
GRAY   = (50, 50, 50)

# --- 기본 스탯 ---
baseStats = {"damage": 10,
             "speed": 5,
             "maxHp": 100,
             "pierce": False,
             "specialAmmo": 3,

             # 2026-05-19 기본 스탯 확장에 특수효과 플래그 추가
            "hp_regen": 0,
            "celest_shield": False,
            "burn_damage": False
            }

# --- 시너지 데이터 ---
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
    },

    # [신규] 진영 (별빛과 재생)
    "GODDESS_FIRE": {
        2: {"name": "화산재(2): 이동 시 화염, 데미지 +5", "effect": {"burn_damage": True, "damage": 5}},
        4: {"name": "용암(4): 관통, 데미지 +15", "effect": {"pierce": True, "damage": 15}}
    },
    
    "WITCH": {
        2: {"name": "별빛(2): 초당 체력 1 재생", "effect": {"hp_regen": 1}},
        4: {"name": "성운(4): 최대체력 +100, 고정 보호막", "effect": {"maxHp": 100, "celest_shield": True}}
    }
}

# --- 아이템 및 적 설정 ---
ITEM_POOL = [
    {"id": "cons_1", "name": "수리 키트", "type": "CONSUMABLE", "price": 300, "desc": "체력 50 회복"},
    {"id": "cons_2", "name": "에너지 셀", "type": "CONSUMABLE", "price": 500, "desc": "특수기 1회 충전"},
    {"id": "w1", "name": "화염 방사기", "tags": ["WEAPON", "TECH", "GODDESS_FIRE"], "price": 500, "desc": "무기, 기술"},
    {"id": "w2", "name": "초합금 검", "tags": ["WEAPON"], "price": 300, "desc": "무기"},
    {"id": "a1", "name": "나노 슈트", "tags": ["TECH", "ARMOR"], "price": 600, "desc": "기술, 장갑"},
    {"id": "a2", "name": "강철 방패", "tags": ["ARMOR"], "price": 400, "desc": "장갑"},
    {"id": "w3", "name": "플라즈마 캐논", "tags": ["WEAPON", "TECH", "GODDESS_FIRE"], "price": 700, "desc": "무기, 기술"},
    {"id": "a3", "name": "반응형 장갑", "tags": ["ARMOR", "WEAPON"], "price": 500, "desc": "장갑, 무기"},
    {"id": "w4", "name": "레일건", "tags": ["WEAPON", "TECH"], "price": 800, "desc": "강력한 단일 데미지"},
    {"id": "s1", "name": "초소형 엔진", "tags": ["TECH", "SPEED"], "price": 400, "desc": "이동속도 대폭 상승"},
    {"id": "g1", "name": "마이다스 코어", "tags": ["MAGIC", "GOLD"], "price": 900, "desc": "적 처치 시 골드 +5"},
    {"id": "l1", "name": "재생의 갑옷", "tags": ["ARMOR", "LIFE", "WITCH"], "price": 700, "desc": "피격 시 10% 확률로 무적"},
    {"id": "m1", "name": "마법 지팡이", "tags": ["MAGIC", "WEAPON", "WITCH"], "price": 550, "desc": "투사체 크기 증가"},
    {"id": "v1", "name": "흡혈귀의 이빨", "tags": ["WEAPON", "LIFE"], "price": 1000, "desc": "적 처치 시 체력 1 회복(고유)"},
]

ENEMY_CONFIG = {
    "type1": {"hp": 5,  "vy": 1.5, "img_key": "type_1"},
    "type2": {"hp": 8,  "vy": 1.5, "img_key": "type_2"},
    "type3": {"hp": 6,  "vy": 1.0, "img_key": "type_3"},
    "type4": {"hp": 5,  "vy": 0.0, "img_key": "type_4"},
    "type5": {"hp": 10, "vy": 1.2, "img_key": "type_5"}, 
    "elite": {"hp": 50, "vy": 0.5, "img_key": "type_1"},
}

ENEMY_SPAWN_POOL = [
    {"type": "type1", "weight": 50.0, "minStage": 1},
    {"type": "type2", "weight": 15.0, "minStage": 2},
    {"type": "type3", "weight": 15.0, "minStage": 3},
    {"type": "type4", "weight": 18.5, "minStage": 5}, 
    {"type": "elite", "weight": 1.5, "minStage": 5},
]