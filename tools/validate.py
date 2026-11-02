import sys, glob, os, warnings, logging
warnings.filterwarnings("ignore"); logging.disable(50)
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.datasets.effects import EffectId
from AoE2ScenarioParser.datasets.conditions import ConditionId
WATER = {1,2,15,22,23,28,48,54,58,59,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113}

def check(path):
    s = AoE2DEScenario.from_file(path)
    pm, um, tm, mm = s.player_manager, s.unit_manager, s.trigger_manager, s.map_manager
    issues = []
    n = mm.map_size
    for i in range(1, pm.active_players + 1):
        c = pm.players[i].color
        c = getattr(c, "value", c)
        if not 0 <= int(c) <= 7:
            issues.append(f"P{i} colour {c}")
    refs = {u.reference_id for u in um.get_all_units()}
    for u in um.get_all_units():
        if not (0 <= u.x < n and 0 <= u.y < n):
            issues.append(f"unit {u.unit_const} out of bounds")
    T = tm.triggers
    for t in T:
        for e in t.effects:
            for attr in ("trigger_id",):
                v = getattr(e, attr, -1)
                if e.effect_type in (EffectId.ACTIVATE_TRIGGER, EffectId.DEACTIVATE_TRIGGER) and not (0 <= v < len(T)):
                    issues.append(f"{t.name}: bad trigger link {v}")
            sel = getattr(e, "selected_object_ids", []) or []
            for r in (sel if isinstance(sel, list) else [sel]):
                if r != -1 and r not in refs:
                    issues.append(f"{t.name}: effect refs missing unit {r}")
            if e.effect_type == EffectId.CREATE_OBJECT and getattr(e, "object_list_unit_id", -1) in (-1, None):
                issues.append(f"{t.name}: create without unit")
            msg = getattr(e, "message", "") or ""
            if len(msg) > 1500:
                issues.append(f"{t.name}: message too long {len(msg)}")
        for c in t.conditions:
            r = getattr(c, "unit_object", -1)
            if r not in (-1, None) and r not in refs:
                issues.append(f"{t.name}: condition refs missing unit {r}")
    objs = [t for t in T if t.display_as_objective]
    first = [t for t in T if t.enabled and t.name.startswith("Story 1")]
    wins = sum(1 for t in T for e in t.effects if e.effect_type == EffectId.DECLARE_VICTORY and e.source_player == 1)
    loss = sum(1 for t in T for e in t.effects if e.effect_type == EffectId.DECLARE_VICTORY and e.source_player != 1)
    civ = [pm.players[i].civilization.name for i in range(1, pm.active_players + 1)]
    print(f"{os.path.basename(path):45} map {n} units {len(refs):4} trig {len(T):3} obj {len(objs)} "
          f"win {wins} loss {loss} story {'Y' if first else 'N'} civs {civ}  {'OK' if not issues else 'ISSUES: ' + '; '.join(issues[:6])}")
    return not issues

res = [check(p) for p in sorted(glob.glob(sys.argv[1] + "/*.aoe2scenario"))]
ok = all(res)
print("ALL OK" if ok else "PROBLEMS FOUND")
