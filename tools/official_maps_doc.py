"""Render docs/official-maps.md from docs/data/official_maps.jsonl (made by scan_official_maps.py)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = [json.loads(l) for l in open(os.path.join(ROOT, "docs", "data", "official_maps.jsonl"))]
ok = [r for r in rows if r["readable"]]
bad = [r for r in rows if not r["readable"]]

def fits(r):
    """Rough map-type tags for the Rise of Swarajya template library. A starting point, not a verdict."""
    t = []
    if r["enemy_castles_raised"] and r["raised_pct"] >= 8 and r["water_pct"] < 30: t.append("hill fort")
    if r["jungle_pct"] >= 20 or (r["green_pct"] >= 60 and r["raised_pct"] >= 15): t.append("Sahyadri/jungle")
    if r["water_pct"] >= 25: t.append("coastal")
    if r["raised_pct"] < 6 and r["water_pct"] < 15 and r["jungle_pct"] < 10: t.append("open field")
    if r["snow_pct"] >= 20: t.append("snow (repaint)")
    if r["desert_pct"] >= 30: t.append("desert (repaint)")
    return ", ".join(t)

def score_hill_fort(r):
    return (15 * (r["enemy_castles_raised"] > 0) + min(r["raised_pct"], 40) + 0.8 * r["jungle_pct"]
            + 0.3 * r["green_pct"] - 0.5 * r["water_pct"] - 0.5 * r["desert_pct"] - 0.6 * r["snow_pct"])

def short(r):
    return (f"| {r['scenario']} | {r['size']} | {r['raised_pct']}% | {r['jungle_pct']}% | {r['green_pct']}% | "
            f"{r['water_pct']}% | {r['enemy_castles']} ({r['enemy_castles_raised']} raised) | {r['players']} | "
            f"{r['triggers']} | {r['mood'] or 'Default'} | {', '.join(r['civs'][:3])} |")

H = ("| Scenario | Size | Raised | Jungle | Green | Water | Enemy castles | Players | Triggers | Mood | First civs |\n"
     "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
out = ["# Official scenario catalog",
       "",
       f"Every scenario in the official AoE2 DE campaigns on this Mac: {len(rows)} scenarios, {len(ok)} readable by our tool "
       "(AoE2ScenarioParser 0.9.8). Use it to pick a template map for a chapter without re-scanning the game files.",
       "",
       "Regenerate after a game update:",
       "",
       "```",
       ".venv/bin/python -I tools/scan_official_maps.py   # about 45 s, writes docs/data/official_maps.jsonl",
       ".venv/bin/python -I tools/official_maps_doc.py    # rewrites this page",
       "```",
       "",
       "## Columns",
       "",
       "- **Raised:** share of tiles at elevation 3 or more. A high number can mean a whole raised plateau rather than separate hills, so check the minimap.",
       "- **Jungle / Green / Water:** share of tiles with jungle, bamboo or rainforest; grass or forest; water, shallows or beach. Dirt counts as neither green nor desert.",
       "- **Enemy castles (raised):** castles owned by players 2 to 8, and how many stand at elevation 3 or more.",
       "- **Triggers:** trigger count; a rough guide to how much scripting there is to reuse or strip out.",
       "- **Tags:** rough map types from these numbers, a starting point only.",
       "",
       "To see a map, render its minimap: extract the scenario from its `.aoe2campaign` (see `extract()` in `tools/scan_official_maps.py`), then run `src/verify.py`'s `check(path, png)`.",
       "",
       "## Shortlist: hill fort (Torna, Pratapgad, Sinhagad, Gingee)",
       "",
       "Top 12 by a hill-fort score: an enemy castle on high ground, raised ground, green or jungle terrain, little water, desert or snow.",
       "", H]
out += [short(r) for r in sorted(ok, key=score_hill_fort, reverse=True)[:12]]
out += ["", "## Shortlist: coastal (Janjira, Goa, Konkan)", "", H]
out += [short(r) for r in sorted([r for r in ok if r["water_pct"] >= 25], key=lambda r: (r["jungle_pct"] + r["green_pct"]), reverse=True)[:10]]
out += ["", "## Shortlist: jungle and green valleys (Javali, Pavan Khind, ambushes)", "", H]
out += [short(r) for r in sorted(ok, key=lambda r: r["jungle_pct"] * 2 + r["green_pct"] - r["water_pct"], reverse=True)[:10]]
out += ["", "## Shortlist: open field (Salher, Burhanpur, field battles)", "", H]
out += [short(r) for r in sorted([r for r in ok if r["raised_pct"] < 6 and r["water_pct"] < 15], key=lambda r: r["green_pct"], reverse=True)[:10]]
out += ["", "## All readable scenarios", "",
        "| Campaign | Ch | Scenario | Size | Raised | Jungle | Green | Water | Desert | Snow | Castles (raised) | Players | Triggers | Mood | Tags | Objectives (first two) |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
for r in ok:
    objs = " / ".join(o.lstrip("+- ")[:90] for o in r["objectives"][:2]).replace("|", "/")
    out.append(f"| {r['campaign']} | {r['chapter']} | {r['scenario']} | {r['size']} | {r['raised_pct']}% | {r['jungle_pct']}% | "
               f"{r['green_pct']}% | {r['water_pct']}% | {r['desert_pct']}% | {r['snow_pct']}% | {r['enemy_castles']} ({r['enemy_castles_raised']}) | "
               f"{r['players']} | {r['triggers']} | {r['mood'] or 'Default'} | {fits(r)} | {objs} |")
out += ["", "## Not readable by our tool", "", "These cannot be used as templates with AoE2ScenarioParser 0.9.8.", "",
        "| Campaign | Scenario | Error |", "| --- | --- | --- |"]
out += [f"| {r['campaign']} | {r['scenario']} | {r['error'][:90]} |" for r in bad]
out += ["", "The Viking campaign (`nocam1` to `nocam3`) and other newer DLC campaigns ship as packed `.gpv` files and are not in this catalog.", ""]
open(os.path.join(ROOT, "docs", "official-maps.md"), "w").write("\n".join(out))
print("wrote docs/official-maps.md:", len(out), "lines")
