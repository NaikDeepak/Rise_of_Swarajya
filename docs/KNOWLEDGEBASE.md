# Rise of Swarajya: Knowledge Base

What has broken in this campaign, why, and how it was fixed. Read this before you change
`src/aoe_lib.py`, add triggers, place units or edit the in-game text. Every entry lists the
symptom, the cause, the fix and the rule to follow from now on.

Last updated 2026-11-03. Add new entries at the end of the matching section.

---

## 0. Build and verify (how to work on this repo)

| Step | Command | Notes |
|---|---|---|
| Build all 15 scenarios + campaign | `cd src && ../.venv/bin/python campaign.py` | Use the project venv; system `python3` has no `AoE2ScenarioParser` (pinned 0.9.8). Copies scenarios to `scenarios/`, both `.aoe2campaign` files to the repo root and syncs everything into the Mac Feral game profile. |
| Rebuild slideshows + narration | `cd src && ../.venv/bin/python build_assets.py` | ~2.5 min. Regenerates `Rise_of_Swarajya.json` / `Rise of Swarajya.json` (slide text), slide PNGs and narration `.wem` via macOS `say`. Run `campaign.py` again afterwards so the new JSON and audio reach the game folder. |
| Inspect one scenario | `cd src && ../.venv/bin/python verify.py <file>` | Prints a summary and renders a minimap PNG. |
| Lint scenarios | `.venv/bin/python tools/validate.py scenarios` | Checks player colours, units out of bounds, broken trigger links, effects/conditions that point at missing units, and messages that are too long. Prints `ALL OK` when clean. It does **not** check elevation (1.1) or object IDs (1.2). |

- Builds are deterministic (fixed seeds), so a rebuild with no source change leaves the binaries unchanged.
- `assets/sounds/*.wem`, `assets/textures/`, `out/` and `backups/` are gitignored. Only `assets/sounds/vo_durations.json` is tracked.
- Never delete game files: move superseded ones to `backups/` (see `backups/README.md`).
- `Rise_of_Swarajya_Codex.html` is **not** rebuilt by the pipeline. `tools/codex.py` needs a meta JSON and a maps folder that are not in the repo, so the Codex is out of date (old hint text, 600 instead of 750 gold per bazaar, 9 em dashes).

---

## 1. Freezes and crashes (highest priority)

The engine on the Mac Feral build has no error dialog. Bad data usually shows up as a hard
**freeze** (game stops responding) or a crash, often minutes into a mission, far from the cause.

### 1.1 Diagonal elevation jump freezes the game
- **Symptom:** mid-game freeze, especially when the camera or units move over hills.
- **Cause:** `Mission.smooth()` only compared the 4 orthogonal neighbours, so two
  diagonal tiles could differ by 2 elevation levels. A diagonal jump of 2 sends the
  engine's screen-to-tile lookup into an endless loop.
- **Fix:** `smooth()` now checks all 8 neighbours (`src/aoe_lib.py`, commit `bd43804`, PR #1).
- **Rule:** neighbouring tiles, **diagonals included**, may differ by at most 1 elevation.
  Always call `smooth()` after `hill()` / `ridge()` / `fort_on_hill()`, and never write
  `tile.elevation` directly without re-smoothing.

### 1.2 Non-standard DLC unit crashes on line of sight
- **Symptom:** crash in RS01 when the player's units came near Torna fort.
- **Cause:** unit 2289 (`O.TREASURE_CHEST`) is a DLC/non-standard object. It crashed when it came into line of sight.
- **Fix:** replaced with `O.RELIC` (285) (`src/m1_torna.py`, commit `e5c2d4d`).
- **Rule:** place only base-game object IDs that official DE campaigns use. If a constant in
  AoE2ScenarioParser has a high or unfamiliar ID, check that it exists in the Feral build before using it.

### 1.3 Dialogue triggers that move the camera, play sounds or spawn objects
- **Symptom:** freezes during story dialogue.
- **Causes and history:**
  1. Dialogue used `change_view` to pan the camera. This yanked and locked the camera. It was replaced with a `MAP_REVEALER` spawn at the line's coordinates.
  2. Those revealer spawns, plus `play_sound` with custom `sw_vo_*` voice files that are
     **not in any Wwise sound bank**, and a `send_chat` copy of every line, still caused freezes.
- **Fix (commit `2f210e1`):** `Mission.line()` is now one `display_instructions` effect (text,
  portrait, duration) with no sound, chat or object spawn. `_cam_move()` is a no-op. `story()`
  chains lines the way official DE campaigns do: line N+1's trigger is activated by line N and waits for N's display time.
  Commit `2eadd68` then removed the leftover `(x, y)` camera tuple from RS01 Tanaji's line.
- **Rule:** dialogue triggers only display text. Don't add `play_sound` (custom audio is unbanked),
  `send_chat`, `change_view` or `create_object` to a dialogue line. Reveal map areas with an explicit
  `m.reveal()` in its own trigger, after the story chain ends (see 2.1).
- **Note:** `BACKLOG.md` Phase 1 and 5 still say chat logging and in-game character voiceovers were
  added. Both were removed by this fix. In-game VO is off (`VO_REGISTRY` stays empty). Only the slideshow narration plays audio.
- **Note:** tuples like `(speaker, text, (x, y))` in `story()` are still accepted, but the coordinates are ignored.

### 1.4 "AI Defensive Stance" trigger removed
- **What:** a timer trigger that set every AI player's units to defensive stance at t=1 was removed in `2f210e1` as part of the freeze cleanup.
- **Rule:** keep garrisons in place with the Immobile AI (see 3.1), not stance triggers.

### 1.5 Stuck on "Game Paused" after Resign / Quit
- **Symptom:** after Resign, Quit Current Game or Victory, the game hung on "Game Paused" instead of returning to the campaign map.
- **Cause:** on return, the engine reloads the campaign by its internal 256-byte `CAMPAIGN_NAME`
  (`Rise of Swarajya`, **with spaces**) from `resources/_common/campaign/Rise of Swarajya.aoe2campaign`. Only the underscored file existed.
- **Fix (commits `ebe4218`, `dc28037`):** ship both `Rise of Swarajya.aoe2campaign` and
  `Rise_of_Swarajya.aoe2campaign`, and set each scenario's metadata tuple to `(fn, fn)` like official campaigns do.
- **Rule:** keep both filenames in sync. `campaign.py` writes both. Never rename the campaign without renaming every file the engine looks up.

### 1.6 Scenario loss text hangs Quit on "Game Paused"
- **Symptom:** Quit (Quit Current Game, Resign) hung on "Game Paused (F3)". Every scenario in
  `archive/v1-generated/` did it, and so did C1-S1 rebuilt on the official Babur 1 map. Not fixed by 1.5.
- **Cause:** the scenario's **loss text** (`message_manager.loss`, set by `Mission.texts(loss=...)`).
  Quitting counts as a defeat and the engine hangs showing it. Official campaigns leave it empty.
- **How it was found (2026-11-05, in-game bisection on Babur 1, Mac Feral build):** stage A (no triggers) and
  stage B (map and units) quit fine. Trigger groups and single triggers all quit fine (tests 7-12).
  `texts()` alone stalled (13). Instructions, history, hints and victory text alone were fine (15-17, 20);
  loss text alone stalled (19). Full Torna with every trigger and text except the loss text quit fine (21).
  Clearing the hints/scouts string-table ids did not help (14).
- **Fix:** `Mission.texts()` accepts `loss` but always writes an empty loss text (`src/aoe_lib.py`).
  The defeat message comes from the loss trigger (`hero_loss`). `tools/validate.py` flags a set loss text.
- **Rule:** never set the scenario loss text. Put defeat messages in the trigger that declares the defeat.
  The victory text is safe.

---

## 2. Triggers and pacing

### 2.1 Side lines overwriting the opening dialogue
- **Symptom:** Bahirji Naik's intel line (RS02, RS04, RS05) appeared on top of the opening story.
- **Fix:** chain those triggers after `m.story()` returns its last trigger, with `timer=8`.
- **Rule:** any line that should follow the story goes in `m.chain(last_story_trigger, t)`, never on an independent timer.

### 2.2 Repeating waves firing too early
- **Fix:** `Mission.wave()` adds a start-gate trigger when `after > repeat_every`, so the first wave waits `after` seconds.

---

## 3. AI, load time and scripts

### 3.1 Garrisons leaving their forts, and slow scenario loads
- **Symptom:** AI garrisons walked out of their forts. Scenarios took a long time to load because the engine compiled the full standard skirmish AI for 7 players.
- **Fix (commits `dc28037`, `4dfb021`):** players 2 to 8 use `Fe Immobile AI` (`human=False`,
  `ai_type=0`, `personality="Fe Immobile AI.ai"`). The `.per` is embedded in `Files.ai_files` and
  `PlayerDataTwo.ai_files` stays empty. `assets/ai/Fe Immobile AI.ai` and `.per` are synced to `resources/_common/ai/`.
- **Script syntax:** the first `.per` used an undefined fact (`sn-Wonders-on-map`) and drop distances of `0`. It now copies Forgotten Empires' official definition (drop distances `-2`, `sn-number-explore-groups 0`).
- **Rule:** copy AI script content from an official DE campaign file. Don't write `.per` rules from memory. A syntax error there fails silently.

---

## 4. Soft-locks (mission cannot be finished)

| Mission | Problem | Fix |
|---|---|---|
| RS05 Surat | 6 bazaars x 600 gold left little margin for the 3000 gold objective | 750 gold per bazaar (4500 total) |
| RS07 Agra | Neutral Rajput guards body-blocked the path to the baskets | Wider palisade gaps `(70, 90, 110)`, guards moved to `(35, 58)` |
| RS08 Sinhagad | Mavalas left below the cliff when Tanaji reached the rope first | Larger `teleport_area` source rect `(10, 30, 40, 98)` |
| RS10 Accession | Objective needed two fragile watch towers alive at once | Trigger variables (var 1, var 2) record each fort visit |
| RS01 Torna | "Seize Torna" needed a stricter win condition | Objective needs `dead(killedar)` + `cleared(torna)` + `present(player 1)` |

- **Rule:** every objective must stay reachable if a fragile object dies or a unit wanders. Prefer
  "has visited" variables over "is still alive" conditions. Give resource goals at least 1.5x headroom.

## 5. Map and placement

- **Docks on land:** `B.DOCK` / `B.HARBOR` are in `_ship_units`, so `Mission.unit()` places them on water.
- **Gaia resources:** `Mission.finish()` adds gold, stone, forage and deer clusters on open flat ground, away from paths.

---

## 6. Campaign UI, slideshows and assets

- **Slideshow lookup:** the engine opens `<CAMPAIGN_NAME>.json` (`Rise of Swarajya.json`, with spaces)
  and reads `Scenarios[idx].IntroSequence` / `OutroSequence`. `build_assets.py` writes both the spaced and underscored names. Keep both.
- **Slide text** is read from the built scenarios (history, first two story lines, victory text,
  epilogue). Edit the mission source, not the JSON. Then run `build_assets.py` followed by `campaign.py`.
- **Narration cache:** each slide set's audio is keyed by an MD5 of its text in `vo_durations.json`. Changing the text re-synthesises only that set.
- **TTS spelling:** `clean_tts_text()` in `build_assets.py` respells Marathi names for the macOS voice. Add new names there if the narrator says them wrong.
- **Layout:** chapter buttons use `"Type": "CampaignTitle"` with `"ClippingOverride": "Background"`. The custom map is `swarajya_map.dds` (5672x2160, DXT1), registered as `CampaignBackgroundSwarajya`.

---

## 7. Writing style for in-game text

### 7.1 Cultural rules (no *Ekeri Ullekh*)
- Always use full honorifics: **Chhatrapati Shivaji Maharaj** (or Shivaji Raje), **Chhatrapati Sambhaji
  Maharaj** (or Sambhaji Raje), **Rajmata Jijabai Aaisaheb**, **Maharani Yesubai Aaisaheb**, **Maharani Tarabai Aaisaheb**, and so on.
- No derogatory enemy epithets ("mountain rat", "rebel" and the like). Narrate martyrdoms with respect.
- Slideshow art comes only from the curated whitelist in `build_assets.py` (no demon/rakshasa or Mughal backgrounds).

### 7.2 Avoid machine-written tells (PR #2)
Text that reads as AI-generated breaks immersion. When writing or reviewing dialogue:
- **No em or en dashes** (`—`, `–`). Use a full stop, comma or colon. Slide titles use `Act | Title`.
- **No puffery:** "stands resplendent", "supreme statecraft", "guiding light", "ignited a sacred fire",
  "glorious", "immortal", "History bows forever". Say what happened.
- **No set-piece patterns:** "X, and not Y", "Instead, ...", "Every hill, every valley, and every ...", "not just X but Y".
- **Avoid stock words:** pivoting, testament, tapestry, delve, beacon, realm (except in character), journey.
- Keep Marathi quotes, but give the translation as its own sentence: `'Gad aala, pan Sinha gela.' The fort is won, but the Lion is gone.`
- **Check dates.** PR #2 fixed an epilogue that had the Bhagwa Dhwaj at Attock by 1707. That happened in 1758.
- **Check after editing:** grep the source with `grep -n "—\|–" src/*.py` (only `clean_tts_text` should match), then scan the built scenarios and the slideshow JSON.

---

## 8. Debugging checklist for a new freeze or crash

1. Note the mission, the in-game minute and what was on screen (dialogue, camera position, units in view).
2. Bisect the triggers: disable trigger groups in the source, rebuild and replay. Freezes are usually trigger effects (section 1.3) or map data (section 1.1).
3. Look for objects that are new or non-standard near the spot (section 1.2).
4. Compare the suspect effect's fields with an official DE campaign (`incam*`, `rcam*`, `acam*`). `Mission.finish()` already sets unused effect fields to `-1` to match them.
5. Write the result up here as a new entry: symptom, cause, fix, commit, rule.
