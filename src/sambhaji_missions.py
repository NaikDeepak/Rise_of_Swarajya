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
    m.diplomacy(2, 3, DiplomacyState.NEUTRAL)     # raiders hunt Sambhaji Maharaj's men, not the council
    m.diplomacy(2, 4, DiplomacyState.ENEMY)
    m.diplomacy(3, 4, DiplomacyState.ALLY)

    # Panhala, where Chhatrapati Sambhaji Maharaj is stationed (SW)
    fort_on_hill(m, 1, 16, 104, r=6, h=5, towers=2, gate_angles=(45,))
    sambhaji = sambhaji_hero(m, 18, 100, desc="Chhatrapati Sambhaji Maharaj (age 23). Crown prince and heir of Chhatrapati Shivaji Maharaj, stationed at Panhala while the council at Raigad debates the succession.")
    kavi = m.unit(1, U.MONK, 20, 102, name="Kavi Kalash")
    m.group(1, U.ELITE_SHRIVAMSHA_RIDER, 8, 22, 98, cols=4)
    m.group(1, U.CHAMPION, 6, 14, 98, cols=3)
    m.camera(1, 18, 100)
    m.hero_setup("Kavi Kalash", hp=150, desc="Kavi Kalash. Sanskrit poet, scholar and Chhatrapati Sambhaji Maharaj's devoted friend and advisor.")

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
                 desc="Sarsenapati Hambirrao Mohite. Commander-in-chief of the Maratha army, and brother of Maharani Soyarabai.")
    m.hero_setup("Annaji Datto", desc="Annaji Datto. Senior minister at Raigad who favours a regency council.")
    m.hero_setup("Maharani Soyarabai", desc="Maharani Soyarabai. Queen of Chhatrapati Shivaji Maharaj and mother of young Rajaram Raje.")

    m.story([
        "April 1680. After Chhatrapati Shivaji Maharaj attains Mahaparinirvan at Raigad, a faction of ministers seeks to place ten-year-old Rajaram Raje on the throne under a regency.",
        ("Annaji Datto", "Yuvaraj Sambhaji Raje commands the frontier at Panhala, while young Rajaram Raje is here at Raigad. The council wishes to govern in the young prince's name.", (95, 21)),
        ("Maharani Soyarabai", "Rajaram Raje is Chhatrapati Shivaji Maharaj's son as well. Let the council guide the realm from Raigad."),
        ("Kavi Kalash", "Maharaj, the Maratha army looks to the rightful heir of Chhatrapati Shivaji Maharaj. Everything turns on Sarsenapati Hambirrao Mohite.", (60, 84)),
        (SAMBHAJI_NAME, "Then I will ride to Hambirrao myself. I will never shed the blood of my father's people. Swarajya must stand united."),
        "Win over Sarsenapati Hambirrao Mohite, rally the killedars of Rajgad and Pratapgad, and enter Raigad. Never attack the council: they are Marathas too.",
    ])

    o1 = m.objective("Obj 1: The Sarsenapati", "Bring Chhatrapati Sambhaji Maharaj to Hambirrao Mohite's camp at Talbid.", 1)
    m.arrive(o1, sambhaji, hamb_area)
    m.line(o1, "Hambirrao Mohite", "Maharaj, Swarajya faces the full might of Aurangzeb. The Maratha army needs its warrior Yuvaraj on the throne. My sword and every horseman are yours, Sambhaji Raje!", 14)
    m.handover(o1, 4, 1, (0, 0, 119, 119), ObjectType.MILITARY)
    m.handover(o1, 4, 1, (0, 0, 119, 119), ObjectType.BUILDING)

    o2 = m.objective("Obj 2: The killedars", "Bring Chhatrapati Sambhaji Maharaj to Rajgad and to Pratapgad so their killedars declare for him.", 2, enabled=False)
    m.chain(o1, o2)
    r1 = m.trig("Rajgad declares", enabled=False)
    m.arrive(r1, sambhaji, rajgad)
    m.handover(r1, 3, 1, rajgad, ObjectType.BUILDING)
    m.handover(r1, 3, 1, rajgad, ObjectType.MILITARY)
    m.set_var(r1, 1, 1)
    m.say(r1, "Rajgad's killedar opens the gates: 'Chhatrapati Shivaji Maharaj's rightful heir is our Chhatrapati!'", 10)
    m.chain(o1, r1)
    r2 = m.trig("Pratapgad declares", enabled=False)
    m.arrive(r2, sambhaji, prat)
    m.handover(r2, 3, 1, prat, ObjectType.BUILDING)
    m.handover(r2, 3, 1, prat, ObjectType.MILITARY)
    m.set_var(r2, 2, 1)
    m.say(r2, "Pratapgad, where Chhatrapati Shivaji Maharaj vanquished Afzal Khan, raises the Bhagwa Dhwaj for Chhatrapati Sambhaji Maharaj.", 10)
    m.chain(o1, r2)
    m.need_var(o2, 1, 1)
    m.need_var(o2, 2, 1)
    m.say(o2, "With the Sarsenapati and the great forts united behind him, the gates of Raigad await. Ride to Raigad.", 10)

    o3 = m.objective("Obj 3: Raigad", "Bring Chhatrapati Sambhaji Maharaj to the gates of Raigad.", 3, enabled=False)
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
        ("Maharani Soyarabai", "You have the army, the forts and Raigad. What is your command, Sambhaji Raje?"),
        (SAMBHAJI_NAME, "Rajaram Raje is my beloved brother. He remains in honour at my side. Our enemy is in Delhi, not in Raigad."),
        "16 January 1681. Chhatrapati Sambhaji Maharaj ascends the golden Simhasan at Raigad as Chhatrapati of Hindavi Swarajya.",
        ("Kavi Kalash", "Aurangzeb's rebel son, Prince Akbar, has fled south and seeks sanctuary under your banner, Maharaj."),
        (SAMBHAJI_NAME, "Then the Mughal Emperor will march south with all his empire. Let us strike the first blow at Burhanpur."),
    ])
    m.hero_loss(sambhaji, 2, "Chhatrapati Sambhaji Maharaj")
    m.mood(ColorMood.AUTUMN)
    m.texts(
        instructions="1680. Following Chhatrapati Shivaji Maharaj's Mahaparinirvan, unite Swarajya peacefully. Win over Sarsenapati Hambirrao Mohite, rally the forts of Rajgad and Pratapgad, and enter Raigad without shedding Maratha blood while repelling Mughal raiders.",
        history="In April 1680, following Chhatrapati Shivaji Maharaj's Mahaparinirvan, Yuvaraj Sambhaji Raje rode from Panhala, secured the allegiance of Sarsenapati Hambirrao Mohite and the hill forts, and entered Raigad without bloodshed. He was formally crowned Chhatrapati Sambhaji Maharaj on 16 January 1681.",
        hints="Ride to Sarsenapati Hambirrao Mohite first: his army joins your banner.\nDo not attack yellow (Raigad council) units or buildings.\nMughal raiders come from the north; protect the forts you rally.",
        victory="Chhatrapati Sambhaji Maharaj reigns at Raigad!",
        loss="Swarajya falls into division.",
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
                 desc="Sarsenapati Hambirrao Mohite. Commander-in-chief of the Maratha army, master of the lightning cavalry raid.")
    m.story([
        "1681. Chhatrapati Sambhaji Maharaj sits on the throne of Hindavi Swarajya, ready to defend every fort his father built.",
        ("Emperor Aurangzeb", "My own son Akbar shelters with Chhatrapati Sambhaji Maharaj? Then I will march to the Deccan myself with the entire imperial army."),
        (SAMBHAJI_NAME, "Before the Emperor marches on our forts, we strike his imperial treasury. To Burhanpur: the gateway of the Mughal Deccan."),
        ("Hambirrao Mohite", "The walled citadel is heavily gunned, Maharaj. But Bahadurpura, the wealthy imperial quarter across the Tapi, lies open to our cavalry.", (70, 56)),
        "Destroy the five imperial bazaars of Bahadurpura, then ride back to Salher before Khan Jahan's army arrives.",
    ])

    o1 = m.objective("Obj 1: Bahadurpura", "Destroy the five bazaars of Bahadurpura.", 1)
    m.cleared(o1, 2, bp, const=B.MARKET)
    m.gold(o1, 1, 2500)
    m.say(o1, "Bahadurpura's imperial warehouses are emptied. The Deccan has seen what Chhatrapati Sambhaji Maharaj can do. Ride for Salher!", 12)
    o2 = m.objective("Obj 2: Salher", "Return Chhatrapati Sambhaji Maharaj to Salher fort (south-west).", 2, enabled=False)
    m.arrive(o2, sambhaji, salher)
    m.chain(o1, o2)
    m.victory(o2, "The Maratha cavalry returns to the Sahyadri hills with the treasury of Burhanpur.", epilogue=[
        ("Hambirrao Mohite", "The smoke of Bahadurpura rises to the sky, Maharaj. The Emperor will hear of this in Ajmer."),
        "In 1682 Aurangzeb descends into the Deccan with the largest army the subcontinent has ever seen. Yet for twenty-five years he will never conquer Swarajya, nor ever return north.",
    ])

    for i, d in enumerate((420, 540, 660)):
        m.wave(f"Khan Jahan {i + 1}", 3, d, [(U.CAVALIER, 8), (U.ELITE_ELEPHANT_ARCHER, 3),
                                             (U.HAND_CANNONEER, 6)], 110, 4, 60, 70)
    warn = m.trig("Warning")
    warn.new_condition.timer(timer=1)
    m.timer_display(warn, 420, "Khan Jahan Bahadur arrives in: %d")

    m.hero_loss(sambhaji, 3, "Chhatrapati Sambhaji Maharaj")
    m.texts(
        instructions="1681. Destroy the five bazaars of Bahadurpura, then return Chhatrapati Sambhaji Maharaj to Salher fort. A Mughal army arrives in 7 minutes.",
        history="In early 1681 Chhatrapati Sambhaji Maharaj and Sarsenapati Hambirrao Mohite led a lightning strike on Burhanpur, the rich Mughal provincial capital on the Tapi river, capturing the treasury of Bahadurpura. The raid showed all of India that the new Chhatrapati was as daring as his father.",
        hints="Ignore the walled city. Its fort is too strong.\nCavalry archers are good against the bazaar guards.\nWatch the timer and leave in time.",
        victory="The Mughal Deccan trembles before Chhatrapati Sambhaji Maharaj.",
        loss="The expedition was intercepted.",
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
        history="Aurangzeb's commanders boasted that the hill fort of Ramsej near Nashik would fall in hours. Instead its heroic killedar Suryaji and 600 Mavalas, backed by relief forces sent by Chhatrapati Sambhaji Maharaj under Sarsenapati Hambirrao Mohite, Rupaji Bhosale, and Manaji More, defied the Mughal Empire for over five years.",
        hints="Repair the walls and castle with villagers between waves.\nKill bombards and trebuchets first.\nHalberdiers counter the war elephants.",
        victory="Ramsej stands unconquered!",
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
    m.say(note, "With Padmadurg and the Maratha fleet commanding the waters, Chhatrapati Sambhaji Maharaj's campaign broke the Siddi grip on the Konkan coast.", 14)
    m.chain(o2, note)
    fin = m.trig("Victory", enabled=False)
    fin.new_condition.timer(timer=14)
    m.victory(fin, epilogue=[
        "With the Siddis contained, Chhatrapati Sambhaji Maharaj turns south toward Goa, where the Portuguese have allowed Mughal armies passage through their ports.",
    ])
    m.chain(note, fin)

    m.wave("Siddi landing", 2, 300, [(U.TWO_HANDED_SWORDSMAN, 6), (U.ARBALESTER, 6)], 80, 106, 100, 80,
           repeat_every=300)
    m.wave("Mughal raid", 3, 480, [(U.CAVALIER, 8), (U.HAND_CANNONEER, 6)], 112, 2, 100, 40,
           repeat_every=360)

    m.hero_loss(sambhaji, 2, "Chhatrapati Sambhaji Maharaj")
    m.texts(
        instructions="1682. Destroy the two Siddi docks at Danda-Rajpuri, then destroy every Bombard Tower guarding the island fort of Janjira. Chhatrapati Sambhaji Maharaj must survive.",
        history="The Siddis of Janjira, allied to the Mughals, threatened the Konkan coast. In 1682 Chhatrapati Sambhaji Maharaj bombarded Janjira, even tried to build a stone causeway across the sea channel, and confined the Siddi fleet with the Maratha navy based at Padmadurg.",
        hints="Fire ships and cannon galleons beat galleons and towers.\nBuild a strong navy before attacking the island.\nKeep some infantry home for Siddi landings.",
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
    # Low-tide fords (Chhatrapati Sambhaji Maharaj's army crossed at low water)
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

    m.hero_setup("Kavi Kalash", hp=150, desc="Kavi Kalash. Sanskrit poet, scholar and Chhatrapati Sambhaji Maharaj's devoted friend and advisor.")
    m.hero_setup("Viceroy Francisco de Tavora", desc="Francisco de Tavora, Count of Alvor, Viceroy of Portuguese India.")
    m.story([
        "1683. The Portuguese of Goa have allied with the Mughals, letting Mughal fleets use their ports and harassing the Konkan.",
        ("Viceroy Francisco de Tavora", "The rivers protect Goa. Our island forts command every channel.", (60, 52)),
        ("Kavi Kalash", "Maharaj, the fishermen say the tide drops very low tonight. The channel to Santo Estevao becomes knee-deep."),
        (SAMBHAJI_NAME, "Then we charge across the sea itself. Bombards to the front! Har Har Mahadev!"),
        "Capture the island fort of Santo Estevao. The Portuguese Viceroy leads the defence: wound him and break the Portuguese line.",
    ])

    hp = m.trig("Setup: Viceroy")
    hp.new_effect.modify_attribute(quantity=1000, object_list_unit_id=H.VASCO_DA_GAMA.ID,
                                   source_player=2, operation=Operation.SET,
                                   object_attributes=ObjectAttribute.HIT_POINTS)
    m.set_hp(hp, 2, viceroy, 1000)

    o1 = m.objective("Obj 1: Santo Estevao", "Destroy every Portuguese building on the island of Santo Estevao.", 1)
    m.cleared(o1, 2, island, ObjectType.BUILDING)
    m.say(o1, "Santo Estevao is conquered! Now Mughal prince Shah Alam descends the ghats with a vast army to relieve Goa.", 12)
    o2 = m.objective("Obj 2 (optional): The Viceroy", "Optional: wound the Viceroy so that he flees.", 2)
    m.hp_below(o2, viceroy, 500)
    m.say(o2, "The wounded Viceroy flees across the Mandovi river in panic! All of Goa trembles before Chhatrapati Sambhaji Maharaj.", 10)
    m.teleport(o2, 2, viceroy, *hold)
    o3 = m.objective("Obj 3: Withdraw", "Bring Chhatrapati Sambhaji Maharaj to the south-east corner to confront Shah Alam's column.", 3, enabled=False)
    m.arrive(o3, sambhaji, retreat)
    m.chain(o1, o3)
    m.victory(o3, "Chhatrapati Sambhaji Maharaj pulls his army back in good order. Goa has been humbled.", epilogue=[
        "Having shattered Portuguese pride at Santo Estevao, Chhatrapati Sambhaji Maharaj turns to meet Shah Alam's Mughal army in the Konkan passes, forcing the Mughal prince into a disastrous retreat.",
        "Six more years of relentless war follow. Even after Bijapur and Golconda fall to Aurangzeb, Hindavi Swarajya under Chhatrapati Sambhaji Maharaj stands undefeated.",
    ])
    for i, d in enumerate((60, 150, 240)):
        w = m.wave(f"Shah Alam {i + 1}", 3, d, [(U.CAVALIER, 10), (U.ELITE_ELEPHANT_ARCHER, 4),
                                                (U.HAND_CANNONEER, 8)], 100, 84, 60, 100, enabled=False)
        m.chain(o1, w)
    m.wave("Portuguese sortie", 2, 300, [(U.ARBALESTER, 6), (U.CONQUISTADOR if hasattr(U, "CONQUISTADOR") else U.HAND_CANNONEER, 6)],
           56, 12, 60, 100, repeat_every=300)

    m.hero_loss(sambhaji, 2, "Chhatrapati Sambhaji Maharaj")
    m.texts(
        instructions="1683. Charge across the low-tide fords and destroy the Portuguese fort of Santo Estevao. Optionally wound the Viceroy. Then move to the south-east corner before Shah Alam's Mughal army arrives. Chhatrapati Sambhaji Maharaj must survive.",
        history="In late 1683 Chhatrapati Sambhaji Maharaj marched against Portuguese Goa for aiding the Mughals. Leading his cavalry across the tidal channel at low water, Chhatrapati Sambhaji Maharaj stormed the island fortress of Santo Estevao and routed the Viceroy Count of Alvor, came close to taking Goa itself, then turned to face Prince Shah Alam's army.",
        hints="Use the shallow fords. Your army can't swim.\nBombard cannons outrange the island's towers.\nRegroup in the south-east once the fort falls.",
        victory="Goa bows before the valour of Chhatrapati Sambhaji Maharaj.",
        loss="The Goa offensive was halted.",
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

    m.hero_setup("Kavi Kalash", hp=150, desc="Kavi Kalash. Sanskrit poet, scholar and Chhatrapati Sambhaji Maharaj's devoted friend unto martyrdom.")
    m.hero_setup("Mhaloji Ghorpade", hp=300, attack=5, melee_armor=2, desc="Senapati Mhaloji Ghorpade. Veteran commander and father of Santaji Ghorpade, who gives his life defending his Chhatrapati.")
    m.mood(ColorMood.TWILIGHT)
    m.story([
        "February 1689. For nine undefeated years Chhatrapati Sambhaji Maharaj has fought Aurangzeb, the Siddis and the Portuguese on every front. More than 120 battles, and he has not lost one, nor a single major fort.",
        "Sarsenapati Hambirrao Mohite attained martyrdom in his victorious battle at Wai. Now Chhatrapati Sambhaji Maharaj holds court briefly at Sangameshwar before riding to Raigad.",
        ("Kavi Kalash", "The judicial council at Sangameshwar is complete, Maharaj. We should ride for Raigad tonight by the ghat road."),
        "Through treachery in the passes, Muqarrab Khan's Mughal cavalry has learned of the Chhatrapati's small escort at Sangameshwar.",
        ("Mhaloji Ghorpade", "Horsemen on both rivers! Muqarrab Khan's detachment! We are outnumbered ten to one, Maharaj!", (50, 20)),
        (SAMBHAJI_NAME, "Then Raigad must be warned first! Maharani Yesubai and Rajaram Raje must safeguard Swarajya. Ride out with the messenger. We will hold the pass here!"),
    ])

    o1 = m.objective("Obj 1: Warn Raigad", "Bring the royal messenger to the Raigad road (south-west corner).", 1)
    m.arrive(o1, messenger, raigad_road)
    m.say(o1, "The royal messenger gallops into the Sahyadri hills! Raigad will be warned. Now hold Sangameshwar so the messenger escapes unpursued!", 12)
    lost = m.trig("Messenger falls")
    lost.new_condition.destroy_object(unit_object=messenger.reference_id)
    m.say(lost, "The messenger has fallen. Raigad will not be warned in time.")
    lost.new_effect.declare_victory(source_player=2, enabled=1)
    o1.new_effect.deactivate_trigger(trigger_id=lost.trigger_id)

    o2 = m.objective("Obj 2: The last stand", "Hold Sangameshwar for 5 minutes.", 2, enabled=False)
    o2.new_condition.timer(timer=300)
    m.chain(o1, o2)
    show = m.trig("Stand timer", enabled=False)
    show.new_condition.timer(timer=1)
    m.timer_display(show, 300, "Hold for: %d")
    m.chain(o1, show)

    m.say(o2, "Senapati Mhaloji Ghorpade attains martyrdom fighting to his last breath. Outnumbered after a fierce stand, Chhatrapati Sambhaji Maharaj and Kavi Kalash are captured.", 12)
    epi = [
        "Brought before Aurangzeb at Bahadurgad, Chhatrapati Sambhaji Maharaj is demanded to surrender all his forts, his treasury, and his Dharma.",
        "The Chhava of Chhatrapati Shivaji Maharaj roars back in defiance, refusing even if offered the Emperor's own throne. For forty days he and Kavi Kalash are tortured, and neither bows his head. They are put to death at Tulapur on 11 March 1689.",
        "Aurangzeb expected the Chhatrapati's death to end Hindavi Swarajya. He was wrong. Word of how Dharmaveer Chhatrapati Sambhaji Maharaj died spread to every Maratha village.",
        "The Mavalas rose across Maharashtra to avenge their Chhatrapati.",
        "At Raigad, Maharani Yesubai Aaisaheb counselled Chhatrapati Rajaram Maharaj to carry the war south to Jinji, while she held the capital. When Raigad fell, she spent nearly thirty years as a Mughal captive.",
        "Senapati Santaji Ghorpade and Senapati Dhanaji Jadhav raided across the Deccan, once riding into the Mughal camp at Tulapur by night to cut the golden ropes of Aurangzeb's own tent.",
        "And when Chhatrapati Rajaram Maharaj passed in 1700, Maharani Tarabai Aaisaheb took command of Swarajya and led the war against the Mughals from the saddle.",
        "Aurangzeb never returned to Delhi. He died in Maharashtra in 1707, his treasury empty and his empire failing. Fifty years later the Bhagwa Dhwaj would fly as far north as Attock.",
        "Dharmaveer Chhatrapati Sambhaji Maharaj, the Chhava, gave his life and never gave up his Dharma or his Swarajya. Har Har Mahadev!",
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

    m.hero_loss(sambhaji, 2, "Chhatrapati Sambhaji Maharaj")
    m.texts(
        instructions="February 1689, Sangameshwar. Escort the royal messenger to the Raigad road (south-west corner), then hold Sangameshwar for 5 minutes. Chhatrapati Sambhaji Maharaj and the messenger must survive.",
        history="In February 1689, after nine undefeated years of defending Hindavi Swarajya against the Mughal Empire, the Siddis, and the Portuguese, Chhatrapati Sambhaji Maharaj was ambushed at Sangameshwar by Muqarrab Khan's forces. Refusing to surrender his Dharma or a single fort of Swarajya, Dharmaveer Chhatrapati Sambhaji Maharaj and Kavi Kalash attained martyrdom at Tulapur on 11 March 1689. Inspired by his sacrifice, the Marathas under Maharani Yesubai, Chhatrapati Rajaram Maharaj, Santaji Ghorpade, Dhanaji Jadhav, and Maharani Tarabai shattered Aurangzeb's invasion, and Aurangzeb died defeated in the Deccan in 1707.",
        hints="Send the messenger immediately, with an escort.\nPalisades and the town centre help the defence.\nThe enemy cavalry comes from both northern corners.",
        victory="Dharmaveer Chhatrapati Sambhaji Maharaj ki Jai!",
        loss="Raigad was not warned in time.",
    )
    return m.finish(OUT)


ALL = [crown_of_conflict, burhanpur, ramsej, janjira, goa, sangameshwar]

if __name__ == "__main__":
    import os
    os.makedirs(OUT, exist_ok=True)
    for f in ALL:
        print(f())
