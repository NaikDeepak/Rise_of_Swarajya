"""Build the Rise of Swarajya Campaign Codex: one self-contained offline HTML file.
All mission text is read back from the generated scenario files, so the codex always
matches what the game will show."""
import base64
import glob
import html
import io
import json
import os
import re
import sys
import warnings
import logging

warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)
from PIL import Image
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.datasets.effects import EffectId

SRC, MAPS, META, OUTFILE = sys.argv[1:5]
meta = json.load(open(META))


def story_chain(s, prefix):
    """Return display_instructions messages of triggers named '<prefix> N' in order."""
    rows = []
    for t in s.trigger_manager.triggers:
        m = re.fullmatch(rf"{prefix} (\d+)", t.name)
        if not m:
            continue
        for e in t.effects:
            if e.effect_type == EffectId.DISPLAY_INSTRUCTIONS and e.message:
                rows.append((int(m.group(1)), e.message))
    return [r[1] for r in sorted(rows)]


def epilogue(s):
    groups = {}
    for t in s.trigger_manager.triggers:
        m = re.fullmatch(r"Epilogue (\d+) (\d+)", t.name) or re.fullmatch(r"Epilogue (\d+)", t.name)
        if not m:
            continue
        key = (int(m.group(1)), int(m.group(2))) if m.lastindex == 2 else (0, int(m.group(1)))
        for e in t.effects:
            if e.effect_type == EffectId.DISPLAY_INSTRUCTIONS and e.message:
                groups[key] = e.message
    return [groups[k] for k in sorted(groups)]


def say(msg):
    """Render 'Speaker: text' as dialogue, everything else as narration."""
    m = re.match(r"^([A-Z][A-Za-z .()'0-9-]{2,40}): (.+)$", msg, re.S)
    if m:
        return (f'<p class="dlg"><span class="who">{html.escape(m.group(1))}</span>'
                f'<span class="txt">&ldquo;{html.escape(m.group(2))}&rdquo;</span></p>')
    return f'<p class="nar">{html.escape(msg)}</p>'


def img64(path):
    im = Image.open(path).convert("RGB")
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=80, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


chapters = []
for p in sorted(glob.glob(SRC + "/*.aoe2scenario")):
    base = os.path.basename(p)[:-13]
    s = AoE2DEScenario.from_file(p)
    mm = s.message_manager
    title, sub = meta[base]
    objs = sorted([t for t in s.trigger_manager.triggers if t.display_as_objective],
                  key=lambda t: t.description_order)
    chapters.append(dict(
        base=base, title=title, sub=sub, act=sub.split("|")[0].strip(),
        instructions=mm.instructions.split("\n\n", 1)[-1], history=mm.history, hints=mm.hints,
        victory=mm.victory, loss=mm.loss,
        story=story_chain(s, "Story"), epilogue=epilogue(s),
        objectives=[t.description for t in objs], img=img64(os.path.join(MAPS, base + ".png")),
    ))

HEROES = [
    ("Chhatrapati Shivaji Maharaj", "Founder of Swarajya", "Playable in chapters 1-9. Bonus health, attack and armour; his fall ends the mission."),
    ("Rajmata Jijabai", "The heart of Swarajya", "Speaks in the prologues and epilogues; a playable unit in The Crown of Swarajya."),
    ("Baji Prabhu Deshpande", "Defender of Pavan Khind", "Huge armour and health. His survival is not required for victory."),
    ("Tanaji Malusare", "The Lion of Sinhagad", "A close-combat titan; Torna companion, Sinhagad climber, and the campaign's great sacrifice."),
    ("Bahirji Naik", "Chief of intelligence", "Reveals enemy camps and hidden paths in Pratapgad, the Lal Mahal raid and Surat."),
    ("Jiva Mahala", "The bodyguard", "+8 attack. 'Hota Jiva mhanun vachla Shiva' - because Jiva was there, Shiva lived."),
    ("Murarbaji Deshpande", "Defender of Purandar", "High morale defender; an optional objective asks you to keep him alive."),
    ("Netaji Palkar", "Cavalry commander", "Fast raider in Pratapgad and Surat."),
    ("Chhatrapati Sambhaji Maharaj", "Warrior, scholar, king", "Playable in chapters 10-15."),
    ("Kavi Kalash", "Poet and advisor", "Sambhaji's companion to the very end."),
    ("Hambirrao Mohite", "Sarsenapati", "Commander-in-chief. Winning him over decides The Crown of Conflict."),
    ("Yesaji Kank, Suryaji Malusare, Hiroji Farzand, Madari Mehtar", "Companions", "Each appears as a named unit with his own story role."),
]
FOES = [
    ("Afzal Khan", "Adilshahi general - Pratapgad"), ("Siddi Jauhar", "Besieger of Panhala - Pavan Khind"),
    ("Shaista Khan", "Mughal viceroy in Pune - the Lal Mahal"), ("Mirza Raja Jai Singh I", "Strategist of the Purandar campaign: honourable, patient, formidable"),
    ("Diler Khan", "Commander of the assault on Purandar"), ("Emperor Aurangzeb", "The overarching imperial antagonist of both halves"),
    ("Udaybhan Rathod", "Killedar of Kondhana"), ("Muqarrab Khan", "Mughal commander at Sangameshwar, 1689"),
]
CIV = [
    ("Civilization name", "Shown in game as <b>Marathas</b> (Gurjaras base, renamed by trigger)."),
    ("Cavalry", "All cavalry +2 line of sight."),
    ("Raiding", "Light cavalry and Shrivamsha Riders +3 attack against buildings."),
    ("Infantry", "Militia, spear and skirmisher lines cost 10% less food."),
    ("Fortifications", "Castles, towers and walls +15% hit points."),
    ("Heroes", "Named heroes receive their own health, attack, armour and lore text."),
    ("Night and weather", "Lighting changes per chapter: monsoon mist at Pavan Khind, night at the Lal Mahal, darkness at Sinhagad, twilight at Sangameshwar."),
]

acts = []
for c in chapters:
    if not acts or acts[-1][0] != c["act"]:
        acts.append((c["act"], []))
    acts[-1][1].append(c)

parts = []
for act, chs in acts:
    parts.append(f'<section class="act"><h2 class="acttitle">{html.escape(act)}</h2>')
    for c in chs:
        parts.append(f'''
<article class="chapter" id="{c["base"]}">
  <header><p class="kicker">{html.escape(c["sub"])}</p><h3>{html.escape(c["title"])}</h3></header>
  <figure><img src="{c["img"]}" alt="Briefing map: {html.escape(c["title"])}" loading="lazy"></figure>
  <div class="cols">
    <div class="col">
      <h4>Before the battle</h4>
      {''.join(say(x) for x in c["story"])}
      <h4>Your orders</h4>
      <ol class="objs">{''.join(f"<li>{html.escape(o)}</li>" for o in c["objectives"])}</ol>
      <p class="hint"><b>Hints.</b> {html.escape(c["hints"]).replace(chr(10), " &middot; ")}</p>
    </div>
    <div class="col">
      <h4>After the battle</h4>
      {''.join(say(x) for x in c["epilogue"]) or say(c["victory"])}
      <h4>History</h4>
      <p class="hist">{html.escape(c["history"])}</p>
    </div>
  </div>
</article>''')
    parts.append("</section>")

toc = "".join(f'<li><a href="#{c["base"]}">{html.escape(c["title"])}</a><span>{html.escape(c["sub"].split("|")[-1].strip())}</span></li>' for c in chapters)
heroes = "".join(f'<div class="card"><h5>{html.escape(a)}</h5><p class="role">{html.escape(b)}</p><p>{html.escape(d)}</p></div>' for a, b, d in HEROES)
foes = "".join(f'<div class="card foe"><h5>{html.escape(a)}</h5><p>{html.escape(b)}</p></div>' for a, b in FOES)
civ = "".join(f"<tr><th>{a}</th><td>{b}</td></tr>" for a, b in CIV)

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rise of Swarajya</title>
<style>
:root{{--ink:#2b1a0e;--paper:#f3e6c8;--paper2:#e9d6ac;--saffron:#d9731a;--deep:#3a1f0d;--gold:#c9a25a;--muted:#6d5338;--bg:#1b120b}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--paper:#2a1d13;--paper2:#33241a;--ink:#f1e2c4;--muted:#c9b08a;--bg:#120c07}}}}
:root[data-theme="dark"]{{--paper:#2a1d13;--paper2:#33241a;--ink:#f1e2c4;--muted:#c9b08a;--bg:#120c07}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 Georgia,"Iowan Old Style","Palatino Linotype",serif}}
.hero{{min-height:78vh;display:grid;place-items:center;text-align:center;padding:48px 16px;
 background:radial-gradient(ellipse at 50% 30%,#5a2c0e 0,#2a140a 55%,#140a05 100%);color:#f6dfb0}}
.hero h1{{font-size:clamp(42px,9vw,96px);letter-spacing:.04em;margin:.1em 0;color:#f4b860;text-shadow:0 3px 0 #5a250a}}
.hero .flag{{width:74px;height:96px;margin:0 auto 18px;background:linear-gradient(135deg,#ff8a1f,#d65c00);clip-path:polygon(0 0,100% 18%,30% 40%,100% 62%,0 100%)}}
.hero p{{max-width:720px;margin:12px auto;color:#e9cfa0}} .hero .sub{{letter-spacing:.3em;text-transform:uppercase;font-size:13px;color:#d9a65c}}
main{{max-width:1180px;margin:0 auto;padding:0 16px 80px}}
.panel{{background:var(--paper);border:1px solid var(--gold);border-radius:6px;padding:28px;margin:28px 0;box-shadow:0 8px 30px #0006}}
h2{{font-size:30px;margin:0 0 14px;color:var(--saffron)}} .acttitle{{text-align:center;font-size:36px;margin:64px 0 8px;color:#f4b860;letter-spacing:.06em}}
.toc{{columns:2 320px;padding:0;list-style:none}} .toc li{{display:flex;justify-content:space-between;gap:12px;border-bottom:1px dotted var(--gold);padding:4px 0;break-inside:avoid}}
.toc a{{color:var(--ink);text-decoration:none}} .toc a:hover{{color:var(--saffron)}} .toc span{{color:var(--muted)}}
.chapter{{background:var(--paper);border:1px solid var(--gold);border-radius:6px;margin:28px 0;overflow:hidden;box-shadow:0 8px 30px #0007}}
.chapter header{{background:var(--deep);color:#f6dfb0;padding:18px 26px}} .chapter h3{{margin:2px 0 0;font-size:30px;color:#f4b860}}
.kicker{{margin:0;font-size:13px;letter-spacing:.18em;text-transform:uppercase;color:#d9a65c}}
figure{{margin:0;background:#c9b07c}} figure img{{display:block;width:100%;height:auto}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:28px;padding:24px 26px}} @media (max-width:800px){{.cols{{grid-template-columns:1fr}}}}
h4{{font-size:14px;letter-spacing:.2em;text-transform:uppercase;color:var(--saffron);border-bottom:1px solid var(--gold);padding-bottom:4px;margin:18px 0 10px}}
.nar{{font-style:italic;color:var(--muted);margin:8px 0}} .dlg{{margin:10px 0;padding-left:12px;border-left:3px solid var(--saffron)}}
.who{{display:block;font-weight:bold;font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--saffron)}}
.objs li{{margin:4px 0}} .hint{{font-size:15px;background:var(--paper2);padding:10px 12px;border-radius:4px}} .hist{{font-size:15.5px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}}
.card{{background:var(--paper2);border-radius:5px;padding:14px;border-top:4px solid var(--saffron)}} .card.foe{{border-top-color:#2f6b3a}}
.card h5{{margin:0 0 4px;font-size:17px}} .card p{{margin:4px 0;font-size:15px}} .role{{color:var(--saffron);font-style:italic}}
table{{width:100%;border-collapse:collapse}} th,td{{text-align:left;padding:8px 10px;border-bottom:1px solid var(--gold);vertical-align:top}} th{{width:28%;color:var(--saffron)}}
code{{background:var(--paper2);padding:1px 5px;border-radius:3px;font-size:14px;word-break:break-all}}
.quote{{font-size:20px;font-style:italic;text-align:center;max-width:760px;margin:24px auto;color:#f4b860}}
footer{{text-align:center;color:#a88b62;font-size:14px;padding:30px 16px}}
</style></head><body>
<section class="hero"><div><div class="flag" aria-hidden="true"></div><p class="sub">An Age of Empires II: Definitive Edition campaign</p>
<h1>Rise of Swarajya</h1><p class="sub">1646 &ndash; 1689 &middot; Fifteen chapters &middot; Five acts</p>
<p>Shivaji Maharaj's story is the creation of Swarajya. Sambhaji Maharaj's is its defence against an empire. And the generation that followed would ensure it survived.</p></div></section>
<main>
<div class="panel"><h2>Chapters</h2><ol class="toc">{toc}</ol></div>
{''.join(parts)}
<p class="quote">&ldquo;The king was gone. The emperor believed the war was over. But Swarajya was not a kingdom held together by one man. It was an idea that had taken root in the Sahyadris. And the struggle continued.&rdquo;</p>
<div class="panel"><h2>Heroes of Swarajya</h2><div class="grid">{heroes}</div></div>
<div class="panel"><h2>Adversaries</h2><p>Opponents are drawn as people with their own reasons, not cartoon villains. The Siddis of Janjira and the Portuguese of Goa appear as political powers, not as communities to be hated.</p><div class="grid">{foes}</div></div>
<div class="panel"><h2>The Marathas as a civilization</h2><table>{civ}</table></div>
<div class="panel"><h2>Coming next: The Unconquered Marathas (1689&ndash;1707)</h2><p>Rajaram's escape to Jinji, the eight-year siege, Santaji Ghorpade and Dhanaji Jadhav's guerrilla war, and Maharani Tarabai's leadership until Aurangzeb's death. The final chapter's epilogue introduces all three.</p></div>
<div class="panel"><h2>Installing on Mac (Feral AoE2 DE)</h2>
<p>Scenarios: copy the fifteen <code>RS01&hellip;RS15 .aoe2scenario</code> files to <code>~/Library/Application Support/Feral Interactive/Age Of Empires II/VFS/User/Games/Age of Empires 2 DE/&lt;steam-id&gt;/resources/_common/scenario/</code></p>
<p>Campaign: copy <code>Rise_of_Swarajya.aoe2campaign</code> to the sibling folder <code>&hellip;/resources/_common/campaign/</code>, then open Campaigns &rarr; Custom Campaigns.</p>
<p>If the campaign does not appear, build it in one minute: Editors &rarr; Campaign Editor &rarr; New, add RS01 to RS15 in order, save as &ldquo;Rise of Swarajya&rdquo;.</p></div>
</main><footer>Rise of Swarajya &middot; fan-made historical campaign &middot; generated with AoE2ScenarioParser</footer></body></html>'''
open(OUTFILE, "w").write(page)
print(OUTFILE, os.path.getsize(OUTFILE) // 1024, "KB")
