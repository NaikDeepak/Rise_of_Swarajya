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
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageChops, ImageFilter

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

                # Smooth pan/zoom ImageRect per slide (JSON Kungfu SlideShow technique)
                img_rects = [
                    {"x": 910, "y": 540, "width": 2000, "height": 1048},
                    {"x": 945, "y": 525, "width": 2036, "height": 1066},
                    {"x": 885, "y": 555, "width": 2000, "height": 1048},
                    {"x": 925, "y": 535, "width": 2020, "height": 1058},
                ]
                slide_obj = {
                    "Duration": round(max(4.5, s_dur), 2),
                    "FadeOutTime": 0.4,
                    "TextFadeDuration": round(max(3.5, s_dur - 1.0), 2),
                    "String": s_txt,
                    "ImageRect": img_rects[(s_i - 1) % len(img_rects)],
                    "TextRect": {
                        "x": 1020,
                        "y": 560 if s_i % 2 == 1 else 620,
                        "width": 1680,
                        "height": 420,
                    },
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

    for fn in ("Rise_of_Swarajya.json", "Rise of Swarajya.json"):
        with open(os.path.join(ROOT, fn), "w") as f:
            json.dump({"Scenarios": scenarios_json}, f, indent=2)

    build_campaign_map_dds()
    build_layout_json()

    print("Saved Rise_of_Swarajya.json, Rise_of_Swarajya_layout.json, swarajya_map.dds, and all storyboard PNGs + .wem voiceovers.")


def build_campaign_map_dds():
    """Generate a 5672x2160 DXT1 .dds custom Maratha / Sahyadri parchment campaign map."""
    import ctypes
    dds_out = os.path.join(TEX_DIR, "swarajya_map.dds")
    if os.path.exists(dds_out) and os.path.getsize(dds_out) > 6_000_000:
        return
    raj_path = os.path.join(GAME_DATA_CAMPAIGN_TEX, "incam2", "rajendra.dds")
    pri_path = os.path.join(GAME_DATA_CAMPAIGN_TEX, "fcam6", "prithviraj.dds")
    if not (os.path.exists(raj_path) and os.path.exists(pri_path)):
        return

    with open(raj_path, "rb") as f:
        dds_header = f.read(128)

    raj = Image.open(raj_path).convert("RGBA")
    pri = Image.open(pri_path).convert("RGBA")

    canvas = raj.copy()
    mask = Image.new("L", (5672, 2160), 0)
    md = ImageDraw.Draw(mask)
    md.polygon([
        (276, 0), (2600, 0), (2600, 260), (4250, 560),
        (4050, 2160), (276, 2160)
    ], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=50))

    pri_padded = Image.new("RGBA", (5672, 2160), (0, 0, 0, 255))
    pri_padded.paste(pri, (276, 0))
    comp = Image.composite(pri_padded, canvas, mask)

    overlay = Image.new("RGBA", (5672, 2160), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    cx, cy = 3680, 760
    for r_oct, w_line, alpha in ((195, 7, 105), (175, 4, 85)):
        pts = [
            (cx + r_oct * math.cos(math.radians(22.5 + 45 * k)),
             cy + r_oct * math.sin(math.radians(22.5 + 45 * k)))
            for k in range(8)
        ]
        d.polygon(pts, outline=(72, 34, 18, alpha), width=w_line)

    d.line([(cx, cy - 110), (cx, cy + 115)], fill=(72, 34, 18, 110), width=6)
    d.polygon([
        (cx + 3, cy - 105), (cx + 115, cy - 80), (cx + 75, cy - 42),
        (cx + 120, cy - 5), (cx + 3, cy + 15)
    ], fill=(140, 55, 18, 75), outline=(72, 34, 18, 115))

    out_im = Image.alpha_composite(comp, overlay)

    c_code = """
    #include <stdint.h>
    void encode_dxt1(const uint8_t* rgba, int w, int h, uint8_t* out) {
        int bw = w / 4, bh = h / 4;
        for (int by = 0; by < bh; by++) {
            for (int bx = 0; bx < bw; bx++) {
                uint8_t min_r = 255, min_g = 255, min_b = 255;
                uint8_t max_r = 0, max_g = 0, max_b = 0;
                uint8_t px[16][3];
                int idx = 0;
                for (int py = 0; py < 4; py++) {
                    const uint8_t* row = rgba + ((by * 4 + py) * w + (bx * 4)) * 4;
                    for (int x = 0; x < 4; x++) {
                        uint8_t r = row[x*4+0], g = row[x*4+1], b = row[x*4+2];
                        px[idx][0] = r; px[idx][1] = g; px[idx][2] = b; idx++;
                        if (r < min_r) min_r = r; if (r > max_r) max_r = r;
                        if (g < min_g) min_g = g; if (g > max_g) max_g = g;
                        if (b < min_b) min_b = b; if (b > max_b) max_b = b;
                    }
                }
                uint16_t c0 = ((max_r >> 3) << 11) | ((max_g >> 2) << 5) | (max_b >> 3);
                uint16_t c1 = ((min_r >> 3) << 11) | ((min_g >> 2) << 5) | (min_b >> 3);
                if (c0 < c1) {
                    uint16_t t = c0; c0 = c1; c1 = t;
                    uint8_t tr = max_r, tg = max_g, tb = max_b;
                    max_r = min_r; max_g = min_g; max_b = min_b;
                    min_r = tr; min_g = tg; min_b = tb;
                } else if (c0 == c1) {
                    uint8_t* dst = out + (by * bw + bx) * 8;
                    dst[0] = c0 & 0xFF; dst[1] = c0 >> 8;
                    dst[2] = c1 & 0xFF; dst[3] = c1 >> 8;
                    dst[4] = dst[5] = dst[6] = dst[7] = 0;
                    continue;
                }
                int pal[4][3] = {
                    {max_r, max_g, max_b},
                    {min_r, min_g, min_b},
                    {(2*max_r + min_r)/3, (2*max_g + min_g)/3, (2*max_b + min_b)/3},
                    {(max_r + 2*min_r)/3, (max_g + 2*min_g)/3, (max_b + 2*min_b)/3}
                };
                uint32_t bits = 0;
                for (int i = 0; i < 16; i++) {
                    int best = 0, best_d = 1000000;
                    for (int k = 0; k < 4; k++) {
                        int dr = (int)px[i][0] - pal[k][0];
                        int dg = (int)px[i][1] - pal[k][1];
                        int db = (int)px[i][2] - pal[k][2];
                        int d = dr*dr + dg*dg + db*db;
                        if (d < best_d) { best_d = d; best = k; }
                    }
                    bits |= ((uint32_t)best << (i * 2));
                }
                uint8_t* dst = out + (by * bw + bx) * 8;
                dst[0] = c0 & 0xFF; dst[1] = c0 >> 8;
                dst[2] = c1 & 0xFF; dst[3] = c1 >> 8;
                dst[4] = bits & 0xFF; dst[5] = (bits >> 8) & 0xFF;
                dst[6] = (bits >> 16) & 0xFF; dst[7] = (bits >> 24) & 0xFF;
            }
        }
    }
    """
    with tempfile.TemporaryDirectory() as td:
        c_path = os.path.join(td, "dxt1.c")
        so_path = os.path.join(td, "dxt1.so")
        with open(c_path, "w") as f:
            f.write(c_code)
        subprocess.run(["clang", "-O3", "-shared", "-fPIC", c_path, "-o", so_path], check=True)
        lib = ctypes.CDLL(so_path)
        w, h = out_im.size
        raw = out_im.tobytes()
        buf = ctypes.create_string_buffer((w // 4) * (h // 4) * 8)
        lib.encode_dxt1(raw, w, h, buf)
        with open(dds_out, "wb") as f:
            f.write(dds_header)
            f.write(buf.raw)


def build_layout_json():
    """Generate Rise_of_Swarajya_layout.json using latest AoE2 DE CampaignTitle + ClippingOverride + NextIndicators."""
    widgets = [
        {
            "Widget": {
                "Type": "Label",
                "Name": "TitleLabel",
                "ViewPort": {
                    "xorigin": 1920,
                    "yorigin": 110,
                    "width": 1600,
                    "height": 100,
                    "alignment": "CentreCentre",
                },
                "ZPlane": 2,
                "StateMaterials": {
                    "StateNormal": {
                        "Font": {
                            "FontIndex": 0,
                            "PointSize": 70,
                            "Style": "Normal",
                            "TextColor": {"r": 57, "g": 28, "b": 27, "a": 255},
                        }
                    }
                },
                "Text": "Rise of Swarajya (1646 - 1689)",
                "TextAnchor": "CentreCentre",
                "ChildWidgets": [],
            }
        }
    ]

    # Place 15 scenarios in 3 rows of 5 over the open parchment map (x: 960..2800, y: 310..1230)
    coords = []
    for idx, (_, _, _, _, title, year) in enumerate(CHAPTERS, 1):
        row = (idx - 1) // 5
        col = (idx - 1) % 5
        x = 960 + col * 450 + (40 if row == 1 else 0)
        y = 310 + row * 450 + (30 if col % 2 == 1 else 0)
        coords.append((x, y))

        font_def = {
            "FontIndex": 0,
            "PointSize": 34,
            "Style": "Normal",
            "TextColor": {"r": 42, "g": 10, "b": 82, "a": 255},
        }
        font_dis = {
            "FontIndex": 0,
            "PointSize": 34,
            "Style": "Normal",
            "TextColor": {"r": 42, "g": 10, "b": 82, "a": 128},
        }
        widgets.append(
            {
                "Widget": {
                    "Type": "Button",
                    "Name": f"ScenarioButton{idx}",
                    "ViewPort": {
                        "xorigin": x,
                        "yorigin": y,
                        "width": 260,
                        "height": 260,
                        "alignment": "TopLeft",
                    },
                    "Image": {
                        "xorigin": 0,
                        "yorigin": 0,
                        "width": 260,
                        "height": 260,
                        "alignment": "TopLeft",
                    },
                    "ZPlane": 1,
                    "StateMaterials": {
                        "StateDisabled": {"Material": "CampaignIcon35RajendraDisabled", "Font": font_dis},
                        "StateNormal": {"Material": "CampaignIcon35RajendraNormal", "Font": font_def},
                        "StateHover": {"Material": "CampaignIcon35RajendraHover", "Font": font_def},
                        "StatePressed": {"Material": "CampaignIcon35RajendraPressed", "Font": font_def},
                    },
                    "ChildWidgets": [
                        {
                            "Widget": {
                                "Type": "CampaignTitle",
                                "Name": "ScenarioButtonLabel",
                                "ViewPort": {
                                    "xorigin": -25,
                                    "yorigin": 225,
                                    "width": 440,
                                    "height": 90,
                                    "alignment": "TopLeft",
                                },
                                "ClippingOverride": "Background",
                                "ZPlane": 2,
                                "Level": 0,
                                "StateMaterials": {
                                    "StateNormal": {
                                        "Font": {
                                            "FontIndex": 0,
                                            "PointSize": 30,
                                            "Style": "Normal",
                                            "TextColor": {"r": 255, "g": 255, "b": 255, "a": 255},
                                        }
                                    }
                                },
                                "Text": f"{idx}. {title} ({year})",
                                "TextAnchor": "TopLeft",
                                "ChildWidgets": [],
                            }
                        }
                    ],
                }
            }
        )

    # Add NextIndicator trail widgets between consecutive chapters on the same row
    for i in range(len(coords) - 1):
        if i % 5 == 4:
            continue
        x1, y1 = coords[i]
        x2, y2 = coords[i + 1]
        widgets.append(
            {
                "Widget": {
                    "Type": "Base",
                    "Name": f"NextIndicator{i + 1}",
                    "ViewPort": {
                        "xorigin": x1 + 210,
                        "yorigin": min(y1, y2) + 80,
                        "width": 260,
                        "height": 140,
                        "alignment": "TopLeft",
                    },
                    "ZPlane": 0,
                    "Wrap": {"width": 0, "height": 0},
                    "StateMaterials": {
                        "StateNormal": {
                            "Material": "GenghisKhanIndicator3" if i % 2 == 0 else "GenghisKhanIndicator5"
                        }
                    },
                }
            }
        )

    layout_obj = {
        "BackgroundMaterial": "CampaignBackgroundSwarajya",
        "UnlockScenarios": True,
        "Widgets": widgets,
    }
    for fn in ("Rise_of_Swarajya_layout.json", "Rise of Swarajya_layout.json"):
        with open(os.path.join(ROOT, fn), "w") as f:
            json.dump(layout_obj, f, indent=2)


if __name__ == "__main__":
    main()
