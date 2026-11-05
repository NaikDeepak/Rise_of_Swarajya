# v1-generated: the fully generated 15-chapter campaign

These scenarios were built entirely by the Python generator in `src/` (AoE2ScenarioParser writes every map, unit
and trigger from scratch). They are archived, not deleted, because:

- They quit with a long stall on "Game Paused (F3)" that we could not trace to a single setting
  (see `docs/KNOWLEDGEBASE.md`). Official scenarios opened and re-saved by the same tool quit cleanly.
- The campaign is being rebuilt chapter by chapter on top of official scenarios as templates
  (see `docs/official-maps.md` and `docs/tasks/`).

The story, dialogue and history text in `src/` stay the source for the new chapters; see the expert review
document for their trace IDs.

- Git tag `v1-generated` marks the last commit before this move.
- `Install_Rise_of_Swarajya.command` still installs this version until new chapters replace it.
- `cd src && ../.venv/bin/python campaign.py` still rebuilds it into this folder.
