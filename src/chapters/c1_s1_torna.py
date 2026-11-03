"""C1-S1 Torna (1646), rebuilt on the official scenario IN1_Babur_1.

Spec: docs/tasks/2026-11-03-c1s1-torna-on-babur1.md.
  Stage A  strip the template to Torna's three players (no triggers)
  Stage B  map: Shivaji Raje's band, garrisons, Murumbdev hill
  Stage C  RS01's triggers and text, verbatim from src/m1_torna.py (commit d03840c)
Run from the repo root: .venv/bin/python -I src/chapters/c1_s1_torna.py [A|B|C]   (default C)
"""
import math
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, ROOT)

from common import *  # noqa: E402,F401,F403  (Mission, U, B, O, H, T, civs, maratha_identity, ...)
from tools.scan_official_maps import CAMPAIGN_DIR, extract  # noqa: E402

TEMPLATE_CAMPAIGN, TEMPLATE_CHAPTER = "incam1", 1          # IN1_Babur_1
OUT = os.path.join(ROOT, "out", "v2", "C1S1_Torna.aoe2scenario")

TORNA_BOX = (30, 10, 75, 55)       # Samarkand plateau core -> Torna fort
OUTPOST_BOX = (125, 0, 167, 45)    # north-east Uzbek castles -> Adilshahi outpost
VILLAGE_CENTRE, VILLAGE_RADIUS = (10, 140), 12   # south-west noble town -> Maval villages
CAMP_BOX = (60, 148, 79, 166)      # Babur's camp -> Shivaji Raje's starting band
START = (70, 152)
TORNA_CENTRE = (52, 36)            # in front of the plateau's town centre (52,32)
MURUMBDEV = (83, 89)               # dry, open ground between Torna and the start (spec allowed (110,110)
                                   # only if dry; it borders shallow water)
MURUMBDEV_TOP, MURUMBDEV_HEIGHT = 5, 5
RAJGAD_BOX = (MURUMBDEV[0] - 6, MURUMBDEV[1] - 6, MURUMBDEV[0] + 6, MURUMBDEV[1] + 6)
VILLAGER_DROP = (52, 58)           # just below Torna's plateau
WAVE_SPAWN = (146, 50)             # just south of the outpost


def inside(u, box):
    x1, y1, x2, y2 = box
    return x1 <= u.x <= x2 + 1 and y1 <= u.y <= y2 + 1


def near(u, centre, r):
    return (u.x - centre[0]) ** 2 + (u.y - centre[1]) ** 2 <= r * r


def template_path(tmp):
    for camp, chapter, path in extract(CAMPAIGN_DIR, tmp):
        if camp == TEMPLATE_CAMPAIGN and chapter == TEMPLATE_CHAPTER:
            return path
    raise FileNotFoundError(f"{TEMPLATE_CAMPAIGN} chapter {TEMPLATE_CHAPTER} not found in {CAMPAIGN_DIR}")


# ------------------------------------------------------------------ stage A
def keep(u):
    """Which template objects survive (owners are changed afterwards)."""
    p = u.player
    if p == 0:
        return True                          # gaia scenery
    if p == 1:
        return True                          # cleared in stage B
    if p in (2, 4):
        return inside(u, TORNA_BOX)
    if p == 3:
        return inside(u, OUTPOST_BOX)
    if p == 6:
        return near(u, VILLAGE_CENTRE, VILLAGE_RADIUS)
    return False                             # P5, P7 and everything else


# Torna's Timurid castles and the Uzbek outpost become Bijapur (P2); the noble town, the Maval villages (P3).
NEW_OWNER = {2: 2, 4: 2, 3: 2, 6: 3}


def stage_a(m):
    m.tm.triggers = []
    m.um.units = [[u for u in plist if keep(u)] for plist in m.um.units]
    for u in [u for u in m.um.get_all_units() if NEW_OWNER.get(u.player, u.player) != u.player]:
        m.um.change_ownership(u, NEW_OWNER[u.player])
    m.pm.active_players = 3


# ------------------------------------------------------------------ stage B
IMMOBILE_AI = "Fe Immobile AI.ai"   # embedded in Babur 1 already; the template uses it for two players


def set_player(m, pid, name, civ, food, wood, gold, stone, age, ai=None):
    """Name, civ, resources and age; the AI script only when given.

    Player 1 keeps the template's settings. Players 2 and 3 must not keep Babur's own scripts
    (Samarkand's and the Uzbek army's): RS01's garrisons hold still and attacks come from triggers.
    """
    p = m.pm.players[pid]
    if ai is not None:
        p.personality = ai
    p.tribe_name = name
    p.civilization = civ
    p.lock_civ = True
    p.food, p.wood, p.gold, p.stone = food, wood, gold, stone
    p.starting_age = age


def stage_b(m):
    # Players, as in RS01 (swarajya() and m.player() would replace the template's AI settings)
    set_player(m, 1, "Swarajya", MARATHA, 300, 300, 0, 0, StartingAge.CASTLE_AGE)
    set_player(m, 2, "Adilshahi Sultanate (Bijapur)", ADILSHAHI, 1500, 1500, 1000, 500, StartingAge.CASTLE_AGE,
               ai=IMMOBILE_AI)
    set_player(m, 3, "Maval villages", MARATHA, 200, 200, 100, 200, StartingAge.CASTLE_AGE, ai=IMMOBILE_AI)
    m.diplomacy(1, 2, DiplomacyState.ENEMY)
    m.diplomacy(1, 3, DiplomacyState.ALLY)
    m.diplomacy(2, 3, DiplomacyState.NEUTRAL)
    m.s.sections["Map"].map_color_mood = ""      # template is "Night"; RS01's Spring is set by trigger

    # Shivaji Raje's band replaces Babur's camp
    m.um.units = [[u for u in plist if u.player != 1] for plist in m.um.units]
    sx, sy = START
    m.band = {
        "shivaji": m.um.add_unit(1, H.PRITHVIRAJ.ID, sx + 0.5, sy + 0.5),
        "tanaji": m.um.add_unit(1, U.CHAMPION.ID, sx + 2.5, sy - 1.5),
        "yesaji": m.um.add_unit(1, U.CHAMPION.ID, sx - 1.5, sy - 1.5),
        "baji": m.um.add_unit(1, U.LIGHT_CAVALRY.ID, sx + 2.5, sy + 2.5),
    }
    m.group(1, U.SPEARMAN, 12, sx - 4, sy + 4, cols=6)
    m.group(1, U.SKIRMISHER, 8, sx + 5, sy + 4, cols=4)
    m.group(1, U.ARCHER, 6, sx + 8, sy, cols=3)
    m.camera(1, sx, sy)

    # Torna garrison (RS01 compositions)
    tx, ty = TORNA_CENTRE
    m.killedar = m.um.add_unit(2, U.LONG_SWORDSMAN.ID, tx + 0.5, ty + 0.5)
    m.group(2, U.SPEARMAN, 8, tx + 2, ty + 2, cols=4)
    m.group(2, U.ARCHER, 6, tx - 3, ty - 4, cols=3)
    m.group(2, U.MAN_AT_ARMS, 4, tx + 4, ty - 2, cols=2)
    m.um.add_unit(0, O.RELIC.ID, tx - 1.5, ty + 1.5)

    # Outpost army (RS01 compositions) in front of the north-east castles
    m.group(2, U.KNIGHT, 4, 140, 30, cols=4)
    m.group(2, U.CROSSBOWMAN, 6, 146, 22, cols=3)

    # Murumbdev hill, the future Rajgad: clear scenery from the footprint, raise, smooth
    cx, cy = MURUMBDEV
    reach = MURUMBDEV_TOP + MURUMBDEV_HEIGHT + 2
    m.um.units = [[u for u in plist if not (u.player == 0 and near(u, MURUMBDEV, reach))]
                  for plist in m.um.units]
    m.hill(cx, cy, MURUMBDEV_TOP, MURUMBDEV_HEIGHT, flat_terrain=T.DIRT_1)
    m.smooth()
    m.um.add_unit(0, O.FLAG_A.ID, cx + 0.5, cy + 0.5)


# ------------------------------------------------------------------ stage C
def stage_c(m):
    """RS01's triggers and text (src/m1_torna.py at d03840c); only coordinates differ."""
    b = m.band
    m.rename(1, b["shivaji"], "Shivaji Raje")
    m.rename(1, b["tanaji"], "Tanaji Malusare")
    m.rename(1, b["yesaji"], "Yesaji Kank")
    m.rename(1, b["baji"], "Baji Pasalkar")
    m.rename(2, m.killedar, "Killedar of Torna")
    maratha_identity(m, 1)
    m.mood(ColorMood.SPRING)
    m.hero_setup("Shivaji Raje", hp=150, attack=2,
                 desc="Shivaji Raje Bhosale, age 16. Son of Shahaji Raje Bhosale and Rajmata Jijabai Aaisaheb. By tradition, he swore at Raireshwar to found Hindavi Swarajya.")
    m.hero_setup("Tanaji Malusare", hp=80, attack=2,
                 desc="Subhedar Tanaji Malusare. Childhood companion of Shivaji Raje from Godoli. A lion in close combat.")
    m.hero_setup("Yesaji Kank", hp=80, melee_armor=1,
                 desc="Sarnaubat Yesaji Kank. Trusted companion of the Raireshwar oath, famed for his valor and strength.")
    m.story([
        "1646. The Nizamshahi is gone, its lands shared out between the Mughals and the Adilshahi of Bijapur. The Maval hills answer to Bijapur.",
        ("Rajmata Jijabai Aaisaheb", "Shivba Raje, your father Shahaji Raje serves far away in Bangalore. But these hills and these people deserve a ruler of their own."),
        ("Shivaji Raje", "Before Mahadev we promised Swarajya, Aaisaheb. Today that promise becomes a fort."),
        ("Tanaji Malusare", "Torna stands neglected, Raje. Its killedar sleeps, and Bijapur's eyes are elsewhere."),
        ("Yesaji Kank", "Then let us wake him. Har Har Mahadev!"),
        "Lead the Mavalas up the road to Torna and take it. Shivaji Raje must survive.",
    ])

    o1 = m.objective("Obj 1: Seize Torna", "Defeat the killedar and garrison of Torna, then bring your troops into the fort.", 1)
    m.dead(o1, m.killedar)
    m.cleared(o1, 2, TORNA_BOX)
    m.present(o1, 1, TORNA_BOX, otype=ObjectType.MILITARY, qty=1)
    m.handover(o1, 2, 1, TORNA_BOX, ObjectType.BUILDING)
    m.say(o1, "Torna is ours! Repairing the walls, the Mavalas unearth a buried treasure. Tradition calls it Bhavani Mata's blessing. It will pay for a new fort.", 12)
    m.gold(o1, 1, 800)
    m.resource(o1, 1, Attribute.STONE_STORAGE, 900)
    m.resource(o1, 1, Attribute.WOOD_STORAGE, 400)
    m.spawn(o1, 1, U.VILLAGER_MALE, 8, *VILLAGER_DROP)

    o2 = m.objective("Obj 2: Raise Rajgad", "Fortify Murumbdev hill (the flag in the east) by building a Castle there. This is the beginning of Rajgad.", 2, enabled=False)
    m.present(o2, 1, RAJGAD_BOX, const=B.CASTLE)
    m.say(o2, "Work begins on Murumbdev, the fort that will become Rajgad. It will be the capital of Swarajya for more than two decades.", 12)
    m.chain(o1, o2)

    o3 = m.objective("Obj 3: Drive out Bijapur", "Destroy every Adilshahi building at the north-east outpost.", 3, enabled=False)
    m.cleared(o3, 2, OUTPOST_BOX, ObjectType.BUILDING)
    m.chain(o2, o3)

    win = m.trig("Victory", enabled=False)
    win.new_condition.timer(timer=3)
    m.victory(win, "With Torna taken and Murumbdev fortified, Shivaji Raje has his first foothold in the Maval country.", epilogue=[
        ("Rajmata Jijabai Aaisaheb", "Shivba, a fort is a promise in stone. Keep faith with the people who build it, and they will keep faith with you."),
        ("Shivaji Raje", "Then Torna is only the first, Aaisaheb. The Sahyadri have many more hills."),
        "News of Torna and Murumbdev reaches Bijapur.",
    ])
    m.chain(o3, win)

    # Bijapur notices the loss and counter-attacks
    alert = m.trig("Bijapur alerted", enabled=False)
    alert.new_condition.timer(timer=240)
    m.line(alert, "Adilshahi outpost commander", "Torna has fallen to Shivaji Raje! Horsemen, ride out and take it back!")
    m.chain(o1, alert)
    wx, wy = WAVE_SPAWN
    w1 = m.wave("Wave 1", 2, 1, [(U.KNIGHT, 4), (U.ARCHER, 6), (U.SPEARMAN, 6)], wx, wy, *TORNA_CENTRE, enabled=False)
    m.chain(alert, w1)
    w2 = m.wave("Wave 2", 2, 300, [(U.KNIGHT, 6), (U.MANGONEL, 2), (U.LONG_SWORDSMAN, 6)], wx, wy, *TORNA_CENTRE, enabled=False)
    m.chain(alert, w2)
    w3 = m.wave("Wave 3", 2, 600, [(U.KNIGHT, 6), (U.CROSSBOWMAN, 8), (U.BATTERING_RAM, 2)], wx, wy, *MURUMBDEV, enabled=False)
    m.chain(alert, w3)

    m.hero_loss(b["shivaji"], 2, "Shivaji Raje")

    m.texts(
        instructions="1646, Maval country. Seize Torna from Bijapur, fortify Murumbdev hill as Rajgad, then drive the Adilshahi outpost out of the valley. Shivaji Raje must survive.",
        history="Shivaji Raje, son of Shahaji Raje Bhosale and Rajmata Jijabai Aaisaheb, grew up in Pune among the Sahyadri hills. Tradition holds that he and his companions from the Maval valleys swore at the Raireshwar temple to found Hindavi Swarajya. Around 1646, at about sixteen, Shivaji Raje took Torna (Prachandagad) and began fortifying nearby Murumbdev, which became Rajgad, his first capital.",
        hints="Use the hills: archers on high ground deal extra damage.\nKeep Shivaji Raje protected behind the spearmen.\nCastle Age is unlocked: you need 650 stone for a Castle.",
        victory="The Bhagwa Dhwaj flies over Torna and Rajgad. Har Har Mahadev!",
        loss="Shivaji Raje has fallen in battle.",
    )


def build(out=OUT, stage="C"):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        m = Mission.from_template(template_path(tmp), os.path.basename(out), "The First Flame - Torna")
        stage_a(m)
        if stage in ("B", "C"):
            stage_b(m)
        if stage == "C":
            stage_c(m)
        return m.save(out)


if __name__ == "__main__":
    print(build(stage=(sys.argv[1] if len(sys.argv) > 1 else "C").upper()))
