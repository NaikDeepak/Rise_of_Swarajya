"""Read-back checks for C1-S1 Torna (spec: docs/tasks/2026-11-03-c1s1-torna-on-babur1.md).

Run from the repo root: .venv/bin/python -I tests/test_c1_s1_torna.py
Builds stage A and the full scenario, then re-reads the written files with the parser.
"""
import logging
import os
import subprocess
import sys
import warnings

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, ROOT)
warnings.filterwarnings("ignore")

import AoE2ScenarioParser.settings as settings  # noqa: E402
settings.PRINT_STATUS_UPDATES = False
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario  # noqa: E402
from AoE2ScenarioParser.datasets.terrains import TerrainId  # noqa: E402
from AoE2ScenarioParser.datasets.buildings import BuildingInfo  # noqa: E402

from chapters import c1_s1_torna as ch  # noqa: E402

STAGE_A_OUT = os.path.join(ROOT, "out", "v2", "C1S1_Torna_stageA.aoe2scenario")
WET = {t.value for t in TerrainId if any(k in t.name for k in ("WATER", "SHALLOW", "BEACH", "SWAMP"))}
BUILDING_IDS = {b.ID for b in BuildingInfo}


def read(path):
    logging.disable(logging.CRITICAL)
    return AoE2DEScenario.from_file(path)


def tile(s, x, y):
    n = s.map_manager.map_size
    return s.map_manager.terrain[int(y) * n + int(x)]


# ------------------------------------------------------------------ stage A
def test_1_stage_a(s):
    fh = s.sections["FileHeader"]
    assert fh.version == "1.55", f"header version {fh.version!r}, expected the template's 1.55"
    assert list(fh.unknown_numbers) == [2, 3, 4, 5, 6, 7], f"dependencies {list(fh.unknown_numbers)}"
    assert len(s.trigger_manager.triggers) == 0, f"{len(s.trigger_manager.triggers)} triggers left"
    assert s.player_manager.active_players == 3, f"{s.player_manager.active_players} active players"
    high = [u for u in s.unit_manager.get_all_units() if u.player >= 4]
    assert not high, f"{len(high)} objects still owned by players 4 to 8"


# ------------------------------------------------------------------ stage B + C (full build)
def test_1_full_header(s):
    fh = s.sections["FileHeader"]
    assert fh.version == "1.55" and list(fh.unknown_numbers) == [2, 3, 4, 5, 6, 7]
    assert s.player_manager.active_players == 3
    assert not [u for u in s.unit_manager.get_all_units() if u.player >= 4]


def test_2_smooth(s):
    n = s.map_manager.map_size
    t = s.map_manager.terrain
    bad = [(x, y) for y in range(n) for x in range(n) for dx, dy in ((1, 0), (0, 1), (1, 1), (1, -1))
           if 0 <= x + dx < n and 0 <= y + dy < n
           and abs(t[y * n + x].elevation - t[(y + dy) * n + x + dx].elevation) > 1]
    assert not bad, f"{len(bad)} neighbour pairs differ by more than 1, first {bad[:3]}"


def test_3_murumbdev(s):
    cx, cy = ch.MURUMBDEV
    assert tile(s, cx, cy).elevation >= 3, f"Murumbdev centre elevation {tile(s, cx, cy).elevation}"
    flags = [u for u in s.unit_manager.get_all_units()
             if u.player == 0 and u.unit_const == ch.O.FLAG_A.ID and abs(u.x - cx - 0.5) <= 1 and abs(u.y - cy - 0.5) <= 1]
    assert flags, "no flag on Murumbdev"


def test_4_p2_buildings_placed(s):
    stray = [(u.unit_const, u.x, u.y) for u in s.unit_manager.get_all_units()
             if u.player == 2 and u.unit_const in BUILDING_IDS
             and not ch.inside(u, ch.TORNA_BOX) and not ch.inside(u, ch.OUTPOST_BOX)]
    assert not stray, f"P2 buildings outside Torna and the outpost: {stray[:5]}"


def test_5_names(s):
    names = [e.message for t in s.trigger_manager.triggers for e in t.effects
             if e.effect_type == 26 and e.message]          # change object name
    assert names.count("Shivaji Raje") == 1, f"'Shivaji Raje' named {names.count('Shivaji Raje')} times"
    assert not [n for n in names if "Chhatrapati" in n], "a unit is named with Chhatrapati"
    texts = [e.message for t in s.trigger_manager.triggers for e in t.effects if e.message]
    mm = s.message_manager
    texts += [mm.instructions or "", mm.history or "", mm.hints or "", mm.victory or "", mm.loss or ""]
    assert not [x for x in texts if "Chhatrapati" in x], "Chhatrapati appears in RS01 text"


def _by_name(s):
    return {t.name: t for t in s.trigger_manager.triggers}


def _activators(s, target):
    tid = _by_name(s)[target].trigger_id
    return [t.name for t in s.trigger_manager.triggers
            for e in t.effects if e.effect_type == 8 and e.trigger_id == tid]   # activate trigger


def test_6_objective_chain(s):
    objs = [t for t in s.trigger_manager.triggers if t.display_as_objective]
    order = [t.name for t in sorted(objs, key=lambda t: t.description_order)]
    assert order == ["Obj 1: Seize Torna", "Obj 2: Raise Rajgad", "Obj 3: Drive out Bijapur"], order
    assert _activators(s, "Obj 2: Raise Rajgad") == ["Obj 1: Seize Torna"]
    assert _activators(s, "Obj 3: Drive out Bijapur") == ["Obj 2: Raise Rajgad"]
    assert _activators(s, "Victory") == ["Obj 3: Drive out Bijapur"]
    assert _by_name(s)["Obj 1: Seize Torna"].enabled and not _by_name(s)["Obj 2: Raise Rajgad"].enabled


def test_7_loss(s):
    loss = _by_name(s)["Loss: Shivaji Raje has fallen"]
    assert loss.enabled
    hero = [e.selected_object_ids for t in s.trigger_manager.triggers for e in t.effects
            if e.effect_type == 26 and e.message == "Shivaji Raje"][0][0]
    assert any(c.condition_type == 6 and c.unit_object == hero for c in loss.conditions), "not tied to the hero"
    assert any(e.effect_type == 13 and e.source_player == 2 for e in loss.effects), "does not declare P2 the winner"


RS01_ARCHIVED = os.path.join(ROOT, "archive", "v1-generated", "scenarios", "RS01_The_First_Flame.aoe2scenario")


def _shown(s):
    """Every player-facing string longer than 30 characters: objectives, messages, briefing texts."""
    out = set()
    for t in s.trigger_manager.triggers:
        if t.description:
            out.add(t.description)
        for e in t.effects:
            if e.message and len(e.message) > 30:
                out.add(e.message)
    mm = s.message_manager
    out |= {(mm.instructions or "").split("\n\n")[-1], mm.history, mm.hints, mm.victory, mm.loss}
    return {x for x in out if x}


def test_8_text_verbatim(s):
    """Same text as the archived, play-test-ready RS01 build (only the instructions' heading is not added)."""
    ref = _shown(read(RS01_ARCHIVED))
    shown = _shown(s)
    assert not ref - shown, f"RS01 text missing: {sorted(ref - shown)[:3]}"
    assert not shown - ref, f"text not in RS01: {sorted(shown - ref)[:3]}"


def test_9_outpost_covers_buildings(s):
    x1, y1, x2, y2 = ch.OUTPOST_BOX
    o3 = _by_name(s)["Obj 3: Drive out Bijapur"]
    c = [c for c in o3.conditions if c.condition_type == 5][0]                 # objects in area
    assert (c.area_x1, c.area_y1, c.area_x2, c.area_y2) == (x1, y1, x2, y2), "Obj 3 area differs from the outpost box"
    stray = [u for u in s.unit_manager.get_all_units()
             if u.player == 2 and u.unit_const in BUILDING_IDS and not ch.inside(u, ch.TORNA_BOX)
             and not (x1 <= u.x <= x2 + 1 and y1 <= u.y <= y2 + 1)]
    assert not stray, f"{len(stray)} P2 buildings outside Obj 3's area"


def test_10_spawn_points_on_land(s):
    """Edge: villagers and waves must not appear in water."""
    for name, (x, y) in (("villager drop", ch.VILLAGER_DROP), ("wave spawn", ch.WAVE_SPAWN), ("start", ch.START)):
        for dx in range(0, 4):
            for dy in range(0, 4):
                assert tile(s, x + dx, y + dy).terrain_id not in WET, f"{name} ({x + dx},{y + dy}) is water"


if __name__ == "__main__":
    failed = 0
    stage_a = read(ch.build(STAGE_A_OUT, stage="A"))
    full = read(ch.build())
    cases = [("1 stage A", test_1_stage_a, stage_a), ("1 full header", test_1_full_header, full),
             ("2 smooth", test_2_smooth, full), ("3 Murumbdev", test_3_murumbdev, full),
             ("4 P2 buildings", test_4_p2_buildings_placed, full), ("5 names", test_5_names, full),
             ("6 objective chain", test_6_objective_chain, full), ("7 loss", test_7_loss, full),
             ("8 text verbatim", test_8_text_verbatim, full), ("9 outpost area", test_9_outpost_covers_buildings, full),
             ("10 spawn on land", test_10_spawn_points_on_land, full)]
    for name, fn, s in cases:
        try:
            fn(s)
            print(f"PASS {name}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {name}: {e}")
        except Exception as e:  # a crash in a check is a failure, not a pass
            failed += 1
            print(f"ERROR {name}: {type(e).__name__}: {e}")
    sys.exit(1 if failed else 0)
