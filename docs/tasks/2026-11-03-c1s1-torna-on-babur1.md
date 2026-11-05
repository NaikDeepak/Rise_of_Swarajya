# Task: C1-S1 Torna rebuilt on the official Babur 1 map

**Assigned to:** agy  **Lead / reviewer:** claude  **Second review:** codex (read-only)
**Branch:** `feat/c1s1-torna-template`  **Worktree:** `../Rise_of_Swarajya.zip_1-wt-agy`

## Goal
Rebuild chapter 1 (Torna, 1646) on top of the official scenario `IN1_Babur_1` instead of the parser's blank
default, keeping RS01's story, text and objectives. The player must be able to Quit the scenario without the
"Game Paused (F3)" stall.

## Why (read first)
- Every scenario built from `AoE2DEScenario.from_default()` (all of `archive/v1-generated/`) stalls on Quit.
- Official scenarios quit cleanly, including `IN1_Babur_1` after a parser load-and-save with no changes.
- So this task works in stages, and the human play-tests Quit after stage A before anything else is built.
  If stage A stalls, stop and hand off: the plan changes.
- Background: `docs/KNOWLEDGEBASE.md`, `docs/official-maps.md` (Babur 1 row), `archive/v1-generated/README.md`.

## Source material
- Template: scenario 1 inside
  `~/Library/Application Support/Steam/steamapps/common/AoE2DE/AgeOfEmpires2Data/resources/_common/campaign/incam1.aoe2campaign`.
  Extract it with `extract()` from `tools/scan_official_maps.py`. Never modify or copy back into the game folder.
- Text, objectives, units and waves: `src/m1_torna.py` at commit `d03840c` (the play-test-ready RS01 text).
  Use its strings verbatim; do not rewrite any text.

## Babur 1 facts (measured, coordinates are tile x,y)
| Thing | Where | Owner now |
| --- | --- | --- |
| Babur's walled camp + fortified tower | box (60,148)-(79,166), tower (70,158) | P1 |
| Samarkand plateau (only large raised area, elevation up to 6) | box (19,0)-(90,74), centre (54,33) | P2, P4, P5 |
| Samarkand town centre (plateau top) | (52,32), elevation 6 | P2 |
| Timurid castles on the plateau | (37,21) elev 4, (64,38) elev 5 | P4 |
| Uzbek castles + town centre (north-east) | (165,2), (134,37), TC (162,10) | P3 |
| Noble town (south-west) | TC (10,140) | P6 |
| Players | 7 active: P1 Babur, P2 Samarkand, P3 Uzbeks, P4/P5 Timurids, P6 nobles, P7 allies | |

## Mapping to Torna (lead's design; change only with lead approval)
| Torna role | Built from | New owner |
| --- | --- | --- |
| Shivaji Raje's band (start) | Babur's camp area: remove every P1 object, place RS01's band around (70,150) | P1 Swarajya (Gurjaras, renamed Marathas by the RS01 setup trigger) |
| Torna fort | Plateau core: keep P2/P4 buildings and walls inside box (30,10)-(75,55), remove all other plateau objects | P2 Adilshahi (Bijapur) |
| Adilshahi outpost | North-east: keep P3 buildings inside box (125,0)-(167,45), remove the rest of P3 | P2 Adilshahi |
| Murumbdev (future Rajgad) | New hill: centre (110,110), flat dirt top radius 5, height 5, flag at centre. If (110,110) is water or occupied, move it at most 15 tiles and report the coordinates | none (gaia flag) |
| Maval villages (ally) | South-west noble town: keep P6 objects within 12 tiles of (10,140) | P3 Maval villages (ally of P1) |
| Everything else | P4, P5, P6 (outside the village), P7 units and buildings | removed |

Players after the change: 3 active (P1 Swarajya, P2 Adilshahi, P3 Maval villages), diplomacy as in RS01.
Map mood: Spring (RS01 uses `ColorMood.SPRING`). Map size stays 168.

## Files you may touch (nothing else)
- `src/aoe_lib.py`: add `Mission.from_template(path, filename, title)`, a classmethod that loads an existing
  scenario instead of `from_default()`, sets `size` from the loaded map and fills `_land_units`/`_ship_units`
  from existing units, plus `Mission.save(path)` that only calls `self.s.write_to_file(path)`.
  Additive only: do not change any existing method's behaviour. Do NOT call `finish()` for this chapter:
  it adds gaia resources, embeds AI files and edits header fields, and any of those may cause the Quit stall.
  The template keeps its own AI settings.
- `src/chapters/__init__.py`, `src/chapters/c1_s1_torna.py`: new. Builds the scenario in stages (below).
- `tests/test_c1_s1_torna.py`: new. Parser read-back checks.
- `docs/tasks/2026-11-03-c1s1-torna-on-babur1.md`: tick the checklist only.

Output goes to `out/v2/C1S1_Torna.aoe2scenario`. Do not write to `archive/`, `scenarios/` or the game folders;
the lead installs builds for play-testing.

## Stages (stop and hand off after each one marked GATE)
**A. Strip (GATE: human Quit test).** Load the template with `from_template`, delete all 130 triggers, remove
the objects listed as removed above, set active players to 3, write the file. No terrain or text changes yet.

**B. Map.** Remove P1's objects in the camp, place RS01's band; reassign Torna and outpost buildings to P2,
the village to P3; raise Murumbdev with `Mission.hill()` and call `Mission.smooth()` (8-neighbour, see
KNOWLEDGEBASE 1.1); set the mood to Spring. Place RS01's Torna garrison (killedar, spearmen, archers,
men-at-arms) inside the Torna box and the outpost army inside the outpost box, using RS01's compositions.

**C. Triggers and text (GATE: human play-test).** Recreate RS01's triggers with the existing helpers
(`story`, `objective`, `dead`, `cleared`, `present`, `handover`, `chain`, `victory`, `wave`, `hero_loss`,
`hero_setup`, `texts`) and RS01's exact strings. Recompute every area and spawn coordinate for this map:
Torna area = the Torna box, Rajgad area = 6 tiles around the Murumbdev centre, outpost area = the outpost box,
waves spawn just south of the outpost and march to Torna (waves 1 and 2) and Murumbdev (wave 3).

## Test cases (`tests/test_c1_s1_torna.py`, read the written file back with the parser; write these first)
1. After stage A: file loads; header version is the template's (1.55, not 1.59); dependency list `[2,3,4,5,6,7]`;
   0 triggers; 3 active players; no units owned by players 4 to 8.
2. After B: no two neighbouring tiles, diagonals included, differ by more than 1 in elevation.
3. After B: the Murumbdev centre tile has elevation ≥ 3 and a flag object within 1 tile.
4. After B: every P2 building lies inside the Torna box or the outpost box.
5. After B: P1 has exactly one unit named "Shivaji Raje"; no unit of any player is named with "Chhatrapati".
6. After C: objectives "Obj 1", "Obj 2", "Obj 3" exist in that order; Obj 2 is activated only by Obj 1, Obj 3
   only by Obj 2, "Victory" only by Obj 3.
7. After C: a loss trigger fires on the destruction of the "Shivaji Raje" unit and declares victory for P2.
8. After C: every display string equals the matching string in `src/m1_torna.py` at `d03840c` (compare the set).
9. Edge: Obj 3's `objects_in_area` box contains every P2 building outside the Torna box (none left uncovered).

Run: `.venv/bin/python -I -m pytest tests/test_c1_s1_torna.py` (pytest is not installed; if missing, write the
tests as plain asserts runnable with `.venv/bin/python -I tests/test_c1_s1_torna.py`).

## Done when
- [ ] Stage A file written, case 1 passes, handoff sent, lead and human confirm Quit works.
- [ ] Stage B and C done, all 9 cases pass 3 runs in a row, `tools/validate.py out/v2` prints ALL OK.
- [ ] Commit on `feat/c1s1-torna-template` (no push).
- [ ] `scripts/collab.sh handoff agy claude "feat/c1s1-torna-template · <stage> · <test result> · <anything unsure>"`
- [ ] `scripts/collab.sh release agy`

## Don'ts
- No new dependencies. No changes outside the file list. No background commands. One command per call.
- Do not edit any text string; text changes go through the expert review document first.
- Do not touch the game install folders or the official campaign files.
- Do not change `Mission.__init__`, `finish()` or any existing helper's behaviour.
