from common import *


# =====================================================================
# 2. PRATAPGAD (1659)
# =====================================================================
def pratapgad():
    m = Mission("SW2_Pratapgad.aoe2scenario", "The Tiger's Claws at Pratapgad", 120,
                T.GRASS_JUNGLE, seed=1659)
    sahyadri_base(m, density=45)
    m.path(T.WATER_MEDIUM, [(0, 95), (40, 88), (80, 100), (119, 92)], 2)       # Koyna
    m.path(T.SHALLOWS, [(58, 90), (60, 98)], 2)
    m.path(T.SHALLOWS, [(100, 90), (101, 99)], 2)
    m.path(T.ROAD_BROKEN, [(30, 36), (44, 50), (70, 70), (95, 100)], 1)
    m.ridge([(0, 60), (25, 55)], 4, 3)
    m.ridge([(75, 10), (85, 45)], 4, 3)

    m.players(3)
    swarajya(m, food=800, wood=800, gold=600, stone=300)
    m.player(2, "Adilshahi army of Afzal Khan", ADILSHAHI, PURPLE, food=3000, wood=3000,
             gold=3000, stone=1000)
    m.player(3, "Hidden Maratha bands", MARATHA, YELLOW)
    m.diplomacy(1, 2, DiplomacyState.NEUTRAL)
    m.diplomacy(1, 3, DiplomacyState.ALLY)
    m.diplomacy(2, 3, DiplomacyState.NEUTRAL)

    fort = fort_on_hill(m, 1, 28, 30, r=7, h=6, towers=4, gate_angles=(45,))
    shivaji = m.unit(1, H.PRITHVIRAJ, 32, 34, name="Shivaji Maharaj")
    jiva = m.unit(1, U.CHAMPION, 33, 35, name="Jiva Mahala")
    m.group(1, U.CHAMPION, 6, 26, 28, cols=3)
    m.group(1, U.ARCHER, 6, 30, 26, cols=3)
    m.camera(1, 32, 34)

    pav = (42, 46, 54, 56)
    m.blob(T.DIRT_1, 48, 51, 5, 0)
    m.unit(0, O.GARDEN_PAVILION, 48, 51)
    for fx, fy in ((44, 47), (52, 47), (44, 55), (52, 55)):
        m.unit(0, O.TORCH_A, fx, fy)
    afzal = m.unit(2, H.IBRAHIM_LODI, 49, 52, name="Afzal Khan")
    banda = m.unit(2, U.ELITE_GHULAM, 51, 52, name="Sayyed Banda")
    m.group(2, U.GHULAM, 4, 52, 54, cols=2)

    # Hidden Maratha bands in the Jawali forest
    bands = [(64, 38), (40, 72), (72, 64)]
    for bx, by in bands:
        m.blob(T.GRASS_JUNGLE, bx, by, 4, 0)
        m.group(3, U.SPEARMAN, 6, bx, by, cols=3)
        m.group(3, U.SKIRMISHER, 4, bx + 3, by, cols=2)
        m.group(3, U.LIGHT_CAVALRY, 3, bx, by + 3, cols=3)
    netaji = m.unit(3, U.LIGHT_CAVALRY, 72, 68, name="Netaji Palkar")
    moro = m.unit(3, U.CHAMPION, 40, 76, name="Moropant Pingle")

    # Afzal Khan's great camp at Wai / Par
    pcamp = camp(m, 2, 96, 108)
    m.unit(2, B.SIEGE_WORKSHOP, 104, 112)
    m.unit(2, B.ARCHERY_RANGE, 88, 112)
    m.group(2, U.BATTLE_ELEPHANT, 6, 96, 100, cols=3, spacing=2)
    m.group(2, U.KNIGHT, 10, 90, 104, cols=5)
    m.group(2, U.CROSSBOWMAN, 10, 100, 103, cols=5)
    m.group(2, U.LONG_SWORDSMAN, 10, 86, 108, cols=5)
    m.group(2, U.BOMBARD_CANNON, 2, 108, 106, cols=2, spacing=2)

    bahirji = m.unit(1, U.SCOUT_CAVALRY, 36, 30, name="Bahirji Naik")
    m.hero_setup("Shivaji Maharaj", hp=200, attack=3, melee_armor=2,
                 desc="Shivaji Maharaj. Under his robe: a steel chainmail coat. On his fingers: the wagh nakh, tiger claws.")
    m.hero_setup("Jiva Mahala", hp=250, attack=8, melee_armor=2,
                 desc="Jiva Mahala. Shivaji's personal bodyguard, a master of the dandpatta. 'Hota Jiva mhanun vachla Shiva.'")
    m.hero_setup("Bahirji Naik", hp=60,
                 desc="Bahirji Naik. Chief of Shivaji's intelligence. Master of disguise; knows every hidden path in Jawali.")
    m.hero_setup("Netaji Palkar", hp=150, attack=3,
                 desc="Netaji Palkar. Sarnaubat of the cavalry, called 'the second Shivaji' for his speed.")
    m.hero_setup("Afzal Khan", hp=300, desc="Afzal Khan. Towering Adilshahi general who has sworn to bring Shivaji back to Bijapur in chains.")
    m.mood(ColorMood.JUNGLE)
    m.story([
        "1659. Bijapur has had enough of the rebel Shivaji. General Afzal Khan marches with a vast army, desecrating temples at Tuljapur and Pandharpur on the way.",
        ("Rajmata Jijabai", "This is the man who killed your elder brother Sambhaji at Kanakgiri. Go with Bhavani's blessing, Shivba. But go armoured."),
        ("Bahirji Naik", "Raje, my men are in the Khan's camp as water-carriers. He hides a dagger in his sleeve. He means to kill you at the meeting.", (96, 104)),
        ("Shivaji Maharaj", "Then we meet him as he wishes: two guards each, no weapons in sight. Jiva, stay close.", (48, 51)),
        ("Netaji Palkar", "My horsemen and Moropant's infantry wait in the Jawali forest. At the cannon's signal, we fall on his army.", (64, 38)),
        "Take Shivaji Maharaj to the pavilion. Do not attack before the meeting: the Adilshahi army is neutral.",
    ])
    intel = m.trig("Bahirji: Jawali paths")
    intel.new_condition.timer(timer=40)
    m.reveal(intel, [(64, 38), (40, 72), (72, 64), (96, 108)])
    m.line(intel, "Bahirji Naik", "I have marked our hidden bands and the Khan's camp at Par. The forest paths are yours, Raje.")

    o1 = m.objective("Obj 1: The meeting", "Bring Shivaji Maharaj to the pavilion at the foot of Pratapgad.", 1)
    m.arrive(o1, shivaji, pav)
    m.say(o1, "Afzal Khan embraces Shivaji and strikes with a hidden dagger — the armour holds! The tiger claws answer. Afzal Khan falls. The fort's cannon fires the signal!", 14)
    m.kill(o1, 2, afzal)
    m.set_diplo(o1, 1, 2, DiplomacyState.ENEMY)
    m.handover(o1, 3, 1, (0, 0, 119, 119), ObjectType.MILITARY)
    m.area_task(o1, 2, pcamp, 48, 51)

    o2 = m.objective("Obj 2: Sayyed Banda", "Defeat Sayyed Banda, Afzal Khan's bodyguard.", 2, enabled=False)
    o2.new_condition.destroy_object(unit_object=banda.reference_id)
    m.say(o2, "Jiva Mahala cuts down Sayyed Banda. 'Hota Jiva mhanun vachla Shiva' — because Jiva was there, Shiva lived.", 12)
    m.chain(o1, o2)

    o3 = m.objective("Obj 3: Rout the army", "Destroy Afzal Khan's camp buildings near Par, south-east.", 3, enabled=False)
    m.cleared(o3, 2, (80, 96, 119, 119), ObjectType.BUILDING)
    m.chain(o1, o3)
    win = m.trig("Victory", enabled=False)
    win.new_condition.timer(timer=3)
    m.victory(win, "The Adilshahi army is shattered in the Jawali forest. Elephants, guns, horses and treasure fall to Swarajya.", epilogue=[
        ("Shivaji Maharaj", "Bury Afzal Khan with honour below the fort. Our quarrel ended with his life."),
        ("Rajmata Jijabai", "Today the whole Deccan learned your name, Shivba. Tomorrow it will learn to fear it."),
        "Within weeks Maratha cavalry sweeps south to Kolhapur. But Bijapur is not finished: Siddi Jauhar is already gathering a siege army.",
    ])
    m.chain(o3, win)

    ca = m.wave("Counterattack", 2, 240, [(U.KNIGHT, 6), (U.LONG_SWORDSMAN, 8), (U.CROSSBOWMAN, 6)],
                100, 80, 28, 34, enabled=False)
    m.chain(o1, ca)
    m.hero_loss(shivaji, 2, "Shivaji Maharaj")
    m.texts(
        instructions="November 1659. Meet Afzal Khan at the pavilion below Pratapgad. When the signal fires, your hidden bands in the Jawali forest join you. Destroy the Adilshahi camp. Shivaji Maharaj must survive.",
        history="Afzal Khan led a large Bijapuri force against Shivaji in 1659. At a meeting below Pratapgad on 10 November, Afzal Khan attacked Shivaji, who killed him with the wagh nakh. Maratha forces concealed in the forest then routed the leaderless army.",
        hints="Do not attack before the meeting — the Adilshahi army is neutral until the signal.\nCavalry and elephants are slow in the jungle: ambush them in the trees.\nJiva Mahala is strong — use him against Sayyed Banda.",
        victory="Pratapgad's victory makes Shivaji's name known across India.",
        loss="Treachery has won the day.",
    )
    return m.finish(OUT)


# =====================================================================
# 3. PAVAN KHIND (1660)
# =====================================================================
def pavan_khind():
    m = Mission("SW3_Pavan_Khind.aoe2scenario", "The Sacred Pass", 140, T.GRASS_2, seed=1660)
    sahyadri_base(m, T.FOREST_JUNGLE, 40)
    # Barrier ridge with a single narrow gorge (Ghod Khind)
    for i in range(0, 141):
        x, y = i, i
        if abs(x - 70) <= 8:
            continue
        m.blob(T.FOREST_JUNGLE, x, y, 4, 0.1)
    m.ridge([(0, 0), (64, 64)], 4, 2)
    m.ridge([(76, 76), (139, 139)], 4, 2)
    m.path(T.DIRT_3, [(20, 120), (50, 95), (70, 70), (95, 45), (120, 20)], 2)
    m.path(T.WATER_MEDIUM, [(0, 85), (30, 75), (52, 60), (60, 30), (65, 0)], 2)
    m.path(T.SHALLOWS, [(38, 74), (42, 80)], 2)

    m.players(4)
    swarajya(m, food=0, wood=0, gold=0, stone=0)
    m.player(2, "Siddi Jauhar's siege army (Bijapur)", ADILSHAHI, PURPLE, food=5000, wood=5000, gold=5000)
    m.player(3, "Surve and Dalvi (Bijapur vassals)", ADILSHAHI, RED, food=2000, wood=2000, gold=1000)
    m.player(4, "Panhala garrison", MARATHA, YELLOW)
    m.diplomacy(1, 2, DiplomacyState.ENEMY)
    m.diplomacy(1, 3, DiplomacyState.ENEMY)
    m.diplomacy(1, 4, DiplomacyState.ALLY)
    m.diplomacy(2, 3, DiplomacyState.ALLY)
    m.diplomacy(2, 4, DiplomacyState.ENEMY)

    # Panhala besieged (SW)
    fort_on_hill(m, 4, 14, 126, r=6, h=5, towers=3, gate_angles=(315,))
    m.group(4, U.SPEARMAN, 6, 12, 124, cols=3)
    siege_ring = []
    for a in range(200, 360, 22):
        x = round(14 + 18 * math.cos(math.radians(a)))
        y = round(126 + 18 * math.sin(math.radians(a)))
        if 0 < x < 139 and 0 < y < 139:
            siege_ring.append((x, y))
            m.group(2, U.CROSSBOWMAN, 3, x, y, cols=3)
    camp(m, 2, 42, 128)
    jauhar = m.unit(2, H.SHAH, 42, 132, name="Siddi Jauhar")
    m.group(2, U.BOMBARD_CANNON, 3, 34, 118, cols=3, spacing=2)

    # Shivaji's escape column, slipped out on a stormy night (NE of the ring)
    shivaji = m.unit(1, H.PRITHVIRAJ, 44, 100, name="Shivaji Maharaj")
    baji = m.unit(1, U.ELITE_URUMI_SWORDSMAN, 46, 98, name="Baji Prabhu Deshpande")
    fulaji = m.unit(1, U.CHAMPION, 47, 100, name="Phulaji Prabhu")
    m.group(1, U.LIGHT_CAVALRY, 6, 41, 102, cols=3)
    m.group(1, U.SPEARMAN, 10, 48, 102, cols=5)
    m.group(1, U.SKIRMISHER, 8, 48, 105, cols=4)
    m.group(1, U.CHAMPION, 6, 44, 105, cols=3)
    m.camera(1, 44, 100)

    gorge = (63, 63, 77, 77)
    m.unit(0, O.TORCH_A, 70, 70)

    # Vishalgad, blockaded by Surve and Dalvi (NE)
    vg = fort_on_hill(m, 4, 124, 16, r=6, h=6, towers=2, gate_angles=(135,))
    m.group(4, U.SKIRMISHER, 4, 124, 14, cols=2)
    for bx, by in ((108, 30), (114, 36), (104, 22)):
        m.group(3, U.LONG_SWORDSMAN, 4, bx, by, cols=2)
        m.group(3, U.CROSSBOWMAN, 3, bx + 2, by + 2, cols=3)
    m.unit(3, B.BARRACKS, 110, 40)
    surve = m.unit(3, U.KNIGHT, 112, 32, name="Suryarao Surve")
    blockade = (96, 14, 120, 46)

    m.hero_setup("Shivaji Maharaj", hp=200, attack=3, melee_armor=2,
                 desc="Shivaji Maharaj. Escaping besieged Panhala through the monsoon night.")
    m.hero_setup("Baji Prabhu Deshpande", hp=700, attack=6, melee_armor=5, pierce_armor=4,
                 desc="Baji Prabhu Deshpande. Deshpande of Hirdas Maval, sworn to hold Ghod Khind until Vishalgad's cannon fires. His survival is not required.")
    m.hero_setup("Phulaji Prabhu", hp=200, attack=3, melee_armor=2,
                 desc="Phulaji Prabhu. Baji Prabhu's brother, who stands beside him in the gorge.")
    m.hero_setup("Siddi Jauhar", hp=300, desc="Siddi Jauhar. Adilshahi general who has besieged Panhala for four months.")
    m.mood(ColorMood.MISTY)
    m.story([
        "July 1660. For four months Siddi Jauhar has besieged Panhala. The monsoon rages; escape seems impossible.",
        ("Siddi Jauhar", "Not a mouse leaves Panhala. When the rains stop, the rebel is mine.", (42, 132)),
        "Tonight Shiva Kashid, a barber who resembles Shivaji, rides out openly in a palanquin as a decoy. The real Shivaji slips out with 600 men.",
        ("Baji Prabhu Deshpande", "Raje, Vishalgad is a night's march away. I will hold Ghod Khind with three hundred men until I hear your cannon. Three shots.", (70, 70)),
        ("Shivaji Maharaj", "Baji... I will fire them the moment I reach the walls. Not a breath later."),
        "Lead Shivaji Maharaj through the gorge to Vishalgad. Move fast: the pursuit is coming.",
    ])

    alarm = m.trig("Ruse discovered")
    alarm.new_condition.timer(timer=90)
    m.say(alarm, "The decoy is unmasked! Shiva Kashid goes to his death with a smile. Siddi Masud's cavalry pursues Shivaji into the night.")
    p1 = m.wave("Pursuit 1", 2, 1, [(U.KNIGHT, 6), (U.LIGHT_CAVALRY, 6)], 30, 92, 70, 70, enabled=False)
    m.chain(alarm, p1)

    o1 = m.objective("Obj 1: Ghod Khind", "Bring Shivaji Maharaj through Ghod Khind, the narrow gorge.", 1)
    m.arrive(o1, shivaji, gorge)
    m.say(o1, "Baji Prabhu: 'Go, Raje! I will hold this pass until I hear Vishalgad's cannon.' Leave the rearguard here and ride on.", 14)
    for i, (comp, delay) in enumerate([([(U.KNIGHT, 8), (U.LONG_SWORDSMAN, 8)], 30),
                                       ([(U.CROSSBOWMAN, 10), (U.KNIGHT, 6)], 120),
                                       ([(U.LONG_SWORDSMAN, 12), (U.CAVALIER, 6)], 210),
                                       ([(U.CAVALIER, 8), (U.HAND_CANNONEER, 8)], 300)]):
        w = m.wave(f"Gorge assault {i + 1}", 2, delay, comp, 40, 92, 72, 68, enabled=False)
        m.chain(o1, w)

    o2 = m.objective("Obj 2: Break the blockade", "Defeat the Surve and Dalvi troops blockading Vishalgad.", 2, enabled=False)
    m.cleared(o2, 3, blockade)
    m.chain(o1, o2)

    o3 = m.objective("Obj 3: Vishalgad", "Bring Shivaji Maharaj into Vishalgad fort.", 3, enabled=False)
    m.arrive(o3, shivaji, vg)
    m.chain(o2, o3)
    m.say(o3, "Three cannon shots echo across the Sahyadri. In the gorge, the wounded Baji Prabhu hears them and falls at peace. Ghod Khind is now Pavan Khind — the sacred pass.", 16)
    win = m.trig("Victory", enabled=False)
    win.new_condition.timer(timer=16)
    m.victory(win, epilogue=[
        ("Shivaji Maharaj", "Ghod Khind is no longer a gorge. It is Pavan Khind, purified by the blood of Baji Prabhu and his Bandal Mavalas."),
        "Shivaji is safe. But the Mughal Empire has watched Bijapur fail. Aurangzeb sends his own uncle, Shaista Khan, to finish the work.",
    ])
    m.chain(o3, win)

    bp = m.trig("Baji Prabhu falls")
    bp.new_condition.destroy_object(unit_object=baji.reference_id)
    m.say(bp, "Baji Prabhu Deshpande has fallen in the gorge. His sacrifice buys Shivaji precious time.", 10)

    m.hero_loss(shivaji, 2, "Shivaji Maharaj")
    m.texts(
        instructions="13 July 1660. Escape from besieged Panhala. Reach Ghod Khind, leave Baji Prabhu's rearguard to hold it, break the Surve–Dalvi blockade and enter Vishalgad. Shivaji Maharaj must survive.",
        history="Besieged in Panhala by Siddi Jauhar, Shivaji escaped on a rainy night towards Vishalgad. Baji Prabhu Deshpande held the Ghod Khind pass with a small force against the pursuing Bijapuri army until Shivaji reached Vishalgad. Baji Prabhu died of his wounds after the signal; the gorge has since been called Pavan Khind.",
        hints="Don't fight the siege ring — run.\nSplit your army at the gorge: infantry stays, cavalry rides with Shivaji.\nThe gorge is only a few tiles wide; spearmen there can hold off cavalry.",
        victory="Shivaji is safe in Vishalgad.",
        loss="The pursuit catches Shivaji. The sacrifice was in vain.",
    )
    return m.finish(OUT)


# =====================================================================
# 4. LAL MAHAL (1663)
# =====================================================================
def lal_mahal():
    m = Mission("SW4_Lal_Mahal.aoe2scenario", "Night Raid on the Lal Mahal", 100, T.DIRT_2, seed=1663)
    m.forest_scatter(T.FOREST_OAK, 0, 0, 99, 99, 12, 2, 4)
    m.path(T.WATER_BROWN, [(0, 12), (40, 16), (99, 8)], 2)        # Mutha river
    m.path(T.SHALLOWS, [(60, 8), (62, 17)], 2)
    m.path(T.ROAD, [(0, 50), (50, 50), (50, 99)], 1)

    m.players(3)
    swarajya(m, food=0, wood=0, gold=0, stone=0)
    m.player(2, "Mughal army of Shaista Khan", MUGHAL, GREEN, food=5000, wood=5000, gold=5000)
    m.player(3, "Wedding party", MARATHA, YELLOW)
    m.diplomacy(1, 2, DiplomacyState.NEUTRAL)
    m.diplomacy(2, 3, DiplomacyState.NEUTRAL)
    m.diplomacy(1, 3, DiplomacyState.ALLY)
    hold = m.holding_cell(2, 96)

    # Pune town & Lal Mahal compound
    m.blob(T.ROAD_BROKEN, 50, 46, 7, 0)
    m.ring_walls(2, 50, 46, 8, wall=B.PALISADE_WALL, gaps=(180, 0))
    m.unit(2, B.CASTLE, 52, 43, name="Lal Mahal")
    compound = (43, 39, 57, 53)
    shaista = m.unit(2, H.BABUR, 48, 48, name="Shaista Khan")
    m.group(2, U.ELITE_GHULAM, 4, 46, 50, cols=2)
    for vx, vy in ((25, 30), (75, 30), (25, 70), (75, 70), (50, 80)):
        village(m, 2, vx, vy, houses=5, spread=5)
        m.group(2, U.LONG_SWORDSMAN, 4, vx, vy, cols=2)
        m.group(2, U.CROSSBOWMAN, 3, vx + 2, vy + 2, cols=3)
    m.group(2, U.BATTLE_ELEPHANT, 4, 70, 50, cols=2, spacing=2)
    m.group(2, U.CAVALIER, 8, 80, 45, cols=4)
    m.unit(2, B.STABLE, 85, 50)
    m.unit(2, B.BARRACKS, 15, 45)
    initial_mil = 4 + 5 * 7 + 4 + 8

    shivaji = m.unit(1, H.PRITHVIRAJ, 6, 52, name="Shivaji Maharaj")
    m.unit(1, U.CHAMPION, 7, 50, name="Chimnaji Deshpande")
    m.unit(1, U.CHAMPION, 7, 54, name="Babaji Deshpande")
    m.group(1, U.CHAMPION, 10, 3, 48, cols=5)
    m.group(1, U.ELITE_SHRIVAMSHA_RIDER, 6, 3, 56, cols=3)
    m.group(3, U.VILLAGER_MALE, 6, 10, 46, cols=3)          # the "wedding procession"
    m.camera(1, 6, 52)
    sinhagad = (40, 90, 60, 99)
    m.unit(0, O.FLAG_A, 50, 96)

    bahirji = m.unit(1, U.SCOUT_CAVALRY, 5, 46, name="Bahirji Naik")
    m.hero_setup("Shivaji Maharaj", hp=200, attack=4, melee_armor=2,
                 desc="Shivaji Maharaj. Returning by night to the Lal Mahal, the house where he grew up.")
    m.hero_setup("Bahirji Naik", hp=60,
                 desc="Bahirji Naik. Has lived in Pune for weeks disguised as a beggar. He knows the gap in the kitchen wall.")
    m.hero_setup("Chimnaji Deshpande", hp=120, attack=2, desc="Chimnaji Deshpande. Grew up in Pune; knows every lane.")
    m.hero_setup("Babaji Deshpande", hp=120, attack=2, desc="Babaji Deshpande. Chimnaji's brother, Shivaji's guide in the dark.")
    m.hero_setup("Shaista Khan", desc="Shaista Khan. Aurangzeb's maternal uncle, Mughal viceroy of the Deccan, asleep in Shivaji's own house.")
    m.mood(ColorMood.NIGHT)
    m.story([
        "April 1663. Mughal general Shaista Khan has occupied Pune for three years, living in the Lal Mahal: Shivaji's own childhood home.",
        ("Rajmata Jijabai", "I raised you in those rooms, Shivba. Now a Mughal sleeps in them. Take back our honour."),
        ("Bahirji Naik", "It is Ramzan. The camp feasts until midnight and sleeps heavily. A wedding procession has permission to enter town tonight.", (50, 46)),
        ("Shivaji Maharaj", "Then we are wedding guests. Four hundred of us. Quietly."),
        "Enter the Lal Mahal compound without raising the alarm. The Mughal army is neutral for now. If you kill too many sentries, the whole camp will wake.",
    ])
    intel = m.trig("Bahirji: Pune lanes")
    intel.new_condition.timer(timer=30)
    m.reveal(intel, [(50, 46), (25, 30), (25, 70), (50, 80)])
    m.line(intel, "Bahirji Naik", "The guard posts are marked, Raje. The kitchen wall on the south side is old and cracked.")

    alarm = m.trig("Alarm")
    alarm.new_condition.own_fewer_objects(quantity=initial_mil - 4, source_player=2,
                                          object_type=ObjectType.MILITARY)
    m.say(alarm, "Drums! The Mughal camp is awake!")
    m.set_diplo(alarm, 1, 2, DiplomacyState.ENEMY)

    hp = m.trig("Setup: Shaista Khan")
    hp.new_effect.modify_attribute(quantity=1200, object_list_unit_id=H.BABUR.ID, source_player=2,
                                   operation=Operation.SET, object_attributes=ObjectAttribute.HIT_POINTS)
    m.set_hp(hp, 2, shaista, 1200)

    o1 = m.objective("Obj 1: Into the Lal Mahal", "Bring Shivaji Maharaj inside the Lal Mahal compound.", 1)
    m.arrive(o1, shivaji, compound)
    m.say(o1, "Through a breach in the kitchen wall! Shaista Khan wakes and runs for a window — strike him before he escapes!", 12)
    m.set_diplo(o1, 1, 2, DiplomacyState.ENEMY)
    m.move(o1, 2, shaista, 95, 5)

    o2 = m.objective("Obj 2: Strike Shaista Khan", "Wound Shaista Khan before he flees north-east.", 2, enabled=False)
    m.hp_below(o2, shaista, 900)
    m.say(o2, "Shivaji's sword takes three of Shaista Khan's fingers as he drops from the window. Humiliated, he leaves the Deccan.", 12)
    m.teleport(o2, 2, shaista, *hold)
    m.chain(o1, o2)

    fled = m.trig("Shaista escapes", enabled=False)
    fled.new_condition.bring_object_to_area(unit_object=shaista.reference_id, area_x1=90, area_y1=0,
                                            area_x2=99, area_y2=10)
    m.say(fled, "Shaista Khan escaped unharmed. The raid has failed.")
    fled.new_effect.declare_victory(source_player=2, enabled=1)
    m.chain(o1, fled)
    o2.new_effect.deactivate_trigger(trigger_id=fled.trigger_id)
    o2b = m.trig("Shaista struck down", enabled=False)
    o2b.new_condition.destroy_object(unit_object=shaista.reference_id)
    o2b.new_effect.deactivate_trigger(trigger_id=fled.trigger_id)
    o2b.new_effect.deactivate_trigger(trigger_id=o2.trigger_id)
    m.say(o2b, "Shaista Khan is cut down in the Lal Mahal! Now escape!", 10)
    m.chain(o1, o2b)

    o3 = m.objective("Obj 3: Ride for Sinhagad", "Escape with Shivaji Maharaj to the Sinhagad road (south).", 3, enabled=False)
    m.arrive(o3, shivaji, sinhagad)
    m.chain(o2, o3)
    m.chain(o2b, o3)
    m.victory(o3, "Torches blaze on Sinhagad as the raiders vanish into the hills. All India hears of the night at the Lal Mahal.", epilogue=[
        ("Rajmata Jijabai", "Three fingers, Shivba. The Emperor's uncle will count them every day of his life."),
        "Aurangzeb recalls the humiliated Shaista Khan to Bengal. Swarajya needs gold to rebuild what the Mughals burned. Shivaji looks north, to Surat.",
    ])
    for i, d in enumerate((20, 90, 160)):
        w = m.wave(f"Pursuit {i + 1}", 2, d, [(U.CAVALIER, 6), (U.ELITE_GHULAM, 4)], 84, 40, 50, 90,
                   enabled=False)
        m.chain(o2, w)
        m.chain(o2b, w)

    m.hero_loss(shivaji, 2, "Shivaji Maharaj")
    m.texts(
        instructions="5 April 1663, Pune. Slip into town under cover of a wedding procession, reach the Lal Mahal, wound Shaista Khan and escape to Sinhagad. Shivaji Maharaj must survive.",
        history="Mughal viceroy Shaista Khan occupied Pune and the Lal Mahal from 1660. On a night in April 1663 Shivaji entered with a small party, attacked the Khan in his quarters and cut off his fingers as he escaped. Emperor Aurangzeb recalled the disgraced general.",
        hints="Avoid the Mughal patrols: the army is neutral but killing sentries triggers the alarm.\nCavalry are best for catching the fleeing Khan.\nAfter the strike, run — don't fight the whole camp.",
        victory="The Mughal grip on Pune is broken.",
        loss="The raid has failed.",
    )
    return m.finish(OUT)


# =====================================================================
# 5. SURAT (1664)
# =====================================================================
def surat():
    m = Mission("SW5_Surat.aoe2scenario", "The Treasury of Surat", 120, T.GRASS_DRY, seed=1664)
    m.rect(T.WATER_DEEP, 0, 0, 10, 119)
    m.rect(T.WATER_MEDIUM, 11, 0, 14, 119)
    m.rect(T.BEACH, 15, 0, 16, 119)
    m.path(T.WATER_MEDIUM, [(14, 84), (50, 86), (90, 80), (119, 84)], 3)      # Tapi
    m.forest_scatter(T.FOREST_PALM_DESERT, 20, 0, 119, 119, 14, 2, 4)
    m.path(T.ROAD, [(40, 55), (80, 55)], 1)
    m.path(T.ROAD, [(60, 35), (60, 78)], 1)

    m.players(4)
    swarajya(m, food=500, wood=500, gold=0, stone=0)
    m.player(2, "Mughal Surat", MUGHAL, GREEN, food=3000, wood=3000, gold=3000)
    m.player(3, "English Company factory", Civ.BRITONS, RED)
    m.player(4, "Mughal relief army", MUGHAL, PURPLE, food=5000, wood=5000, gold=5000)
    m.diplomacy(1, 2, DiplomacyState.ENEMY)
    m.diplomacy(1, 4, DiplomacyState.ENEMY)
    m.diplomacy(1, 3, DiplomacyState.NEUTRAL)
    m.diplomacy(2, 3, DiplomacyState.NEUTRAL)
    m.diplomacy(2, 4, DiplomacyState.ALLY)

    m.blob(T.ROAD_BROKEN, 60, 56, 18, 0.05)
    m.ring_walls(2, 60, 56, 22, wall=B.PALISADE_WALL, gaps=(45, 180, 300))
    m.unit(2, B.CASTLE, 36, 74, name="Surat Castle")
    inayat = m.unit(2, U.CHAMPION, 36, 70, name="Inayat Khan")
    m.unit(2, B.TOWN_CENTER, 60, 56, name="Mughal Customs House")
    markets = []
    for i, (mx, my) in enumerate([(48, 44), (72, 44), (46, 64), (74, 66), (60, 40), (60, 70)]):
        mk = m.unit(2, B.MARKET, mx, my, name=["Mirza Ali's bazaar", "Virji Vora's warehouse",
                                               "Haji Zahid Beg's warehouse", "Spice market",
                                               "Cloth market", "Jewellers' bazaar"][i])
        markets.append(mk)
    for i in range(14):
        a = math.radians(i * 360 / 14)
        m.unit(2, B.HOUSE, round(60 + 13 * math.cos(a)), round(56 + 13 * math.sin(a)))
    m.group(2, U.CROSSBOWMAN, 8, 56, 52, cols=4)
    m.group(2, U.LONG_SWORDSMAN, 6, 62, 60, cols=3)
    m.unit(2, B.DOCK, 15, 60)
    # English factory, fortified (NE quarter)
    m.ring_walls(3, 78, 36, 4, wall=B.STONE_WALL, gaps=(200,))
    m.unit(3, B.GUARD_TOWER, 78, 36, name="English factory")
    m.group(3, U.HAND_CANNONEER, 6, 78, 40, cols=3)

    shivaji = m.unit(1, H.PRITHVIRAJ, 108, 108, name="Shivaji Maharaj")
    m.group(1, U.ELITE_SHRIVAMSHA_RIDER, 12, 100, 104, cols=4)
    m.group(1, U.LIGHT_CAVALRY, 12, 110, 98, cols=4)
    m.group(1, U.CAVALRY_ARCHER, 8, 104, 112, cols=4)
    m.group(1, U.BATTERING_RAM, 2, 112, 110, cols=2, spacing=2)
    m.camera(1, 108, 108)
    home = (104, 104, 119, 119)

    bahirji = m.unit(1, U.SCOUT_CAVALRY, 112, 104, name="Bahirji Naik")
    netaji = m.unit(1, U.HUSSAR, 104, 100, name="Netaji Palkar")
    m.hero_setup("Shivaji Maharaj", hp=200, attack=3, melee_armor=2,
                 desc="Shivaji Maharaj. Striking the Mughal treasury itself to pay for Swarajya's forts.")
    m.hero_setup("Bahirji Naik", hp=60,
                 desc="Bahirji Naik. Spent weeks in Surat posing as a beggar, mapping every warehouse.")
    m.hero_setup("Netaji Palkar", hp=200, attack=4, melee_armor=1,
                 desc="Netaji Palkar. Sarnaubat of the Maratha cavalry. Excellent mobility and raiding.")
    m.story([
        "January 1664. Mughal armies have ravaged Maharashtra for three years. Swarajya needs gold, and Surat, the Mughals' richest port, has plenty.",
        ("Bahirji Naik", "Raje, I have begged in every lane of Surat. The richest houses are Virji Vora's and Haji Zahid Beg's. The walls are mud.", (60, 56)),
        ("Shivaji Maharaj", "We take from the Emperor's port what his armies took from our villages. No temple, no mosque, no church is to be touched."),
        ("Inayat Khan", "Close the castle gates! Let the merchants fend for themselves!", (36, 74)),
        "Collect 3000 gold by sacking the bazaars, then ride home before the Mughal relief army arrives. The English factory is neutral: leave it alone.",
    ])
    intel = m.trig("Bahirji: Surat map")
    intel.new_condition.timer(timer=25)
    m.reveal(intel, [(48, 44), (72, 44), (46, 64), (74, 66), (60, 40), (60, 70)])
    m.line(intel, "Bahirji Naik", "Every warehouse is marked on your map. Strike fast and keep away from the castle guns.")

    names = ["Mirza Ali", "Virji Vora", "Haji Zahid Beg", "spice market", "cloth market", "jewellers"]
    for mk, nm in zip(markets, names):
        t = m.trig(f"Loot: {nm}")
        t.new_condition.destroy_object(unit_object=mk.reference_id)
        m.gold(t, 1, 600)
        m.say(t, f"The {nm} warehouses are emptied: +600 gold.", 6)

    o1 = m.objective("Obj 1: Treasury", "Collect 3000 gold from Surat's bazaars.", 1)
    o1.new_condition.accumulate_attribute(quantity=3000, attribute=Attribute.GOLD_STORAGE, source_player=1)
    m.say(o1, "The carts are full — gold, pearls and silk. Ride home!", 10)
    o2 = m.objective("Obj 2: Ride home", "Bring Shivaji Maharaj back to the south-east corner.", 2, enabled=False)
    m.arrive(o2, shivaji, home)
    m.chain(o1, o2)
    m.victory(o2, "The plunder of Surat pays for forts, fleets and soldiers. The Mughals have been struck in their own treasury.", epilogue=[
        "Aurangzeb is furious. He sends his finest general, the Rajput Mirza Raja Jai Singh, with Diler Khan and an army of 80,000.",
        ("Shivaji Maharaj", "Jai Singh is no Shaista Khan. He fights with patience, gold and diplomacy. We must guard Purandar."),
    ])

    relief = m.trig("Relief army")
    relief.new_condition.timer(timer=600)
    m.say(relief, "Mughal relief army sighted to the north!")
    m.timer_display(relief, 1, "")
    for i, d in enumerate((1, 120, 240, 360)):
        w = m.wave(f"Relief {i + 1}", 4, d, [(U.CAVALIER, 6), (U.ELITE_ELEPHANT_ARCHER, 3), (U.HAND_CANNONEER, 6)],
                   60, 2, 60, 56, enabled=False)
        m.chain(relief, w)
    warn = m.trig("Relief warning")
    warn.new_condition.timer(timer=1)
    m.timer_display(warn, 600, "Mughal relief army arrives in: %d")

    m.hero_loss(shivaji, 2, "Shivaji Maharaj")
    m.texts(
        instructions="January 1664. Sack the bazaars and customs house of Surat to collect 3000 gold, then return to the south-east corner. A Mughal relief army arrives in 10 minutes. Shivaji Maharaj must survive.",
        history="In January 1664 Shivaji raided Surat, the Mughal empire's busiest port, for several days while its governor sheltered in the fort. The plunder financed the Maratha state and navy. The English and Dutch factories defended themselves and were largely left alone.",
        hints="Each bazaar gives 600 gold when destroyed.\nThe castle has long range — stay out of it.\nThe English factory is neutral and well defended.",
        victory="Swarajya's coffers overflow.",
        loss="Surat becomes Shivaji's grave.",
    )
    return m.finish(OUT)



# =====================================================================
# 6. PURANDAR (1665)  - new chapter: siege, sacrifice and diplomacy
# =====================================================================
def purandar():
    m = Mission("SW5b_Purandar.aoe2scenario", "The Treaty of Purandar", 120, T.GRASS_2, seed=1665)
    sahyadri_base(m, T.FOREST_JUNGLE, 26)
    m.ridge([(0, 30), (24, 40), (30, 20)], 3, 2)
    m.ridge([(70, 100), (100, 90), (119, 104)], 3, 2)
    m.path(T.DIRT_3, [(100, 26), (80, 40), (60, 52), (46, 62)], 2)        # Mughal approach
    m.path(T.ROAD_BROKEN, [(12, 108), (30, 90), (60, 80), (76, 80)], 1)    # road to the treaty camp

    m.players(2)
    swarajya(m, food=1200, wood=1500, gold=600, stone=800, age=StartingAge.IMPERIAL_AGE)
    m.player(2, "Mughal army of Mirza Raja Jai Singh", MUGHAL, GREEN, food=20000, wood=20000,
             gold=20000, stone=10000, age=StartingAge.IMPERIAL_AGE)
    m.diplomacy(1, 2, DiplomacyState.ENEMY)

    # Purandar (main fort) and Vajragad (its twin on the eastern spur)
    pur = fort_on_hill(m, 1, 40, 64, r=8, h=6, towers=4, gate_angles=(200,))
    pur_castle = None
    for u in m.um.get_all_units():
        if u.unit_const == B.CASTLE.ID and int(u.x) == 40 and int(u.y) == 64:
            pur_castle = u
    murar = m.unit(1, H.MIHIRA_BHOJA, 42, 66, name="Murarbaji Deshpande")
    m.group(1, U.HALBERDIER, 8, 38, 68, cols=4)
    m.group(1, U.ARBALESTER, 8, 42, 60, cols=4)
    m.group(1, U.CHAMPION, 6, 36, 62, cols=3)
    m.group(1, U.VILLAGER_MALE, 8, 34, 70, cols=4)
    vaj = fort_on_hill(m, 1, 58, 50, r=4, h=5, castle=False, towers=2, walls=False)
    m.unit(1, B.WATCH_TOWER, 58, 50, name="Vajragad")
    m.group(1, U.ARBALESTER, 4, 57, 52, cols=2)
    m.camera(1, 40, 64)

    shivaji = m.unit(1, H.PRITHVIRAJ, 12, 108, name="Shivaji Maharaj")
    m.group(1, U.LIGHT_CAVALRY, 6, 14, 104, cols=3)

    # Jai Singh's great camp (NE)
    mcamp = camp(m, 2, 96, 22, tents=8)
    m.unit(2, B.CASTLE, 108, 12)
    m.unit(2, B.SIEGE_WORKSHOP, 88, 14)
    jai = m.unit(2, H.AMOGHAVARSHA, 98, 26, name="Mirza Raja Jai Singh")
    diler = m.unit(2, H.SHAYBANI_KHAN, 92, 30, name="Diler Khan")
    m.group(2, U.CAVALIER, 8, 100, 30, cols=4)
    m.group(2, U.ELITE_ELEPHANT_ARCHER, 4, 104, 20, cols=2, spacing=2)
    # The treaty pavilion, between the armies
    tent = (72, 76, 82, 86)
    m.blob(T.DIRT_1, 77, 81, 4, 0)
    m.unit(0, O.GARDEN_PAVILION, 77, 81)
    for fx, fy in ((74, 78), (80, 78), (74, 84), (80, 84)):
        m.unit(0, O.TORCH_A, fx, fy)

    m.hero_setup("Murarbaji Deshpande", hp=900, attack=6, melee_armor=4, pierce_armor=3,
                 desc="Murarbaji Deshpande. Killedar of Purandar. High morale, ferocious in defence. Keep him alive as long as you can.")
    m.hero_setup("Shivaji Maharaj", hp=200, desc="Shivaji Maharaj. Watching from Rajgad as the empire's finest general closes the net.")
    m.hero_setup("Mirza Raja Jai Singh", hp=400,
                 desc="Mirza Raja Jai Singh I of Amber. Aurangzeb's most able general: patient, honourable and relentless.")
    m.hero_setup("Diler Khan", hp=500, attack=6,
                 desc="Diler Khan. Pathan commander leading the assault on Purandar.")
    m.mood(ColorMood.SUMMER)

    m.story([
        "1665. After Surat, Aurangzeb sends his best: Mirza Raja Jai Singh of Amber, with Diler Khan and an army of 80,000.",
        ("Mirza Raja Jai Singh", "Shaista Khan chased Shivaji. I will not chase him. I will take his forts one by one, until he comes to me.", (98, 26)),
        ("Diler Khan", "Purandar first. Give me the guns and it will fall within a week.", (40, 64)),
        ("Murarbaji Deshpande", "Seven hundred Mavalas hold Purandar. Tell the Pathan he will need more than a week."),
        ("Shivaji Maharaj", "Hold, Murarbaji. Every day Purandar stands, I gain a day to save the rest of Swarajya."),
        "Defend Purandar for 12 minutes. Keep Murarbaji Deshpande alive as long as possible.",
    ])

    o1 = m.objective("Obj 1: Hold Purandar", "Keep Purandar's castle standing for 12 minutes.", 1)
    o1.new_condition.timer(timer=720)
    show = m.trig("Siege timer")
    show.new_condition.timer(timer=1)
    m.timer_display(show, 720, "Jai Singh offers terms in: %d")

    om = m.objective("Obj (optional): Murarbaji's stand", "Optional: keep Murarbaji Deshpande alive until the siege ends.", 2)
    om.new_condition.timer(timer=720)
    om.new_condition.objects_in_area(quantity=1, object_list=H.MIHIRA_BHOJA.ID, source_player=1,
                                     area_x1=0, area_y1=0, area_x2=119, area_y2=119)
    m.line(om, "Murarbaji Deshpande", "Purandar still stands, Raje! They will sing of this siege in every village of the Maval.")

    fall = m.trig("Murarbaji falls")
    fall.new_condition.destroy_object(unit_object=murar.reference_id)
    m.line(fall, "Diler Khan", "What a warrior! Surrender, Murarbaji, and I will make you a commander in the Emperor's army!")
    fall2 = m.trig("Murarbaji falls 2", enabled=False)
    fall2.new_condition.timer(timer=8)
    m.say(fall2, "Murarbaji refused, charged Diler Khan's guard with his last breath, and fell. His men fight on in the ruins.", 12)
    m.chain(fall, fall2)
    o1.new_effect.deactivate_trigger(trigger_id=fall.trigger_id)

    vfall = m.trig("Vajragad falls")
    vfall.new_condition.timer(timer=360)
    m.handover(vfall, 1, 2, vaj, ObjectType.BUILDING)
    m.say(vfall, "Mughal guns have dragged themselves onto Vajragad! From its height they can fire down into Purandar.", 12)

    for i in range(6):
        comp = [(U.ELITE_GHULAM, 6 + i), (U.HAND_CANNONEER, 6)]
        if i >= 1:
            comp.append((U.BOMBARD_CANNON, 1 + i // 2))
        if i >= 2:
            comp.append((U.ELITE_ELEPHANT_ARCHER, 2 + i // 2))
        if i >= 4:
            comp.append((U.IMPERIAL_CAMEL_RIDER, 6))
        m.wave(f"Diler Khan assault {i + 1}", 2, 70 + i * 110, comp, 100, 32 if i % 2 else 36, 42, 64)

    lose = m.trig("Purandar falls")
    lose.new_condition.objects_in_area(quantity=1, object_list=B.CASTLE.ID, source_player=1,
                                       area_x1=31, area_y1=55, area_x2=49, area_y2=73, inverted=1)
    m.say(lose, "Purandar has fallen. With it falls the hope of an honourable peace.")
    lose.new_effect.declare_victory(source_player=2, enabled=1)
    o1.new_effect.deactivate_trigger(trigger_id=lose.trigger_id)

    # ---- Ceasefire and treaty
    m.set_diplo(o1, 1, 2, DiplomacyState.NEUTRAL)
    m.line(o1, "Mirza Raja Jai Singh", "Enough blood. Tell Shivaji Raje: come to my tent under my personal guarantee of safety. Let us talk as Rajputs and Marathas.", 14)
    o2 = m.objective("Obj 2: The treaty", "Bring Shivaji Maharaj to Jai Singh's pavilion to negotiate.", 3, enabled=False)
    m.arrive(o2, shivaji, tent)
    m.chain(o1, o2)
    m.teleport(o2, 2, jai, 78, 82)
    m.move(o1, 2, jai, 78, 82)

    m.victory(o2, epilogue=[
        ("Mirza Raja Jai Singh", "The Emperor asks for twenty-three of your forts, including Purandar, Sinhagad and Lohagad. You keep twelve, and your son Sambhaji receives a mansab."),
        ("Shivaji Maharaj", "Twenty-three forts... the work of twenty years. But my people live, and twelve forts remain. I accept."),
        ("Mirza Raja Jai Singh", "And one thing more. Come to Agra, to the Emperor's birthday durbar. My son Ram Singh will guarantee your safety with his life."),
        ("Shivaji Maharaj", "To Agra, then. Into the tiger's den."),
        "11 June 1665: the Treaty of Purandar. Shivaji has lost the battle, but not the war. He sets out for Agra with nine-year-old Sambhaji.",
    ])
    m.hero_loss(shivaji, 2, "Shivaji Maharaj")
    m.texts(
        instructions="1665. Defend Purandar against the army of Mirza Raja Jai Singh and Diler Khan for 12 minutes. Keep Murarbaji Deshpande alive as long as possible. Then bring Shivaji Maharaj to the treaty pavilion. Purandar's castle and Shivaji Maharaj must survive.",
        history="In 1665 the Mughal general Mirza Raja Jai Singh besieged Purandar with Diler Khan. Its killedar Murarbaji Deshpande died fighting after refusing Diler Khan's offer to join the Mughals. To save his remaining territory, Shivaji agreed to the Treaty of Purandar (June 1665), ceding 23 forts, and later agreed to visit Aurangzeb at Agra.",
        hints="Repair the castle with villagers between assaults.\nKill the bombard cannons first.\nMurarbaji is strong but not invincible: pull him back when wounded.\nShivaji can stay safely in the south-west until the treaty.",
        victory="Swarajya bends, but does not break.",
        loss="Purandar is lost.",
    )
    return m.finish(OUT)

# =====================================================================
# 7. AGRA (1666)
# =====================================================================
def agra():
    m = Mission("SW6_Agra.aoe2scenario", "Escape from Agra", 100, T.DIRT_2, seed=1666)
    m.path(T.WATER_MEDIUM, [(99, 0), (88, 30), (95, 60), (99, 99)], 3)       # Yamuna
    m.path(T.SHALLOWS, [(90, 28), (95, 30)], 2)
    m.forest_scatter(T.FOREST_PALM_DESERT, 0, 0, 80, 99, 10, 2, 3)
    m.rect(T.ROAD, 20, 20, 70, 70)
    hold = m.holding_cell(3, 96)

    m.players(4)
    swarajya(m, food=0, wood=0, gold=0, stone=0)
    m.player(2, "Mughal Agra", MUGHAL, GREEN, food=5000, wood=5000, gold=5000)
    m.player(3, "Maratha agents outside Agra", MARATHA, YELLOW)
    m.player(4, "Sweet-sellers", MUGHAL, GRAY)
    m.diplomacy(1, 2, DiplomacyState.NEUTRAL)
    m.diplomacy(1, 3, DiplomacyState.ALLY)
    m.diplomacy(1, 4, DiplomacyState.NEUTRAL)
    m.diplomacy(2, 4, DiplomacyState.NEUTRAL)
    m.diplomacy(2, 3, DiplomacyState.NEUTRAL)

    m.ring_walls(2, 45, 45, 27, wall=B.STONE_WALL, gaps=(30, 210))
    m.unit(2, B.CASTLE, 55, 30, name="Agra Fort")
    m.unit(2, B.WONDER, 30, 30, name="Diwan-i-Aam")
    for gx, gy in ((68, 58), (22, 32)):
        m.group(2, U.ELITE_GHULAM, 4, gx, gy, cols=2)
    for px, py in ((45, 60), (35, 45), (55, 45), (45, 35)):
        m.group(2, U.CROSSBOWMAN, 3, px, py, cols=3)
    m.unit(2, B.STABLE, 60, 62)
    m.unit(2, B.BARRACKS, 30, 62)

    # Ram Singh's haveli where Shivaji is confined
    m.blob(T.GRASS_FOUNDATION, 42, 52, 4, 0)
    m.ring_walls(2, 42, 52, 5, wall=B.PALISADE_WALL, gaps=(90,))
    shivaji = m.unit(1, H.PRITHVIRAJ, 41, 51, name="Shivaji Maharaj")
    sambhaji = m.unit(1, U.VILLAGER_MALE, 43, 51, name="Sambhaji Raje (age 9)")
    hiroji = m.unit(1, U.VILLAGER_MALE, 42, 53, name="Hiroji Farzand")
    m.group(2, U.LONG_SWORDSMAN, 4, 42, 60, cols=4)
    m.camera(1, 42, 52)
    kitchen = (44, 58, 50, 64)
    m.blob(T.DIRT_1, 47, 61, 2, 0)
    basket = m.unit(4, U.TRADE_CART_FULL, 47, 61, name="Basket of sweets")
    basket2 = m.unit(4, U.TRADE_CART_FULL, 48, 62, name="Basket of sweets")

    agents = (80, 82, 92, 95)
    m.group(3, U.LIGHT_CAVALRY, 6, 84, 88, cols=3)
    mathura = (0, 0, 12, 12)
    m.unit(0, O.FLAG_A, 5, 5)

    madari = m.unit(1, U.VILLAGER_MALE, 40, 53, name="Madari Mehtar")
    m.hero_setup("Shivaji Maharaj", hp=200, desc="Shivaji Maharaj. A prisoner in a golden cage, with no army, only wits.")
    m.hero_setup("Hiroji Farzand", desc="Hiroji Farzand. Shivaji's half-brother in looks. He will lie in the royal bed wearing Shivaji's ring.")
    m.hero_setup("Madari Mehtar", desc="Madari Mehtar. A loyal young servant who stays behind to massage 'Shivaji's' feet and fool the guards.")
    m.hero_setup("Sambhaji Raje (age 9)", desc="Sambhaji Raje, nine years old, held hostage with his father.")
    m.mood(ColorMood.EVENING)
    m.story([
        "1666. Under the Treaty of Purandar, Shivaji has come to Aurangzeb's court at Agra. Placed among lesser nobles, he walks out in protest.",
        ("Emperor Aurangzeb", "The mountain rat insults my Diwan-i-Aam? Let him rest in Ram Singh's haveli. Under guard. Forever.", (30, 30)),
        ("Shivaji Maharaj", "I am ill, Hiroji. Very ill. Send sweets to every Brahmin and fakir in Agra. Every day. In the biggest baskets you can find."),
        ("Hiroji Farzand", "The guards checked the first baskets, Raje. Now they only wave them through."),
        "Walk Shivaji Maharaj to the kitchen courtyard where the baskets are loaded. Hiroji will lie in his bed, wearing his ring.",
    ])

    o1 = m.objective("Obj 1: The baskets", "Bring Shivaji Maharaj to the kitchen courtyard (south of the haveli).", 1)
    m.arrive(o1, shivaji, kitchen)
    m.say(o1, "Shivaji and Sambhaji climb into the baskets. Carry them out of Agra and north-west to Mathura!", 12)
    m.teleport(o1, 1, shivaji, *hold)
    m.teleport(o1, 1, sambhaji, hold[0], hold[1])
    m.give(o1, 4, 1, basket)
    m.give(o1, 4, 1, basket2)
    m.handover(o1, 3, 1, (78, 80, 99, 99), ObjectType.MILITARY)

    disc = m.trig("Escape discovered", enabled=False)
    disc.new_condition.timer(timer=150)
    m.say(disc, "Fulad Khan finds Hiroji in the bed! 'He is gone!' Mughal horsemen ride out of every gate!")
    m.set_diplo(disc, 1, 2, DiplomacyState.ENEMY)
    m.chain(o1, disc)
    for i, d in enumerate((1, 60, 120)):
        w = m.wave(f"Hunters {i + 1}", 2, d, [(U.CAVALIER, 5), (U.CAVALRY_ARCHER, 4)], 58, 62, 6, 6,
                   enabled=False)
        m.chain(disc, w)

    o2 = m.objective("Obj 2: Mathura", "Bring a basket of sweets to Mathura (north-west corner).", 2, enabled=False)
    o2.new_condition.bring_object_to_area(unit_object=basket.reference_id, area_x1=0, area_y1=0,
                                          area_x2=12, area_y2=12)
    m.chain(o1, o2)
    alt = m.trig("Mathura (second basket)", enabled=False)
    alt.new_condition.bring_object_to_area(unit_object=basket2.reference_id, area_x1=0, area_y1=0,
                                           area_x2=12, area_y2=12)
    m.chain(o1, alt)
    for t in (o2, alt):
        m.teleport(t, 1, shivaji, 6, 6)
        m.say(t, "At Mathura, Shivaji shaves his beard and becomes a wandering sadhu. Sambhaji stays hidden with trusted Brahmins. Twenty-five days later, Shivaji is home at Rajgad.", 16)
    fin = m.trig("Victory", enabled=False)
    fin.new_condition.timer(timer=14)
    m.victory(fin, epilogue=[
        ("Emperor Aurangzeb", "Vanished? From the heart of my capital? Find him! Search every road to the Deccan!"),
        ("Rajmata Jijabai", "Twenty-five days I waited, and a ragged sadhu knelt at my feet. Only a mother would know him."),
        "Sambhaji is brought home months later. Shivaji now sets about winning back every fort he surrendered at Purandar.",
    ])
    m.chain(o2, fin)
    m.chain(alt, fin)

    lost = m.trig("Both baskets lost", enabled=False)
    lost.new_condition.destroy_object(unit_object=basket.reference_id)
    lost.new_condition.destroy_object(unit_object=basket2.reference_id)
    m.say(lost, "The baskets are seized. Shivaji is recaptured.")
    lost.new_effect.declare_victory(source_player=2, enabled=1)
    m.chain(o1, lost)

    m.hero_loss(shivaji, 2, "Shivaji Maharaj")
    m.texts(
        instructions="August 1666, Agra. Walk Shivaji to the kitchen courtyard, then smuggle the baskets out of the city to Mathura (north-west corner). The guards are neutral — until the escape is discovered.",
        history="Placed under house arrest at Agra after an angry exchange at Aurangzeb's court, Shivaji arranged for large baskets of sweets to be sent out daily. On 17 August 1666 he and Sambhaji escaped in them, while Hiroji Farzand lay in his bed. Shivaji reached Rajgad in disguise weeks later.",
        hints="Two baskets — only one needs to reach Mathura.\nMeet your agents (yellow cavalry, east) for an escort.\nOnce the alarm sounds, take the shortest route out.",
        victory="Aurangzeb's prisoner has vanished.",
        loss="Shivaji remains Aurangzeb's prisoner.",
    )
    return m.finish(OUT)


# =====================================================================
# 7. SINHAGAD (1670)
# =====================================================================
def sinhagad():
    m = Mission("SW7_Sinhagad.aoe2scenario", "The Lion's Fort", 100, T.GRASS_2, seed=1670)
    sahyadri_base(m, T.FOREST_JUNGLE, 20)
    m.hill(52, 44, 11, 7, flat_terrain=T.DIRT_1)
    m.blob(T.FOREST_BUSH, 28, 44, 5, 0.2)

    m.players(2)
    swarajya(m, food=0, wood=0, gold=0, stone=0)
    m.player(2, "Mughal garrison of Kondhana", MUGHAL, GREEN, food=3000, wood=3000, gold=3000)
    m.diplomacy(1, 2, DiplomacyState.ENEMY)

    m.ring_walls(2, 52, 44, 10, gaps=(0, 270))
    m.unit(2, B.CASTLE, 56, 40, name="Kondhana")
    for tx, ty in ((62, 44), (52, 34), (60, 34), (62, 50)):
        m.unit(2, B.GUARD_TOWER, tx, ty)
    udaybhan = m.unit(2, H.PRITHVI, 52, 46, name="Udaybhan Rathod")
    m.group(2, U.TWO_HANDED_SWORDSMAN, 10, 48, 44, cols=5)
    m.group(2, U.HAND_CANNONEER, 6, 58, 46, cols=3)
    m.group(2, U.ELITE_ELEPHANT_ARCHER, 2, 54, 50, cols=2, spacing=2)
    m.group(2, U.CROSSBOWMAN, 6, 64, 40, cols=3)       # gate guard (east)
    m.group(2, U.CROSSBOWMAN, 6, 50, 32, cols=3)       # gate guard (north)
    fort = (40, 32, 64, 56)

    tanaji = m.unit(1, H.GENERAL_ARAIYAN, 26, 88, name="Tanaji Malusare")
    suryaji = m.unit(1, U.CHAMPION, 28, 88, name="Suryaji Malusare")
    shelar = m.unit(1, U.CHAMPION, 24, 88, name="Shelar Mama")
    m.group(1, U.CHAMPION, 10, 22, 92, cols=5)
    m.group(1, U.SPEARMAN, 10, 30, 92, cols=5)
    m.group(1, U.SKIRMISHER, 6, 26, 95, cols=3)
    m.camera(1, 26, 88)
    cliff = (22, 38, 34, 50)
    m.unit(0, O.TORCH_A, 28, 44)

    m.hero_setup("Tanaji Malusare", hp=600, attack=8, melee_armor=3, pierce_armor=2,
                 desc="Tanaji Malusare. Subhedar of the Mavalas. Left his son Rayaba's wedding: 'Aadhi lagin Kondhanyache, mag Rayabache.'")
    m.hero_setup("Suryaji Malusare", hp=250, attack=4, melee_armor=2, desc="Suryaji Malusare. Tanaji's brother, who will carry his legacy.")
    m.hero_setup("Shelar Mama", hp=250, attack=3, melee_armor=2, desc="Shelar Mama. Eighty years old, and still the fiercest swordsman of the Mavalas.")
    m.hero_setup("Udaybhan Rathod", hp=500, attack=4, desc="Udaybhan Rathod. Rajput killedar of Kondhana for the Mughals, a formidable duelist.")
    m.mood(ColorMood.DARKNESS)
    m.story([
        "February 1670. Under the Treaty of Purandar, Shivaji had to give Kondhana fort to the Mughals. Every morning Jijabai looks at it from Rajgad.",
        ("Rajmata Jijabai", "As long as the Mughal flag flies on Kondhana, I cannot rest. Who will bring it back?"),
        ("Tanaji Malusare", "My son's wedding can wait, Aaisaheb. First Kondhana's wedding, then Rayaba's."),
        ("Shelar Mama", "The gates are a wall of Rathod swords. But the Doneghar cliff on the west... nobody guards a cliff that no man can climb.", (28, 44)),
        "Bring Tanaji to the foot of the cliff. On this moonless night his men will climb with ropes.",
    ])

    early = m.trig("Tanaji falls before the climb")
    early.new_condition.destroy_object(unit_object=tanaji.reference_id)
    m.say(early, "Tanaji has fallen before the assault. The attack collapses.")
    early.new_effect.declare_victory(source_player=2, enabled=1)

    o1 = m.objective("Obj 1: The cliff", "Bring Tanaji Malusare to the foot of the western cliff (torch).", 1)
    m.arrive(o1, tanaji, cliff)
    o1.new_effect.deactivate_trigger(trigger_id=early.trigger_id)
    m.say(o1, "Rope by rope, the Mavalas climb the sheer cliff in the dark and drop inside the walls!", 10)
    m.teleport_area(o1, 1, (18, 34, 38, 54), 46, 48)

    o2 = m.objective("Obj 2: Udaybhan", "Defeat Udaybhan Rathod, the fort commander.", 2, enabled=False)
    o2.new_condition.destroy_object(unit_object=udaybhan.reference_id)
    m.chain(o1, o2)

    td = m.trig("Tanaji falls", enabled=False)
    td.new_condition.destroy_object(unit_object=tanaji.reference_id)
    m.say(td, "Tanaji and Udaybhan clash in a terrible duel. Tanaji falls! Suryaji cuts the climbing ropes: 'There is no way back — fight!'", 12)
    m.chain(o1, td)

    o3 = m.objective("Obj 3: Capture Kondhana", "Destroy the fort garrison.", 3, enabled=False)
    m.cleared(o3, 2, fort)
    m.handover(o3, 2, 1, fort, ObjectType.BUILDING)
    m.chain(o1, o3)
    m.say(o3, "Bonfires announce the victory to Rajgad. Shivaji grieves: 'Gad aala, pan Sinha gela' — the fort is won, but the lion is gone. Kondhana is renamed Sinhagad.", 16)
    fin = m.trig("Victory", enabled=False)
    fin.new_condition.timer(timer=16)
    m.victory(fin, epilogue=[
        ("Rajmata Jijabai", "I asked for a fort and was given a lion's life. Let Rayaba's wedding be held at Rajgad, with all of Swarajya as his family."),
        "Within months the Marathas recover fort after fort lost at Purandar. The time has come for Swarajya to have a crowned king.",
    ])
    m.chain(o3, fin)

    lose = m.trig("Army destroyed")
    lose.new_condition.own_fewer_objects(quantity=0, source_player=1, object_type=ObjectType.MILITARY)
    m.say(lose, "No Maratha warriors remain. Kondhana stays in Mughal hands.")
    lose.new_effect.declare_victory(source_player=2, enabled=1)

    m.texts(
        instructions="4 February 1670. Bring Tanaji Malusare to the western cliff of Kondhana to climb in at night. Defeat Udaybhan Rathod and wipe out the garrison.",
        history="Kondhana, ceded to the Mughals in 1665, was recaptured on the night of 4 February 1670 by Tanaji Malusare, who scaled its western cliffs with his men. Tanaji was killed in combat with the commander Udaybhan; his brother Suryaji completed the capture. Shivaji is said to have mourned: 'Gad aala, pan Sinha gela'.",
        hints="Don't attack the gates — the cliff is the only way in.\nThe climbers land in the middle of the garrison: fight in a tight group.\nKeep Suryaji and Shelar Mama alive to lead after Tanaji.",
        victory="Kondhana is Sinhagad — the Lion's Fort.",
        loss="The assault on Kondhana has failed.",
    )
    return m.finish(OUT)


# =====================================================================
# 8. RAIGAD (1674)
# =====================================================================
def raigad():
    m = Mission("SW8_Raigad.aoe2scenario", "Chhatrapati", 140, T.GRASS_1, seed=1674)
    sahyadri_base(m, T.FOREST_JUNGLE, 30)
    m.rect(T.WATER_DEEP, 0, 0, 9, 139)
    m.rect(T.WATER_MEDIUM, 10, 0, 13, 139)
    m.rect(T.BEACH, 14, 0, 15, 139)
    m.path(T.WATER_MEDIUM, [(14, 90), (40, 95), (70, 110), (139, 100)], 2)   # Kal river
    m.path(T.SHALLOWS, [(56, 100), (58, 108)], 2)
    m.path(T.SHALLOWS, [(110, 96), (112, 104)], 2)
    m.hill(70, 60, 11, 7, flat_terrain=T.DIRT_1)
    m.path(T.ROAD, [(70, 72), (70, 135)], 1)

    m.players(3)
    swarajya(m, food=2500, wood=2500, gold=2000, stone=1500, age=StartingAge.IMPERIAL_AGE)
    m.player(2, "Mughal Empire", MUGHAL, GREEN, food=10000, wood=10000, gold=10000, stone=5000,
             age=StartingAge.IMPERIAL_AGE)
    m.player(3, "Siddis of Janjira", SIDDI, GRAY, food=5000, wood=5000, gold=5000,
             age=StartingAge.IMPERIAL_AGE)
    m.diplomacy(1, 2, DiplomacyState.ENEMY)
    m.diplomacy(1, 3, DiplomacyState.ENEMY)
    m.diplomacy(2, 3, DiplomacyState.ALLY)

    raigad_area = (58, 48, 82, 72)
    m.ring_walls(1, 70, 60, 12, gaps=(90,))
    m.unit(1, B.CASTLE, 63, 55, name="Raigad")
    shivaji = m.unit(1, H.PRITHVIRAJ, 70, 66, name="Shivaji Maharaj")
    m.unit(1, B.TOWN_CENTER, 70, 80)
    m.group(1, U.VILLAGER_MALE, 12, 66, 84, cols=6)
    m.group(1, U.VILLAGER_FEMALE, 8, 66, 87, cols=4)
    village(m, 1, 70, 82, houses=8, spread=8)
    m.unit(1, B.DOCK, 15, 92)
    m.unit(1, B.BARRACKS, 80, 84)
    m.unit(1, B.STABLE, 60, 84)
    m.group(1, U.ELITE_SHRIVAMSHA_RIDER, 8, 74, 64, cols=4)
    m.group(1, U.HALBERDIER, 8, 66, 64, cols=4)
    m.group(1, U.ARBALESTER, 8, 74, 56, cols=4)
    m.camera(1, 70, 66)

    gaga = m.unit(1, U.MONK, 134, 120, name="Gaga Bhatt of Varanasi")
    jijabai = m.unit(1, H.SANYOGITA, 72, 64, name="Rajmata Jijabai")
    m.hero_setup("Shivaji Maharaj", hp=250, attack=4, melee_armor=2,
                 desc="Shivaji Maharaj, about to become Chhatrapati: the sovereign of Swarajya.")
    m.hero_setup("Rajmata Jijabai", hp=200,
                 desc="Rajmata Jijabai. The ideological and emotional foundation of Swarajya. She has waited her whole life for this day.")
    m.hero_setup("Gaga Bhatt of Varanasi", hp=150, desc="Gaga Bhatt. The great Sanskrit scholar of Varanasi who will perform the coronation.")
    m.group(1, U.MONK, 2, 132, 122, cols=2)
    m.group(1, U.LIGHT_CAVALRY, 3, 132, 118, cols=3)

    # Mughal frontier base (NE)
    m.unit(2, B.CASTLE, 124, 14)
    m.unit(2, B.TOWN_CENTER, 112, 10)
    m.unit(2, B.SIEGE_WORKSHOP, 130, 26)
    m.group(2, U.VILLAGER_MALE, 10, 108, 16, cols=5)
    # Siddi base (SW sea)
    m.rect(T.GRASS_1, 2, 128, 8, 136)
    m.unit(3, B.CASTLE, 5, 132, name="Danda-Rajpuri")
    m.unit(3, B.DOCK, 11, 124)

    m.story([
        "1674. Swarajya stretches from the Konkan coast to the Deccan plateau: some 300 forts and a navy. Yet the sultans and the Mughals still call Shivaji a rebel.",
        ("Rajmata Jijabai", "A kingdom without a crown is a rebellion, Shivba. Let the world see what we have built."),
        ("Shivaji Maharaj", "Then let it be done properly: with full Vedic rites, the first coronation of its kind in the Deccan in centuries."),
        ("Gaga Bhatt of Varanasi", "I have travelled from Kashi to see the king of the Sahyadri. Bring me safely up the mountain.", (134, 120)),
        "Escort Gaga Bhatt to Raigad, build the Raj Sabha, and guard the rites. Mughal and Siddi raiders will try to stop you.",
    ])

    o1 = m.objective("Obj 1: Gaga Bhatt", "Escort Gaga Bhatt from the eastern road to the Raigad plateau.", 1)
    m.arrive(o1, gaga, raigad_area)
    m.say(o1, "Gaga Bhatt arrives. Now build the Raj Sabha — the great coronation hall — on Raigad.", 10)
    o2 = m.objective("Obj 2: Raj Sabha", "Build a Wonder (the Raj Sabha) on the Raigad plateau.", 2, enabled=False)
    m.present(o2, 1, raigad_area, const=B.WONDER)
    m.chain(o1, o2)
    m.say(o2, "The hall stands complete. Guard Raigad while the rites are performed!", 10)
    o3 = m.objective("Obj 3: The rites", "Defend Raigad for 5 minutes while the coronation rites are performed.", 3, enabled=False)
    o3.new_condition.timer(timer=300)
    m.chain(o2, o3)
    show = m.trig("Rites timer", enabled=False)
    show.new_condition.timer(timer=1)
    m.timer_display(show, 300, "Coronation completes in: %d", slot=1)
    m.chain(o2, show)
    m.say(o3, "6 June 1674. To the sound of conch shells and cannon, Shivaji is crowned Chhatrapati — sovereign of Hindavi Swarajya. A new era, the Rajyabhishek Shaka, begins.", 16)
    fin = m.trig("Victory", enabled=False)
    fin.new_condition.timer(timer=16)
    m.victory(fin, epilogue=[
        ("Rajmata Jijabai", "I have seen my son crowned. Now I can go to Mahadev in peace."),
        "Twelve days after the coronation, Rajmata Jijabai dies at Pachad, at the foot of Raigad.",
        "Chhatrapati Shivaji Maharaj rules for six more years, expanding Swarajya south to Jinji. He dies at Raigad in April 1680.",
        "His son Sambhaji inherits the throne, the forts, and every one of his father's enemies. Aurangzeb is coming.",
    ])
    m.chain(o3, fin)

    m.wave("Mughal raid", 2, 240, [(U.CAVALIER, 6), (U.ELITE_ELEPHANT_ARCHER, 4), (U.HAND_CANNONEER, 8),
                                   (U.BOMBARD_CANNON, 1)], 118, 30, 70, 70, repeat_every=240)
    m.wave("Siddi raid", 3, 300, [(U.TWO_HANDED_SWORDSMAN, 6), (U.ARBALESTER, 6)], 18, 120, 70, 82,
           repeat_every=300)

    lose = m.trig("Raigad falls")
    lose.new_condition.objects_in_area(quantity=1, object_list=B.CASTLE.ID, source_player=1,
                                       area_x1=58, area_y1=48, area_x2=82, area_y2=72, inverted=1)
    m.say(lose, "Raigad has fallen.")
    lose.new_effect.declare_victory(source_player=2, enabled=1)
    m.hero_loss(shivaji, 2, "Shivaji Maharaj")
    m.texts(
        instructions="1674. Escort Gaga Bhatt to Raigad, build the Raj Sabha (a Wonder) on the plateau, and hold out for five minutes while the coronation rites are performed. Mughal and Siddi raids will come. Raigad castle and Shivaji Maharaj must survive.",
        history="On 6 June 1674 Shivaji was crowned Chhatrapati at Raigad by Gaga Bhatt of Varanasi, formally establishing the Maratha kingdom as a sovereign state. He died at Raigad in April 1680, leaving a kingdom of some 300 forts and a navy.",
        hints="Grow the economy first: the Wonder needs 1000 food, wood, stone and gold.\nThe Mughal raids come every 4 minutes from the north-east.\nPalisades and towers on the plateau's ramp make defence easier.",
        victory="Jai Bhavani! Jai Shivaji! The Chhatrapati reigns.",
        loss="The dream of a crowned Swarajya fades.",
    )
    return m.finish(OUT)


ALL = [pratapgad, pavan_khind, lal_mahal, surat, purandar, agra, sinhagad, raigad]

if __name__ == "__main__":
    import os
    os.makedirs(OUT, exist_ok=True)
    for f in ALL:
        print(f())
