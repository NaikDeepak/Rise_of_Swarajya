"""Read-back checks for C1-S1 Torna (spec: docs/tasks/2026-11-03-c1s1-torna-on-babur1.md).

Run from the repo root: .venv/bin/python -I tests/test_c1_s1_torna.py
Builds the scenario, then re-reads the written file with the parser.
"""
import logging
import os
import sys
import warnings

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, ROOT)
warnings.filterwarnings("ignore")

import AoE2ScenarioParser.settings as settings  # noqa: E402
settings.PRINT_STATUS_UPDATES = False
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario  # noqa: E402

from chapters import c1_s1_torna as ch  # noqa: E402


def load():
    path = ch.build()
    logging.disable(logging.CRITICAL)
    return AoE2DEScenario.from_file(path)


def test_stage_a(s):
    fh = s.sections["FileHeader"]
    assert fh.version == "1.55", f"header version {fh.version!r}, expected the template's 1.55"
    assert list(fh.unknown_numbers) == [2, 3, 4, 5, 6, 7], f"dependencies {list(fh.unknown_numbers)}"
    assert len(s.trigger_manager.triggers) == 0, f"{len(s.trigger_manager.triggers)} triggers left"
    assert s.player_manager.active_players == 3, f"{s.player_manager.active_players} active players"
    units = s.unit_manager.get_all_units()
    high = [u for u in units if u.player >= 4]
    assert not high, f"{len(high)} objects still owned by players 4 to 8"


def test_stage_a_placement(s):
    """Edge: every kept enemy object sits where the spec maps it."""
    units = s.unit_manager.get_all_units()
    p2_stray = [u for u in units if u.player == 2
                and not ch.inside(u, ch.TORNA_BOX) and not ch.inside(u, ch.OUTPOST_BOX)]
    assert not p2_stray, f"{len(p2_stray)} P2 objects outside Torna and the outpost"
    p3_stray = [u for u in units if u.player == 3 and not ch.near(u, ch.VILLAGE_CENTRE, ch.VILLAGE_RADIUS)]
    assert not p3_stray, f"{len(p3_stray)} P3 objects outside the Maval village"
    assert any(ch.inside(u, ch.TORNA_BOX) for u in units if u.player == 2), "Torna is empty"
    assert any(ch.inside(u, ch.OUTPOST_BOX) for u in units if u.player == 2), "outpost is empty"
    assert any(u.player == 3 for u in units), "Maval village is empty"


if __name__ == "__main__":
    scenario = load()
    failed = 0
    for name, fn in [("1 stage A strip", test_stage_a), ("1b stage A placement", test_stage_a_placement)]:
        try:
            fn(scenario)
            print(f"PASS {name}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {name}: {e}")
    sys.exit(1 if failed else 0)
