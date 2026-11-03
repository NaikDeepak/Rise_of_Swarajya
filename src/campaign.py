"""Build the Rise of Swarajya campaign: 15 scenarios + one .aoe2campaign file.

Usage:  python campaign.py            (writes into ../out/campaign)
"""
import json
import os
import shutil
import struct
import sys

import aoe_lib
from common import OUT
import m1_torna
import shivaji_missions as sw
import sambhaji_missions as sb

CAMPAIGN_NAME = "Rise of Swarajya"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEST = os.path.join(OUT, "campaign")
# The generated 15-chapter campaign is archived; rebuilds of it land there (tag v1-generated).
ARCHIVE_DIR = os.path.join(ROOT, "archive", "v1-generated")
SCENARIOS_DIR = os.path.join(ARCHIVE_DIR, "scenarios")

# (builder, generator filename, final filename, act, chapter title, year)
CHAPTERS = [
    (m1_torna.build,       "SW1_Torna.aoe2scenario",         "RS01_The_First_Flame",              "Act I: The Foundation", "The First Flame - Torna", "1646"),
    (sw.pratapgad,         "SW2_Pratapgad.aoe2scenario",     "RS02_The_Tiger_of_Pratapgad",       "Act I: The Foundation", "The Tiger of Pratapgad", "1659"),
    (sw.pavan_khind,       "SW3_Pavan_Khind.aoe2scenario",   "RS03_The_Sacrifice_of_Pavan_Khind", "Act I: The Foundation", "The Sacrifice of Pavan Khind", "1660"),
    (sw.lal_mahal,         "SW4_Lal_Mahal.aoe2scenario",     "RS04_The_Night_of_Shaista_Khan",    "Act II: The Defiance", "The Night of Shaista Khan", "1663"),
    (sw.surat,             "SW5_Surat.aoe2scenario",         "RS05_The_Wealth_of_Surat",          "Act II: The Defiance", "The Wealth of Surat", "1664"),
    (sw.purandar,          "SW5b_Purandar.aoe2scenario",     "RS06_The_Treaty_of_Purandar",       "Act II: The Defiance", "The Treaty of Purandar", "1665"),
    (sw.agra,              "SW6_Agra.aoe2scenario",          "RS07_The_Great_Escape",             "Act II: The Defiance", "The Great Escape - Agra", "1666"),
    (sw.sinhagad,          "SW7_Sinhagad.aoe2scenario",      "RS08_The_Lion_of_Sinhagad",         "Act III: The Crown", "The Lion of Sinhagad", "1670"),
    (sw.raigad,            "SW8_Raigad.aoe2scenario",        "RS09_The_Crown_of_Swarajya",        "Act III: The Crown", "The Crown of Swarajya - Raigad", "1674"),
    (sb.crown_of_conflict, "SB0_Crown_of_Conflict.aoe2scenario", "RS10_The_Crown_of_Conflict",    "Act IV: The Storm", "The Crown of Conflict", "1680-81"),
    (sb.burhanpur,         "SB1_Burhanpur.aoe2scenario",     "RS11_The_Riches_of_Burhanpur",      "Act IV: The Storm", "The Riches of Burhanpur", "1681"),
    (sb.ramsej,            "SB2_Ramsej.aoe2scenario",        "RS12_The_Lion_Against_the_Empire",  "Act IV: The Storm", "The Lion Against the Empire - Ramsej", "1682"),
    (sb.janjira,           "SB3_Janjira.aoe2scenario",       "RS13_The_Island_Fortress",          "Act V: The Last Stand", "The Island Fortress - Janjira", "1682"),
    (sb.goa,               "SB4_Goa.aoe2scenario",           "RS14_The_Gates_of_Goa",             "Act V: The Last Stand", "The Gates of Goa", "1683"),
    (sb.sangameshwar,      "SB5_Sangameshwar.aoe2scenario",  "RS15_The_Flame_That_Would_Not_Die", "Act V: The Last Stand", "The Flame That Would Not Die", "1689"),
]

# Same DLC dependency list the user's own AoE2 DE build writes into scenario files.
DEPENDENCIES = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19]


def de_string(text):
    raw = text.encode("utf-8")
    return struct.pack("<HH", 0x0A60, len(raw)) + raw


def write_campaign(path, name, scenarios):
    """AoE2 DE campaign format, version 2.00:
    'version'[4] u32 dep_count, i32 deps[], name[256], u32 count,
    per scenario: u32 size, u32 offset, str name, str filename; then raw scenario files."""
    head = b"2.00" + struct.pack("<I", len(DEPENDENCIES))
    head += b"".join(struct.pack("<i", d) for d in DEPENDENCIES)
    head += name.encode("utf-8")[:255].ljust(256, b"\0")
    head += struct.pack("<I", len(scenarios))
    metas_len = sum(8 + len(de_string(n)) + len(de_string(f)) for n, f, _ in scenarios)
    offset = len(head) + metas_len
    metas, blobs = b"", b""
    for n, f, data in scenarios:
        metas += struct.pack("<II", len(data), offset) + de_string(n) + de_string(f)
        blobs += data
        offset += len(data)
    with open(path, "wb") as fh:
        fh.write(head + metas + blobs)


def read_campaign(path):
    """Independent reader (mirrors genie-cpx) used to verify what we wrote."""
    b = open(path, "rb").read()
    assert b[:4] == b"2.00"
    p = 4
    n_dep = struct.unpack_from("<I", b, p)[0]; p += 4 + 4 * n_dep
    name = b[p:p + 256].split(b"\0")[0].decode(); p += 256
    count = struct.unpack_from("<I", b, p)[0]; p += 4
    out = []
    for _ in range(count):
        size, off = struct.unpack_from("<II", b, p); p += 8
        strs = []
        for _ in range(2):
            mark, ln = struct.unpack_from("<HH", b, p); p += 4
            assert mark == 0x0A60
            strs.append(b[p:p + ln].decode()); p += ln
        assert b[off:off + 4] == b"1.59", "scenario data misplaced"
        out.append((strs[0], strs[1], size, off))
    return name, out


def main():
    os.makedirs(DEST, exist_ok=True)
    for _, old, new, act, title, year in CHAPTERS:
        n = int(new[2:4])
        heading = f"RISE OF SWARAJYA  |  {act}\nChapter {n}: {title} ({year})"
        aoe_lib.RENAME[old] = (new + ".aoe2scenario", heading)
    os.environ["SWARAJYA_OUT"] = DEST
    built = []
    for build, old, new, *_ in CHAPTERS:
        # missions write to common.OUT; point every module at the campaign folder
        for mod in (m1_torna, sw, sb):
            mod.OUT = DEST
        path = build()
        built.append(path)
        print("built", os.path.basename(path))
    scenarios = []
    for _, _, new, _, title, _ in CHAPTERS:
        fn = new + ".aoe2scenario"
        data = open(os.path.join(DEST, fn), "rb").read()
        scenarios.append((fn, fn, data))
    cpath = os.path.join(DEST, f"{CAMPAIGN_NAME}.aoe2campaign")
    write_campaign(cpath, CAMPAIGN_NAME, scenarios)
    name, entries = read_campaign(cpath)
    print("campaign:", name, len(entries), "scenarios,", os.path.getsize(cpath), "bytes")
    os.makedirs(SCENARIOS_DIR, exist_ok=True)
    for _, _, new, *_ in CHAPTERS:
        fn = new + ".aoe2scenario"
        shutil.copy2(os.path.join(DEST, fn), os.path.join(SCENARIOS_DIR, fn))
    shutil.copy2(cpath, os.path.join(ARCHIVE_DIR, f"{CAMPAIGN_NAME}.aoe2campaign"))
    shutil.copy2(cpath, os.path.join(ARCHIVE_DIR, "Rise_of_Swarajya.aoe2campaign"))
    game_profile = os.path.expanduser(
        "~/Library/Application Support/Feral Interactive/Age Of Empires II/VFS/User/Games/Age of Empires 2 DE/76561198054484915"
    )
    if os.path.isdir(game_profile):
        game_scen = os.path.join(game_profile, "resources", "_common", "scenario")
        game_camp = os.path.join(game_profile, "resources", "_common", "campaign")
        mod_camp = os.path.join(game_profile, "mods", "local", "Rise of Swarajya", "resources", "_common", "campaign")
        mod_scen = os.path.join(game_profile, "mods", "local", "Rise of Swarajya", "resources", "_common", "scenario")
        os.makedirs(game_scen, exist_ok=True)
        os.makedirs(game_camp, exist_ok=True)
        # Move any superseded underscore .aoe2campaign files to backups/superseded_game_files/ (never delete)
        backup_dir = os.path.join(ROOT, "backups", "superseded_game_files")
        for label, d in (("profile_campaign", game_camp), ("mod_campaign", mod_camp)):
            if os.path.isdir(d):
                for old_f in os.listdir(d):
                    if old_f == "Rise_of_Swarajya.aoe2campaign" or (label == "mod_campaign" and "Swarajya" in old_f):
                        os.makedirs(os.path.join(backup_dir, label), exist_ok=True)
                        shutil.move(os.path.join(d, old_f), os.path.join(backup_dir, label, old_f))
        for _, _, new, *_ in CHAPTERS:
            fn = new + ".aoe2scenario"
            shutil.copy2(os.path.join(DEST, fn), os.path.join(game_scen, fn))
            if os.path.isdir(mod_scen):
                shutil.copy2(os.path.join(DEST, fn), os.path.join(mod_scen, fn))
        # The engine looks up <CAMPAIGN_NAME>.aoe2campaign ("Rise of Swarajya.aoe2campaign") when
        # returning to CampaignScenarioSelection on Resign / Quit Current Game / Victory.
        shutil.copy2(cpath, os.path.join(game_camp, f"{CAMPAIGN_NAME}.aoe2campaign"))
        # Sync custom storyboard PNGs, Wwise .wem voiceover audio, and Fe Immobile AI scripts
        src_tex = os.path.join(ROOT, "assets", "textures", "campaign", "swarajya")
        src_snd = os.path.join(ROOT, "assets", "sounds")
        src_ai = os.path.join(ROOT, "assets", "ai")
        steam_data = os.path.expanduser(
            "~/Library/Application Support/Steam/steamapps/common/AoE2DE/AgeOfEmpires2Data"
        )
        json_targets = [
            game_camp,
            os.path.join(game_profile, "widgetui"),
        ]
        tex_targets = [os.path.join(game_profile, "widgetui", "textures", "campaign", "swarajya")]
        snd_targets = [os.path.join(game_profile, "resources", "_common", "drs", "sounds")]
        ai_targets = [os.path.join(game_profile, "resources", "_common", "ai")]
        if os.path.isdir(steam_data):
            json_targets.extend([
                os.path.join(steam_data, "resources", "_common", "campaign"),
                os.path.join(steam_data, "widgetui"),
            ])
            tex_targets.append(os.path.join(steam_data, "widgetui", "textures", "campaign", "swarajya"))
            snd_targets.append(os.path.join(steam_data, "resources", "_common", "drs", "sounds"))
            ai_targets.append(os.path.join(steam_data, "resources", "_common", "ai"))
        for jt in json_targets:
            os.makedirs(jt, exist_ok=True)
            for stem in ("Rise_of_Swarajya", CAMPAIGN_NAME):
                for ext in ("_layout.json", ".json"):
                    src_j = os.path.join(ROOT, "Rise_of_Swarajya" + ext)
                    if os.path.exists(src_j):
                        shutil.copy2(src_j, os.path.join(jt, stem + ext))
            mat_path = os.path.join(steam_data, "widgetui", "materials.json")
            if os.path.isfile(mat_path):
                mat_data = json.load(open(mat_path, "r", encoding="utf-8"))
                mats = mat_data.get("Materials", [])
                texs = mat_data.get("GlobalTextures", [])
                changed = False
                if not any(m.get("MaterialDef", {}).get("Name") == "CampaignBackgroundSwarajya" for m in mats):
                    mats.append({
                        "MaterialDef": {
                            "Name": "CampaignBackgroundSwarajya",
                            "Type": "Texture",
                            "Blend": "None",
                            "TextureRef": "CampaignBackgroundSwarajya"
                        }
                    })
                    changed = True
                if not any(t.get("TextureDef", {}).get("Name") == "CampaignBackgroundSwarajya" for t in texs):
                    texs.append({
                        "TextureDef": {
                            "Name": "CampaignBackgroundSwarajya",
                            "FileName": "textures/campaign/swarajya/swarajya_map.dds",
                            "Cached": "none"
                        }
                    })
                    changed = True
                if changed:
                    with open(mat_path, "w", encoding="utf-8") as mf:
                        json.dump(mat_data, mf, indent=2)
        if os.path.isdir(src_tex):
            for tt in tex_targets:
                shutil.copytree(src_tex, tt, dirs_exist_ok=True)
        if os.path.isdir(src_snd):
            for st in snd_targets:
                os.makedirs(st, exist_ok=True)
                for fn in os.listdir(src_snd):
                    if fn.endswith(".wem"):
                        shutil.copy2(os.path.join(src_snd, fn), os.path.join(st, fn))
        if os.path.isdir(src_ai):
            for at in ai_targets:
                os.makedirs(at, exist_ok=True)
                for fn in os.listdir(src_ai):
                    shutil.copy2(os.path.join(src_ai, fn), os.path.join(at, fn))
        print("synced to in-game folder:", game_scen)


if __name__ == "__main__":
    main()
