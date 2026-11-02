from common import *


def build():
    m = Mission("SW1_Torna.aoe2scenario", "The Oath at Torna", 120, T.GRASS_2, seed=1646)
    sahyadri_base(m)
    # Sahyadri ridges
    m.ridge([(0, 70), (30, 62), (45, 75)], 3, 3)
    m.ridge([(70, 0), (78, 25), (70, 55)], 3, 2)
    m.path(T.WATER_MEDIUM, [(0, 20), (30, 28), (55, 18), (119, 30)], 2)   # Kanad river
    m.path(T.SHALLOWS, [(38, 22), (40, 28)], 2)                            # ford
    m.path(T.SHALLOWS, [(96, 24), (98, 31)], 2)
    m.path(T.ROAD_BROKEN, [(14, 104), (35, 90), (55, 60), (60, 48)], 1)

    m.players(3)
    swarajya(m, food=300, wood=300, gold=0, stone=0)
    m.player(2, "Adilshahi Sultanate (Bijapur)", ADILSHAHI, PURPLE, food=1500, wood=1500,
             gold=1000, stone=500, age=StartingAge.CASTLE_AGE)
    m.player(3, "Maval villages", MARATHA, YELLOW, age=StartingAge.CASTLE_AGE)
    m.diplomacy(1, 2, DiplomacyState.ENEMY)
    m.diplomacy(1, 3, DiplomacyState.ALLY)
    m.diplomacy(2, 3, DiplomacyState.NEUTRAL)

    # --- Shivaji's band (Maval valley, SW)
    shivaji = m.unit(1, H.PRITHVIRAJ, 14, 104, name="Shivaji Raje Bhosale")
    tanaji = m.unit(1, U.CHAMPION, 16, 102, name="Tanaji Malusare")
    yesaji = m.unit(1, U.CHAMPION, 12, 102, name="Yesaji Kank")
    baji = m.unit(1, U.LIGHT_CAVALRY, 16, 106, name="Baji Pasalkar")
    m.group(1, U.SPEARMAN, 12, 10, 108, cols=6)
    m.group(1, U.SKIRMISHER, 8, 18, 108, cols=4)
    m.group(1, U.ARCHER, 6, 22, 104, cols=3)
    m.camera(1, 14, 104)
    village(m, 3, 25, 112, houses=5)
    m.unit(3, B.TOWN_CENTER, 25, 112)

    # --- Torna (Prachandagad), neglected Adilshahi fort
    torna = fort_on_hill(m, 2, 60, 40, r=7, h=6, castle=False, towers=3, gate_angles=(110,))
    m.unit(2, B.WATCH_TOWER, 60, 40, name="Torna Killa")
    m.unit(2, B.BARRACKS, 57, 37)
    m.group(2, U.SPEARMAN, 8, 60, 43, cols=4)
    m.group(2, U.ARCHER, 6, 63, 37, cols=3)
    m.group(2, U.MAN_AT_ARMS, 4, 56, 42, cols=2)
    killedar = m.unit(2, U.LONG_SWORDSMAN, 61, 39, name="Killedar of Torna")
    m.unit(0, O.TREASURE_CHEST, 59, 41)

    # --- Murumbdev hill: future Rajgad
    m.hill(95, 82, 5, 6, flat_terrain=T.DIRT_1)
    rajgad = (89, 76, 101, 88)
    m.unit(0, O.FLAG_A, 95, 82)

    # --- Adilshahi outpost (NE)
    outpost = camp(m, 2, 104, 12)
    m.unit(2, B.TOWN_CENTER, 104, 4)
    m.unit(2, B.WATCH_TOWER, 96, 12)
    m.unit(2, B.WATCH_TOWER, 112, 18)
    m.group(2, U.KNIGHT, 4, 104, 16, cols=4)
    m.group(2, U.CROSSBOWMAN if hasattr(U, "CROSSBOWMAN") else U.ARCHER, 6, 100, 8, cols=3)
    m.group(2, U.VILLAGER_MALE, 6, 108, 6, cols=3)

    # ----------------------------------------------------------- triggers
    m.mood(ColorMood.SPRING)
    m.hero_setup("Shivaji Raje Bhosale", hp=150, attack=2,
                 desc="Shivaji Raje Bhosale, 16. Son of Shahaji Raje and Jijabai. Sworn at Raireshwar to found Hindavi Swarajya.")
    m.hero_setup("Tanaji Malusare", hp=80, attack=2,
                 desc="Tanaji Malusare. Childhood friend of Shivaji from Godoli. A lion in close combat.")
    m.hero_setup("Yesaji Kank", hp=80, melee_armor=1,
                 desc="Yesaji Kank. Trusted companion of the Raireshwar oath, famed for his strength.")
    m.story([
        "1646. The Deccan bleeds between three thrones: the Adilshahi of Bijapur, the fading Nizamshahi, and the Mughal Empire pressing from the north.",
        ("Rajmata Jijabai", "Shivba, your father serves the Sultan far away in Bangalore. But these hills and these people deserve a king of their own."),
        ("Shivaji Raje Bhosale", "At Raireshwar we swore it before Mahadev, Aai: Hindavi Swarajya. Today the oath becomes a fort."),
        ("Tanaji Malusare", "Torna stands neglected, Raje. Its killedar sleeps, and Bijapur's eyes are elsewhere.", (60, 40)),
        ("Yesaji Kank", "Then let us wake him. Har Har Mahadev!"),
        "Lead the Mavalas up the road to Torna and take it. Shivaji Raje must survive.",
    ])

    o1 = m.objective("Obj 1: Seize Torna", "Defeat the garrison of Torna fort.", 1)
    m.cleared(o1, 2, torna)
    m.handover(o1, 2, 1, torna, ObjectType.BUILDING)
    m.say(o1, "Torna is ours! In its ruins the Mavalas find a buried treasure — gold and stone for a new capital.", 12)
    m.gold(o1, 1, 800)
    m.resource(o1, 1, Attribute.STONE_STORAGE, 900)
    m.resource(o1, 1, Attribute.WOOD_STORAGE, 400)
    m.spawn(o1, 1, U.VILLAGER_MALE, 8, 56, 50)

    o2 = m.objective("Obj 2: Raise Rajgad", "Build a Castle on Murumbdev hill (the flag in the east) — it will become Rajgad.", 2, enabled=False)
    m.present(o2, 1, rajgad, const=B.CASTLE)
    m.say(o2, "Murumbdev becomes Rajgad — the king of forts. It will be the capital of Swarajya for 25 years.", 12)
    m.chain(o1, o2)

    o3 = m.objective("Obj 3: Drive out Bijapur", "Destroy every Adilshahi building at the north-east outpost.", 3, enabled=False)
    m.cleared(o3, 2, (90, 0, 119, 26), ObjectType.BUILDING)
    m.chain(o2, o3)

    win = m.trig("Victory", enabled=False)
    win.new_condition.timer(timer=3)
    m.victory(win, "Bijapur's hold on the Maval country is broken. The first stones of Swarajya are laid.", epilogue=[
        ("Rajmata Jijabai", "A fort is a promise made in stone, Shivba. Keep it, and the people will keep you."),
        ("Shivaji Raje Bhosale", "Then we will build a hundred promises across the Sahyadri."),
        "In Bijapur the court laughs at the news of a boy playing at forts. It will not laugh for long.",
    ])
    m.chain(o3, win)

    # Bijapur notices the loss and counter-attacks
    alert = m.trig("Bijapur alerted", enabled=False)
    alert.new_condition.timer(timer=240)
    m.line(alert, "Killedar of Torna", "A jagirdar's son has taken Torna! Bijapur's outpost sends horsemen to punish him!")
    m.chain(o1, alert)
    w1 = m.wave("Wave 1", 2, 1, [(U.KNIGHT, 4), (U.ARCHER, 6), (U.SPEARMAN, 6)], 100, 30, 60, 46,
                enabled=False)
    m.chain(alert, w1)
    w2 = m.wave("Wave 2", 2, 300, [(U.KNIGHT, 6), (U.MANGONEL, 2), (U.LONG_SWORDSMAN, 6)], 100, 30,
                60, 46, enabled=False)
    m.chain(alert, w2)
    w3 = m.wave("Wave 3", 2, 600, [(U.KNIGHT, 6), (U.CROSSBOWMAN, 8), (U.BATTERING_RAM, 2)], 100, 30,
                95, 82, enabled=False)
    m.chain(alert, w3)

    m.hero_loss(shivaji, 2, "Shivaji Raje")

    m.texts(
        instructions="1646, Maval country. Seize Torna from Bijapur, raise a new fort on Murumbdev hill (Rajgad), then drive the Adilshahi outpost out of the valley. Shivaji Raje must survive.",
        history="Shivaji, son of Shahaji Raje Bhosale and Jijabai, grew up in Pune amid the Sahyadri hills. With companions from the Maval valleys he resolved to free the land from the Deccan sultanates. Around 1646 he took Torna, reportedly found treasure there, and used it to fortify Murumbdev, renamed Rajgad.",
        hints="Use the hills: archers on high ground deal extra damage.\nKeep Shivaji behind the spearmen.\nCastle Age is unlocked: you need 650 stone for a Castle.",
        victory="Torna and Rajgad stand under the saffron Bhagwa Dhwaj.",
        loss="The dream of Swarajya ends before it begins.",
    )
    return m.finish(OUT)


if __name__ == "__main__":
    import os
    os.makedirs(OUT, exist_ok=True)
    print(build())
