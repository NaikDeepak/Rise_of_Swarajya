# Rise of Swarajya — Campaign Backlog & Status Tracker

Status Legend:
- `[DONE]` — Implemented, built, and synced to the in-game folder
- `[IN PROGRESS]` — Currently being tested or actively worked on
- `[TODO]` — Planned next (ordered by priority)

---

## Phase 1: Core Engine, Custom Campaign UI & Chapter 1 Stability
- `[DONE]` **GitHub Repository Setup:** Created public repository [`NaikDeepak/Rise_of_Swarajya`](https://github.com/NaikDeepak/Rise_of_Swarajya) and pushed codebase.
- `[DONE]` **Auto-Sync Build Pipeline (`src/campaign.py`):** Automatically copies all 15 `.aoe2scenario` files, `Rise_of_Swarajya.aoe2campaign`, `Rise_of_Swarajya_layout.json`, `Rise_of_Swarajya.json`, storyboard `.png` textures, and Wwise `.wem` audio files directly into the active Steam profile folder (`76561198054484915/`) and `AgeOfEmpires2Data/`.
- `[DONE]` **Single Custom Campaign Entry & Map Layout:** Generated `Rise_of_Swarajya_layout.json` (15 chapter nodes on `CampaignBackground35Rajendra`) and `Rise_of_Swarajya.json` (pre/post-mission `SlideShow` storyboards for all 15 chapters), and removed duplicate `.aoe2campaign` copies across `scenario/`, `campaign/`, and `0/`.
- `[DONE]` **Official DE Trigger Binary Sanitization (`src/aoe_lib.py`):** Sanitized unused `operation` and `variable` fields on all trigger effects to `-1` in `Mission.finish()` to match official AoE2 DE campaign binaries (`incam2`, `rcam1`, `acam1`).
- `[DONE]` **Official DE Chat History Logging (`src/aoe_lib.py`):** Added `send_chat` alongside `display_instructions` in `Mission.line()` and `Mission.say()` so all character dialogue and objective alerts persist in the in-game Chat History log just like official campaigns.
- `[DONE]` **Fix Camera/Dialogue Freeze in Chapter 1 (`RS01_The_First_Flame`):** Replaced `change_view` (`_cam_move`) during dialogue with `O.MAP_REVEALER` at target coordinates `(60, 40)` so Torna Fort is revealed on the map/minimap when Tanaji speaks without yanking or locking the player's camera.
- `[DONE]` **Fix AI Garrison Abandoning Forts (`src/aoe_lib.py`, `src/m1_torna.py`):** Set `p.set_immobile_ai()` on AI players in `Mission.player()` so garrisons hold their posts and only fight when approached, and updated `RS01` `o1` to require `m.dead(o1, killedar)` + `m.cleared(o1, 2, torna)` + `m.present(o1, 1, torna)`.

---

## Phase 2: Dialogue & Timing Collisions (Official Campaign Pacing)
- `[DONE]` **`RS02_The_Tiger_of_Pratapgad` (`src/shivaji_missions.py`):** Chained `Bahirji: Jawali paths` trigger (`timer=8s`) after `m.story()` finishes so it never overwrites opening dialogue or voiceovers.
- `[DONE]` **`RS04_The_Night_of_Shaista_Khan` (`src/shivaji_missions.py`):** Chained `Bahirji: Pune lanes` trigger (`timer=8s`) after `m.story()` finishes.
- `[DONE]` **`RS05_The_Wealth_of_Surat` (`src/shivaji_missions.py`):** Chained `Bahirji: Surat map` trigger (`timer=8s`) after `m.story()` finishes.

---

## Phase 3: Gameplay Soft-Lock Fixes
- `[DONE]` **`RS05_The_Wealth_of_Surat` (`src/shivaji_missions.py`):** Increased gold per looted bazaar from `600` to `750` (4,500 total across 6 bazaars for a 3,000 gold objective) so the player cannot be soft-locked.
- `[DONE]` **`RS07_The_Great_Escape` (`src/shivaji_missions.py`):** Widened Ram Singh's haveli palisade entrance (`gaps=(70, 90, 110)`) and moved the 4 neutral Rajput `U.LONG_SWORDSMAN` guards away from `(42, 60)` to `(35, 58)` so they never body-block Chhatrapati Shivaji Maharaj from reaching the kitchen baskets.
- `[DONE]` **`RS08_The_Lion_of_Sinhagad` (`src/shivaji_missions.py`):** Expanded the `teleport_area` source rectangle on the Donagiri cliff climb (`(10, 30, 40, 98)`) so trailing Mavalas aren't stranded below the cliff when Subhedar Tanaji Malusare reaches the rope first.
- `[DONE]` **`RS10_The_Crown_of_Conflict` (`src/sambhaji_missions.py`):** Used trigger variables (`var 1` and `var 2`) when Chhatrapati Sambhaji Maharaj visits Rajgad and Pratapgad instead of requiring both fragile `B.WATCH_TOWER` flags to stay alive simultaneously under Diler Khan's cavalry raids.

---

## Phase 4: Economy, Gaia Resource Deposits & Naval Terrain Fixes
- `[DONE]` **Naval `B.DOCK` Water Placement Bug (`src/aoe_lib.py`):** Included `B.DOCK` and `B.HARBOR` in `self._ship_units` in `Mission.unit()` so Docks in `RS05`, `RS06`, `RS13`, and `RS14` sit on water (`T.WATER_MEDIUM`) and can build/repair ships.
- `[DONE]` **Gaia Resource Deposits (`src/aoe_lib.py`):** Automatically populate safe, non-blocking clusters of `O.GOLD_MINE`, `O.STONE_MINE`, `O.FORAGE_BUSH`, and `U.DEER` on open flat terrain in `Mission.finish()` across all missions.

---

## Phase 5: Roster Variety, AI Waves & Multimedia Polish
- `[DONE]` **Gurjaras Roster in `maratha_identity()` (`src/common.py`):** Added `U.CAMEL_SCOUT`, `U.CAMEL_RIDER`, `U.HEAVY_CAMEL_RIDER`, `U.CHAKRAM_THROWER`, `U.ELITE_CHAKRAM_THROWER`, `U.ELEPHANT_ARCHER`, `U.ELITE_ELEPHANT_ARCHER`, `U.ARMORED_ELEPHANT`, and `U.SIEGE_ELEPHANT` to `maratha_identity()`.
- `[DONE]` **Fix `Mission.wave()` Initial Delay (`src/aoe_lib.py`):** Added a start-gate trigger when `repeat_every` is passed and `after > repeat_every` so repeating waves wait `after` seconds before the first wave.
- `[DONE]` **Custom Maratha Storyboard Illustrations (`src/build_assets.py`):** Generated `2000x1048` ink-on-parchment storyboard PNG sequences (`textures/campaign/swarajya/<1..15>/intro/%d.png` & `.../outro/%d.png`) with Maratha fort battlements, Bhagwa Dhwaj banners, and octagonal Rajmudra seals over authentic Indian parchment backgrounds (`fcam6/prithviraj_background.dds`, `incam2/rajendra_background.dds`, `incam3/devapala_background.dds`).
- `[DONE]` **Narrator & Character Voiceover Audio (`src/build_assets.py`, `src/aoe_lib.py`):** Generated 30 storyboard narration `.wem` files (`rs01_intro.wem`–`rs15_outro.wem`) with slide durations matched to the audio, plus in-game character dialogue `.wem` voiceover files (`sw_vo_*.wem`) hooked into `Mission.line()` with distinct voices per speaker.

---

## Phase 6: Cultural Reverence & Strict Honorifics (No *Ekeri Ullekh*)
- `[DONE]` **Full Honorifics Across All 15 Chapters (`src/m1_torna.py`, `src/shivaji_missions.py`, `src/sambhaji_missions.py`, `README.md`):** Eliminated every bare first-name reference (*Ekeri Ullekh*) across all hero names, dialogues, narrations, objectives, history texts, hints, victory/loss texts, and docs. Every mention now uses full reverent titles: **Chhatrapati Shivaji Maharaj** (or **Shivaji Raje**), **Chhatrapati Sambhaji Maharaj** (or **Sambhaji Raje**), **Rajmata Jijabai Aaisaheb**, **Shahaji Raje Bhosale**, **Chhatrapati Rajaram Maharaj** (or **Rajaram Raje**), **Maharani Yesubai Aaisaheb**, **Maharani Tarabai Aaisaheb**, and **Maharani Soyarabai**.
- `[DONE]` **Removed All Derogatory Enemy Remarks:** Removed all disrespectful enemy epithets (`"mountain rat"`, `"rebel"`, `"boy playing at forts"`, `"jagirdar's son"`, and Annaji Datto's `"rash"` remark) and ensured the martyrdom of **Dharmaveer Chhatrapati Sambhaji Maharaj**, **Veer Baji Prabhu Deshpande**, **Veer Murarbaji Deshpande**, **Subhedar Tanaji Malusare**, **Veer Shiva Kashid**, and **Senapati Mhaloji Ghorpade** is narrated with the highest reverence.
- `[DONE]` **Curated Noble Storyboard Artwork (`src/build_assets.py`):** Replaced unverified pool selection with a strictly verified whitelist of 13 noble Indian king/warrior/cavalry/temple/fleet ink-wash illustrations (excluding all demon/rakshasa myth slides and Mughal backgrounds).

---

## User Playtest Notes / Future Additions
*(Add any playtest feedback or new ideas below)*
