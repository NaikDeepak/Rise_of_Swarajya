"""Generate custom Maratha storyboard illustrations (.png) and Wwise voiceover audio (.wem)."""
import os
import glob
import json
import math
import struct
import shutil
import wave
import tempfile
import subprocess
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageChops

import aoe_lib
from campaign import CHAPTERS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOUNDS_DIR = os.path.join(ROOT, "assets", "sounds")
TEX_DIR = os.path.join(ROOT, "assets", "textures", "campaign", "swarajya")

GAME_DATA_CAMPAIGN_TEX = os.path.expanduser(
    "~/Library/Application Support/Steam/steamapps/common/AoE2DE/AgeOfEmpires2Data/widgetui/textures/campaign"
)
USER_PROFILE = os.path.expanduser(
    "~/Library/Application Support/Feral Interactive/Age Of Empires II/VFS/User/Games/Age of Empires 2 DE/76561198054484915"
)


def voice_for_speaker(who: str):
    if not who or who == "Narrator":
        return ("Rishi", "162")
    w = who.lower()
    if any(k in w for k in ("jijabai", "yesubai", "tarabai", "soyarabai")):
        return ("Tara", "162")
    if any(k in w for k in ("shivaji", "sambhaji", "rajaram", "shahaji")):
        return ("Aman", "168")
    if any(k in w for k in ("killedar", "afzal", "jauhar", "shaista", "aurangzeb", "udaybhan", "siddi", "alvor", "muqarrab", "zulfiqar", "diler", "jai singh", "ikhlaskhan")):
        return ("Rocko (English (UK))", "158")
    if any(k in w for k in ("yesaji", "bahirji", "kanhoji", "kavi", "gaga", "tukaram", "hiroji", "moropant", "annaji", "ram singh", "inayat", "baji pasalkar")):
        return ("Reed (English (UK))", "168")
    return ("Daniel", "168")


def pcm_to_wem(pcm: bytes) -> bytes:
    """Wrap raw 44.1kHz 16-bit mono PCM bytes in a Wwise 0xFFFE WAVE/RIFF .wem container."""
    if len(pcm) % 2:
        pcm += b"\x00"
    data_len = len(pcm)
    riff_len = data_len + 56
    return (
        b"RIFF" + struct.pack("<I", riff_len) +
        b"WAVEfmt \x18\x00\x00\x00\xfe\xff\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00\x06\x00\x00\x00\x01A\x00\x00"
        b"JUNK\x04\x00\x00\x00\x00\x00\x00\x00"
        b"data" + struct.pack("<I", data_len) + pcm
    )


def clean_tts_text(text: str) -> str:
    return (
        text.replace("—", ", ")
        .replace("–", ", ")
        .replace("Chhatrapati", "Chhatra-pati")
        .replace("Maharaj", "Mahaaraaj")
        .replace("Aaisaheb", "Aai-saaheb")
        .replace("Dharmaveer", "Dharma-veer")
        .replace("Swarajya", "Swaraajya")
        .replace("Raje", "Raajay")
        .replace("Shivba", "Shivbaa")
        .replace("Mavalas", "Maavalaas")
        .replace("Maval", "Maaval")
        .replace("Sahyadri", "Sahyaadri")
        .replace("Simhasan", "Simhaasan")
        .replace("Rajgad", "Raaj-gad")
        .replace("Raigad", "Raai-gad")
        .replace("Pratapgad", "Prataap-gad")
        .replace("Sinhagad", "Sinha-gad")
        .replace("Vishalgad", "Vishaal-gad")
    )


def synth_pcm(text: str, voice: str = "Rishi", rate: str = "162") -> tuple[bytes, float]:
    fd, wav_path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    try:
        subprocess.run(
            ["say", "-v", voice, "-r", str(rate), "-o", wav_path, "--data-format=LEI16@44100", clean_tts_text(text)],
            check=True,
        )
        with wave.open(wav_path, "rb") as w:
            pcm = w.readframes(w.getnframes())
            dur = w.getnframes() / float(w.getframerate())
        return pcm, dur
    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)


def build_vo_line(item):
    vo_name, (speaker, text) = item
    wem_path = os.path.join(SOUNDS_DIR, f"{vo_name}.wem")
    voice, rate = voice_for_speaker(speaker)
    spoken = text
    pcm, dur = synth_pcm(spoken, voice=voice, rate=rate)
    with open(wem_path, "wb") as f:
        f.write(pcm_to_wem(pcm))
    return vo_name, round(dur, 2)


def draw_maratha_emblem(im: Image.Image, chapter_idx: int, slide_idx: int, is_outro: bool):
    """Add hand-drawn ink-wash Maratha fort / Bhagwa Dhwaj / octagonal Rajmudra accent to a 2000x1048 LA slide."""
    la = im.convert("RGBA")
    overlay = Image.new("RGBA", (2000, 1048), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    bx = 250 if (slide_idx % 2 == 1 and not is_outro) else 1720
    by = 210

    if slide_idx in (1, 3):
        # Staff and forked Bhagwa Dhwaj banner silhouette in classical ink-wash on margin
        d.line([(bx, by), (bx, by + 560)], fill=(25, 25, 25, 195), width=7)
        # Kalash finial atop flagpole
        d.ellipse([bx - 9, by - 18, bx + 9, by], fill=(30, 30, 30, 200))
        # Forked swallowtail Bhagwa Dhwaj banner
        direction = 1 if bx < 1000 else -1
        pts = [
            (bx + 4 * direction, by + 16),
            (bx + 215 * direction, by + 48),
            (bx + 150 * direction, by + 105),
            (bx + 225 * direction, by + 165),
            (bx + 4 * direction, by + 195),
        ]
        d.polygon(pts, fill=(40, 40, 40, 140), outline=(20, 20, 20, 205))
        # Sahyadri fort battlements (buruj) at base of flagpole
        base_y = by + 520
        for crenel in range(-4, 5):
            cx = bx + crenel * 26
            d.rectangle([cx - 10, base_y - 22, cx + 10, base_y], fill=(35, 35, 35, 155))
        d.rectangle([bx - 115, base_y, bx + 115, base_y + 45], fill=(30, 30, 30, 170))
    else:
        # Octagonal Rajmudra royal seal silhouette in ink-wash
        cx, cy = bx, by + 220
        for r_oct, alpha in ((110, 175), (96, 145)):
            oct_pts = [
                (
                    cx + r_oct * math.cos(math.radians(22.5 + 45 * k)),
                    cy + r_oct * math.sin(math.radians(22.5 + 45 * k)),
                )
                for k in range(8)
            ]
            d.polygon(oct_pts, outline=(25, 25, 25, alpha), width=4)

    comp = Image.alpha_composite(la, overlay)
    gray = comp.convert("L")
    alpha = comp.split()[3]
    return Image.merge("LA", (gray, alpha))


# Strictly curated whitelist of verified, dignified Indian warrior/king/fort/temple/fleet ink-wash illustrations
# (Excludes all rakshasa/demon myth slides and Mughal slides)
CURATED_SLIDES = {
    "king": "fcam6/2/intro/2.png",          # Regal bearded Indian king seated in royal robes & turban
    "swordsman": "fcam6/1/intro/4.png",     # Warrior with talwar & round shield before the rising sun
    "spearman": "fcam6/1/outro/1.png",      # Mustachioed warrior holding a bhala spear
    "cavalry": "incam2/1/intro/6.png",      # Warrior-king on rearing warhorse raising his sword
    "rider": "incam2/1/outro/1.png",        # Lone horseman galloping at full speed through the pass
    "temple": "incam2/1/outro/6.png",       # Sacred temple mandapa with warriors standing before it
    "valley": "incam2/1/intro/5.png",       # Mountain range & river valley with temple
    "fire": "fcam6/1/intro/2.png",          # Sacred Agni fire
    "bard": "fcam6/1/intro/5.png",          # Shahir / bard playing tanpura
    "sea_king": "incam2/3/intro/3.png",     # King on horseback gazing at ships on the sea
    "fleet": "incam2/3/intro/4.png",        # Indian warships under sail on the ocean
    "night_palace": "incam2/3/outro/2.png", # Palace pavilion under the crescent moon at night
    "enemy_gen": "fcam6/4/intro/4.png",     # Armoured opposing general with shield
}

CHAPTER_SLIDE_THEMES = {
    1: (["temple", "king", "swordsman", "valley"], ["swordsman", "king", "fire"]),                # Torna
    2: (["valley", "enemy_gen", "king", "swordsman"], ["swordsman", "cavalry", "king"]),           # Pratapgad
    3: (["valley", "rider", "spearman", "swordsman"], ["spearman", "king", "fire"]),               # Pavan Khind
    4: (["night_palace", "king", "rider", "swordsman"], ["swordsman", "rider", "king"]),           # Lal Mahal
    5: (["sea_king", "rider", "cavalry", "swordsman"], ["cavalry", "king", "bard"]),               # Surat
    6: (["valley", "spearman", "enemy_gen", "king"], ["king", "spearman", "bard"]),                # Purandar
    7: (["night_palace", "king", "rider", "temple"], ["rider", "king", "fire"]),                   # Agra
    8: (["night_palace", "swordsman", "spearman", "valley"], ["swordsman", "fire", "king"]),       # Sinhagad
    9: (["temple", "king", "fire", "cavalry"], ["king", "temple", "fire"]),                        # Raigad
    10: (["king", "cavalry", "rider", "temple"], ["cavalry", "king", "fire"]),                     # Crown of Conflict
    11: (["cavalry", "rider", "swordsman", "valley"], ["cavalry", "king", "fire"]),                # Burhanpur
    12: (["valley", "spearman", "swordsman", "cavalry"], ["spearman", "cavalry", "king"]),         # Ramsej
    13: (["sea_king", "fleet", "swordsman", "cavalry"], ["fleet", "sea_king", "king"]),            # Janjira
    14: (["sea_king", "fleet", "cavalry", "swordsman"], ["cavalry", "sea_king", "king"]),          # Goa
    15: (["king", "cavalry", "rider", "swordsman"], ["fire", "cavalry", "king"]),                  # Sangameshwar
}


def main():
    os.makedirs(SOUNDS_DIR, exist_ok=True)
    os.makedirs(TEX_DIR, exist_ok=True)

    # 1. Run all 15 scenario builders into a temp dir to collect VO_REGISTRY and messages
    tmp_out = tempfile.mkdtemp()
    chapter_meta = []
    for _, old, new, act, title, year in CHAPTERS:
        aoe_lib.RENAME[old] = (new + ".aoe2scenario", f"Rise of Swarajya — {act}\n{title} ({year})")

    import m1_torna
    import shivaji_missions as sm
    import sambhaji_missions as sbm

    from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
    import AoE2ScenarioParser.settings as asp_settings
    asp_settings.PRINT_STATUS_UPDATES = False

    for idx, (fn, old, new, act, title, year) in enumerate(CHAPTERS, 1):
        for mod in (m1_torna, sm, sbm):
            mod.OUT = tmp_out
        path = fn()
        s = AoE2DEScenario.from_file(path)
        mm = s.message_manager
        history = (mm.history or "").strip()
        instructions = (mm.instructions or "").strip()
        # Extract non-header instructions paragraph
        inst_lines = [ln.strip() for ln in instructions.splitlines() if ln.strip()]
        brief = inst_lines[-1] if inst_lines else title
        victory_txt = (mm.victory or "").strip()

        # Also extract first 2 story lines and epilogue lines from triggers
        story_lines = []
        epilogue_lines = []
        for t in s.trigger_manager.triggers:
            for e in t.effects:
                if e.effect_type == 20 and e.message:
                    if t.name.startswith("Story "):
                        story_lines.append(e.message)
                    elif t.name.startswith("Epilogue "):
                        epilogue_lines.append(e.message)

        intro_texts = [
            f"{act} — {title}",
            history if history else brief,
            story_lines[0] if len(story_lines) > 0 else brief,
            story_lines[1] if len(story_lines) > 1 else f"Objective: {brief}",
        ]
        outro_texts = [
            victory_txt if victory_txt else f"{title} — Victory for Swarajya.",
        ] + (epilogue_lines[:2] if epilogue_lines else ["The saffron Bhagwa Dhwaj flies high above the Sahyadri."])

        chapter_meta.append((idx, new, act, title, intro_texts, outro_texts))
    shutil.rmtree(tmp_out, ignore_errors=True)

    # 2. Synthesize in-game VO lines (cached if already in vo_durations.json)
    dur_map = dict(aoe_lib.VO_DURATIONS)
    todo_vo = [
        (k, v) for k, v in aoe_lib.VO_REGISTRY.items()
        if k not in dur_map or not os.path.exists(os.path.join(SOUNDS_DIR, f"{k}.wem"))
    ]
    print(f"In-game VO lines: {len(aoe_lib.VO_REGISTRY)} total, {len(todo_vo)} to synthesize...")
    if todo_vo:
        with ThreadPoolExecutor(max_workers=8) as ex:
            for vo_name, dur in ex.map(build_vo_line, todo_vo):
                dur_map[vo_name] = dur
        with open(os.path.join(SOUNDS_DIR, "vo_durations.json"), "w") as f:
            json.dump(dur_map, f, indent=2)
    aoe_lib.VO_DURATIONS.update(dur_map)

    # 3. Build storyboard narrations (rs01_intro.wem .. rs15_outro.wem) + custom PNG slides + Rise_of_Swarajya.json
    import hashlib

    # Choose background per Act so each Act has rich Indian parchment art (no Mughal backgrounds)
    act_bg = {
        "Act I: The Foundation": "textures/campaign/fcam6/prithviraj_background.dds",
        "Act II: The Storm": "textures/campaign/incam3/devapala_background.dds",
        "Act III: The Chhatrapati": "textures/campaign/fcam6/prithviraj_background.dds",
        "Act IV: The Chhava": "textures/campaign/incam2/rajendra_background.dds",
        "Act V: Total War": "textures/campaign/fcam6/prithviraj_background.dds",
    }

    scenarios_json = []
    silence_gap = b"\x00\x00" * int(44100 * 0.55)

    print("Generating 15 Intro + 15 Outro storyboard illustrations and narrator .wem files...")
    for idx, new, act, title, intro_texts, outro_texts in chapter_meta:
        bg_dds = act_bg.get(act, "textures/campaign/fcam6/prithviraj_background.dds")
        scen_entry = {}
        intro_themes, outro_themes = CHAPTER_SLIDE_THEMES[idx]
        for seq_key, sub, texts, themes in (
            ("IntroSequence", "intro", intro_texts, intro_themes),
            ("OutroSequence", "outro", outro_texts, outro_themes),
        ):
            snd_name = f"rs{idx:02d}_{sub}"
            wem_path = os.path.join(SOUNDS_DIR, f"{snd_name}.wem")
            txt_hash = hashlib.md5("||".join(texts).encode("utf-8")).hexdigest()[:8]
            dur_cache_key = f"__slide_{snd_name}_{txt_hash}"

            slide_durs = dur_map.get(dur_cache_key)
            if not slide_durs or len(slide_durs) != len(texts) or not os.path.exists(wem_path):
                pcm_parts = []
                slide_durs = []
                for s_txt in texts:
                    p_bytes, s_dur = synth_pcm(s_txt, voice="Rishi", rate="160")
                    pcm_parts.append(p_bytes)
                    pcm_parts.append(silence_gap)
                    slide_durs.append(round(s_dur + 0.55, 2))
                with open(wem_path, "wb") as f:
                    f.write(pcm_to_wem(b"".join(pcm_parts)))
                dur_map[dur_cache_key] = slide_durs

            # Generate 1.png .. N.png in assets/textures/campaign/swarajya/<idx>/<sub>/
            seq_dir = os.path.join(TEX_DIR, str(idx), sub)
            os.makedirs(seq_dir, exist_ok=True)
            for old_png in glob.glob(os.path.join(seq_dir, "*.png")):
                os.remove(old_png)

            slides_arr = []
            for s_i, (s_txt, s_dur) in enumerate(zip(texts, slide_durs), 1):
                theme_key = themes[(s_i - 1) % len(themes)]
                src_png = os.path.join(GAME_DATA_CAMPAIGN_TEX, CURATED_SLIDES[theme_key])
                im = Image.open(src_png)
                custom_im = draw_maratha_emblem(im, idx, s_i, is_outro=(sub == "outro"))
                custom_im.save(os.path.join(seq_dir, f"{s_i}.png"))

                slide_obj = {
                    "Duration": round(max(4.5, s_dur), 2),
                    "TextFadeDuration": round(max(3.5, s_dur - 1.0), 2),
                    "String": s_txt,
                    "TextRect": {
                        "x": 1020,
                        "y": 560 if s_i % 2 == 1 else 620,
                        "width": 1680,
                        "height": 420,
                    },
                }
                if s_i == 1:
                    slide_obj["ImageRect"] = {
                        "x": 910,
                        "y": 550,
                        "width": 2000,
                        "height": 1048,
                    }
                slides_arr.append(slide_obj)

            scen_entry[seq_key] = {
                "SequenceItems": [
                    {
                        "Type": "SlideShow",
                        "Data": {
                            "SlideBackgroundImage": bg_dds,
                            "SlideImageSequence": f"textures/campaign/swarajya/{idx}/{sub}/%d.png",
                            "Sound": snd_name,
                            "Slides": slides_arr,
                        },
                    }
                ]
            }
        scenarios_json.append(scen_entry)

    # Prune any old sw_vo_*.wem files no longer referenced in VO_REGISTRY
    active_wems = {f"{k}.wem" for k in aoe_lib.VO_REGISTRY} | {f"rs{i:02d}_{s}.wem" for i in range(1, 16) for s in ("intro", "outro")}
    for wem_file in glob.glob(os.path.join(SOUNDS_DIR, "*.wem")):
        if os.path.basename(wem_file) not in active_wems:
            os.remove(wem_file)

    with open(os.path.join(SOUNDS_DIR, "vo_durations.json"), "w") as f:
        json.dump(dur_map, f, indent=2)

    with open(os.path.join(ROOT, "Rise_of_Swarajya.json"), "w") as f:
        json.dump({"Scenarios": scenarios_json}, f, indent=2)

    print("Saved Rise_of_Swarajya.json and all storyboard PNGs + .wem voiceovers.")


if __name__ == "__main__":
    main()
