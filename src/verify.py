"""Reload a generated scenario, print a summary and render a minimap PNG."""
import sys, logging, warnings
warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)
from collections import Counter
from PIL import Image, ImageDraw
from aoe_lib import AoE2DEScenario, WATER, FOREST, T

COLORS = {1: (255, 140, 0), 2: (200, 40, 40), 3: (240, 220, 40), 4: (60, 120, 255),
          5: (40, 200, 200), 6: (160, 60, 200), 7: (130, 130, 130), 8: (255, 120, 180), 0: (255, 255, 255)}


def check(path, png=None):
    s = AoE2DEScenario.from_file(path)
    mm = s.map_manager
    n = mm.map_size
    units = s.unit_manager.get_all_units()
    per = Counter(u.player for u in units)
    trig = s.trigger_manager.triggers
    print(f"{path.split('/')[-1]}: map {n}, units {dict(per)}, triggers {len(trig)}, "
          f"objectives {sum(1 for t in trig if t.display_as_objective)}")
    # sanity: units standing in water / forest
    bad = 0
    for u in units:
        t = mm.get_tile(min(n - 1, int(u.x)), min(n - 1, int(u.y)))
        if t.terrain_id in FOREST:
            bad += 1
    print(f"  units on forest tiles: {bad}; max elevation {max(t.elevation for t in mm.terrain)}")
    pl = s.player_manager.players
    print("  players:", [(i, pl[i].tribe_name, pl[i].civilization.name) for i in range(1, s.player_manager.active_players + 1)])
    if png:
        img = Image.new("RGB", (n, n))
        px = img.load()
        for t in mm.terrain:
            if t.terrain_id in WATER:
                c = (40, 90, 170)
            elif t.terrain_id in FOREST:
                c = (20, 80, 30)
            elif t.terrain_id == T.SHALLOWS:
                c = (90, 150, 200)
            else:
                g = 120 + t.elevation * 14
                c = (min(255, g - 30), min(255, g), 70)
            px[t.x, t.y] = c
        img = img.resize((n * 5, n * 5), Image.NEAREST)
        d = ImageDraw.Draw(img)
        for u in units:
            x, y = u.x * 5, u.y * 5
            d.rectangle([x - 2, y - 2, x + 2, y + 2], fill=COLORS.get(u.player, (0, 0, 0)))
        img.save(png)
    return s


if __name__ == "__main__":
    for p in sys.argv[1:]:
        check(p, p.replace(".aoe2scenario", ".png"))
