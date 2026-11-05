# Rise of Swarajya — AoE II DE campaign (1646–1689)

15 chapters in 5 acts. Chhatrapati Shivaji Maharaj builds Hindavi Swarajya (1–9); Chhatrapati Sambhaji Maharaj defends it (10–15).

## Install (Mac, Feral build)

Double-click `Install_Rise_of_Swarajya.command`.
If macOS blocks it: right-click → Open → Open.

It copies (never deletes):

- `archive/v1-generated/scenarios/RS01…RS15.aoe2scenario` → `…/Age of Empires 2 DE/<steam-id>/resources/_common/scenario/`
- `archive/v1-generated/Rise_of_Swarajya.aoe2campaign` → `…/resources/_common/campaign/`

Play: **Campaigns → Custom Campaigns → Rise of Swarajya**.
Single chapter: **Single Player → Skirmish → Game Mode: Scenario**.

If the campaign doesn't list (or the menu misbehaves), remove that one `.aoe2campaign` file and build it in-game:
**Editors → Campaign Editor → New → add RS01…RS15 in order → Save as "Rise of Swarajya"**.

Open `Rise_of_Swarajya_Codex.html` in any browser for the illustrated campaign book: maps, every briefing, dialogue, epilogue, heroes and history.

## Chapters

| # | Act | Chapter | Year |
|---|-----|---------|------|
| 1 | I The Foundation | The First Flame – Torna | 1646 |
| 2 | I | The Tiger of Pratapgad | 1659 |
| 3 | I | The Sacrifice of Pavan Khind | 1660 |
| 4 | II The Defiance | The Night of Shaista Khan | 1663 |
| 5 | II | The Wealth of Surat | 1664 |
| 6 | II | The Treaty of Purandar *(new)* | 1665 |
| 7 | II | The Great Escape – Agra | 1666 |
| 8 | III The Crown | The Lion of Sinhagad | 1670 |
| 9 | III | The Crown of Swarajya – Raigad | 1674 |
| 10 | IV The Storm | The Crown of Conflict *(new)* | 1680–81 |
| 11 | IV | The Riches of Burhanpur | 1681 |
| 12 | IV | The Lion Against the Empire – Ramsej | 1682 |
| 13 | V The Last Stand | The Island Fortress – Janjira | 1682 |
| 14 | V | The Gates of Goa | 1683 |
| 15 | V | The Flame That Would Not Die | 1689 |

## What changed from the first version

- **Crash fix.** Player colours were written as 1–8; the game expects 0–7. Saffron became invalid colour 8. Fixed in `aoe_lib.player()`.
- **Two new chapters:** Purandar (siege, Veer Murarbaji Deshpande's stand, treaty, decision to travel to Agra) and The Crown of Conflict (succession: win over Sarsenapati Hambirrao Mohite, rally forts, enter Raigad without civil war).
- **Cinematic openings:** dialogue with hero portraits, camera reveals of key locations, custom Maratha storyboard illustrations, and full spoken narration/voiceovers.
- **Epilogues** after every victory, like the original campaigns.
- **Heroes** with real stat boosts and lore text: Chhatrapati Shivaji Maharaj, Chhatrapati Sambhaji Maharaj, Rajmata Jijabai Aaisaheb, Veer Baji Prabhu Deshpande, Subhedar Tanaji Malusare, Veer Jiva Mahala, Veer Murarbaji Deshpande, Bahirji Naik, Sarnaubat Netaji Palkar, Sarsenapati Hambirrao Mohite, Kavi Kalash, and more.
- **Bahirji Naik's intelligence** reveals enemy camps and paths (Pratapgad, Lal Mahal, Surat).
- **Lighting per chapter:** monsoon mist, night, darkness, twilight.
- **Marathas civilization:** Gurjaras renamed "Marathas" with cavalry LOS, raiding vs buildings, cheaper infantry, stronger forts.
- Final chapter honours Dharmaveer Chhatrapati Sambhaji Maharaj and introduces Chhatrapati Rajaram Maharaj, Maharani Yesubai Aaisaheb, Senapati Santaji Ghorpade, Senapati Dhanaji Jadhav, and Maharani Tarabai Aaisaheb.

## Known limits

- Not play-tested in game yet. Expect balance tweaks.
- Custom briefing images can't be shown in DE's scenario screen, so maps live in the Codex.
- "Fort network" continuity between chapters is narrative only; AoE2 campaigns don't carry state between scenarios.
- Unit types can't be renamed per civ, so "Mavala", "Bargir", "Shiledar" stay design notes.
- Marathas use the Gurjaras civ (Dynasties of India DLC); enemies use Persians, Hindustanis, Ethiopians, Portuguese, Britons.

## Regenerate

`src/` holds the generator (AoE2ScenarioParser 0.9.8). `python campaign.py` rebuilds all 15 scenarios and the campaign file into `out/campaign`.
