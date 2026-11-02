from common import *

SAMBHAJI_NAME = "Chhatrapati Sambhaji Maharaj"


def sambhaji_hero(m, x, y, desc="Chhatrapati Sambhaji Maharaj. Warrior, Sanskrit scholar and poet-king, author of the Budhbhushanam."):
    u = m.unit(1, H.RAJENDRA_CHOLA, x, y, name=SAMBHAJI_NAME)
    m.hero_setup(SAMBHAJI_NAME, hp=250, attack=5, melee_armor=2, pierce_armor=1, desc=desc)
    return u


# =====================================================================
# 0. THE CROWN OF CONFLICT (1680-81)  - new chapter: succession and authority
# =====================================================================
def crown_of_conflict():
    m = Mission("SB0_Crown_of_Conflict.aoe2scenario", "The Crown of Conflict", 120, T.GRASS_2, seed=1680)
    sahyadri_base(m, T.FOREST_JUNGLE, 28)
    m.ridge([(30, 0), (40, 30), (34, 56)], 3, 2)
    m.ridge([(70, 119), (80, 92), (100, 86)], 3, 2)
    m.path(T.WATER_MEDIUM, [(0, 62), (40, 70), (80, 60), (119, 66)], 2)      # Krishna
    m.path(T.SHALLOWS, [(44, 64), (46, 74)], 2)
    m.path(T.SHALLOWS, [(96, 58), (98, 68)], 2)
    m.path(T.ROAD_BROKEN, [(16, 104), (45, 70), (70, 44), (94, 22)], 1)

    m.players(4)
    swarajya(m, food=800, wood=800, gold=600, stone=300, age=StartingAge.IMPERIAL_AGE)
    m.player(2, "Mughal raiders of Diler Khan", MUGHAL, GREEN, food=8000, wood=8000, gold=8000,
             age=StartingAge.IMPERIAL_AGE)
    m.player(3, "Raigad council", MARATHA, YELLOW, age=StartingAge.IMPERIAL_AGE)
    m.player(4, "Army of Hambirrao Mohite", MARATHA, GRAY, age=StartingAge.IMPERIAL_AGE)
    m.diplomacy(1, 2, DiplomacyState.ENEMY)
    m.diplomacy(1, 3, DiplomacyState.NEUTRAL)
    m.diplomacy(1, 4, DiplomacyState.NEUTRAL)
    m.diplomacy(2, 3, DiplomacyState.NEUTRAL)     # raiders hunt Sambhaji's men, not the council
    m.diplomacy(2, 4, DiplomacyState.ENEMY)
    m.diplomacy(3, 4, DiplomacyState.ALLY)

    # Panhala, where Sambhaji is held (SW)
    fort_on_hill(m, 1, 16, 104, r=6, h=5, towers=2, gate_angles=(45,))
    sambhaji = sambhaji_hero(m, 18, 100, desc="Sambhaji Raje, 23. Heir of Shivaji Maharaj, kept at Panhala while the council at Raigad decides the succession.")
    kavi = m.unit(1, U.MONK, 20, 102, name="Kavi Kalash")
    m.group(1, U.ELITE_SHRIVAMSHA_RIDER, 8, 22, 98, cols=4)
    m.group(1, U.CHAMPION, 6, 14, 98, cols=3)
    m.camera(1, 18, 100)
    m.hero_setup("Kavi Kalash", hp=150, desc="Kavi Kalash. Poet, scholar and Sambhaji's closest friend and advisor.")

    # Hambirrao Mohite's army at Talbid (centre)
    hamb_area = (52, 76, 70, 92)
    hamb = m.unit(4, U.HUSSAR, 60, 84, name="Hambirrao Mohite")
    m.group(4, U.HUSSAR, 10, 56, 86, cols=5)
    m.group(4, U.ELITE_SHRIVAMSHA_RIDER, 10, 62, 88, cols=5)
    m.group(4, U.HEAVY_CAVALRY_ARCHER, 6, 58, 80, cols=3)
    camp(m, 4, 62, 86, tents=4)

    # Forts held by the council's killedars
    rajgad = fort_on_hill(m, 3, 56, 30, r=5, h=5, castle=False, towers=2, gate_angles=(220,))
    m.unit(3, B.WATCH_TOWER, 56, 30, name="Rajgad")
    m.group(3, U.HALBERDIER, 4, 55, 33, cols=2)
    prat = fort_on_hill(m, 3, 24, 40, r=5, h=5, castle=False, towers=2, gate_angles=(300,))
    m.unit(3, B.WATCH_TOWER, 24, 40, name="Pratapgad")
    m.group(3, U.HALBERDIER, 4, 23, 43, cols=2)

    # Raigad (NE), held by the council
    raigad = (86, 12, 104, 30)
    m.ring_walls(3, 95, 21, 8, gaps=(225,))
    raicastle = m.unit(3, B.CASTLE, 96, 20, name="Raigad")
    annaji = m.unit(3, U.MONK, 92, 22, name="Annaji Datto")
    soyara = m.unit(3, U.QUEEN, 94, 24, name="Maharani Soyarabai")
    rajaram = m.unit(3, U.VILLAGER_MALE, 95, 25, name="Rajaram Raje (age 10)")
    m.group(3, U.ARBALESTER, 6, 98, 24, cols=3)
    m.group(3, U.CHAMPION, 6, 90, 18, cols=3)
    m.hero_setup("Hambirrao Mohite", hp=300, attack=5, melee_armor=2,
                 desc="Hambirrao Mohite. Sarsenapati, commander-in-chief of the Maratha army. Soyarabai's own brother.")
    m.hero_setup("Annaji Datto", desc="Annaji Datto. Long-serving minister of Shivaji Maharaj, wary of Sambhaji's temper.")
    m.hero_setup("Maharani Soyarabai", desc="Maharani Soyarabai. Shivaji's widow, who wants her son Rajaram on the throne.")

    m.story([
        "April 1680. Chhatrapati Shivaji Maharaj is dead. At Raigad, a council of ministers proclaims his ten-year-old son Rajaram king.",
        ("Annaji Datto", "Sambhaji Raje is brave, but rash. He even went over to the Mughals once. The kingdom needs steadier hands.", (95, 21)),
        ("Maharani Soyarabai", "Rajaram is Shivaji's son too. Let him be crowned, and let the council guide him."),
        ("Kavi Kalash", "Raje, the army will not follow a child and a council. Everything turns on one man: Hambirrao Mohite.", (60, 84)),
        (SAMBHAJI_NAME, "Then I will go to Hambirrao myself. I will not draw my sword on my father's people. Swarajya cannot survive a civil war."),
        "Win over Hambirrao Mohite, rally the killedars of Rajgad and Pratapgad, and enter Raigad. Never attack the council: they are Marathas too.",
    ])

    o1 = m.objective("Obj 1: The Sarsenapati", "Bring Sambhaji Raje to Hambirrao Mohite's camp at Talbid.", 1)
    m.arrive(o1, sambhaji, hamb_area)
    m.line(o1, "Hambirrao Mohite", "My sister wants her son on the throne. But the army needs a king who can fight Aurangzeb. My sword is yours, Raje.", 14)
    m.handover(o1, 4, 1, (0, 0, 119, 119), ObjectType.MILITARY)
    m.handover(o1, 4, 1, (0, 0, 119, 119), ObjectType.BUILDING)

    o2 = m.objective("Obj 2: The killedars", "Bring Sambhaji Raje to Rajgad and to Pratapgad so their killedars declare for him.", 2, enabled=False)
    m.chain(o1, o2)
    r1 = m.trig("Rajgad declares", enabled=False)
    m.arrive(r1, sambhaji, rajgad)
    m.handover(r1, 3, 1, rajgad, ObjectType.BUILDING)
    m.handover(r1, 3, 1, rajgad, ObjectType.MILITARY)
    m.say(r1, "Rajgad's killedar opens the gates: 'Shivaji Maharaj's son is our king.'", 10)
    m.chain(o1, r1)
    r2 = m.trig("Pratapgad declares", enabled=False)
    m.arrive(r2, sambhaji, prat)
    m.handover(r2, 3, 1, prat, ObjectType.BUILDING)
    m.handover(r2, 3, 1, prat, ObjectType.MILITARY)
    m.say(r2, "Pratapgad, where Shivaji faced Afzal Khan, raises its flag for his son.", 10)
    m.chain(o1, r2)
    for t in (r1, r2):
        t.new_effect.activate_trigger(trigger_id=o2.trigger_id)
    o2.new_condition.objects_in_area(quantity=1, object_list=B.WATCH_TOWER.ID, source_player=1,
                                     area_x1=50, area_y1=24, area_x2=62, area_y2=36)
    o2.new_condition.objects_in_area(quantity=1, object_list=B.WATCH_TOWER.ID, source_player=1,
                                     area_x1=18, area_y1=34, area_x2=30, area_y2=46)
    m.say(o2, "With the army and the forts behind him, the council can no longer refuse. March on Raigad.", 10)

    o3 = m.objective("Obj 3: Raigad", "Bring Sambhaji Raje to the gates of Raigad.", 3, enabled=False)
    m.arrive(o3, sambhaji, raigad)
    m.chain(o2, o3)
    m.handover(o3, 3, 1, raigad, ObjectType.BUILDING)

    civil = m.trig("Civil war")
    civil.new_condition.destroy_object(unit_object=raicastle.reference_id)
    m.say(civil, "Maratha fights Maratha at the gates of Raigad. Aurangzeb could not have wished for more.")
    civil.new_effect.declare_victory(source_player=2, enabled=1)
    o3.new_effect.deactivate_trigger(trigger_id=civil.trigger_id)
    for who in (annaji, soyara, rajaram):
        k = m.trig(f"Council harmed {who.reference_id}")
        k.new_condition.destroy_object(unit_object=who.reference_id)
        m.say(k, "Blood of the royal household is spilt. Swarajya tears itself apart.")
        k.new_effect.declare_victory(source_player=2, enabled=1)
        o3.new_effect.deactivate_trigger(trigger_id=k.trigger_id)

    for i, d in enumerate((180, 330, 480, 630)):
        m.wave(f"Diler Khan raid {i + 1}", 2, d, [(U.CAVALIER, 6 + i), (U.HAND_CANNONEER, 4 + i)],
               60, 2, 56 if i % 2 else 24, 30 if i % 2 else 40)

    m.victory(o3, epilogue=[
        ("Maharani Soyarabai", "You have the army, the forts and Raigad. What will you do with us?"),
        (SAMBHAJI_NAME, "Rajaram is my brother. He stays at my side. The council keeps its seats. Our enemy is in Delhi, not in Raigad."),
        "16 January 1681. Sambhaji is crowned Chhatrapati at Raigad. Within months a plot against him is uncovered; the reconciliation will not last.",
        ("Kavi Kalash", "Aurangzeb's rebel son, Prince Akbar, has fled south and asks for your protection, Maharaj."),
        (SAMBHAJI_NAME, "Then the Emperor will come for both of us. Let us strike first. Burhanpur."),
    ])
    m.hero_loss(sambhaji, 2, "Sambhaji Raje")
    m.mood(ColorMood.AUTUMN)
    m.texts(
        instructions="1680. After Shivaji Maharaj's death, a council at Raigad has proclaimed young Rajaram king. Win over the commander-in-chief Hambirrao Mohite, rally the forts of Rajgad and Pratapgad, and enter Raigad. Never attack the council or the royal household. Fight off Mughal raiders exploiting the turmoil.",
        history="On Shivaji's death in April 1680 a group of ministers, with the support of Queen Soyarabai, placed Rajaram on the throne. Sambhaji, then at Panhala, won the support of the commander-in-chief Hambirrao Mohite and took control of Raigad. He was formally crowned on 16 January 1681. The succession dispute left lasting divisions at court.",
        hints="Ride to Hambirrao first: his army changes everything.\nDo not attack yellow (Raigad council) units or buildings.\nMughal raiders come from the north; protect the forts you win.",
        victory="Sambhaji is Chhatrapati.",
        loss="Swarajya falls into civil war.",
    )
    return m.finish(OUT)


# =====================================================================
# 1. BURHANPUR (1681)
# =====================================================================
def burhanpur():
    m = Mission("SB1_Burhanpur.aoe2scenario", "The Raid on Burhanpur", 120, T.GRASS_DRY, seed=1681)
    m.forest_scatter(T.FOREST_BUSH, 0, 0, 119, 119, 14, 2, 4)
    m.path(T.WATER_MEDIUM, [(0, 30), (60, 26), (119, 34)], 3)                # Tapi
    m.path(T.SHALLOWS, [(30, 24), (31, 33)], 2)
    m.path(T.SHALLOWS, [(90, 26), (91, 36)], 2)
    m.hill(10, 108, 6, 6, flat_terrain=T.DIRT_1)                              # Salher

    m.players(3)
    swarajya(m, food=500, wood=500, gold=0, stone=0, age=StartingAge.IMPERIAL_AGE)
    m.player(2, "Mughal Burhanpur", MUGHAL, GREEN, food=5000, wood=5000, gold=5000,
             age=StartingAge.IMPERIAL_AGE)
    m.player(3, "Army of Khan Jahan Bahadur", MUGHAL, PURPLE, food=8000, wood=8000, gold=8000,
             age=StartingAge.IMPERIAL_AGE)
    m.diplomacy(1, 2, DiplomacyState.ENEMY)
    m.diplomacy(1, 3, DiplomacyState.ENEMY)
    m.diplomacy(2, 3, DiplomacyState.ALLY)

    # Walled city (north bank) and the rich suburb of Bahadurpura (south bank)
    m.ring_walls(2, 70, 12, 11, gaps=(90,))
    m.unit(2, B.CASTLE, 70, 10, name="Burhanpur Fort")
    m.group(2, U.HAND_CANNONEER, 6, 66, 16, cols=3)
    bp = (40, 44, 100, 70)
    m.blob(T.ROAD_BROKEN, 70, 56, 12, 0.1)
    for i, (mx, my) in enumerate([(56, 50), (70, 48), (84, 50), (60, 62), (80, 62)]):
        m.unit(2, B.MARKET, mx, my, name=f"Bahadurpura bazaar {i + 1}")
    for i in range(12):
        a = math.radians(i * 30)
        m.unit(2, B.HOUSE, round(70 + 16 * math.cos(a)), round(56 + 12 * math.sin(a)))
    m.group(2, U.ARBALESTER, 6, 70, 56, cols=3)
    m.group(2, U.CHAMPION, 6, 64, 54, cols=3)
    m.unit(2, B.WATCH_TOWER, 52, 56)
    m.unit(2, B.WATCH_TOWER, 88, 56)

    sambhaji = sambhaji_hero(m, 14, 96)
    hambir = m.unit(1, U.HUSSAR, 16, 94, name="Hambirrao Mohite")
    m.group(1, U.ELITE_SHRIVAMSHA_RIDER, 16, 10, 90, cols=4)
    m.group(1, U.HUSSAR, 12, 20, 90, cols=4)
    m.group(1, U.HEAVY_CAVALRY_ARCHER, 8, 16, 100, cols=4)
    m.camera(1, 14, 96)
    salher = (2, 100, 18, 116)

    m.hero_setup("Hambirrao Mohite", hp=300, attack=5, melee_armor=2,
                 desc="Hambirrao Mohite. Sarsenapati of the Maratha army, master of the lightning cavalry raid.")
    m.story([
        "1681. Chhatrapati Sambhaji Maharaj sits on his father's throne. He has inherited a kingdom, and every one of its enemies.",
        ("Emperor Aurangzeb", "My own son Akbar shelters with the son of Shivaji? Then I will march to the Deccan myself and end them both."),
        (SAMBHAJI_NAME, "Before the Emperor comes to us, we go to him. Burhanpur: the gateway of the Mughal Deccan."),
        ("Hambirrao Mohite", "The walled city is too strong, Maharaj. But Bahadurpura, the merchants' quarter across the Tapi, sleeps unguarded.", (70, 56)),
        "Burn the five bazaars of Bahadurpura, then ride back to Salher before Khan Jahan's army catches you.",
    ])

    o1 = m.objective("Obj 1: Bahadurpura", "Destroy the five bazaars of Bahadurpura.", 1)
    m.cleared(o1, 2, bp, const=B.MARKET)
    m.gold(o1, 1, 2500)
    m.say(o1, "Bahadurpura burns for three days. The Deccan learns the new Chhatrapati is no less bold than his father. Ride for Salher!", 12)
    o2 = m.objective("Obj 2: Salher", "Return Sambhaji Maharaj to Salher fort (south-west).", 2, enabled=False)
    m.arrive(o2, sambhaji, salher)
    m.chain(o1, o2)
    m.victory(o2, "The raiders vanish into the hills, laden with treasure.", epilogue=[
        ("Hambirrao Mohite", "Bahadurpura will burn for three days, Maharaj. The Emperor will hear of it in Ajmer."),
        "He does. In 1682 Aurangzeb arrives in the Deccan with the largest army the subcontinent has seen. He will never return to the north.",
    ])

    for i, d in enumerate((420, 540, 660)):
        m.wave(f"Khan Jahan {i + 1}", 3, d, [(U.CAVALIER, 8), (U.ELITE_ELEPHANT_ARCHER, 3),
                                             (U.HAND_CANNONEER, 6)], 110, 4, 60, 70)
    warn = m.trig("Warning")
    warn.new_condition.timer(timer=1)
    m.timer_display(warn, 420, "Khan Jahan Bahadur arrives in: %d")

    m.hero_loss(sambhaji, 3, "Sambhaji Maharaj")
    m.texts(
        instructions="1681. Destroy the five bazaars of Bahadurpura, then return Sambhaji Maharaj to Salher fort. A Mughal army arrives in 7 minutes.",
        history="In early 1681 Sambhaji Maharaj raided Burhanpur, a major Mughal city on the Tapi, sacking its wealthy suburb Bahadurpura. The raid announced that the new Chhatrapati would continue his father's war against the Mughals.",
        hints="Ignore the walled city — its fort is too strong.\nCavalry archers are good against the bazaar guards.\nWatch the timer and leave in time.",
        victory="The Mughal Deccan trembles.",
        loss="The raid ends in disaster.",
    )
    return m.finish(OUT)


# =====================================================================
# 2. RAMSEJ (1682)
# =====================================================================
def ramsej():
    m = Mission("SB2_Ramsej.aoe2scenario", "The Unbreakable Ramsej", 100, T.GRASS_DRY, seed=1682)
    m.forest_scatter(T.FOREST_BUSH, 0, 0, 99, 99, 12, 2, 4)
    m.hill(50, 55, 8, 6, flat_terrain=T.DIRT_1)

    m.players(3)
    swarajya(m, food=1500, wood=1500, gold=800, stone=800, age=StartingAge.IMPERIAL_AGE)
    m.player(2, "Mughal army of Shahabuddin Khan", MUGHAL, GREEN, food=20000, wood=20000,
             gold=20000, stone=10000, age=StartingAge.IMPERIAL_AGE)
    m.player(3, "Maratha relief force", MARATHA, YELLOW, age=StartingAge.IMPERIAL_AGE)
    m.diplomacy(1, 2, DiplomacyState.ENEMY)
    m.diplomacy(1, 3, DiplomacyState.ALLY)
    m.diplomacy(2, 3, DiplomacyState.ENEMY)
    hold = m.holding_cell(96, 96)

    m.ring_walls(1, 50, 55, 9, gaps=(135,))
    castle = m.unit(1, B.CASTLE, 50, 55, name="Ramsej")
    for tx, ty in ((44, 50), (56, 50), (44, 60), (56, 60)):
        m.unit(1, B.GUARD_TOWER, tx, ty)
    m.unit(1, B.TOWN_CENTER, 62, 72)
    m.group(1, U.VILLAGER_MALE, 8, 58, 76, cols=4)
    m.group(1, U.HALBERDIER, 8, 48, 58, cols=4)
    m.group(1, U.ARBALESTER, 10, 50, 52, cols=5)
    m.group(1, U.ELITE_SKIRMISHER, 6, 54, 58, cols=3)
    m.unit(1, U.CHAMPION, 52, 56, name="Killedar Suryaji")
    m.camera(1, 50, 55)

    scamp = (2, 2, 40, 22)
    m.blob(T.DIRT_2, 20, 12, 12, 0.1)
    m.unit(2, B.CASTLE, 20, 8, name="Mughal siege camp")
    m.unit(2, B.SIEGE_WORKSHOP, 10, 16)
    m.unit(2, B.SIEGE_WORKSHOP, 30, 16)
    m.unit(2, B.BARRACKS, 14, 4)
    m.unit(2, B.STABLE, 30, 4)
    m.group(2, U.CAVALIER, 6, 20, 16, cols=3)
    m.group(2, U.HAND_CANNONEER, 6, 24, 12, cols=3)

    m.hero_setup("Killedar Suryaji", hp=400, attack=4, melee_armor=3, pierce_armor=2,
                 desc="Suryaji, killedar of Ramsej. His small garrison will hold an empire at bay for five years.")
    m.story([
        "1682. Aurangzeb has come to the Deccan with an army of half a million, vowing not to return north until the Marathas are crushed.",
        ("Emperor Aurangzeb", "Begin with that little hill fort near Nashik. Ramsej. Shahabuddin Khan says it will fall in a few days."),
        ("Killedar Suryaji", "A few days? Let them come. Every Maratha fort is a mountain, and every mountain is a fortress.", (50, 55)),
        ("Hambirrao Mohite", "Hold, Suryaji. The Chhatrapati is sending Rupaji Bhosale and Manaji More with the cavalry. Fifteen minutes."),
        "Hold Ramsej until the relief force arrives, then smash the siege camp.",
    ])

    for i in range(6):
        comp = [(U.HAND_CANNONEER, 6), (U.TWO_HANDED_SWORDSMAN, 6)]
        if i >= 1:
            comp.append((U.BOMBARD_CANNON, 1 + i // 2))
        if i >= 2:
            comp.append((U.ELITE_BATTLE_ELEPHANT, 2 + i // 2))
        if i >= 3:
            comp.append((U.TREBUCHET, 1))
        m.wave(f"Assault {i + 1}", 2, 60 + i * 140, comp, 40 if i % 2 else 8, 26 if i % 2 else 30, 50, 55)

    o1 = m.objective("Obj 1: Hold Ramsej", "Keep Ramsej castle standing until the relief force arrives (15 min).", 1)
    o1.new_condition.timer(timer=900)
    m.say(o1, "War drums from the south-west! Rupaji Bhosale and Manaji More arrive with the Chhatrapati's cavalry!", 12)
    m.spawn(o1, 1, U.ELITE_SHRIVAMSHA_RIDER, 12, 4, 86)
    m.spawn(o1, 1, U.HUSSAR, 12, 10, 86)
    m.spawn(o1, 1, U.HEAVY_CAVALRY_ARCHER, 8, 4, 92)
    show = m.trig("Relief timer")
    show.new_condition.timer(timer=1)
    m.timer_display(show, 900, "Relief force arrives in: %d")

    o2 = m.objective("Obj 2: Smash the siege camp", "Destroy the Mughal siege camp buildings (north-west).", 2, enabled=False)
    m.cleared(o2, 2, scamp, ObjectType.BUILDING)
    m.chain(o1, o2)
    m.victory(o2, "The Mughal siege collapses. Ramsej will hold out for more than five years: Aurangzeb's first, bitter lesson in the Deccan.", epilogue=[
        "Across the Sahyadri the pattern repeats: the Mughals besiege, the forts hold, Maratha cavalry cuts their supply lines.",
        (SAMBHAJI_NAME, "The Emperor's land army is stalled. Now he turns to the sea, and to his allies the Siddis of Janjira."),
    ])

    lose = m.trig("Ramsej falls")
    lose.new_condition.destroy_object(unit_object=castle.reference_id)
    m.say(lose, "Ramsej castle has fallen.")
    lose.new_effect.declare_victory(source_player=2, enabled=1)
    m.texts(
        instructions="1682. Defend Ramsej fort for 15 minutes against the Mughal siege. When the relief force arrives, destroy the Mughal siege camp. Ramsej castle must survive.",
        history="Aurangzeb's commanders expected the small fort of Ramsej to fall quickly. Instead its garrison, supported by relief forces sent by Sambhaji Maharaj, resisted for over five years, an early sign of how costly the Deccan war would be for the Mughals.",
        hints="Repair the walls and castle with villagers between waves.\nKill bombards and trebuchets first.\nHalberdiers counter the war elephants.",
        victory="Ramsej stands.",
        loss="Ramsej has fallen.",
    )
    return m.finish(OUT)


# =====================================================================
# 3. JANJIRA (1682)
# =====================================================================
def janjira():
    m = Mission("SB3_Janjira.aoe2scenario", "The Sea Fort of Janjira", 120, T.GRASS_1, seed=16821)
    m.rect(T.WATER_DEEP, 0, 0, 70, 119)
    m.rect(T.WATER_MEDIUM, 71, 0, 74, 119)
    m.rect(T.BEACH, 75, 0, 76, 119)
    m.forest_scatter(T.FOREST_PALM_GRASS, 80, 0, 119, 119, 16, 2, 4)
    # Janjira island
    m.blob(T.GRASS_1, 36, 60, 9, 0.05)
    m.blob(T.BEACH, 36, 60, 10, 0.0)
    m.blob(T.GRASS_1, 36, 60, 9, 0.0)
    # Danda-Rajpuri shore (Siddi docks), south-east
    m.rect(T.GRASS_1, 60, 100, 76, 119)
    m.rect(T.BEACH, 60, 99, 76, 99)

    m.players(3)
    swarajya(m, food=3000, wood=3000, gold=2000, stone=1000, age=StartingAge.IMPERIAL_AGE)
    m.player(2, "Siddis of Janjira", SIDDI, GRAY, food=10000, wood=10000, gold=10000, stone=5000,
             age=StartingAge.IMPERIAL_AGE)
    m.player(3, "Mughal allies of the Siddis", MUGHAL, GREEN, food=5000, wood=5000, gold=5000,
             age=StartingAge.IMPERIAL_AGE)
    m.diplomacy(1, 2, DiplomacyState.ENEMY)
    m.diplomacy(1, 3, DiplomacyState.ENEMY)
    m.diplomacy(2, 3, DiplomacyState.ALLY)

    isl = (24, 48, 48, 72)
    m.unit(2, B.CASTLE, 36, 60, name="Janjira (Jazeera Mahroob)")
    m.ring_walls(2, 36, 60, 7, gaps=())
    sea_towers = [(26, 50), (46, 50), (26, 70), (46, 70), (36, 48), (36, 72)]
    for tx, ty in sea_towers:
        m.unit(2, B.BOMBARD_TOWER, tx, ty)
    m.group(2, U.ARBALESTER, 8, 34, 58, cols=4)
    docks = [m.unit(2, B.DOCK, 64, 98), m.unit(2, B.DOCK, 72, 98)]
    m.unit(2, B.TOWN_CENTER, 68, 110)
    m.group(2, U.VILLAGER_MALE, 6, 64, 106, cols=3)
    m.group(2, U.WAR_GALLEY, 6, 50, 80, cols=3, spacing=2)
    m.group(2, U.GALLEON, 4, 20, 40, cols=2, spacing=2)
    m.group(2, U.FAST_FIRE_SHIP, 4, 54, 40, cols=2, spacing=2)
    m.group(2, U.CANNON_GALLEON, 2, 30, 84, cols=2, spacing=2)

    sambhaji = sambhaji_hero(m, 96, 60)
    m.unit(1, B.CASTLE, 100, 60, name="Padmadurg works")
    m.unit(1, B.DOCK, 74, 50)
    m.unit(1, B.DOCK, 74, 70)
    m.unit(1, B.TOWN_CENTER, 100, 80)
    m.unit(1, B.TOWN_CENTER, 100, 40)
    m.group(1, U.VILLAGER_MALE, 10, 96, 84, cols=5)
    m.group(1, U.VILLAGER_FEMALE, 10, 96, 36, cols=5)
    m.group(1, U.WAR_GALLEY, 6, 66, 58, cols=3, spacing=2)
    m.group(1, U.FIRE_SHIP, 4, 66, 66, cols=2, spacing=2)
    m.unit(1, U.GALLEON, 66, 50, name="Daulat Khan's flagship")
    m.group(1, U.HALBERDIER, 6, 92, 56, cols=3)
    m.camera(1, 96, 60)

    m.story([
        "1682. Just off the Konkan coast stands Janjira, the island fortress of the Siddis: Mughal allies who raid Maratha villages and ships.",
        ("Daulat Khan's flagship", "Maharaj, my father served your father's navy. Janjira has never fallen to anyone. Its walls rise straight from the sea.", (36, 60)),
        (SAMBHAJI_NAME, "My father built Padmadurg right under their noses. I will finish what he began, and if I must, I will build a road across the sea."),
        "First cut the Siddis off from their supplies: burn the docks at Danda-Rajpuri. Then silence the bombard towers that guard Janjira's walls.",
    ])

    o1 = m.objective("Obj 1: Danda-Rajpuri", "Destroy both Siddi docks on the south shore.", 1)
    for d in docks:
        o1.new_condition.destroy_object(unit_object=d.reference_id)
    m.say(o1, "The Siddi shipyards burn. No more reinforcements by sea!", 10)
    o2 = m.objective("Obj 2: Silence Janjira", "Destroy every Bombard Tower around the island of Janjira.", 2, enabled=False)
    m.cleared(o2, 2, isl, const=B.BOMBARD_TOWER)
    m.chain(o1, o2)
    m.say(o2, "Janjira's guns are silent and its harbour blockaded. The Siddis will not threaten the Konkan for years.", 12)
    note = m.trig("Epilogue", enabled=False)
    note.new_condition.timer(timer=12)
    m.say(note, "History: Janjira itself was never taken — not by Shivaji, Sambhaji, or anyone. But Sambhaji's campaign broke the Siddi grip on the coast.", 14)
    m.chain(o2, note)
    fin = m.trig("Victory", enabled=False)
    fin.new_condition.timer(timer=14)
    m.victory(fin, epilogue=[
        "The Siddi threat is checked, but the Portuguese at Goa have let Mughal fleets use their harbours. Sambhaji turns south.",
    ])
    m.chain(note, fin)

    m.wave("Siddi landing", 2, 300, [(U.TWO_HANDED_SWORDSMAN, 6), (U.ARBALESTER, 6)], 80, 106, 100, 80,
           repeat_every=300)
    m.wave("Mughal raid", 3, 480, [(U.CAVALIER, 8), (U.HAND_CANNONEER, 6)], 112, 2, 100, 40,
           repeat_every=360)

    m.hero_loss(sambhaji, 2, "Sambhaji Maharaj")
    m.texts(
        instructions="1682. Destroy the two Siddi docks at Danda-Rajpuri, then destroy every Bombard Tower guarding the island fort of Janjira. Sambhaji Maharaj must survive.",
        history="The Siddis of Janjira, allied to the Mughals, were a constant threat to the Maratha coast. Sambhaji Maharaj besieged Janjira in 1682 and even tried to build a stone causeway to it, but the fort held. Janjira was never captured by force.",
        hints="Fire ships and cannon galleons beat galleons and towers.\nBuild a big navy before attacking the island.\nKeep some infantry home for Siddi landings.",
        victory="The Siddi menace is checked.",
        loss="The Konkan coast is lost.",
    )
    return m.finish(OUT)


# =====================================================================
# 4. GOA (1683)
# =====================================================================
def goa():
    m = Mission("SB4_Goa.aoe2scenario", "Low Tide at Santo Estevao", 120, T.GRASS_JUNGLE, seed=1683)
    sahyadri_base(m, T.FOREST_PALM_GRASS, 18)
    m.rect(T.WATER_DEEP, 0, 0, 119, 8)
    m.path(T.WATER_MEDIUM, [(0, 30), (40, 34), (80, 30), (119, 36)], 4)       # Mandovi
    m.path(T.WATER_MEDIUM, [(0, 75), (40, 72), (80, 76), (119, 70)], 4)       # southern channel
    m.path(T.WATER_MEDIUM, [(40, 34), (40, 72)], 3)
    m.path(T.WATER_MEDIUM, [(80, 30), (80, 76)], 3)
    # Low-tide fords (Sambhaji's army crossed at low water)
    m.path(T.SHALLOWS, [(60, 70), (60, 80)], 2)
    m.path(T.SHALLOWS, [(96, 66), (98, 78)], 2)
    m.path(T.SHALLOWS, [(20, 24), (22, 38)], 2)

    m.players(3)
    swarajya(m, food=1500, wood=1500, gold=1500, stone=500, age=StartingAge.IMPERIAL_AGE)
    m.player(2, "Estado da India (Portuguese Goa)", PORTUGUESE, BLUE, food=10000, wood=10000,
             gold=10000, stone=5000, age=StartingAge.IMPERIAL_AGE)
    m.player(3, "Mughal army of Shah Alam", MUGHAL, GREEN, food=10000, wood=10000, gold=10000,
             age=StartingAge.IMPERIAL_AGE)
    m.diplomacy(1, 2, DiplomacyState.ENEMY)
    m.diplomacy(1, 3, DiplomacyState.ENEMY)
    m.diplomacy(2, 3, DiplomacyState.ALLY)
    hold = m.holding_cell(116, 116)

    island = (44, 38, 76, 68)
    m.unit(2, B.CASTLE, 60, 52, name="Fort of Santo Estevao")
    m.unit(2, B.FORTIFIED_TOWER if hasattr(B, "FORTIFIED_TOWER") else B.GUARD_TOWER, 50, 44)
    m.unit(2, B.GUARD_TOWER, 70, 60)
    m.unit(2, B.MONASTERY, 66, 44)
    m.group(2, U.ARBALESTER, 6, 56, 56, cols=3)
    m.group(2, U.HAND_CANNONEER, 6, 62, 58, cols=3)
    m.group(2, U.ELITE_ORGAN_GUN, 2, 58, 48, cols=2, spacing=2)
    viceroy = m.unit(2, H.VASCO_DA_GAMA, 60, 56, name="Viceroy Francisco de Tavora")
    # Goa city across the Mandovi (north)
    m.ring_walls(2, 60, 18, 8, gaps=(270,))
    m.unit(2, B.CASTLE, 60, 18, name="Velha Goa")
    m.unit(2, B.DOCK, 30, 9)
    m.unit(2, B.DOCK, 90, 9)
    m.group(2, U.ELITE_CARAVEL, 4, 50, 31, cols=4, spacing=2)
    m.group(2, U.ELITE_CARAVEL, 3, 90, 33, cols=3, spacing=2)
    m.group(2, U.ELITE_CARAVEL, 3, 40, 50, cols=1, spacing=2)

    sambhaji = sambhaji_hero(m, 60, 100)
    kavi = m.unit(1, U.MONK, 62, 102, name="Kavi Kalash")
    m.group(1, U.ELITE_SHRIVAMSHA_RIDER, 10, 52, 96, cols=5)
    m.group(1, U.CHAMPION, 10, 64, 96, cols=5)
    m.group(1, U.ARBALESTER, 8, 56, 104, cols=4)
    m.group(1, U.BOMBARD_CANNON, 3, 66, 104, cols=3, spacing=2)
    m.unit(1, B.CASTLE, 60, 110, name="Maratha camp")
    m.camera(1, 60, 100)
    retreat = (104, 104, 119, 119)

    m.hero_setup("Kavi Kalash", hp=150, desc="Kavi Kalash. Poet, scholar and Sambhaji's closest friend and advisor.")
    m.hero_setup("Viceroy Francisco de Tavora", desc="Francisco de Tavora, Count of Alvor, Viceroy of Portuguese India.")
    m.story([
        "1683. The Portuguese of Goa have allied with the Mughals, letting Mughal fleets use their ports and harassing the Konkan.",
        ("Viceroy Francisco de Tavora", "The Marathas have no ships to speak of. The rivers protect Goa. We have nothing to fear.", (60, 52)),
        ("Kavi Kalash", "Maharaj, the fishermen say the tide drops very low tonight. The channel to Santo Estevao becomes knee-deep."),
        (SAMBHAJI_NAME, "Then we walk across the sea. Bombards to the front."),
        "Capture the island fort. The Viceroy himself leads the defence: wound him and the Portuguese will lose heart.",
    ])

    hp = m.trig("Setup: Viceroy")
    hp.new_effect.modify_attribute(quantity=1000, object_list_unit_id=H.VASCO_DA_GAMA.ID,
                                   source_player=2, operation=Operation.SET,
                                   object_attributes=ObjectAttribute.HIT_POINTS)
    m.set_hp(hp, 2, viceroy, 1000)

    o1 = m.objective("Obj 1: Santo Estevao", "Destroy every Portuguese building on the island of Santo Estevao.", 1)
    m.cleared(o1, 2, island, ObjectType.BUILDING)
    m.say(o1, "Santo Estevao is taken! But Mughal prince Shah Alam is descending the ghats with a huge army to help Goa.", 12)
    o2 = m.objective("Obj 2 (optional): The Viceroy", "Optional: wound the Viceroy so that he flees.", 2)
    m.hp_below(o2, viceroy, 500)
    m.say(o2, "The wounded Viceroy flees across the river. Goa's churches ring their bells in fear.", 10)
    m.teleport(o2, 2, viceroy, *hold)
    o3 = m.objective("Obj 3: Withdraw", "Bring Sambhaji Maharaj to the south-east corner before Shah Alam traps you.", 3, enabled=False)
    m.arrive(o3, sambhaji, retreat)
    m.chain(o1, o3)
    m.victory(o3, "Sambhaji withdraws in good order. Goa has been humbled, and the Mughal army must now march through the barren Konkan.", epilogue=[
        "History: the Goa campaign did not conquer Goa. Prince Shah Alam's arrival forced the Marathas back. But the Portuguese never again openly aided the Mughals at sea.",
        "Six more years of war follow. Bijapur and Golconda fall to Aurangzeb. Swarajya stands alone against the Empire.",
    ])
    for i, d in enumerate((60, 150, 240)):
        w = m.wave(f"Shah Alam {i + 1}", 3, d, [(U.CAVALIER, 10), (U.ELITE_ELEPHANT_ARCHER, 4),
                                                (U.HAND_CANNONEER, 8)], 100, 84, 60, 100, enabled=False)
        m.chain(o1, w)
    m.wave("Portuguese sortie", 2, 300, [(U.ARBALESTER, 6), (U.CONQUISTADOR if hasattr(U, "CONQUISTADOR") else U.HAND_CANNONEER, 6)],
           56, 12, 60, 100, repeat_every=300)

    m.hero_loss(sambhaji, 2, "Sambhaji Maharaj")
    m.texts(
        instructions="1683. Wade across the low-tide fords and destroy the Portuguese fort of Santo Estevao. Optionally wound the Viceroy. Then withdraw to the south-east corner before Shah Alam's Mughal army arrives. Sambhaji Maharaj must survive.",
        history="In late 1683 Sambhaji Maharaj invaded Portuguese Goa, which had been aiding the Mughals. His forces crossed to Santo Estevao at low tide and took the fort; the Viceroy was wounded in the fighting. The arrival of a Mughal army under Prince Shah Alam forced the Marathas to withdraw.",
        hints="Use the shallow fords — your army can't swim.\nBombard cannons outrange the island's towers.\nDon't linger after the fort falls.",
        victory="Goa learns to fear the Chhatrapati.",
        loss="The Goa campaign ends in disaster.",
    )
    return m.finish(OUT)


# =====================================================================
# 5. SANGAMESHWAR (1689)
# =====================================================================
def sangameshwar():
    m = Mission("SB5_Sangameshwar.aoe2scenario", "Dharmaveer", 100, T.GRASS_JUNGLE, seed=1689)
    sahyadri_base(m, T.FOREST_JUNGLE, 26)
    m.path(T.WATER_MEDIUM, [(0, 30), (50, 50)], 2)              # Shastri
    m.path(T.WATER_MEDIUM, [(99, 25), (50, 50)], 2)             # Varuna (Alaknanda)
    m.path(T.WATER_MEDIUM, [(50, 50), (45, 99)], 3)             # confluence, flowing south
    m.path(T.SHALLOWS, [(46, 70), (54, 70)], 2)
    m.path(T.SHALLOWS, [(22, 36), (24, 44)], 2)
    m.path(T.SHALLOWS, [(74, 33), (76, 42)], 2)

    m.players(2)
    swarajya(m, food=800, wood=800, gold=400, stone=400, age=StartingAge.IMPERIAL_AGE)
    m.player(2, "Mughal army of Muqarrab Khan", MUGHAL, GREEN, food=20000, wood=20000, gold=20000,
             age=StartingAge.IMPERIAL_AGE)
    m.diplomacy(1, 2, DiplomacyState.ENEMY)

    village(m, 1, 62, 66, houses=6, spread=6)
    m.unit(1, B.TOWN_CENTER, 62, 66)
    m.ring_walls(1, 62, 66, 10, wall=B.PALISADE_WALL, gaps=(200,))
    sambhaji = sambhaji_hero(m, 62, 70)
    kavi = m.unit(1, U.MONK, 64, 70, name="Kavi Kalash")
    mhaloji = m.unit(1, U.HUSSAR, 60, 72, name="Mhaloji Ghorpade")
    messenger = m.unit(1, U.LIGHT_CAVALRY, 58, 66, name="Royal messenger to Raigad")
    m.group(1, U.CHAMPION, 8, 66, 74, cols=4)
    m.group(1, U.ELITE_SKIRMISHER, 6, 56, 62, cols=3)
    m.group(1, U.HUSSAR, 6, 66, 60, cols=3)
    m.group(1, U.VILLAGER_MALE, 6, 64, 62, cols=3)
    m.camera(1, 62, 70)
    raigad_road = (0, 86, 14, 99)
    m.unit(0, O.FLAG_A, 6, 94)

    m.hero_setup("Kavi Kalash", hp=150, desc="Kavi Kalash. Poet, scholar and Sambhaji's closest friend. He will share his king's fate.")
    m.hero_setup("Mhaloji Ghorpade", hp=300, attack=5, melee_armor=2, desc="Mhaloji Ghorpade. Veteran commander who will die defending his king.")
    m.mood(ColorMood.TWILIGHT)
    m.story([
        "February 1689. For eight years Sambhaji Maharaj has fought Aurangzeb, the Siddis and the Portuguese at once. Not one major fort has been lost.",
        "Hambirrao Mohite has fallen in battle at Wai. Bijapur and Golconda are gone. The pressure on the Deccan grows month by month.",
        ("Kavi Kalash", "The council at Sangameshwar is done, Maharaj. We should ride for Raigad tonight, by the hidden road."),
        "But word of the Chhatrapati's route has reached the Mughals, through disaffected men and failures of watch that historians still debate.",
        ("Mhaloji Ghorpade", "Horsemen on both rivers! Muqarrab Khan's cavalry! We are surrounded, Maharaj!", (50, 20)),
        (SAMBHAJI_NAME, "Then Raigad must be warned. Yesubai and Rajaram must carry on the war. Send the messenger. Now."),
    ])

    o1 = m.objective("Obj 1: Warn Raigad", "Bring the royal messenger to the Raigad road (south-west corner).", 1)
    m.arrive(o1, messenger, raigad_road)
    m.say(o1, "The messenger gallops into the hills. Raigad will know. Now hold Sangameshwar so the trail goes cold.", 12)
    lost = m.trig("Messenger falls")
    lost.new_condition.destroy_object(unit_object=messenger.reference_id)
    m.say(lost, "The messenger is cut down. Raigad will not be warned in time.")
    lost.new_effect.declare_victory(source_player=2, enabled=1)
    o1.new_effect.deactivate_trigger(trigger_id=lost.trigger_id)

    o2 = m.objective("Obj 2: The last stand", "Hold Sangameshwar for 5 minutes.", 2, enabled=False)
    o2.new_condition.timer(timer=300)
    m.chain(o1, o2)
    show = m.trig("Stand timer", enabled=False)
    show.new_condition.timer(timer=1)
    m.timer_display(show, 300, "Hold for: %d")
    m.chain(o1, show)

    m.say(o2, "Mhaloji Ghorpade falls defending his king. Sambhaji Maharaj and Kavi Kalash are surrounded and taken.", 12)
    epi = [
        "Brought before Aurangzeb at Bahadurgad, Sambhaji Maharaj is offered his life in exchange for his forts, his treasure and his faith.",
        "He refuses. For weeks he and Kavi Kalash endure torture without yielding. On 11 March 1689 they are executed at Tulapur, on the Bhima.",
        "The king was gone. The emperor believed the war was over. But Swarajya was not a kingdom held together by one man.",
        "It was an idea that had taken root in the Sahyadris. And the struggle continued.",
        "At Raigad, Maharani Yesubai sends young Rajaram Maharaj south to Jinji, while she stays to hold the capital and is taken captive.",
        "Santaji Ghorpade and Dhanaji Jadhav ride out with the cavalry, striking Mughal camps across the Deccan. At Tulapur, Santaji even cuts the ropes of the Emperor's own tent.",
        "And when Rajaram dies in 1700, Maharani Tarabai takes up the fight for her young son, leading the Marathas for seven more years.",
        "Aurangzeb never returned north. He died in the Deccan in 1707, his treasury empty. Within decades, Maratha horsemen rode to Attock and Delhi.",
        "History remembers Sambhaji Maharaj as Dharmaveer: the hero who would not yield. The flame of Swarajya would not die.",
    ]
    prev = o2
    for i, line in enumerate(epi):
        t = m.trig(f"Epilogue {i + 1}", enabled=False)
        t.new_condition.timer(timer=12)
        who = {4: "Maharani Yesubai", 5: "Santaji Ghorpade", 6: "Maharani Tarabai"}.get(i)
        m.line(t, who, line, 12, named=False)
        m.chain(prev, t)
        prev = t
    fin = m.trig("Victory", enabled=False)
    fin.new_condition.timer(timer=12)
    m.victory(fin)
    m.chain(prev, fin)

    for i in range(8):
        comp = [(U.CAVALIER, 6 + i), (U.HEAVY_CAVALRY_ARCHER, 3 + i // 2)]
        if i >= 3:
            comp.append((U.HAND_CANNONEER, 6))
        m.wave(f"Muqarrab Khan {i + 1}", 2, 60 + i * 70, comp, 88 if i % 2 else 6, 4, 62, 66)

    m.hero_loss(sambhaji, 2, "Sambhaji Maharaj")
    m.texts(
        instructions="February 1689, Sangameshwar. Get the royal messenger to the Raigad road (south-west corner), then hold Sangameshwar for 5 minutes. Sambhaji Maharaj and the messenger must survive.",
        history="In February 1689 Sambhaji Maharaj was captured at Sangameshwar by Mughal forces under Muqarrab Khan, reportedly after betrayal. He refused Aurangzeb's demands and was executed at Tulapur on 11 March 1689. The Marathas fought on under Rajaram and Tarabai; Aurangzeb died in the Deccan in 1707 without subduing them.",
        hints="Send the messenger immediately, with an escort.\nPalisades and the town centre help the defence.\nThe enemy cavalry comes from both northern corners.",
        victory="Dharmaveer Sambhaji Maharaj ki jai!",
        loss="Raigad was not warned in time.",
    )
    return m.finish(OUT)


ALL = [crown_of_conflict, burhanpur, ramsej, janjira, goa, sangameshwar]

if __name__ == "__main__":
    import os
    os.makedirs(OUT, exist_ok=True)
    for f in ALL:
        print(f())
