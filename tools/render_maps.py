"""Render a parchment-style isometric briefing map for every scenario in a folder.

The map is drawn from the scenario's real terrain, elevation and objects, in the same
diamond orientation as the in-game minimap, with labels for named forts and heroes."""
import glob
import math
import os
import random
import sys
import warnings
import logging

warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.datasets.effects import EffectId
from AoE2ScenarioParser.datasets.buildings import BuildingInfo as B
from AoE2ScenarioParser.datasets.other import OtherInfo as O

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from aoe_lib import WATER, FOREST, T  # noqa: E402

W, H = 1400, 820
PLAYER = {0: (250, 245, 230), 1: (232, 120, 20), 2: (176, 52, 52), 3: (210, 180, 40), 4: (70, 110, 200),
          5: (60, 170, 170), 6: (140, 70, 170), 7: (120, 120, 120), 8: (230, 120, 170)}
PLAYER_BY_COLOR = {0: (60, 100, 210), 1: (190, 45, 45), 2: (60, 140, 60), 3: (215, 185, 40),
                   4: (60, 170, 170), 5: (140, 70, 170), 6: (120, 120, 120), 7: (232, 120, 20)}
FORTS = {B.CASTLE.ID, B.WATCH_TOWER.ID, B.GUARD_TOWER.ID, B.KEEP.ID, B.BOMBARD_TOWER.ID, B.WONDER.ID,
         B.TOWN_CENTER.ID, B.MARKET.ID, B.DOCK.ID}
GOALS = {O.FLAG_A.ID, O.TORCH_A.ID, O.GARDEN_PAVILION.ID}


def font(size, bold=False):
    for f in (["DejaVuSerif-Bold.ttf", "DejaVuSerif.ttf"] if bold else ["DejaVuSerif.ttf"]):
        for d in ("/usr/share/fonts/truetype/dejavu/", ""):
            try:
                return ImageFont.truetype(d + f, size)
            except OSError:
                pass
    return ImageFont.load_default()


def parchment(w, h, seed):
    rng = random.Random(seed)
    img = Image.new("RGB", (w, h), (226, 206, 160))
    px = img.load()
    noise = Image.effect_noise((w // 4, h // 4), 40).resize((w, h), Image.BICUBIC)
    n = noise.load()
    for y in range(h):
        for x in range(w):
            v = (n[x, y] - 128) * 0.25
            dx, dy = (x - w / 2) / (w / 2), (y - h / 2) / (h / 2)
            vig = (dx * dx + dy * dy) * 38
            r, g, b = px[x, y]
            px[x, y] = (int(r + v - vig), int(g + v - vig * 1.1), int(b + v - vig * 1.3))
    d = ImageDraw.Draw(img)
    for _ in range(14):
        cx, cy, r = rng.randint(0, w), rng.randint(0, h), rng.randint(20, 90)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(205, 182, 135))
    return img


def terrain_colour(tid, elev):
    if tid in WATER:
        return (78, 112, 140) if tid not in (T.WATER_SHALLOW,) else (110, 140, 160)
    if tid == T.SHALLOWS:
        return (140, 160, 160)
    if tid in FOREST:
        return (72, 98, 58)
    if tid == T.BEACH:
        return (214, 196, 150)
    if tid in (T.ROAD, T.ROAD_BROKEN, T.DIRT_1, T.DIRT_2, T.DIRT_3):
        return (190, 160, 112)
    g = 186 - elev * 9
    return (g - 8, g + 4 - elev * 2, 120 - elev * 6)


def names_from_triggers(s):
    out = {}
    for t in s.trigger_manager.triggers:
        for e in t.effects:
            if e.effect_type == EffectId.CHANGE_OBJECT_NAME and e.message:
                ids = e.selected_object_ids if isinstance(e.selected_object_ids, list) else [e.selected_object_ids]
                for r in ids:
                    out[r] = e.message
    return out


def render(path, out_png, title, subtitle):
    s = AoE2DEScenario.from_file(path)
    mm, um = s.map_manager, s.unit_manager
    n = mm.map_size
    colors = {i: PLAYER_BY_COLOR.get(int(getattr(s.player_manager.players[i].color, "value",
                                                 s.player_manager.players[i].color)), (0, 0, 0))
              for i in range(1, s.player_manager.active_players + 1)}
    colors[0] = (250, 245, 230)
    img = parchment(W, H, n)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    scale = min((W - 160) / (2 * n), (H - 190) / n)
    ox, oy = W / 2, 130

    def iso(x, y):
        return ox + (x - y) * scale, oy + (x + y) * scale / 2

    elev = {(t.x, t.y): t.elevation for t in mm.terrain}
    for t in mm.terrain:
        c = terrain_colour(t.terrain_id, t.elevation)
        # hill shading: lighter facing the north-west light
        e_r = elev.get((t.x + 1, t.y), t.elevation)
        shade = (t.elevation - e_r) * 14
        c = tuple(max(0, min(255, v + shade)) for v in c)
        pts = [iso(t.x, t.y), iso(t.x + 1, t.y), iso(t.x + 1, t.y + 1), iso(t.x, t.y + 1)]
        d.polygon(pts, fill=c + (235,))
    # forest stipple
    rng = random.Random(n)
    for t in mm.terrain:
        if t.terrain_id in FOREST and rng.random() < 0.35:
            cx, cy = iso(t.x + 0.5, t.y + 0.5)
            d.ellipse([cx - 2.2, cy - 3, cx + 2.2, cy + 1.4], fill=(44, 70, 40, 255))
    border = [iso(0, 0), iso(n, 0), iso(n, n), iso(0, n)]
    d.polygon(border, outline=(92, 62, 30, 255))
    d.line(border + [border[0]], fill=(92, 62, 30, 255), width=3)
    img.paste(layer, (0, 0), layer)
    d = ImageDraw.Draw(img)

    names = names_from_triggers(s)
    units = um.get_all_units()
    for u in units:  # army dots
        if u.unit_const in FORTS or u.unit_const in GOALS or u.player == 0:
            continue
        cx, cy = iso(u.x, u.y)
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=colors.get(u.player, (0, 0, 0)))
    for u in units:  # forts and towns
        if u.unit_const not in FORTS:
            continue
        cx, cy = iso(u.x, u.y)
        c = colors.get(u.player, (0, 0, 0))
        if u.unit_const in (B.CASTLE.ID, B.WONDER.ID):
            d.polygon([(cx - 9, cy + 6), (cx - 9, cy - 6), (cx - 5, cy - 6), (cx - 5, cy - 10), (cx, cy - 10),
                       (cx, cy - 6), (cx + 5, cy - 6), (cx + 5, cy - 10), (cx + 9, cy - 10), (cx + 9, cy + 6)],
                      fill=c, outline=(40, 25, 10))
        else:
            d.rectangle([cx - 4, cy - 4, cx + 4, cy + 4], fill=c, outline=(40, 25, 10))
    goal_objs = [u for u in units if u.unit_const in GOALS]
    def is_goal(u):
        if u.unit_const != O.TORCH_A.ID:
            return True
        # camp and pavilion torches come in rings; a lone torch marks a goal
        return not any(o is not u and abs(o.x - u.x) < 10 and abs(o.y - u.y) < 10 for o in goal_objs)
    for u in goal_objs:  # objectives: flags, lone torches, pavilions
        if is_goal(u):
            cx, cy = iso(u.x, u.y)
            pts = []
            for k in range(10):
                r = 11 if k % 2 == 0 else 5
                a = -math.pi / 2 + k * math.pi / 5
                pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
            d.polygon(pts, fill=(200, 30, 30), outline=(80, 10, 10))

    lab = font(15, True)
    placed = []
    for u in units:
        nm = names.get(u.reference_id)
        if not nm or nm.startswith("Basket"):
            continue
        cx, cy = iso(u.x, u.y)
        tw = d.textlength(nm, font=lab)
        for dx_, dy_ in ((10, -22), (10, 2), (-tw - 10, -22), (-tw - 10, 2), (10, -44), (10, 24),
                         (-tw - 10, -44), (-tw - 10, 24), (10, -66), (10, 46)):
            x0, y0 = cx + dx_, cy + dy_
            box = (x0, y0, x0 + tw, y0 + 18)
            if not any(box[0] < b[2] and b[0] < box[2] and box[1] < b[3] and b[1] < box[3] for b in placed):
                break
        placed.append((x0, y0, x0 + tw, y0 + 18))
        d.line([(cx, cy), (x0 if x0 > cx else x0 + tw, y0 + 9)], fill=(70, 45, 20), width=1)
        for ddx, ddy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            d.text((x0 + ddx, y0 + ddy), nm, font=lab, fill=(240, 228, 196))
        d.text((x0, y0), nm, font=lab, fill=(60, 30, 10) if u.player != 1 else (150, 60, 0))

    # cartouche
    d.rectangle([40, 28, W - 40, 92], fill=(64, 34, 14), outline=(200, 150, 70), width=3)
    d.text((W / 2, 50), title, font=font(30, True), fill=(250, 214, 140), anchor="mm")
    d.text((W / 2, 78), subtitle, font=font(16), fill=(230, 200, 150), anchor="mm")
    # compass
    cx, cy = W - 110, H - 110
    d.ellipse([cx - 44, cy - 44, cx + 44, cy + 44], outline=(92, 62, 30), width=2)
    for a, lbl in ((-90, "N"), (0, "E"), (90, "S"), (180, "W")):
        r = math.radians(a + 26)
        d.line([(cx, cy), (cx + 40 * math.cos(r), cy + 40 * math.sin(r))], fill=(92, 62, 30), width=2)
        d.text((cx + 56 * math.cos(r), cy + 56 * math.sin(r)), lbl, font=font(16, True), fill=(92, 62, 30), anchor="mm")
    # legend
    lx, ly = 50, H - 120
    d.rectangle([lx - 12, ly - 14, lx + 250, ly + 96], fill=(236, 220, 180), outline=(92, 62, 30))
    items = [((232, 120, 20), "Swarajya"), ((200, 30, 30), "Objective / meeting point"),
             ((92, 62, 30), "Fort, town or market")]
    for i, (c, t) in enumerate(items):
        d.rectangle([lx, ly + i * 26, lx + 14, ly + 14 + i * 26], fill=c)
        d.text((lx + 24, ly + i * 26 - 2), t, font=font(15), fill=(50, 30, 10))
    img = img.filter(ImageFilter.SMOOTH_MORE)
    img.save(out_png, optimize=True)
    return out_png


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    os.makedirs(dst, exist_ok=True)
    import json
    meta = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else {}
    for p in sorted(glob.glob(src + "/*.aoe2scenario")):
        base = os.path.basename(p)[:-13]
        title, sub = meta.get(base, (base, ""))
        print(render(p, os.path.join(dst, base + ".png"), title, sub))
