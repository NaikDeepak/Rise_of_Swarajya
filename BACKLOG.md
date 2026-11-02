# Rise of Swarajya — Campaign Backlog & Status Tracker

Status Legend:
- `[DONE]` — Implemented, built, and synced to the in-game folder
- `[IN PROGRESS]` — Currently being tested or actively worked on
- `[TODO]` — Planned next (ordered by priority)

---

## Phase 1: Core Engine, Custom Campaign UI & Chapter 1 Stability
- `[DONE]` **GitHub Repository Setup:** Created public repository [`NaikDeepak/Rise_of_Swarajya`](https://github.com/NaikDeepak/Rise_of_Swarajya) and pushed codebase.
- `[DONE]` **Auto-Sync Build Pipeline (`src/campaign.py`):** Automatically copies all 15 `.aoe2scenario` files, `Rise_of_Swarajya.aoe2campaign`, `Rise_of_Swarajya_layout.json`, and `Rise_of_Swarajya.json` directly into the active Steam profile folder (`76561198054484915/resources/_common/scenario` and `.../campaign`).
- `[DONE]` **Single Custom Campaign Entry & Map Layout:** Generated `Rise_of_Swarajya_layout.json` (15 chapter nodes on `CampaignBackground35Rajendra`) and `Rise_of_Swarajya.json` (pre/post-mission `SlideShow` storyboards for all 15 chapters), and removed duplicate `.aoe2campaign` copies across `scenario/`, `campaign/`, and `0/`.
- `[DONE]` **Official DE Trigger Binary Sanitization (`src/aoe_lib.py`):** Sanitized unused `operation` and `variable` fields on all trigger effects to `-1` in `Mission.finish()` to match official AoE2 DE campaign binaries (`incam2`, `rcam1`, `acam1`).
- `[DONE]` **Official DE Chat History Logging (`src/aoe_lib.py`):** Added `send_chat` alongside `display_instructions` in `Mission.line()` so all character dialogue persists in the in-game Chat History log just like official campaigns.
- `[IN PROGRESS]` **Fix Camera/Dialogue Freeze in Chapter 1 (`RS01_The_First_Flame`):** Replaced `change_view` (`_cam_move`) during dialogue with `O.MAP_REVEALER` at target coordinates `(60, 40)` so Torna Fort is revealed on the map/minimap when Tanaji speaks without yanking or locking the player's camera. *(Ready for in-game verification)*

---

## Phase 2: Dialogue & Timing Collisions (Official Campaign Pacing)
- `[TODO]` **`RS02_The_Tiger_of_Pratapgad` (`src/shivaji_missions.py`):** Chain `Bahirji Naik: intel` trigger after `m.story()` finishes (currently fires at `t=25s` and overwrites `Story 3`/`Story 4` on `PanelLocation.TOP`).
- `[TODO]` **`RS04_The_Night_of_Shaista_Khan` (`src/shivaji_missions.py`):** Chain `Bahirji Naik: intel` trigger after `m.story()` finishes (currently fires at `t=25s` and overwrites `Story 3` on `PanelLocation.TOP`).
- `[TODO]` **`RS05_The_Wealth_of_Surat` (`src/shivaji_missions.py`):** Chain `Bahirji Naik: intel` trigger after `m.story()` finishes (currently fires at `t=40s` and overwrites `Story 4` on `PanelLocation.TOP`).

---

## Phase 3: Gameplay Soft-Lock Fixes
- `[TODO]` **`RS05_The_Wealth_of_Surat` (`src/shivaji_missions.py`):** Prevent gold-spending soft-lock in Objective 1 (*"Accumulate 2500 gold"*). Either require destroying all 3 Mughal Treasury buildings to claim the tribute or disable gold-spending buildings until Objective 1 completes.
- `[TODO]` **`RS07_The_Great_Escape` (`src/shivaji_missions.py`):** Widen Ram Singh's haveli palisade entrance (`gaps=(70, 90, 110)`) and move the 4 neutral Rajput `U.LONG_SWORDSMAN` guards away from `(18, 94)` so they don't body-block Shivaji from reaching the Kachhwaha horses at `(18, 92)`.
- `[TODO]` **`RS08_The_Lion_of_Sinhagad` (`src/shivaji_missions.py`):** Expand the `teleport_area` source rectangle on the Donagiri cliff climb (`(14, 34, 40, 96)`) so trailing Mavalas aren't stranded below the cliff when Tanaji reaches the rope first.
- `[TODO]` **`RS10_The_Crown_of_Conflict` (`src/sambhaji_missions.py`):** Use trigger variables (`visited_rajgad`, `visited_pratapgad`) when Sambhaji reaches each fort instead of requiring both fragile `B.WATCH_TOWER` flags to stay alive simultaneously under Diler Khan's cavalry raids.

---

## Phase 4: Economy, Gaia Resource Deposits & Naval Terrain Fixes
- `[TODO]` **Naval `B.DOCK` Water Placement Bug (`src/aoe_lib.py`):** Exclude `B.DOCK` from `self._land_units` in `Mission.unit()` and ensure a `3x3` patch around docks is `T.WATER_MEDIUM` / `T.SHALLOWS` so Docks in `RS06`, `RS13`, and `RS14` can build and repair ships.
- `[TODO]` **Gaia Resource Deposits (`src/common.py`, `src/m1_torna.py`, `src/shivaji_missions.py`, `src/sambhaji_missions.py`):** Add `gold_mine()`, `stone_mine()`, `forage_patch()`, `deer_herd()`, and `fish_patch()` helpers and populate economy missions (`RS01`, `RS06`, `RS09`, `RS12`, `RS13`, `RS14`) with realistic mineable gold/stone, berries, huntables, and coastal fish.

---

## Phase 5: Roster Variety, AI Waves & Polish
- `[TODO]` **Gurjaras Roster in `maratha_identity()` (`src/common.py`):** Add `U.CAMEL_RIDER`, `U.CHAKRAM_THROWER`, and `U.ARMORED_ELEPHANT` / `U.SIEGE_ELEPHANT` to `maratha_identity()` so the Gurjaras civilization bonuses apply to the player's army.
- `[TODO]` **Fix `Mission.wave()` Initial Delay (`src/aoe_lib.py`):** When `repeat_every` is passed to `m.wave()`, wait `after` seconds before the first wave and then repeat every `repeat_every` seconds (currently overwrites `after` and spawns the first wave at `t=60s`).
- `[TODO]` **Fix `hero_setup()` Multi-Unit Targeting (`src/aoe_lib.py`):** Pass `selected_object_ids=ids` (and `source_player=pid`) to `change_object_description` so heroes sharing a base unit constant (e.g., `Gaga Bhatta` and `Sant Tukaram` in `RS09`) don't overwrite each other's descriptions.
- `[TODO]` **Continuous AI Pressure / Production (Official Campaign Style):** Add repeating unit patrols/reinforcements tied to enemy production buildings (Barracks/Stables/Castles) so enemies remain active until their bases are destroyed.

---

## Optional Enhancements / User Notes
*(Add any new ideas, balance notes, or bug reports below)*
- `[TODO]` *(Optional)* Custom Maratha storyboard slide artwork (`.dds` converted from PNG/JPG).
- `[TODO]` *(Optional)* Narrator / character voiceover audio files (`.wem` / `.wav`) for storyboards and in-game dialogue.

