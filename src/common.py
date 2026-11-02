from aoe_lib import *

import os
OUT = os.environ.get("SWARAJYA_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out"))

MARATHA = Civ.GURJARAS      # light cavalry, raids, hill infantry
MUGHAL = Civ.HINDUSTANIS
ADILSHAHI = Civ.PERSIANS
SIDDI = Civ.ETHIOPIANS
PORTUGUESE = Civ.PORTUGUESE

SAFFRON = PlayerColorId.ORANGE
GREEN = PlayerColorId.GREEN
PURPLE = PlayerColorId.PURPLE
GRAY = PlayerColorId.GRAY
BLUE = PlayerColorId.BLUE
YELLOW = PlayerColorId.YELLOW
RED = PlayerColorId.RED


CAVALRY = [U.SCOUT_CAVALRY, U.LIGHT_CAVALRY, U.HUSSAR, U.SHRIVAMSHA_RIDER, U.ELITE_SHRIVAMSHA_RIDER,
           U.CAVALRY_ARCHER, U.HEAVY_CAVALRY_ARCHER, U.KNIGHT, U.CAVALIER, U.PALADIN]
RAIDERS = [U.LIGHT_CAVALRY, U.HUSSAR, U.SHRIVAMSHA_RIDER, U.ELITE_SHRIVAMSHA_RIDER]
# (unit, new food cost) - infantry 10% cheaper in food
INFANTRY_FOOD = [(U.MILITIA, 54), (U.MAN_AT_ARMS, 54), (U.LONG_SWORDSMAN, 54),
                 (U.TWO_HANDED_SWORDSMAN, 54), (U.CHAMPION, 54), (U.SPEARMAN, 32),
                 (U.PIKEMAN, 32), (U.HALBERDIER, 32), (U.SKIRMISHER, 23), (U.ELITE_SKIRMISHER, 23)]
# (building, extra hit points) - fortifications +15%
FORT_HP = [(B.CASTLE, 720), (B.STONE_WALL, 270), (B.FORTIFIED_WALL, 450), (B.PALISADE_WALL, 40),
           (B.WATCH_TOWER, 150), (B.GUARD_TOWER, 225), (B.KEEP, 340), (B.BOMBARD_TOWER, 330)]


def maratha_identity(m, pid=1):
    """The Marathas as a campaign civilization: Gurjaras base, renamed, with Swarajya bonuses.
    Cavalry +2 line of sight; light cavalry raiders +3 attack vs buildings;
    infantry -10% food; fortifications +15% hit points."""
    t = m.trig("Setup: Maratha civilization")
    t.new_effect.change_civilization_name(source_player=pid, message="Marathas")
    for u in CAVALRY:
        t.new_effect.modify_attribute(quantity=2, object_list_unit_id=u.ID, source_player=pid,
                                      operation=Operation.ADD,
                                      object_attributes=ObjectAttribute.LINE_OF_SIGHT)
    for u in RAIDERS:
        t.new_effect.modify_attribute(armour_attack_quantity=3, armour_attack_class=21,
                                      object_list_unit_id=u.ID, source_player=pid,
                                      operation=Operation.ADD,
                                      object_attributes=ObjectAttribute.ATTACK)
    for u, food in INFANTRY_FOOD:
        t.new_effect.set_object_cost(object_list_unit_id=u.ID, source_player=pid, quantity=food,
                                     tribute_list=Attribute.FOOD_STORAGE)
    for b, hp in FORT_HP:
        t.new_effect.modify_attribute(quantity=hp, object_list_unit_id=b.ID, source_player=pid,
                                      operation=Operation.ADD,
                                      object_attributes=ObjectAttribute.HIT_POINTS)
    return t


def swarajya(m, name="Swarajya", **kw):
    kw.setdefault("age", StartingAge.CASTLE_AGE)
    p = m.player(1, name, MARATHA, SAFFRON, human=True, **kw)
    maratha_identity(m, 1)
    return p


def sahyadri_base(m, forest=T.FOREST_JUNGLE, density=22):
    """Green Deccan plateau with jungle patches."""
    m.forest_scatter(forest, 0, 0, m.size - 1, m.size - 1, density, 2, 6)
    m.forest_scatter(T.GRASS_JUNGLE, 0, 0, m.size - 1, m.size - 1, 12, 3, 7)


def fort_on_hill(m, pid, cx, cy, r=6, h=6, castle=True, towers=4, walls=True,
                 gate_angles=(270,), terrain=T.ROAD_BROKEN):
    m.hill(cx, cy, r + 1, h, flat_terrain=T.DIRT_1)
    m.blob(terrain, cx, cy, 2, 0)
    if castle:
        m.unit(pid, B.CASTLE, cx, cy)
    for i in range(towers):
        a = math.radians(45 + i * 360 / max(towers, 1))
        m.unit(pid, B.GUARD_TOWER, round(cx + (r - 2) * math.cos(a)),
               round(cy + (r - 2) * math.sin(a)))
    if walls:
        m.ring_walls(pid, cx, cy, r, gaps=gate_angles)
    return (cx - r - 1, cy - r - 1, cx + r + 1, cy + r + 1)


def village(m, pid, cx, cy, houses=6, market=False, spread=7):
    for i in range(houses):
        a = math.radians(i * 360 / houses + 15)
        m.unit(pid, B.HOUSE, round(cx + spread * math.cos(a)), round(cy + spread * math.sin(a)))
    if market:
        m.unit(pid, B.MARKET, cx, cy)


def camp(m, pid, cx, cy, tents=6):
    m.blob(T.DIRT_2, cx, cy, 7, 0.15)
    m.unit(pid, B.BARRACKS, cx - 3, cy)
    m.unit(pid, B.STABLE, cx + 3, cy)
    for i in range(tents):
        a = math.radians(i * 360 / tents)
        m.unit(0, O.FLAG_C if i % 2 else O.TORCH_A, round(cx + 6 * math.cos(a)),
               round(cy + 6 * math.sin(a)))
    return (cx - 8, cy - 8, cx + 8, cy + 8)
