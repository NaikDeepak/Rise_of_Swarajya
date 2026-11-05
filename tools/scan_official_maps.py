"""Catalogue every official AoE2 DE campaign scenario on this machine.

Writes docs/data/official_maps.jsonl (one JSON object per scenario). Each scenario is parsed in its
own process: AoE2ScenarioParser keeps version state between files, so parsing many files in one
process makes later ones fail with false version errors.

Usage: .venv/bin/python tools/scan_official_maps.py [campaign_dir] [out_jsonl]
"""
import collections, glob, json, os, struct, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor

CAMPAIGN_DIR = os.path.expanduser(
    "~/Library/Application Support/Steam/steamapps/common/AoE2DE/AgeOfEmpires2Data/resources/_common/campaign")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def extract(campaign_dir, tmp):
    """Yield (campaign, chapter, scenario_path) for every scenario inside every .aoe2campaign."""
    for camp in sorted(glob.glob(os.path.join(campaign_dir, "*.aoe2campaign"))):
        b = open(camp, "rb").read()
        n = struct.unpack_from("<I", b, 4)[0]
        o = 8 + 4 * n + 256
        count = struct.unpack_from("<I", b, o)[0]
        o += 4
        for i in range(count):
            size, off = struct.unpack_from("<II", b, o)
            o += 8
            names = []
            for _ in range(2):
                _, ln = struct.unpack_from("<HH", b, o)
                o += 4
                names.append(b[o:o + ln].decode(errors="replace"))
                o += ln
            path = os.path.join(tmp, names[1])
            open(path, "wb").write(b[off:off + size])
            yield os.path.basename(camp)[:-len(".aoe2campaign")], i + 1, path


def profile(path):
    """Runs in a child process: print one JSON line describing the scenario."""
    import logging, warnings
    warnings.filterwarnings("ignore")
    logging.disable(50)
    import AoE2ScenarioParser.settings as st
    st.PRINT_STATUS_UPDATES = False
    from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
    from AoE2ScenarioParser.datasets.terrains import TerrainId
    def ids(*keys):
        return {t.value for t in TerrainId if any(k in t.name for k in keys)}
    jungle, water = ids("JUNGLE", "BAMBOO", "RAINFOREST", "MANGROVE"), ids("WATER", "SHALLOW", "BEACH")
    desert, snow = ids("DESERT", "SAND"), ids("SNOW", "ICE")
    green = {t.value for t in TerrainId if t.name.startswith("GRASS") or "FOREST" in t.name}
    out = {"scenario": os.path.basename(path)[:-len(".aoe2scenario")]}
    try:
        s = AoE2DEScenario.from_file(path)
        tiles = s.map_manager.terrain
        n, side = len(tiles), s.map_manager.map_size
        tc = collections.Counter(t.terrain_id for t in tiles)
        pct = lambda ks: round(100 * sum(tc[k] for k in ks) / n)
        elev = [t.elevation for t in tiles]
        units = s.unit_manager.get_all_units()
        castles = [u for u in units if u.unit_const == 82 and u.player >= 2]
        at = lambda u: tiles[min(n - 1, int(u.y) * side + int(u.x))].elevation
        pm = s.player_manager
        objectives = [t.description.strip().replace("\n", " ") for t in s.trigger_manager.triggers
                      if t.display_as_objective and t.description and t.description.strip()[:1] in "+-"]
        out.update(readable=True, version=s.sections["FileHeader"].version, size=side,
                   max_elevation=max(elev), raised_pct=round(100 * sum(e >= 3 for e in elev) / n),
                   jungle_pct=pct(jungle), green_pct=pct(green), water_pct=pct(water),
                   desert_pct=pct(desert), snow_pct=pct(snow),
                   enemy_castles=len(castles), enemy_castles_raised=sum(at(u) >= 3 for u in castles),
                   players=pm.active_players, triggers=len(s.trigger_manager.triggers),
                   civs=[str(pm.players[i].civilization).split(".")[-1].title() for i in range(1, pm.active_players + 1)],
                   player_names=[pm.players[i].tribe_name for i in range(1, pm.active_players + 1)],
                   mood=s.sections["Map"].map_color_mood or "", objectives=objectives[:6])
    except Exception as e:  # report, don't hide: an unreadable file can't be used as a template
        out.update(readable=False, error=str(e).strip().split("\n")[0][:120])
    print(json.dumps(out, ensure_ascii=False))


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--one":
        return profile(sys.argv[2])
    campaign_dir = sys.argv[1] if len(sys.argv) > 1 else CAMPAIGN_DIR
    out_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "docs", "data", "official_maps.jsonl")
    with tempfile.TemporaryDirectory() as tmp:
        jobs = list(extract(campaign_dir, tmp))
        def run(job):
            camp, chapter, path = job
            res = subprocess.run([sys.executable, "-I", __file__, "--one", path], capture_output=True, text=True)
            line = next((l for l in res.stdout.splitlines() if l.startswith("{")), None)
            row = json.loads(line) if line else {"scenario": os.path.basename(path), "readable": False,
                                                 "error": (res.stderr.strip().splitlines() or ["no output"])[-1][:120]}
            return {"campaign": camp, "chapter": chapter, **row}
        with ThreadPoolExecutor(max_workers=6) as ex:
            rows = list(ex.map(run, jobs))
    with open(out_path, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{len(rows)} scenarios, {sum(not r['readable'] for r in rows)} unreadable -> {out_path}")


if __name__ == "__main__":
    main()
