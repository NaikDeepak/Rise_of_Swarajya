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

    # --- Shivaji Raje's band (Maval valley, SW)
    shivaji = m.unit(1, H.PRITHVIRAJ, 14, 104, name="Shivaji Raje")
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
    m.unit(0, O.RELIC, 59, 41)

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
    m.hero_setup("Shivaji Raje", hp=150, attack=2,
                 desc="Shivaji Raje Bhosale, age 16. Son of Shahaji Raje Bhosale and Rajmata Jijabai Aaisaheb. By tradition, he swore at Raireshwar to found Hindavi Swarajya.")
    m.hero_setup("Tanaji Malusare", hp=80, attack=2,
                 desc="Subhedar Tanaji Malusare. Childhood companion of Shivaji Raje from Godoli. A lion in close combat.")
    m.hero_setup("Yesaji Kank", hp=80, melee_armor=1,
                 desc="Sarnaubat Yesaji Kank. Trusted companion of the Raireshwar oath, famed for his valor and strength.")
    m.story([
        "1646. The Nizamshahi is gone, its lands shared out between the Mughals and the Adilshahi of Bijapur. The Maval hills answer to Bijapur.",
        ("Rajmata Jijabai Aaisaheb", "Shivba Raje, your father Shahaji Raje serves far away in Bangalore. But these hills and these people deserve a ruler of their own."),
        ("Shivaji Raje", "Before Mahadev we promised Swarajya, Aaisaheb. Today that promise becomes a fort."),
        ("Tanaji Malusare", "Torna stands neglected, Raje. Its killedar sleeps, and Bijapur's eyes are elsewhere."),
        ("Yesaji Kank", "Then let us wake him. Har Har Mahadev!"),
        "Lead the Mavalas up the road to Torna and take it. Shivaji Raje must survive.",
    ])

    o1 = m.objective("Obj 1: Seize Torna", "Defeat the killedar and garrison of Torna, then bring your troops into the fort.", 1)
    m.dead(o1, killedar)
    m.cleared(o1, 2, torna)
    m.present(o1, 1, torna, otype=ObjectType.MILITARY, qty=1)
    m.handover(o1, 2, 1, torna, ObjectType.BUILDING)
    m.say(o1, "Torna is ours! Repairing the walls, the Mavalas unearth a buried treasure. Tradition calls it Bhavani Mata's blessing. It will pay for a new fort.", 12)
    m.gold(o1, 1, 800)
    m.resource(o1, 1, Attribute.STONE_STORAGE, 900)
    m.resource(o1, 1, Attribute.WOOD_STORAGE, 400)
    m.spawn(o1, 1, U.VILLAGER_MALE, 8, 56, 50)

    o2 = m.objective("Obj 2: Raise Rajgad", "Fortify Murumbdev hill (the flag in the east) by building a Castle there. This is the beginning of Rajgad.", 2, enabled=False)
    m.present(o2, 1, rajgad, const=B.CASTLE)
    m.say(o2, "Work begins on Murumbdev, the fort that will become Rajgad. It will be the capital of Swarajya for more than two decades.", 12)
    m.chain(o1, o2)

    o3 = m.objective("Obj 3: Drive out Bijapur", "Destroy every Adilshahi building at the north-east outpost.", 3, enabled=False)
    m.cleared(o3, 2, (90, 0, 119, 26), ObjectType.BUILDING)
    m.chain(o2, o3)

    win = m.trig("Victory", enabled=False)
    win.new_condition.timer(timer=3)
    m.victory(win, "With Torna taken and Murumbdev fortified, Shivaji Raje has his first foothold in the Maval country.", epilogue=[
        ("Rajmata Jijabai Aaisaheb", "Shivba, a fort is a promise in stone. Keep faith with the people who build it, and they will keep faith with you."),
        ("Shivaji Raje", "Then Torna is only the first, Aaisaheb. The Sahyadri have many more hills."),
        "News of Torna and Murumbdev reaches Bijapur.",
    ])
    m.chain(o3, win)

    # Bijapur notices the loss and counter-attacks
    alert = m.trig("Bijapur alerted", enabled=False)
    alert.new_condition.timer(timer=240)
    m.line(alert, "Adilshahi outpost commander", "Torna has fallen to Shivaji Raje! Horsemen, ride out and take it back!")
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
        instructions="1646, Maval country. Seize Torna from Bijapur, fortify Murumbdev hill as Rajgad, then drive the Adilshahi outpost out of the valley. Shivaji Raje must survive.",
        history="Shivaji Raje, son of Shahaji Raje Bhosale and Rajmata Jijabai Aaisaheb, grew up in Pune among the Sahyadri hills. Tradition holds that he and his companions from the Maval valleys swore at the Raireshwar temple to found Hindavi Swarajya. Around 1646, at about sixteen, Shivaji Raje took Torna (Prachandagad) and began fortifying nearby Murumbdev, which became Rajgad, his first capital.",
        hints="Use the hills: archers on high ground deal extra damage.\nKeep Shivaji Raje protected behind the spearmen.\nCastle Age is unlocked: you need 650 stone for a Castle.",
        victory="The Bhagwa Dhwaj flies over Torna and Rajgad. Har Har Mahadev!",
        loss="Shivaji Raje has fallen in battle.",
    )
    return m.finish(OUT)


if __name__ == "__main__":
    import os
    os.makedirs(OUT, exist_ok=True)
    print(build())
