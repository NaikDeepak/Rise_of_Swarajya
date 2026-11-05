# Official scenario catalog

Every scenario in the official AoE2 DE campaigns on this Mac: 235 scenarios, 227 readable by our tool (AoE2ScenarioParser 0.9.8). Use it to pick a template map for a chapter without re-scanning the game files.

Regenerate after a game update:

```
.venv/bin/python -I tools/scan_official_maps.py   # about 45 s, writes docs/data/official_maps.jsonl
.venv/bin/python -I tools/official_maps_doc.py    # rewrites this page
```

## Columns

- **Raised:** share of tiles at elevation 3 or more. A high number can mean a whole raised plateau rather than separate hills, so check the minimap.
- **Jungle / Green / Water:** share of tiles with jungle, bamboo or rainforest; grass or forest; water, shallows or beach. Dirt counts as neither green nor desert.
- **Enemy castles (raised):** castles owned by players 2 to 8, and how many stand at elevation 3 or more.
- **Triggers:** trigger count; a rough guide to how much scripting there is to reuse or strip out.
- **Tags:** rough map types from these numbers, a starting point only.

To see a map, render its minimap: extract the scenario from its `.aoe2campaign` (see `extract()` in `tools/scan_official_maps.py`), then run `src/verify.py`'s `check(path, png)`.

## Shortlist: hill fort (Torna, Pratapgad, Sinhagad, Gingee)

Top 12 by a hill-fort score: an enemy castle on high ground, raised ground, green or jungle terrain, little water, desert or snow.

| Scenario | Size | Raised | Jungle | Green | Water | Enemy castles | Players | Triggers | Mood | First civs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R4_LeLoi_6 | 144 | 1% | 52% | 86% | 7% | 11 (1 raised) | 4 | 38 | Default | Vietnamese, Vietnamese, Chinese |
| F6_Prithviraj_4 | 120 | 91% | 0% | 42% | 7% | 3 (3 raised) | 6 | 84 | Default | Gurjaras, Hindustanis, Persians |
| IN2_Rajendra_4 | 200 | 27% | 22% | 43% | 21% | 8 (1 raised) | 8 | 137 | Jungle | Dravidians, Dravidians, Dravidians |
| C3_Montezuma_2 | 200 | 22% | 29% | 53% | 31% | 1 (1 raised) | 5 | 44 | Jungle | Aztecs, Aztecs, Aztecs |
| C3_Montezuma_1 | 144 | 8% | 46% | 68% | 10% | 2 (0 raised) | 4 | 32 | Jungle | Aztecs, Aztecs, Mayans |
| IN2_Rajendra_1 | 168 | 4% | 28% | 59% | 14% | 3 (2 raised) | 8 | 146 | Night | Dravidians, Dravidians, Gurjaras |
| C4_4_Manzikert | 168 | 47% | 0% | 11% | 6% | 5 (2 raised) | 6 | 27 | Desert | Turks, Byzantines, Byzantines |
| IN3_Devapala_2 | 144 | 0% | 27% | 68% | 14% | 3 (1 raised) | 4 | 71 | Default | Bengalis, Gurjaras, Gurjaras |
| WE3_Hautevilles_4 | 200 | 37% | 0% | 5% | 7% | 2 (1 raised) | 8 | 213 | Default | Sicilians, Byzantines, Saracens |
| R4_LeLoi_1 | 200 | 1% | 40% | 76% | 13% | 7 (0 raised) | 8 | 76 | Autumn | Vietnamese, Chinese, Vietnamese |
| R4_LeLoi_4 | 144 | 2% | 48% | 59% | 19% | 3 (0 raised) | 6 | 54 | Jungle | Vietnamese, Chinese, Chinese |
| R2_Suryavarman I_1 CO-OP | 120 | 3% | 30% | 73% | 5% | 1 (0 raised) | 6 | 35 | Jungle | Khmer, Khmer, Khmer |

## Shortlist: coastal (Janjira, Goa, Konkan)

| Scenario | Size | Raised | Jungle | Green | Water | Enemy castles | Players | Triggers | Mood | First civs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C3_Montezuma_2 | 200 | 22% | 29% | 53% | 31% | 1 (1 raised) | 5 | 44 | Jungle | Aztecs, Aztecs, Aztecs |
| IN3_Devapala_1 | 144 | 0% | 29% | 49% | 33% | 1 (0 raised) | 5 | 61 | Empty | Bengalis, Bengalis, Bengalis |
| IN3_Devapala_5 | 168 | 0% | 21% | 56% | 28% | 3 (1 raised) | 4 | 108 | Default | Bengalis, Bengalis, Gurjaras |
| R3_Bayinnaung_1 | 144 | 0% | 29% | 47% | 29% | 7 (0 raised) | 6 | 106 | Jungle | Burmese, Bengalis, Khmer |
| R3_Bayinnaung_3 | 144 | 1% | 30% | 46% | 29% | 4 (1 raised) | 6 | 93 | Jungle | Burmese, Burmese, Burmese |
| F6_Prithviraj_5 | 168 | 0% | 26% | 49% | 26% | 9 (0 raised) | 8 | 138 | Jungle | Gurjaras, Gurjaras, Gurjaras |
| R1_GajahMada_5 | 200 | 0% | 27% | 42% | 36% | 1 (0 raised) | 7 | 132 | Default | Malay, Malay, Malay |
| IN3_Devapala_4 | 144 | 0% | 17% | 51% | 31% | 8 (0 raised) | 4 | 54 | Default | Bengalis, Dravidians, Dravidians |
| R2_Suryavarman I_5 CO-OP | 168 | 2% | 16% | 48% | 29% | 9 (0 raised) | 8 | 48 | Jungle | Khmer, Burmese, Burmese |
| C3_Montezuma_5 | 168 | 21% | 26% | 37% | 51% | 4 (1 raised) | 3 | 18 | Jungle | Aztecs, Aztecs, Spanish |

## Shortlist: jungle and green valleys (Javali, Pavan Khind, ambushes)

| Scenario | Size | Raised | Jungle | Green | Water | Enemy castles | Players | Triggers | Mood | First civs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R4_LeLoi_6 | 144 | 1% | 52% | 86% | 7% | 11 (1 raised) | 4 | 38 | Default | Vietnamese, Vietnamese, Chinese |
| C3_Montezuma_1 | 144 | 8% | 46% | 68% | 10% | 2 (0 raised) | 4 | 32 | Jungle | Aztecs, Aztecs, Mayans |
| R4_LeLoi_1 | 200 | 1% | 40% | 76% | 13% | 7 (0 raised) | 8 | 76 | Autumn | Vietnamese, Chinese, Vietnamese |
| R4_LeLoi_4 | 144 | 2% | 48% | 59% | 19% | 3 (0 raised) | 6 | 54 | Jungle | Vietnamese, Chinese, Chinese |
| R2_Suryavarman I_1 CO-OP | 120 | 3% | 30% | 73% | 5% | 1 (0 raised) | 6 | 35 | Jungle | Khmer, Khmer, Khmer |
| R2_Suryavarman I_1 | 120 | 1% | 25% | 77% | 5% | 1 (0 raised) | 5 | 9 | Jungle | Khmer, Khmer, Khmer |
| R4_LeLoi_5 | 240 | 0% | 32% | 64% | 11% | 6 (0 raised) | 6 | 84 | Jungle | Vietnamese, Vietnamese, Khmer |
| R1_GajahMada_1 | 200 | 0% | 38% | 58% | 19% | 2 (0 raised) | 5 | 209 | Jungle | Malay, Malay, Mongols |
| R4_LeLoi_2 | 200 | 2% | 37% | 44% | 7% | 7 (0 raised) | 5 | 95 | Jungle | Vietnamese, Chinese, Vietnamese |
| R2_Suryavarman I_2 CO-OP | 168 | 3% | 28% | 68% | 14% | 4 (0 raised) | 6 | 64 | Jungle | Khmer, Malay, Khmer |

## Shortlist: open field (Salher, Burhanpur, field battles)

| Scenario | Size | Raised | Jungle | Green | Water | Enemy castles | Players | Triggers | Mood | First civs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F4_Sforza_1 | 144 | 0% | 0% | 87% | 3% | 1 (0 raised) | 8 | 74 | Empty | Italians, Italians, Italians |
| R4_LeLoi_6 | 144 | 1% | 52% | 86% | 7% | 11 (1 raised) | 4 | 38 | Default | Vietnamese, Vietnamese, Chinese |
| R2_Suryavarman I_1 | 120 | 1% | 25% | 77% | 5% | 1 (0 raised) | 5 | 9 | Jungle | Khmer, Khmer, Khmer |
| C1_Attila_5 CO-OP | 200 | 0% | 0% | 76% | 12% | 0 (0 raised) | 6 | 22 | Default | Huns, Goths, Romans |
| EE3_Zizka_2 | 168 | 0% | 0% | 76% | 14% | 2 (2 raised) | 7 | 45 | Empty | Bohemians, Poles, Lithuanians |
| EE3_Zizka_3 | 168 | 0% | 0% | 76% | 11% | 4 (0 raised) | 6 | 59 | Default | Bohemians, Bohemians, Bohemians |
| R4_LeLoi_1 | 200 | 1% | 40% | 76% | 13% | 7 (0 raised) | 8 | 76 | Autumn | Vietnamese, Chinese, Vietnamese |
| C1_Attila_5 | 200 | 0% | 0% | 76% | 12% | 0 (0 raised) | 6 | 20 | Default | Huns, Goths, Romans |
| 2_Joan_5 | 200 | 0% | 0% | 75% | 12% | 4 (0 raised) | 5 | 58 | Winter | Franks, Burgundians, Britons |
| 2_Joan_6 | 144 | 5% | 0% | 74% | 13% | 5 (1 raised) | 4 | 37 | Default | Franks, Burgundians, Britons |

## All readable scenarios

| Campaign | Ch | Scenario | Size | Raised | Jungle | Green | Water | Desert | Snow | Castles (raised) | Players | Triggers | Mood | Tags | Objectives (first two) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| acam1 | 1 | A1_Tariq1 | 144 | 0% | 0% | 35% | 42% | 2% | 0% | 3 (0) | 6 | 41 | Default | coastal | March to the northwest and defeat Roderic's Army (Green). Killing Roderic will cause his a / Conquer Cordoba by destroying its Castle. |
| acam1 | 2 | A1_Tariq2 | 168 | 0% | 0% | 48% | 19% | 0% | 0% | 9 (0) | 8 | 52 | Default |  | Capture Toledo by defeating the Visigoth Garrison (Green) and destroying all of its Watch  / Defeat 3 of the 4 enemy towns (Seville, Merida, Talavera, and Guadalajara). |
| acam1 | 3 | A1_Tariq3 | 168 | 0% | 0% | 39% | 32% | 0% | 0% | 9 (0) | 6 | 22 | Default | coastal | Destroy the Castles of the following cities: / Theodemir of Murcia will provide you with tribute and supplementary troops every 10 minute |
| acam1 | 4 | A1_Tariq4 | 144 | 0% | 0% | 7% | 1% | 0% | 66% | 8 (0) | 6 | 42 | Winter | open field, snow (repaint) | Abd ar-Rahman al-Ghafiqi, 15 of your men, and at least one supply cart must reach the Umay |
| acam1 | 5 | A1_Tariq5 | 144 | 0% | 0% | 51% | 26% | 0% | 0% | 7 (0) | 4 | 22 | Default | coastal | Scare the Aquitanian villages into submission by destroying their Monasteries. / Defeat Bordeaux. |
| acam2 | 1 | A2_Sundjata_1 | 144 | 0% | 0% | 7% | 14% | 8% | 0% | 1 (0) | 4 | 40 | Default | open field | Flee the city of Niani and seek refuge elsewhere. / Destroy the camp of the Sosso scouts. |
| acam2 | 2 | A2_Sundjata_2 | 168 | 0% | 11% | 57% | 7% | 8% | 0% | 1 (0) | 6 | 40 | Default |  | Bring the cart carrying the baobab stick (Relic Cart) to the flagged areas in Sangaran (Re |
| acam2 | 3 | A2_Sundjata_3 | 168 | 0% | 0% | 11% | 12% | 4% | 0% | 1 (0) | 6 | 95 | Autumn | open field | Destroy all Markets inside the walls of Djenne. / Raid as many enemy villages as you can by destroying their storage buildings and stealing  |
| acam2 | 4 | A2_Sundjata_4 | 168 | 1% | 0% | 4% | 24% | 19% | 0% | 6 (1) | 5 | 62 | Desert |  | Defeat the army of Sumanguru (Red). / Fakoli is willing to join you if you can convince them that you are trustworthy. First, th |
| acam2 | 5 | A2_Sundjata_5 | 144 | 0% | 0% | 13% | 53% | 5% | 0% | 2 (0) | 3 | 31 | Default | coastal | Destroy the city of Koumbi Saleh. / Get rid of the evil ruler Sumanguru once and for all. |
| acam3 | 1 | A3_Almeida_1 | 144 | 0% | 0% | 64% | 15% | 0% | 0% | 1 (0) | 8 | 120 | Default |  | Defend the City of Toro. / Destroy the three Aragonese military camps. |
| acam3 | 2 | A3_Almeida_2 | 144 | 3% | 0% | 7% | 38% | 28% | 0% | 1 (0) | 7 | 79 | Desert | coastal | Defend the Castle at Fort Graciosa. / Destroy the three Docks of the Barbary Pirates. |
| acam3 | 3 | A3_Almeida_3 | 200 | 0% | 0% | 23% | 45% | 4% | 0% | 4 (0) | 7 | 157 | Autumn | coastal | Bring Muhammad ibn Rukn ad Din to the Swahili villages. / Destroy Kilwa's Castle. |
| acam3 | 4 | A3_Almeida_4 | 144 | 1% | 10% | 22% | 52% | 5% | 0% | 4 (0) | 5 | 112 | Default | coastal | Sink the Zamorin's Cannon Galleons before they are ready to sail. / Kill the pirate scum and recover the stolen goods. |
| acam3 | 5 | A3_Almeida_5 | 168 | 1% | 8% | 33% | 39% | 3% | 0% | 4 (1) | 7 | 150 | Default | coastal | Find and kill Malik Ayyaz, Amir Husain al-Kurdi, and the Turkish Pasha. / Defeat 2 of 3 enemies. |
| acam4 | 1 | A4_Yodit_1 | 168 | 0% | 0% | 13% | 9% | 12% | 0% | 1 (0) | 6 | 66 | Desert | open field | Bring Yodit to the loyal village. / Escape from Gidajan's grasp. |
| acam4 | 2 | A4_Yodit_2 | 168 | 11% | 0% | 14% | 20% | 23% | 0% | 4 (0) | 7 | 68 | Desert |  | Visit the surrounding settlements. Complete the quests that they give you to build Yodit's / Prove yourself to the Nobatians by defeating the Ikshids. |
| acam4 | 3 | A4_Yodit_3 | 200 | 11% | 0% | 44% | 12% | 2% | 0% | 4 (1) | 8 | 89 | Default | hill fort | Do not let Dagnajan destroy the Darginda castle (Orange). / Kill Dagnajan while he marches with his army. |
| acam4 | 4 | A4_Yodit_4 | 144 | 9% | 0% | 13% | 25% | 15% | 0% | 1 (0) | 5 | 88 | Autumn | coastal | Loot enemy Monasteries by destroying them. / Capture and hold Stelae to earn additional resources. |
| acam4 | 5 | A4_Yodit_5 | 200 | 15% | 0% | 18% | 3% | 4% | 0% | 3 (1) | 8 | 55 | Desert | hill fort | Wait for instructions. / Conquer Aksum by destroying at least 6 of the towers Gidajan has built in the city. |
| cam2 | 1 | 2_Joan_1 | 144 | 1% | 0% | 67% | 15% | 0% | 0% | 2 (0) | 6 | 47 | Winter |  | Escort Joan from the camp at Vaucouleurs to the Château of Chinon. / Joan must survive. |
| cam2 | 2 | 2_Joan_2 | 200 | 6% | 0% | 70% | 16% | 0% | 0% | 5 (0) | 7 | 55 | Default |  | The Cathedral in Orléans must remain standing. / Escort Joan to Blois so that she may command the French army. |
| cam2 | 3 | 2_Joan_3 | 168 | 6% | 0% | 66% | 18% | 0% | 0% | 4 (0) | 4 | 39 | Desert |  | Destroy 3 of the 4 English Castles. / Joan must survive. |
| cam2 | 4 | 2_Joan_4 | 144 | 1% | 0% | 63% | 18% | 0% | 0% | 2 (0) | 5 | 34 | Winter |  | Joan must survive. / Travel west to help reinforce the French camp. Be wary of opposition along the way. |
| cam2 | 5 | 2_Joan_5 | 200 | 0% | 0% | 75% | 12% | 0% | 0% | 4 (0) | 5 | 58 | Winter | open field | After you locate the refugees, rendezvous with the king's reinforcements in Paris, just so / Refugee villagers in Paris are attempting to escape English tyranny. Locate at least 6 of  |
| cam2 | 6 | 2_Joan_6 | 144 | 5% | 0% | 74% | 13% | 0% | 0% | 5 (1) | 4 | 37 | Default | open field | Rendezvous with the French army, commanded by Constable Richemont. / Rendezvous with the French artillery, commanded by Jean Bureau. |
| cam3 | 1 | 3_Saladin_1 | 144 | 8% | 0% | 11% | 13% | 18% | 0% | 1 (1) | 4 | 28 | Desert | hill fort | Bring your soldiers to the Mosque in Cairo. / Defeat the Franks west of Cairo. |
| cam3 | 2 | 3_Saladin_2 | 200 | 0% | 0% | 10% | 37% | 15% | 0% | 1 (0) | 6 | 31 | Desert | coastal | Defeat Reynald's raiders, bandits, and pirates. / The Town Center of Aqaba must not be destroyed. |
| cam3 | 3 | 3_Saladin_3 | 120 | 4% | 0% | 11% | 24% | 28% | 0% | 0 (0) | 5 | 14 | Desert |  | Capture the Piece of the True Cross (a Relic) and return it to the Horns of Hattin (marked |
| cam3 | 4 | 3_Saladin_4 | 168 | 9% | 0% | 12% | 2% | 14% | 0% | 3 (0) | 4 | 30 | Desert |  | Destroy the 5 towers defending Jerusalem so that Saladin's army can occupy the city. / Do not allow any Jerusalem Monastery or the Dome of the Rock to be destroyed. |
| cam3 | 5 | 3_Saladin_5 | 220 | 1% | 0% | 11% | 48% | 12% | 0% | 4 (0) | 6 | 24 | Desert | coastal | Defeat any 2 of the 3 crusader cities: / Tribute 1,000 gold to Tiberias to form an alliance. |
| cam3 | 6 | 3_Saladin_6 | 200 | 1% | 0% | 6% | 51% | 13% | 0% | 4 (0) | 7 | 24 | Desert | coastal | Construct and defend a Wonder. |
| cam4 | 1 | 4_Genghis_1 | 168 | 2% | 0% | 26% | 19% | 1% | 0% | 0 (0) | 8 | 62 | Winter |  | The Kereyids will join if you bring them 20 sheep. / The Naiman will join if you defeat the Tayichi'uds and return to tell the tale. |
| cam4 | 2 | 4_Genghis_2 | 144 | 2% | 1% | 19% | 6% | 1% | 0% | 0 (0) | 4 | 25 | Winter | open field | Kill the traitor, Kushluk. / Prevent the tent of Genghis Khan (Wonder) from being destroyed. |
| cam4 | 3 | 4_Genghis_3 | 200 | 8% | 4% | 57% | 19% | 0% | 0% | 3 (1) | 6 | 23 | Default | hill fort | Conquer the Tanguts, Hsi Hsia, Jin, and Song. |
| cam4 | 4 | 4_Genghis_4 | 220 | 8% | 0% | 65% | 5% | 3% | 0% | 3 (0) | 4 | 26 | Default |  | In the south, the Khwarazm shah is expecting a gift, but he will find assassins in our Tra / In the north, deploy Subotai's horde to conquer Russia. |
| cam4 | 5 | 4_Genghis_5 | 144 | 2% | 0% | 67% | 4% | 2% | 0% | 4 (0) | 4 | 43 | Autumn | open field | Construct 3 Castles within the flagged area to withstand the assault of the Bohemian army. / Capture the German flag. |
| cam4 | 6 | 4_Genghis_6 | 144 | 6% | 0% | 73% | 11% | 0% | 7% | 2 (1) | 2 | 19 | Winter |  | Survive until Subotai's reinforcements arrive. / Destroy all Hungarian Town Centers and Castles. |
| cam5 | 1 | 5_Barbarossa_1 | 200 | 0% | 0% | 74% | 12% | 0% | 0% | 2 (0) | 8 | 21 | Default | open field | Capture, and garrison in your Monasteries, 4 of the 6 Relics from the surrounding German d / Tribute 200 gold to the Cumans (Grey) to hire their army. |
| cam5 | 2 | 5_Barbarossa_2 | 168 | 1% | 0% | 68% | 19% | 0% | 0% | 4 (1) | 5 | 26 | Default |  | Defeat Poland. / Defeat Henry the Lion |
| cam5 | 3 | 5_Barbarossa_3 | 200 | 5% | 0% | 66% | 18% | 0% | 0% | 4 (0) | 5 | 35 | Default |  | The Cathedral in Milan must remain standing. / Convert the Cathedral in Milan. |
| cam5 | 4 | 5_Barbarossa_4 | 168 | 1% | 0% | 38% | 46% | 0% | 0% | 4 (3) | 5 | 19 | Default | coastal | Construct a Wonder within the city walls of Venice, Padua, or Verona. |
| cam5 | 5 | 5_Barbarossa_5 | 220 | 3% | 0% | 18% | 30% | 10% | 0% | 9 (1) | 6 | 49 | Desert | coastal | At least 10 troops must survive to reach the Hospitaller camp. / To force the Byzantines to surrender, threaten the Hagia Sophia Wonder by stationing troop |
| cam5 | 6 | 5_Barbarossa_6 | 168 | 8% | 0% | 14% | 3% | 22% | 0% | 4 (2) | 5 | 33 | Default | hill fort | Deliver the body of Barbarossa (in the pickle barrel) to the Dome of the Rock in Jerusalem / Do not destroy the Dome of the Rock, an important holy site in Jerusalem. |
| coop10 | 1 | F1_Alaric_1 CO-OP | 144 | 2% | 0% | 65% | 7% | 0% | 2% | 2 (1) | 6 | 69 | Default | open field | Defeat the Western Roman Empire (Blue). / Destroy Arbogast's (Cyan) Town Center. |
| coop10 | 2 | F1_Alaric_2 CO-OP | 200 | 0% | 0% | 26% | 27% | 2% | 0% | 3 (0) | 8 | 72 | Desert | coastal | Sack Sparta by destroying its Town Center. / Sack Argos by destroying its Town Center. |
| coop10 | 3 | F1_Alaric_3 CO-OP | 200 | 0% | 0% | 47% | 32% | 0% | 0% | 6 (1) | 6 | 52 | Autumn | coastal | Defeat Aquileia. / Defeat Cremona. |
| coop10 | 4 | F1_Alaric_4 CO-OP | 200 | 0% | 0% | 29% | 8% | 0% | 0% | 12 (0) | 6 | 40 | Autumn | open field | Take the city of Rome by destroying all 12 Castles within its city walls. / Send a unit to the Gothic army in the east to tell them to commence the assault. |
| coop10 | 5 | F1_Alaric_5 CO-OP | 200 | 1% | 0% | 27% | 20% | 0% | 51% | 6 (0) | 7 | 44 | Default | snow (repaint) | Narbo / Tolosa |
| coop17 | 1 | A1_Tariq1 (CO-OP) | 144 | 0% | 0% | 32% | 42% | 2% | 0% | 3 (0) | 7 | 47 | Default | coastal | March to the northwest and defeat Roderic's Army (Green). Killing Roderic will cause his a / Conquer Cordoba by destroying its Castle. |
| coop17 | 2 | A1_Tariq2 (CO-OP) | 168 | 0% | 0% | 46% | 20% | 0% | 0% | 6 (0) | 8 | 77 | Default |  | Defeat 3 of the 4 enemy towns (Seville, Merida, Talavera, and Guadalajara). / Capture Toledo by defeating the Visigoth Garrison (Green) and destroying all of its Watch  |
| coop17 | 3 | A1_Tariq3 (CO-OP) | 168 | 0% | 0% | 39% | 32% | 0% | 0% | 9 (0) | 7 | 45 | Default | coastal | Destroy the Castles of the following cities: / Theodemir of Murcia will provide you with tribute and supplementary troops every 10 minute |
| coop17 | 4 | A1_Tariq4 (CO-OP) | 144 | 0% | 0% | 7% | 1% | 0% | 66% | 8 (0) | 6 | 62 | Winter | open field, snow (repaint) | Abd ar-Rahman al-Ghafiqi, 15 of your men, and at least one supply cart must reach the Umay |
| coop17 | 5 | A1_Tariq5 (CO-OP) | 144 | 0% | 0% | 47% | 29% | 1% | 0% | 7 (0) | 5 | 52 | Default | coastal | Scare the Aquitanian villages into submission by destroying their Monasteries. / Defeat Bordeaux. |
| coop22 | 1 | R2_Suryavarman I_1 CO-OP | 120 | 3% | 30% | 73% | 5% | 0% | 0% | 1 (0) | 6 | 35 | Jungle | Sahyadri/jungle | Storm the city of Angkor and kill Udayadityavarman I. |
| coop22 | 2 | R2_Suryavarman I_2 CO-OP | 168 | 3% | 28% | 68% | 14% | 0% | 0% | 4 (0) | 6 | 64 | Jungle | Sahyadri/jungle | Defeat the Northern Rebels. / Defeat the Eastern Rebels. |
| coop22 | 3 | R2_Suryavarman I_3 CO-OP | 120 | 0% | 22% | 67% | 13% | 1% | 0% | 0 (0) | 6 | 74 | Jungle | Sahyadri/jungle | The Envoy must reach the Andaman port in the west. / Each player (Cyan and Green) must recruit one of the four companies of soldiers camped nea |
| coop22 | 4 | R2_Suryavarman I_4 CO-OP | 168 | 1% | 11% | 27% | 57% | 0% | 0% | 5 (0) | 4 | 34 | Jungle | coastal | Defeat the Tambralingas. / Defeat the Srivijaya. |
| coop22 | 5 | R2_Suryavarman I_5 CO-OP | 168 | 2% | 16% | 48% | 29% | 0% | 0% | 9 (0) | 8 | 48 | Jungle | coastal | Defeat all enemy factions. / Either player must construct and defend a Wonder. |
| coop25 | 1 | K1_Tamerlane_1 (CO-OP) | 144 | 0% | 0% | 24% | 16% | 1% | 0% | 4 (0) | 7 | 63 | Default |  | Capture 3 of the 4 Relics held by the rival Transoxianan khanates. / Kill Urus Khan (Orange) so that Tokhtamysh can take control of the White Horde (Cyan). |
| coop25 | 2 | K1_Tamerlane_2 (CO-OP) | 168 | 3% | 0% | 24% | 16% | 3% | 0% | 8 (2) | 8 | 81 | Empty |  | Destroy the Castle in 3 of the 5 enemy cities (Herat, Zaranj, Isfahan, Soltaniyeh, and Tab / Defeat Tokhtamysh by tearing down his two Castles. |
| coop25 | 3 | K1_Tamerlane_3 (CO-OP) | 168 | 1% | 0% | 6% | 13% | 0% | 78% | 9 (1) | 8 | 84 | Winter | open field, snow (repaint) | Defeat the enemy force blocking your way across the icy ford. / Destroy 2 of Tokhtamysh's 3 power centers: |
| coop25 | 4 | K1_Tamerlane_4 (CO-OP) | 144 | 2% | 3% | 32% | 4% | 0% | 0% | 5 (1) | 8 | 53 | Default | open field | Defeat Shah Tughluq's army outside the walls of Delhi. / Destroy the 5 Castles defending Delhi before the timer runs out. |
| coop25 | 5 | K1_Tamerlane_5 (CO-OP) | 144 | 1% | 0% | 40% | 13% | 7% | 0% | 7 (0) | 8 | 72 | Default | open field | Acquire 10,000 gold in plunder, tribute, or any other means. |
| coop25 | 6 | K1_Tamerlane_6 (CO-OP) | 168 | 1% | 0% | 39% | 15% | 0% | 0% | 10 (1) | 7 | 126 | Default |  | Prepare your defenses. Bayezid will attack in 30 minutes. / Raid outlying Ottoman camps (Blue) to weaken Bayezid's army. |
| coop3 | 1 | 3_Saladin_1 CO-OP | 144 | 8% | 0% | 11% | 13% | 18% | 0% | 1 (1) | 5 | 43 | Desert | hill fort | Bring your soldiers to the Mosque in Cairo. / Defeat the Franks west of Cairo. |
| coop3 | 2 | 3_Saladin_2 CO-OP | 200 | 0% | 0% | 10% | 37% | 15% | 0% | 1 (0) | 7 | 42 | Desert | coastal | Defeat Reynald's raiders, bandits, and pirates. / The Town Center of Aqaba must not be destroyed. |
| coop3 | 3 | 3_Saladin_3 CO-OP | 120 | 4% | 0% | 12% | 22% | 29% | 0% | 0 (0) | 6 | 34 | Desert |  | Capture the Piece of the True Cross (a Relic) and return it to the Horns of Hattin (marked |
| coop3 | 4 | 3_Saladin_4 CO-OP | 168 | 10% | 0% | 14% | 2% | 15% | 0% | 3 (0) | 5 | 52 | Desert |  | Destroy the 5 towers defending Jerusalem so that Saladin's army can occupy the city. / Do not allow any Jerusalem Monastery or the Dome of the Rock to be destroyed. |
| coop3 | 5 | 3_Saladin_5 CO-OP | 220 | 1% | 0% | 11% | 49% | 12% | 0% | 4 (0) | 6 | 31 | Desert | coastal | Defeat any 2 of the 3 Crusader cities (Tyre, Tiberias, and Ascalon). / Tribute 1,000 gold to Tiberias to form an alliance. |
| coop3 | 6 | 3_Saladin_6 CO-OP | 200 | 1% | 0% | 7% | 50% | 13% | 0% | 4 (0) | 7 | 34 | Desert | coastal |  |
| coop6 | 1 | C1_Attila_1 CO-OP | 144 | 8% | 0% | 37% | 26% | 4% | 2% | 3 (1) | 6 | 165 | Autumn | hill fort, coastal | Defeat 2 of your remaining 3 enemies (the Scythians, Romans and Persians). / Send 10 Horses to the flagged Scythian palisade so that the Scythians can supply Attila wi |
| coop6 | 2 | C1_Attila_2 CO-OP | 168 | 4% | 0% | 70% | 12% | 0% | 1% | 2 (0) | 8 | 86 | Winter | open field | Raid the Roman villages. Once you have enough resources to build a forward base, then you  / Train an army and defeat the Romans by leveling their Town Center. |
| coop6 | 3 | C1_Attila_3 CO-OP | 144 | 5% | 0% | 42% | 40% | 1% | 0% | 1 (0) | 5 | 42 | Empty | coastal | Stockpile 10,000 gold in tribute from the Romans. |
| coop6 | 4 | C1_Attila_4 CO-OP | 168 | 10% | 0% | 30% | 5% | 0% | 78% | 3 (0) | 6 | 45 | Default | snow (repaint) | Defeat Burgundy. / Defeat Metz. |
| coop6 | 5 | C1_Attila_5 CO-OP | 200 | 0% | 0% | 76% | 12% | 0% | 0% | 0 (0) | 6 | 22 | Default | open field | Defeat the Romans. / Defeat the Visigoths. |
| coop6 | 6 | C1_Attila_6 CO-OP | 240 | 10% | 0% | 40% | 38% | 0% | 4% | 6 (0) | 7 | 42 | Default | coastal | Attila must meet with Pope Leo I outside the gates of Rome. / Attila must survive. |
| coop9 | 1 | C4_1_Tours CO-OP | 168 | 3% | 0% | 47% | 16% | 0% | 0% | 1 (0) | 5 | 54 | Autumn |  | Capture the 6 Trade Carts in the Moors' baggage train and bring them to the Cathedral in T / Prevent the Muslims from destroying any of your 3 Town Centers. |
| coop9 | 2 | C4_3_Hastings CO-OP | 220 | 4% | 0% | 48% | 38% | 1% | 2% | 5 (3) | 7 | 92 | Default | coastal | Conquer England by destroying the Castle of Harold the Saxon (Orange). / Send Transport Ships to the north to pick up Harald Hardrada's Viking Berserks. |
| coop9 | 3 | F7_4_Honfoglalas (895) CO-OP | 240 | 1% | 0% | 58% | 15% | 0% | 0% | 4 (0) | 7 | 256 | Empty |  | Defeat 2 of the 3 main factions (Bulgaria, Great Moravia, and East Francia.) / While nomadic, bring Sheep to the enclosure to generate food. |
| coop9 | 4 | F7_5_Kurikara (1183) CO-OP | 200 | 0% | 0% | 26% | 36% | 3% | 0% | 9 (0) | 8 | 79 | Empty | coastal | Bring the supply cart (Blue) and at least one soldier to Yoshinaka's palace (marked by the / Protect Yoshinaka's palace (Wonder) in Kurikara. |
| coop9 | 5 | F7_7_Bapheus (1302) CO-OP | 220 | 0% | 0% | 14% | 19% | 5% | 0% | 9 (0) | 8 | 124 | Empty |  | Osman must survive. / Defeat the Byzantines by destroying <TotalCastles> Byzantine Castles. |
| dcam0 | 1 | 0_June_Event_Scenario | 120 | 0% | 0% | 64% | 11% | 1% | 2% | 6 (0) | 8 | 89 | Empty | open field | Defeat the Japanese (Red) by destroying their Wonder for 4,000 points. / Defeat the Franks (Yellow) by destroying their Castle for 1,000 points. |
| dcam0 | 2 | 0_September_Event_Scenario | 200 | 0% | 0% | 74% | 12% | 0% | 0% | 2 (0) | 8 | 73 | Empty | open field | Capture, and garrison in your Monasteries, the 6 Relics from the surrounding German duchie / Tribute 200 gold to the Cumans (Grey) to hire their army. |
| dcam0 | 3 | Mangudai Madness | 120 | 2% | 0% | 6% | 3% | 0% | 0% | 4 (0) | 3 | 101 | Default | open field |  |
| dcam0 | 4 | The Siege | 240 | 1% | 0% | 59% | 32% | 0% | 0% | 4 (0) | 6 | 89 | Default | coastal | Capture the Hagia Sophia before 1 June 1453. / Do not allow the Hagia Sophia to be lost. |
| eecam1 | 1 | EE1_Algirdas_1 | 200 | 1% | 0% | 55% | 16% | 1% | 0% | 2 (0) | 8 | 136 | Autumn |  | Drive Jaunutis out of Vilnius by razing his Wonder in the center of the city. / Build Monasteries in neutral villages to convert their residents to Christianity. Settleme |
| eecam1 | 2 | EE1_Algirdas_2 | 240 | 2% | 0% | 50% | 20% | 1% | 12% | 5 (2) | 6 | 139 | Default |  | Put an end to the Teutonic Order's assaults by destroying at least two of its Castles. / Burn down the Monasteries in Kursk to rob the city of its Relics and force its inhabitants |
| eecam1 | 3 | EE1_Algirdas_3 | 220 | 2% | 0% | 46% | 21% | 5% | 0% | 4 (1) | 8 | 133 | Default |  | Conquer Kiev by killing the separatist forces that oppose the Lithuanian claim to the city / Defeat all three portions of the Golden Horde (Bulgars, Kipchaks, and Tatars). |
| eecam1 | 4 | EE1_Algirdas_4 | 200 | 0% | 0% | 41% | 19% | 6% | 0% | 5 (0) | 8 | 161 | Default |  | Hurry to Mikhail of Tver's aid before the Muscovites kill him. / Build a camp and prepare for battle. |
| eecam1 | 5 | EE1_Algirdas_5 | 220 | 2% | 0% | 57% | 10% | 5% | 0% | 7 (0) | 8 | 177 | Default | open field | Bring the cart to Kestutis' Castle in time to ransom Jogaila. / The ransom cart must not be destroyed. |
| eecam2 | 1 | EE2_Jadwiga_1 | 144 | 4% | 0% | 54% | 13% | 6% | 0% | 4 (1) | 7 | 113 | Default | open field | Do not let the rebel dukes capture (kill) Jadwiga. / Bring Jadwiga to her coronation at Wawel Cathedral in Krakow. |
| eecam2 | 2 | EE2_Jadwiga_2 | 144 | 4% | 0% | 22% | 14% | 0% | 0% | 3 (0) | 7 | 149 | Autumn | open field | Defeat Halych. / Use your heroes in combat (to fight, heal or convert). The more experience that they gain, |
| eecam2 | 3 | EE2_Jadwiga_3 | 200 | 14% | 0% | 14% | 21% | 0% | 64% | 11 (6) | 6 | 190 | Winter | hill fort, snow (repaint) | Wait for instructions. / Place a flare in the town that you want to take control of. |
| eecam2 | 4 | EE2_Jadwiga_4 | 144 | 1% | 0% | 48% | 14% | 0% | 0% | 7 (0) | 7 | 176 | Default | open field | Wait for instructions. / Defeat the Teutonic detachment besieging the southern gate. |
| eecam2 | 5 | EE2_Jadwiga_5 | 200 | 4% | 0% | 50% | 20% | 0% | 0% | 8 (0) | 8 | 195 | Desert |  | Vytautas must survive. / Force Kazikermen into submission so that Tokhtamysh can reclaim his throne. |
| eecam2 | 6 | EE2_Jadwiga_6 | 200 | 5% | 0% | 63% | 10% | 0% | 0% | 5 (2) | 8 | 193 | Default | open field | You will soon have to deal with the main Teutonic army. To prevail, you must first increas / Defeat the Teutonic Order at the Battle of Grunwald. |
| eecam3 | 1 | EE3_Zizka_1 | 144 | 0% | 0% | 67% | 18% | 0% | 0% | 1 (0) | 5 | 136 | Default |  | Destroy Heinrich of Rozmberk’s Castle. / Plunder enemy supply convoys to obtain additional resources. |
| eecam3 | 2 | EE3_Zizka_2 | 168 | 0% | 0% | 76% | 14% | 0% | 0% | 2 (2) | 7 | 45 | Empty | open field | Wladyslaw II Jagiello must survive. / Defeat the Teutonic Order (Grey). |
| eecam3 | 3 | EE3_Zizka_3 | 168 | 0% | 0% | 76% | 11% | 0% | 0% | 4 (0) | 6 | 59 | Default | open field | At least 10 units (including 3 Hussite Wagons) must reach Tabor. / Destroy the Castle in 2 of the 3 enemy fortresses (Sedlec, Pisek, and Prachatice). |
| eecam3 | 4 | EE3_Zizka_4 | 144 | 1% | 0% | 60% | 20% | 0% | 0% | 3 (1) | 7 | 74 | Default |  | Defend Prague by defeating Emperor Sigismund, the Royalists, and the Crusaders. / Capture the St. Vitus Cathedral (Monument) to retake the Lesser Town from the Royalists. |
| eecam3 | 5 | EE3_Zizka_5 | 144 | 0% | 0% | 15% | 17% | 0% | 72% | 5 (0) | 6 | 75 | Winter | snow (repaint) | Escape Kutna Hora and reach your Hussite allies in the north. / Defeat Emperor Sigismund and Zawisza to drive the crusaders from Bohemia. |
| eecam3 | 6 | EE3_Zizka_6 | 200 | 0% | 0% | 67% | 19% | 0% | 0% | 8 (0) | 7 | 40 | Empty |  | Defeat Prague, Plzen, and the Royalists. / Bring Zygimantas Korybut to the St. Vitus Cathedral (Monument) in Prague so that he will t |
| fcam1 | 1 | F1_Alaric_1 | 144 | 3% | 0% | 66% | 6% | 0% | 3% | 2 (1) | 5 | 47 | Default | open field | Defeat the Western Roman Empire (Blue). / Destroy Arbogast's (Teal) Town Center. |
| fcam1 | 2 | F1_Alaric_2 | 200 | 0% | 0% | 25% | 27% | 2% | 0% | 3 (0) | 7 | 57 | Default | coastal | Sack Sparta by destroying its Town Center. / Sack Argos by destroying its Town Center. |
| fcam1 | 3 | F1_Alaric_3 | 200 | 0% | 0% | 46% | 33% | 0% | 0% | 6 (1) | 6 | 40 | Autumn | coastal | Defeat Aquileia. / Defeat Cremona. |
| fcam1 | 4 | F1_Alaric_4 | 200 | 0% | 0% | 29% | 8% | 0% | 0% | 12 (0) | 6 | 48 | Autumn | open field | Take the city of Rome by destroying all 12 Castles within its city walls. / Send a unit to Ataulf to have him attack the city from the west. |
| fcam1 | 5 | F1_Alaric_5 | 200 | 1% | 0% | 28% | 20% | 0% | 50% | 6 (0) | 6 | 30 | Default | snow (repaint) | Narbo / Tolosa |
| fcam2 | 1 | F2_Dracula1 | 120 | 0% | 0% | 57% | 16% | 1% | 0% | 1 (0) | 6 | 41 | Default |  | Vlad Dracula must survive. / Bring Vlad Dracula to the local voivods to convince them to join you against Vladislav II. |
| fcam2 | 2 | F2_Dracula2 | 200 | 4% | 0% | 28% | 20% | 2% | 2% | 8 (0) | 8 | 127 | Default |  | Protect the Bran Castle. / Vlad Dracula must reach the Bran Castle to the north. |
| fcam2 | 3 | F2_Dracula3 | 200 | 0% | 0% | 50% | 24% | 0% | 0% | 4 (0) | 8 | 47 | Default |  | Conquer Giurgiu by destroying its Castle and all towers. / Defeat all enemy towns and fortresses by destroying all of their Town Centers, Castles and |
| fcam2 | 4 | F2_Dracula4 | 168 | 1% | 0% | 68% | 11% | 0% | 0% | 7 (2) | 7 | 41 | Default | open field | Win the initial battle against the Ottoman forces. / Ensure that all of your Castles remain standing until the timer expires. |
| fcam2 | 5 | F2_Dracula5 | 120 | 2% | 0% | 27% | 27% | 3% | 0% | 3 (0) | 8 | 40 | Default | coastal | Win the initial battle against the Ottoman forces. / Conquer Sabac for Hungary by slaying the Ottoman garrison there. |
| fcam3 | 1 | F3_Bari1 | 168 | 0% | 0% | 47% | 25% | 0% | 0% | 3 (0) | 8 | 59 | Default | coastal | Wait for instructions from Emperor Louis II. / Ensure that the siege of Bari is not broken. |
| fcam3 | 2 | F3_Bari2 | 168 | 0% | 0% | 43% | 24% | 1% | 0% | 5 (0) | 8 | 58 | Default |  | Escape from Bari through the western gates as quickly as possible. / Find a place to take refuge from the rebel forces. |
| fcam3 | 3 | F3_Bari3 | 120 | 1% | 0% | 57% | 8% | 0% | 0% | 2 (0) | 4 | 24 | Default | open field | Defeat Melus’ Army. / Defeat the Norman Mercenaries. |
| fcam3 | 4 | F3_Bari4 | 168 | 0% | 0% | 54% | 9% | 1% | 0% | 5 (0) | 8 | 71 | Default | open field | Destroy Dattus’ tower on the Garigliano to end his raids into Apulia. / Plunder the Abbey of Montecassino to seize its wealth and relics. |
| fcam3 | 5 | F3_Bari5 | 168 | 0% | 0% | 29% | 19% | 0% | 0% | 5 (0) | 8 | 87 | Default |  | Wait for instructions from Stephanos Pateranos. / Destroy the Norman siege engines. |
| fcam4 | 1 | F4_Sforza_1 | 144 | 0% | 0% | 87% | 3% | 0% | 0% | 1 (0) | 8 | 74 | Empty | open field | Escape Brescia. / Destroy the Venetians in Brescia. |
| fcam4 | 2 | F4_Sforza_2 | 144 | 0% | 0% | 39% | 35% | 0% | 0% | 3 (0) | 6 | 57 | Autumn | coastal | Destroy Piccinino's military buildings. / Bring the Relic to Monasteries to capture cities. |
| fcam4 | 3 | F4_Sforza_3 | 144 | 0% | 0% | 41% | 31% | 0% | 0% | 2 (0) | 3 | 40 | Empty | coastal | Defeat Piccinino. |
| fcam4 | 4 | F4_Sforza_4 | 144 | 3% | 0% | 28% | 17% | 0% | 0% | 4 (0) | 6 | 44 | Default |  | Destroy the Castle in Caravaggio. / Destroy the Castle in Piacenza. |
| fcam4 | 5 | F4_Sforza_5 | 168 | 9% | 0% | 65% | 6% | 0% | 0% | 2 (0) | 4 | 82 | Empty |  | Destroy Milan's Castle and build a new Castle over the ruins. / Defeat Milan. |
| fcam5 | 1 | F5_Pachacuti_1 | 168 | 0% | 11% | 43% | 15% | 3% | 0% | 2 (0) | 5 | 96 | Jungle |  | Capture at least 3 artifacts (Relic Carts) and bring them to the flagged area near your se / Tribute 300 gold to the Quechua to win their friendship. OR Force them to submit to your r |
| fcam5 | 2 | F5_Pachacuti_2 | 168 | 0% | 12% | 37% | 13% | 2% | 0% | 10 (0) | 8 | 70 | Jungle |  | Defeat Anccu Hualloc's army, which is marching on Cuzco. / Wait for new instructions. |
| fcam5 | 3 | F5_Pachacuti_3 | 144 | 0% | 1% | 65% | 4% | 0% | 4% | 2 (0) | 8 | 132 | Winter | open field | Kill Urqu. / Leaderless Inca soldiers will join your army if they get so see Pachacuti. |
| fcam5 | 4 | F5_Pachacuti_4 | 200 | 0% | 15% | 40% | 28% | 2% | 0% | 7 (0) | 8 | 101 | Default | coastal | Wait for your armies to assemble. / Conquer Waman Karpa by destroying the 4 Castles of the city. |
| fcam6 | 1 | F6_Prithviraj_1 | 168 | 0% | 4% | 31% | 12% | 11% | 0% | 4 (0) | 7 | 111 | Jungle | open field | Save one of the two Chauhan Town Centers. / Kill the rebellious cousin, Nagarjuna. |
| fcam6 | 2 | F6_Prithviraj_2 | 168 | 0% | 13% | 43% | 25% | 6% | 0% | 2 (0) | 7 | 103 | Default | coastal | Find and kill the Tiger by following the trail of animal remains. / Kill the enemy rajas to conquer all of Rajasthan. |
| fcam6 | 3 | F6_Prithviraj_3 | 144 | 0% | 26% | 69% | 11% | 0% | 0% | 2 (0) | 7 | 81 | Jungle | Sahyadri/jungle | Bring Sanyogita to the Wonder in Lal Kot. / Sanyogita and Prithviraj must survive. |
| fcam6 | 4 | F6_Prithviraj_4 | 120 | 91% | 0% | 42% | 7% | 1% | 0% | 3 (3) | 6 | 84 | Default | hill fort | Destroy Monasteries to prevent an enemy victory. / Bring the 3 Relic Carts to the Buddhist Monks. |
| fcam6 | 5 | F6_Prithviraj_5 | 168 | 0% | 26% | 49% | 26% | 0% | 0% | 9 (0) | 8 | 138 | Jungle | Sahyadri/jungle, coastal | Choose your starting kingdom by converting a raja. / Convert the remaining rajas. |
| fcam7 | 1 | C4_1_Tours | 168 | 3% | 0% | 47% | 16% | 0% | 0% | 1 (0) | 4 | 36 | Autumn |  | Capture the 6 Trade Carts in the Moors' baggage train and bring them to the Cathedral in T / Prevent the Muslims from destroying any of your 3 Town Centers. |
| fcam7 | 2 | C4_2_Vinlandsaga | 220 | 7% | 0% | 9% | 67% | 0% | 31% | 2 (1) | 4 | 45 | Winter | coastal, snow (repaint) | Transport Erik the Red west across the ocean to the New World and establish a colony there / The Vikings must build a Town Center, a Market, and 12 Houses in the New World. |
| fcam7 | 3 | C4_3_Hastings | 220 | 4% | 0% | 48% | 38% | 1% | 2% | 3 (2) | 5 | 36 | Default | coastal | Conquer England by destroying the Castle of Harold the Saxon (Orange). / Send Transport Ships to the north to pick up Harald Hardrada's Viking Berserks. |
| fcam7 | 4 | C4_4_Manzikert | 168 | 47% | 0% | 11% | 6% | 10% | 0% | 5 (2) | 6 | 27 | Desert | hill fort | Defeat the Byzantine Army. / Receive tributes from the Theme of Cappadocia by capturing their Town Center. |
| fcam7 | 5 | C4_5_Agincourt | 144 | 3% | 0% | 54% | 26% | 1% | 0% | 3 (0) | 6 | 58 | Default | coastal | King Henry V must survive. / King Henry V must return home to England. |
| fcam7 | 6 | C4_6_Lepanto | 144 | 1% | 0% | 19% | 67% | 9% | 0% | 7 (0) | 3 | 68 | Default | coastal | Complete and then defend your Wonder from the Turkish navy for 200 years. / Tribute the Greeks (Green) 800 gold so that they will ally with you. |
| fcam7 | 7 | C4_7_Japan | 200 | 1% | 2% | 39% | 40% | 0% | 17% | 7 (1) | 5 | 45 | Winter | coastal | Your lord, Nobunaga, is trapped in Kyoto. You must rescue him to restore his honor. / Establish a base in Osaka (Red) from which to attack Kyoto. |
| fcam7 | 8 | C4_8_Noryang | 200 | 5% | 5% | 27% | 65% | 4% | 0% | 9 (5) | 5 | 56 | Default | coastal | Find Admiral Yi and learn of his secret weapon. / Prevent the Japanese from destroying Korea's Wonder. |
| fcam7 | 9 | F7_1_Bukhara (557) | 200 | 0% | 0% | 21% | 12% | 1% | 0% | 5 (0) | 6 | 110 | Autumn | open field | Follow the guide down the mountain. / Protect the Persian villages to keep getting their resources. |
| fcam7 | 10 | F7_2_Dos Pilas (648) | 220 | 1% | 18% | 63% | 6% | 0% | 0% | 13 (0) | 8 | 143 | Jungle |  | Head to Dos Pilas to warn its citizens. / Your Town Center must remain standing. |
| fcam7 | 11 | F7_3_York (865) | 480 | 0% | 0% | 25% | 58% | 3% | 1% | 31 (0) | 8 | 135 | Default | coastal | Construct a camp - build a Town Center at any one of the 5 campsites (marked on the map by / Instead of founding a camp at one of the unoccupied locations, you could attack the Monast |
| fcam7 | 12 | F7_4_Honfoglalas (895) | 220 | 1% | 0% | 57% | 17% | 0% | 0% | 4 (0) | 6 | 167 | Default |  | Defeat 2 of the 3 main factions (Bulgaria, Great Moravia, and East Francia.) / While nomadic, bring Sheep to the enclosure to generate food. |
| fcam7 | 13 | F7_5_Kurikara (1183) | 200 | 0% | 0% | 27% | 36% | 3% | 0% | 9 (0) | 8 | 78 | Default | coastal | Bring the supply cart and at least one soldier to Yoshinaka's palace (marked by the blue f / Protect Yoshinaka's palace (Wonder) in Kurikara. |
| fcam7 | 14 | F7_6_Cyprus (1191) | 168 | 0% | 1% | 23% | 49% | 9% | 0% | 3 (0) | 5 | 35 | Default | coastal | Force Isaac Komnenos to surrender by defeating Nicosia. / Take the city of Limassol by destroying its Castle. |
| fcam7 | 15 | F7_7_Bapheus (1302) | 220 | 0% | 0% | 14% | 18% | 5% | 0% | 9 (0) | 7 | 119 | Empty |  | Osman must survive. / Defeat the Byzantines by destroying 3 Byzantine Castles. |
| fcam7 | 16 | F7_8_Poyang (1363) | 200 | 1% | 2% | 27% | 59% | 0% | 0% | 2 (0) | 8 | 144 | Default | coastal | Clear the way for the first shipment for the Nanchang temple complex. You have 25 minutes. / Escort the first shipment to the temple complex. |
| incam1 | 1 | IN1_Babur_1 | 168 | 14% | 0% | 30% | 15% | 2% | 0% | 5 (2) | 7 | 130 | Night | hill fort | Hold off the enemy Timurids until morning breaks and the sun rises. / The Fortified Tower in Babur's camp must not be destroyed. |
| incam1 | 2 | IN1_Babur_2 | 168 | 8% | 0% | 14% | 8% | 63% | 0% | 5 (1) | 6 | 149 | Default | hill fort, desert (repaint) | Babur and Qutlugh must reach Herat to meet with Babur's uncle Husain Baiqara (location mar / Defeat both Uzbek armies. |
| incam1 | 4 | IN1_Babur_4 | 144 | 2% | 0% | 46% | 11% | 1% | 0% | 4 (0) | 6 | 117 | Default | open field | Raid the Delhi Auxiliary Forces' Supply Stores (Trade Workshops). This will make them trai / Destroy all enemy towers on the road to the northeast so that your Ottoman allies can brin |
| incam1 | 5 | IN1_Babur_5 | 200 | 2% | 1% | 53% | 23% | 4% | 1% | 4 (2) | 7 | 103 | Default |  | Defeat both Rajput factions (the Kingdom of Amber and the Kingdom of Mewar). / Repair damaged Town Centers (Grey) to win over the rural population. |
| incam2 | 1 | IN2_Rajendra_1 | 168 | 4% | 28% | 59% | 14% | 0% | 0% | 3 (2) | 8 | 146 | Night | Sahyadri/jungle | Wait for instructions. / Scout the Chalukyan position and exploit whatever weaknesses you can find. |
| incam2 | 2 | IN2_Rajendra_2 | 200 | 2% | 15% | 24% | 61% | 0% | 0% | 4 (2) | 7 | 153 | Desert | coastal | Land your troops in the Chola harbor. / Rajendra must survive. |
| incam2 | 3 | IN2_Rajendra_3 | 240 | 4% | 10% | 27% | 64% | 0% | 0% | 9 (0) | 8 | 236 | Desert | coastal | Bring the Envoy and the Grand Chariot safely to Rajendra Chola. / Wait for instructions. |
| incam2 | 4 | IN2_Rajendra_4 | 200 | 27% | 22% | 43% | 21% | 0% | 0% | 8 (1) | 8 | 137 | Jungle | hill fort, Sahyadri/jungle | Rendezvous with General Araiyan near the Bengali army's camp. / Seize Kalinga by killing its defenders. |
| incam2 | 5 | IN2_Rajendra_5 | 240 | 0% | 10% | 25% | 65% | 0% | 1% | 8 (1) | 7 | 173 | Desert | coastal | Establish a beachhead by capturing one of the Castles marked on the minimap. To capture a  / Capture <TargetCastles> of the <TotalCastles> Castles marked on the minimap. To capture a  |
| incam3 | 1 | IN3_Devapala_1 | 144 | 0% | 29% | 49% | 33% | 0% | 0% | 1 (0) | 5 | 61 | Empty | Sahyadri/jungle, coastal | Capture Kamarupa’s Town Center by bringing a soldier to it. / Defeat Utkala. |
| incam3 | 2 | IN3_Devapala_2 | 144 | 0% | 27% | 68% | 14% | 0% | 0% | 3 (1) | 4 | 71 | Default | Sahyadri/jungle | Capture and hold the Monument in Kannauj. / Build a Castle and train <RathasToTrain> Rathas. |
| incam3 | 3 | IN3_Devapala_3 | 168 | 0% | 3% | 54% | 19% | 22% | 0% | 4 (0) | 6 | 75 | Default |  | Eliminate all 3 Huna Khans. / Convert the Huna Khans rather than killing them. |
| incam3 | 4 | IN3_Devapala_4 | 144 | 0% | 17% | 51% | 31% | 0% | 0% | 8 (0) | 4 | 54 | Default | coastal | Defeat the Pandyas by destroying their Castles. / Destroy the Rashtrakuta Wonder. |
| incam3 | 5 | IN3_Devapala_5 | 168 | 0% | 21% | 56% | 28% | 1% | 0% | 3 (1) | 4 | 108 | Default | Sahyadri/jungle, coastal | Defeat the Pratiharas. / Defeat the Rashtrakutas. |
| kcam1 | 1 | K1_Tamerlane_1 | 144 | 0% | 0% | 24% | 14% | 2% | 0% | 4 (0) | 7 | 42 | Default | open field | Capture 3 of the 4 Relics held by the rival Transoxianan khanates. / Kill Urus Khan so Tokhtamysh can take control of the White Horde. |
| kcam1 | 2 | K1_Tamerlane_2 | 168 | 3% | 0% | 24% | 16% | 3% | 0% | 8 (2) | 8 | 72 | Default |  | Destroy the Castle in 3 of the following enemy cities: / Defeat Tokhtamysh by tearing down his two Castles. |
| kcam1 | 3 | K1_Tamerlane_3 | 168 | 1% | 0% | 6% | 13% | 0% | 78% | 9 (1) | 8 | 72 | Winter | open field, snow (repaint) | Defeat the enemy force blocking your way across the icy ford. / Destroy 2 of Tokhtamysh's 3 power centers: |
| kcam1 | 4 | K1_Tamerlane_4 | 144 | 2% | 3% | 33% | 4% | 0% | 0% | 5 (1) | 7 | 40 | Default | open field | Defeat Shah Tughluq's army outside the walls of Delhi. / Destroy the 5 Castles defending Delhi before the timer runs out. |
| kcam1 | 6 | K1_Tamerlane_6 | 168 | 1% | 0% | 39% | 15% | 0% | 0% | 10 (1) | 6 | 77 | Empty |  | Prepare your defenses. Bayezid will attack in 30 minutes. / Raid outlying Ottoman camps to weaken Bayezid's army. |
| kcam2 | 1 | K2_Ivaylo_1 | 168 | 87% | 0% | 12% | 2% | 0% | 82% | 4 (4) | 4 | 111 | Winter | hill fort, snow (repaint) | Kill the bolyars (Kings) hiding in their Castles. / Ally with Tsar Konstantin or attack him. |
| kcam2 | 2 | K2_Ivaylo_2 | 144 | 3% | 0% | 57% | 12% | 0% | 0% | 5 (1) | 5 | 95 | Autumn | open field | Capture and hold the Church of the Patriarchs. / Enter Tarnovo to fulfill the Tsarina's request. |
| kcam2 | 3 | K2_Ivaylo_3 | 144 | 0% | 0% | 42% | 16% | 0% | 0% | 5 (0) | 7 | 108 | Default |  | Reach Drastar before Hranislav is slain in single combat. / Destroy Nogai's Great Tent. |
| kcam2 | 4 | K2_Ivaylo_4 | 144 | 2% | 0% | 72% | 5% | 0% | 0% | 3 (1) | 8 | 116 | Default | open field | Bring Ivaylo to the allied Bulgarian camp. / Ivaylo, Georgi Terter, and the Bulgarians must survive. |
| kcam2 | 5 | K2_Ivaylo_5 | 200 | 1% | 0% | 61% | 17% | 0% | 0% | 6 (1) | 7 | 151 | Default |  | Escape the church courtyard. / Find Radu Negru. |
| kcam3 | 1 | K3_Kotyan_1 | 220 | 1% | 0% | 27% | 18% | 0% | 63% | 1 (1) | 6 | 99 | Default | snow (repaint) | Seul Kotyan Khan peut recruter des troupes. S'il meurt, vous perdrez la partie. / Rencontrez toutes les tribus coumanes afin de recruter des troupes. Dépêchez-vous, car l'e |
| kcam3 | 4 | K3_Kotyan_4 | 200 | 1% | 0% | 61% | 21% | 0% | 0% | 4 (0) | 6 | 139 | Default |  | Rendez-vous au camp couman pour vous présenter. / Explorez la campagne et cherchez des moyens d'aider les Hongrois. |
| kcam3 | 5 | K3_Kotyan_5 | 240 | 0% | 0% | 52% | 24% | 0% | 0% | 6 (0) | 8 | 203 | Autumn |  | Follow the Cuman Chief to the Danube River. / Liberate the Bulgarian Villagers. |
| rcam1 | 1 | R1_GajahMada_1 | 200 | 0% | 38% | 58% | 19% | 0% | 0% | 2 (0) | 5 | 209 | Jungle | Sahyadri/jungle | Defeat the Singhasari (Blue). / Defeat Kediri (Cyan) by destroying their castle. |
| rcam1 | 2 | R1_GajahMada_2 | 168 | 0% | 18% | 45% | 12% | 0% | 3% | 4 (0) | 6 | 68 | Default |  | King Jayanegara must survive. / Reach King Jayanegara before the rebels overwhelm his royal guard. |
| rcam1 | 3 | R1_GajahMada_3 | 200 | 0% | 12% | 27% | 61% | 0% | 0% | 2 (0) | 8 | 73 | Default | coastal | Defeat 2 of the 3 enemies. / At least 3 colonies must exist and have a market. |
| rcam1 | 4 | R1_GajahMada_4 | 168 | 0% | 12% | 24% | 65% | 0% | 0% | 2 (0) | 5 | 48 | Autumn | coastal | Destroy all of Kutai's docks. / Destroy all of Makassar's docks. |
| rcam1 | 5 | R1_GajahMada_5 | 200 | 0% | 27% | 42% | 36% | 1% | 0% | 1 (0) | 7 | 132 | Default | Sahyadri/jungle, coastal | There are two ways to approach the capital. You can disembark to the west and approach the / Destroy bandit camps to gain extra resources. |
| rcam2 | 1 | R2_Suryavarman I_1 | 120 | 1% | 25% | 77% | 5% | 0% | 0% | 1 (0) | 5 | 9 | Jungle | Sahyadri/jungle | Storm the city of Angkor and kill Udayadityavarman I. |
| rcam2 | 2 | R2_Suryavarman I_2 | 168 | 3% | 23% | 69% | 14% | 0% | 0% | 4 (0) | 6 | 26 | Jungle | Sahyadri/jungle | Defeat the Northern Rebels. / Defeat the Eastern Rebels. |
| rcam2 | 3 | R2_Suryavarman I_3 | 120 | 0% | 20% | 68% | 14% | 1% | 0% | 0 (0) | 5 | 28 | Jungle | Sahyadri/jungle | The Envoy and the chariot (Trade Cart) laden with gifts must reach the Andaman port in the / Recruit any two of the four companies of soldiers camped nearby by selecting their leader  |
| rcam2 | 4 | R2_Suryavarman I_4 | 168 | 1% | 8% | 30% | 55% | 1% | 0% | 5 (0) | 4 | 14 | Jungle | coastal | Defeat the Tambralingas. / Defeat the Srivijaya. |
| rcam2 | 5 | R2_Suryavarman I_5 | 168 | 2% | 14% | 48% | 30% | 0% | 0% | 9 (0) | 7 | 25 | Jungle | coastal | Defeat three of your five enemies (Hariphunchai, Lavo Kingdom, Northern Cham, Southern Cha / Construct and defend a Wonder. |
| rcam3 | 1 | R3_Bayinnaung_1 | 144 | 0% | 29% | 47% | 29% | 0% | 1% | 7 (0) | 6 | 106 | Jungle | Sahyadri/jungle, coastal | Kill King Takayutpi of Hanthawaddy (King). / Capture the Monument in Prome. |
| rcam3 | 2 | R3_Bayinnaung_2 | 144 | 2% | 30% | 44% | 20% | 1% | 0% | 3 (0) | 5 | 61 | Jungle | Sahyadri/jungle | Accumulate 4,000 gold. / Kill King Hkonmaing of Ava (King) and take the Pagan crown. |
| rcam3 | 3 | R3_Bayinnaung_3 | 144 | 1% | 30% | 46% | 29% | 2% | 2% | 4 (1) | 6 | 93 | Jungle | Sahyadri/jungle, coastal | Bring word of King Tabinshwehti's death to Bayinnaung. / Defeat all four pretenders. |
| rcam3 | 4 | R3_Bayinnaung_4 | 144 | 4% | 17% | 48% | 15% | 3% | 0% | 2 (0) | 7 | 114 | Jungle |  | Place a Relic in each flagged Monastery before the season ends. / Convert Prince Ramesuan and King Mekuti. |
| rcam3 | 5 | R3_Bayinnaung_5 | 168 | 0% | 26% | 33% | 39% | 2% | 0% | 12 (0) | 7 | 94 | Default | Sahyadri/jungle, coastal | Bring Bayinnaung to the four Buddhist temples (Wonders). / Bayinnaung must survive. |
| rcam4 | 1 | R4_LeLoi_1 | 200 | 1% | 40% | 76% | 13% | 1% | 0% | 7 (0) | 8 | 76 | Autumn | Sahyadri/jungle | Liberate the Vietnamese people by destroying every Ming tower in the five villages marked  / The Trinh and the Nguyen are two powerful Vietnamese families that support your cause. The |
| rcam4 | 2 | R4_LeLoi_2 | 200 | 2% | 37% | 44% | 7% | 1% | 0% | 7 (0) | 5 | 95 | Jungle | Sahyadri/jungle | At least one of yours' or your allies' Castles must keep standing. / At least <TotalSoldiers> allied soldiers must be able to escape. |
| rcam4 | 4 | R4_LeLoi_4 | 144 | 2% | 48% | 59% | 19% | 0% | 0% | 3 (0) | 6 | 54 | Jungle | Sahyadri/jungle | Capture the 3 gunpowder stores in the southeastern Ming fortress by destroying the Keep ne / Win the support of the Villagers by wiping out the Ming forces occupying their settlement. |
| rcam4 | 5 | R4_LeLoi_5 | 240 | 0% | 32% | 64% | 11% | 0% | 2% | 6 (0) | 6 | 84 | Jungle | Sahyadri/jungle | Capture the Monument in the city of Nghe An by killing the units defending it and bringing / Defeat General Wang Tong. |
| rcam4 | 6 | R4_LeLoi_6 | 144 | 1% | 52% | 86% | 7% | 0% | 0% | 11 (1) | 4 | 38 | Default | Sahyadri/jungle | It may be wise to defeat the Ming Vanguard before assaulting the fortress. / Defeat the Ming by destroying all Castles in their fortress. |
| wecam1 | 1 | WE1_Edward_1 | 200 | 2% | 0% | 60% | 20% | 0% | 0% | 3 (1) | 7 | 95 | Default |  | Edward Longshanks must survive. / Gilbert de Clare must survive. |
| wecam1 | 2 | WE1_Edward_2 | 200 | 3% | 0% | 49% | 27% | 0% | 0% | 13 (9) | 8 | 69 | Empty | coastal | Hold Acre and Tripoli until the Mamluk forces withdraw. At least one Castle in each city m / Destroy Qaqun and Nazareth to weaken the enemy war effort. |
| wecam1 | 3 | WE1_Edward_3 | 168 | 1% | 0% | 62% | 24% | 0% | 0% | 2 (0) | 6 | 66 | Default |  | Travel to the site of the first Castle. / Defend the builders while they construct the first Castle. |
| wecam1 | 4 | WE1_Edward_4 | 168 | 0% | 0% | 61% | 28% | 0% | 0% | 1 (0) | 5 | 31 | Default | coastal | Capture Berwick by defeating its garrison. / Defeat the Scottish Army. |
| wecam1 | 5 | WE1_Edward_5 | 168 | 0% | 0% | 62% | 26% | 0% | 0% | 4 (1) | 8 | 58 | Empty | coastal | Defend the English engineers from Scottish attacks. / Research Warwolf at your Castle. |
| wecam2 | 1 | WE2_GrandDukes_1 | 168 | 0% | 0% | 69% | 9% | 0% | 0% | 3 (0) | 5 | 90 | Autumn | open field | Capture the city of Liège by destroying 2 of its 3 Castles. / Loot Markets, Mills, and Trade Workshops in the nearby villages to receive additional reso |
| wecam2 | 2 | WE2_GrandDukes_2 | 220 | 3% | 0% | 60% | 19% | 1% | 0% | 7 (1) | 8 | 231 | Default |  | Drive the Écorcheurs out of Ile-de-France. / Defeat Bernard d’Armagnac. |
| wecam2 | 3 | WE2_GrandDukes_3 | 200 | 0% | 0% | 67% | 11% | 0% | 0% | 4 (0) | 7 | 139 | Empty | open field | You must conquer the city before Henry V and his army arrive. / Kill Bernard d'Armagnac to conquer Paris. |
| wecam2 | 4 | WE2_GrandDukes_4 | 200 | 2% | 0% | 61% | 16% | 0% | 0% | 5 (1) | 6 | 65 | Default |  | Defeat Jacqueline of Hainaut. / Defeat Humphrey of Lancaster. |
| wecam2 | 5 | WE2_GrandDukes_5 | 220 | 0% | 0% | 37% | 47% | 1% | 3% | 5 (0) | 6 | 125 | Winter | coastal | Force Jacqueline to surrender by destroying her Castles in Leiden, Utrecht, and Rotterdam. / Drive the Hooks out of the Dutch villages so that your allies, the Cods, can take over. |
| wecam2 | 6 | WE2_GrandDukes_6 | 220 | 1% | 0% | 66% | 14% | 2% | 0% | 8 (1) | 7 | 80 | Default | open field | Set the Castle in Choisy on fire (reduce the Castle’s HP to 1000 or less) to take over the / Build a Market in Soissons to win the favor of the townspeople. |
| wecam3 | 1 | WE3_Hautevilles_1 | 255 | 10% | 0% | 26% | 54% | 0% | 0% | 3 (1) | 6 | 380 | Default | coastal | Betray and capture a Norman barony by killing its garrison. To betray a player, go to the  / Travel to Salerno to serve the Lombards. |
| wecam3 | 2 | WE3_Hautevilles_2 | 255 | 13% | 0% | 22% | 53% | 0% | 0% | 5 (2) | 8 | 252 | Default | coastal | Surrender Ibn at-Timnah to his rival by making him board Ibn al-Hawwas’ Transport Ship. / Ignore Ibn al-Hawwas’ demands. |
| wecam3 | 4 | WE3_Hautevilles_4 | 200 | 37% | 0% | 5% | 7% | 1% | 0% | 2 (1) | 8 | 213 | Default | hill fort | Defend Antioch until Alexios Komnenos arrives. / Defend Antioch until Kerbogha retreats. |
| wecam3 | 5 | WE3_Hautevilles_5 | 255 | 6% | 0% | 18% | 61% | 6% | 0% | 10 (6) | 7 | 229 | Default | coastal | Construct and defend a Wonder to achieve a cultural victory. / Defeat or ally with all factions (<Count Defeated or Allied>/6). |
| xcam1 | 1 | C1_Attila_1 | 144 | 8% | 0% | 37% | 26% | 4% | 2% | 3 (1) | 5 | 134 | Autumn | hill fort, coastal | Defeat 2 of your remaining 3 enemies (the Scythians, Romans and Persians). / Send 10 Horses to the flagged Scythian palisade so that the Scythians can supply Attila wi |
| xcam1 | 2 | C1_Attila_2 | 168 | 4% | 0% | 70% | 12% | 0% | 1% | 2 (0) | 8 | 47 | Winter | open field | Raid the Roman villages. Once you have enough resources to build a forward base, then you  / Train an army and defeat the Romans by leveling their Town Center. |
| xcam1 | 3 | C1_Attila_3 | 144 | 5% | 0% | 42% | 40% | 1% | 0% | 1 (0) | 4 | 31 | Default | coastal | Stockpile 10,000 gold in tribute from the Romans. |
| xcam1 | 4 | C1_Attila_4 | 168 | 10% | 0% | 30% | 5% | 0% | 78% | 3 (0) | 5 | 33 | Default | snow (repaint) | Defeat Burgundy. / Defeat Metz. |
| xcam1 | 5 | C1_Attila_5 | 200 | 0% | 0% | 76% | 12% | 0% | 0% | 0 (0) | 6 | 20 | Default | open field | Defeat the Romans. / Defeat the Visigoths. |
| xcam1 | 6 | C1_Attila_6 | 220 | 5% | 0% | 42% | 34% | 0% | 2% | 6 (0) | 6 | 36 | Default | coastal | Attila must meet with Pope Leo I outside the gates of Rome. / Attila must survive. |
| xcam2 | 1 | C2_ElCid_1 | 120 | 30% | 0% | 13% | 13% | 1% | 6% | 7 (6) | 6 | 66 | Default | hill fort | Become King Sancho's champion in a trial by combat. / Take command of the Castillian army in order to capture King Sancho's conniving, ambitious |
| xcam2 | 2 | C2_ElCid_2 | 168 | 2% | 0% | 15% | 19% | 1% | 0% | 2 (0) | 6 | 35 | Default |  | El Cid must meet with the Imam, for he will know how to quell the unrest in Toledo. / Recover the 4 Relics from the rebel leaders and return them to the Imam. |
| xcam2 | 3 | C2_ElCid_3 | 144 | 3% | 0% | 17% | 14% | 0% | 21% | 5 (0) | 4 | 27 | Winter | open field, snow (repaint) | El Cid must find a new city in which to live and a new lord to serve. / Join Motamid of the Moors at his Castle in Zaragoza. |
| xcam2 | 4 | C2_ElCid_4 | 168 | 14% | 0% | 15% | 18% | 18% | 0% | 5 (0) | 5 | 66 | Autumn |  | Destroy the 6 Black Guard Docks. / King Alfonso must survive. |
| xcam2 | 5 | C2_ElCid_5 | 144 | 1% | 0% | 21% | 36% | 3% | 0% | 2 (0) | 6 | 36 | Default | coastal | El Cid must flee and establish a new base. / El Cid must once again find a new city in which to live. |
| xcam2 | 6 | C2_ElCid_6 | 144 | 1% | 0% | 5% | 52% | 9% | 0% | 5 (0) | 5 | 12 | Default | coastal | The body of The Cid (near the Castle) must come to no harm, lest the people of Valencia re / Defeat the three armies of Yusuf so that Valencia will remain free. |
| xcam3 | 1 | C3_Montezuma_1 | 144 | 8% | 46% | 68% | 10% | 0% | 0% | 2 (0) | 4 | 32 | Jungle | Sahyadri/jungle | Capture the 4 shrines (Monasteries) sacred to Quetzalcoatl. / Place a sacred Relic in each of the 4 shrines (Monasteries). |
| xcam3 | 2 | C3_Montezuma_2 | 200 | 22% | 29% | 53% | 31% | 0% | 0% | 1 (1) | 5 | 44 | Jungle | Sahyadri/jungle, coastal | Deliver the summons of war to the Tlacopan Town Center. / Deliver the summons of war to the Texcoco Town Center. |
| xcam3 | 4 | C3_Montezuma_4 | 200 | 2% | 11% | 18% | 68% | 0% | 0% | 6 (0) | 4 | 30 | Jungle | coastal | Rescue the Aztec warriors held prisoner by the Tlaxcala. / Travel across Lake Texcoco, where you may safely gather resources. |
| xcam3 | 5 | C3_Montezuma_5 | 168 | 21% | 26% | 37% | 51% | 0% | 0% | 4 (1) | 3 | 18 | Jungle | Sahyadri/jungle, coastal | Defeat the Tlaxcala and Spanish. |
| xcam3 | 6 | C3_Montezuma_6 | 200 | 1% | 8% | 18% | 67% | 0% | 0% | 6 (0) | 4 | 13 | Jungle | coastal | Prevent Tenochtitlan's Wonder from being destroyed to preserve the morale of your warriors / Defeat the Tlaxcala, Cortéz' Army, and Cortéz' Navy. |

## Not readable by our tool

These cannot be used as templates with AoE2ScenarioParser 0.9.8.

| Campaign | Scenario | Error |
| --- | --- | --- |
| fcam5 | F5_Pachacuti_5 | End of file reached. (Requested: 4 bytes, only 2 left. |
| incam1 | IN1_Babur_3 | Scenario version: [1.54] with trigger version: [3.9] cannot be supported. :( |
| kcam1 | K1_Tamerlane_5 | embedded null byte |
| kcam3 | K3_Kotyan_2 | End of file reached. (Requested: 4 bytes, only 0 left. |
| kcam3 | K3_Kotyan_3 | End of file reached. (Requested: 300351488 bytes, only 202196 left. |
| rcam4 | R4_LeLoi_3 | End of file reached. (Requested: 301989888 bytes, only 137159 left. |
| wecam3 | WE3_Hautevilles_3 | End of file reached. (Requested: 318767104 bytes, only 327831 left. |
| xcam3 | C3_Montezuma_3 | The version DE:1.52 is not supported by AoE2ScenarioParser. :( |

The Viking campaign (`nocam1` to `nocam3`) and other newer DLC campaigns ship as packed `.gpv` files and are not in this catalog.
