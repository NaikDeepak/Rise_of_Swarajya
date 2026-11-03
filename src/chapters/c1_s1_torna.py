"""C1-S1 Torna (1646), rebuilt on the official scenario IN1_Babur_1.

Spec: docs/tasks/2026-11-03-c1s1-torna-on-babur1.md. Only stage A (strip) is implemented so far.
Run from the repo root: .venv/bin/python -I src/chapters/c1_s1_torna.py
"""
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, ROOT)

from aoe_lib import Mission  # noqa: E402
from tools.scan_official_maps import CAMPAIGN_DIR, extract  # noqa: E402

TEMPLATE_CAMPAIGN, TEMPLATE_CHAPTER = "incam1", 1          # IN1_Babur_1
OUT = os.path.join(ROOT, "out", "v2", "C1S1_Torna.aoe2scenario")

TORNA_BOX = (30, 10, 75, 55)       # plateau core kept as Torna fort
OUTPOST_BOX = (125, 0, 167, 45)    # north-east Uzbek castles kept as the Adilshahi outpost
VILLAGE_CENTRE, VILLAGE_RADIUS = (10, 140), 12   # south-west noble town kept as the Maval villages


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


def keep(u):
    """Stage A rule for which template objects survive (owner is not changed yet)."""
    p = u.player
    if p == 0 or p == 1:
        return True                          # gaia scenery; P1 is cleared in stage B
    if p in (2, 4):
        return inside(u, TORNA_BOX)          # Samarkand core -> Torna
    if p == 3:
        return inside(u, OUTPOST_BOX)        # Uzbek north-east -> outpost
    if p == 6:
        return near(u, VILLAGE_CENTRE, VILLAGE_RADIUS)   # noble town -> Maval villages
    return False                             # P5, P7 and everything else


# Owner after stage A: Torna's Timurid castles and the Uzbek outpost become Bijapur (P2),
# the noble town becomes the Maval villages (P3).
NEW_OWNER = {2: 2, 4: 2, 3: 2, 6: 3}


def strip(m):
    m.tm.triggers = []
    m.um.units = [[u for u in plist if keep(u)] for plist in m.um.units]
    moved = [u for u in m.um.get_all_units() if u.player in NEW_OWNER and NEW_OWNER[u.player] != u.player]
    for u in moved:
        m.um.change_ownership(u, NEW_OWNER[u.player])
    m.pm.active_players = 3


def build(out=OUT):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        m = Mission.from_template(template_path(tmp), os.path.basename(out), "The First Flame - Torna")
        strip(m)
        return m.save(out)


if __name__ == "__main__":
    print(build())
