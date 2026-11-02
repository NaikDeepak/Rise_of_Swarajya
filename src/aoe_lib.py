"""Small builder on top of AoE2ScenarioParser for the Swarajya campaign."""
import math
import random
import warnings
import logging

warnings.filterwarnings("ignore")

from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.datasets.terrains import TerrainId as T
from AoE2ScenarioParser.datasets.units import UnitInfo as U
from AoE2ScenarioParser.datasets.buildings import BuildingInfo as B
from AoE2ScenarioParser.datasets.heroes import HeroInfo as H
from AoE2ScenarioParser.datasets.other import OtherInfo as O
from AoE2ScenarioParser.datasets.object_support import Civilization as Civ, StartingAge
from AoE2ScenarioParser.datasets.players import PlayerColorId
from AoE2ScenarioParser.datasets.trigger_lists import (
    VictoryCondition, DiplomacyState, ActionType, Attribute, PanelLocation,
    Operation, Comparison, ObjectAttribute, ObjectType, TimeUnit,
    ColorMood, AttackStance,
)
import os as _os
import hashlib as _hashlib
import json as _json

# Campaign driver can map generator filenames to final campaign filenames and chapter titles.
RENAME = {}      # old filename -> (new filename, chapter heading)
VO_REGISTRY = {} # vo_name -> (speaker, text)
_VO_MAN_PATH = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "assets", "sounds", "vo_durations.json")
VO_DURATIONS = _json.load(open(_VO_MAN_PATH)) if _os.path.exists(_VO_MAN_PATH) else {}

# Portraits for characters who speak in narration but are not on the map.
PORTRAITS = {
    "Rajmata Jijabai": H.SANYOGITA.ID,
    "Maharani Yesubai": H.SANYOGITA.ID,
    "Maharani Soyarabai": U.QUEEN.ID,
    "Maharani Tarabai": H.SANYOGITA.ID,
    "Shahaji Raje": H.PRITHVI.ID,
    "Aurangzeb": H.BABUR.ID,
    "Emperor Aurangzeb": H.BABUR.ID,
    "Bahirji Naik": U.SCOUT_CAVALRY.ID,
    "Mirza Raja Jai Singh": H.AMOGHAVARSHA.ID,
    "Diler Khan": H.SHAYBANI_KHAN.ID,
    "Rajaram Maharaj": U.KING.ID,
    "Santaji Ghorpade": U.HUSSAR.ID,
    "Dhanaji Jadhav": U.HUSSAR.ID,
    "Annaji Datto": U.MONK.ID,
    "Moropant Pingle": U.CHAMPION.ID,
    "Kavi Kalash": U.MONK.ID,
}

WATER = {T.WATER_MEDIUM, T.WATER_DEEP, T.WATER_SHALLOW, T.WATER_DEEP_OCEAN,
         T.WATER_GREEN, T.WATER_BROWN, T.WATER_AZURE}
FOREST = {T.FOREST_JUNGLE, T.FOREST_BAMBOO, T.FOREST_OAK, T.FOREST_PALM_DESERT,
          T.FOREST_RAINFOREST, T.FOREST_BUSH, T.FOREST_DEAD, T.FOREST_MANGROVE,
          T.FOREST_LUSH_BAMBOO, T.FOREST_PALM_GRASS, T.FOREST_ACACIA}

SHIPS = {U.FIRE_GALLEY, U.GALLEY, U.WAR_GALLEY, U.GALLEON, U.CANNON_GALLEON,
         U.ELITE_CANNON_GALLEON, U.FIRE_SHIP, U.FAST_FIRE_SHIP, U.TRANSPORT_SHIP,
         U.CARAVEL, U.ELITE_CARAVEL, U.DEMOLITION_SHIP, U.FISHING_SHIP, U.TRADE_COG,
         U.DROMON}

# footprint radius (tiles) used to clear terrain under buildings
FOOT = {B.CASTLE: 2, B.WONDER: 3, B.TOWN_CENTER: 2, B.MONASTERY: 1, B.MARKET: 2,
        B.BARRACKS: 1, B.STABLE: 1, B.DOCK: 1, B.HOUSE: 1, B.FORTRESS: 2,
        B.KREPOST: 1, B.HARBOR: 1}


class Mission:
    def __init__(self, filename, title, size=120, base=T.GRASS_1, seed=1):
        logging.disable(logging.CRITICAL)
        self.s = AoE2DEScenario.from_default()
        self.filename = filename
        self.title = title
        self.size = size
        self.rng = random.Random(seed)
        mm = self.s.map_manager
        mm.map_size = size
        for t in mm.terrain:
            t.terrain_id = base
            t.elevation = 0
        self.base = base
        self.um = self.s.unit_manager
        self.tm = self.s.trigger_manager
        self.pm = self.s.player_manager
        self._land_units = []   # (x, y, r)
        self._ship_units = []
        self._chain_ix = 0
        self.heroes = {}          # display name -> (player, unit)
        self._home_cam = None
        self.s.option_manager.victory_condition = VictoryCondition.CUSTOM

    # ------------------------------------------------------------ terrain
    def tile(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.s.map_manager.get_tile(int(x), int(y))
        return None

    def paint(self, terrain, x, y):
        t = self.tile(x, y)
        if t is not None:
            t.terrain_id = terrain

    def rect(self, terrain, x1, y1, x2, y2):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.paint(terrain, x, y)

    def blob(self, terrain, cx, cy, r, jitter=0.25):
        for x in range(int(cx - r - 2), int(cx + r + 3)):
            for y in range(int(cy - r - 2), int(cy + r + 3)):
                d = math.hypot(x - cx, y - cy)
                if d <= r * (1 + self.rng.uniform(-jitter, jitter)):
                    self.paint(terrain, x, y)

    def forest_scatter(self, terrain, x1, y1, x2, y2, n, rmin=2, rmax=5):
        for _ in range(n):
            self.blob(terrain, self.rng.randint(x1, x2), self.rng.randint(y1, y2),
                      self.rng.uniform(rmin, rmax))

    def path(self, terrain, pts, width=2):
        """Paint a thick polyline (river, road)."""
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            steps = int(max(abs(bx - ax), abs(by - ay))) * 2 + 1
            for i in range(steps + 1):
                px = ax + (bx - ax) * i / steps
                py = ay + (by - ay) * i / steps
                for dx in range(-width, width + 1):
                    for dy in range(-width, width + 1):
                        if dx * dx + dy * dy <= width * width + 1:
                            self.paint(terrain, round(px + dx), round(py + dy))

    def hill(self, cx, cy, top_r, h, flat_terrain=None):
        """Plateau of height h with radius top_r, slopes of 1 per tile."""
        h = min(h, 7)
        for x in range(int(cx - top_r - h - 2), int(cx + top_r + h + 3)):
            for y in range(int(cy - top_r - h - 2), int(cy + top_r + h + 3)):
                t = self.tile(x, y)
                if t is None:
                    continue
                d = math.hypot(x - cx, y - cy)
                e = h if d <= top_r else max(0, h - int(d - top_r + 0.5))
                if e > t.elevation:
                    t.elevation = e
                if flat_terrain is not None and d <= top_r:
                    t.terrain_id = flat_terrain

    def ridge(self, pts, h, width=3):
        """Mountain ridge (Sahyadri ghat) along a polyline."""
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            steps = int(max(abs(bx - ax), abs(by - ay))) + 1
            for i in range(steps + 1):
                self.hill(ax + (bx - ax) * i / steps, ay + (by - ay) * i / steps, width, h)

    def smooth(self):
        """Guarantee neighbouring tiles differ by at most 1 in elevation."""
        n = self.size
        changed = True
        while changed:
            changed = False
            for x in range(n):
                for y in range(n):
                    t = self.tile(x, y)
                    for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                        o = self.tile(x + dx, y + dy)
                        if o is not None and t.elevation - o.elevation > 1:
                            t.elevation = o.elevation + 1
                            changed = True

    # ------------------------------------------------------------ players
    def player(self, pid, name, civ, color=None, food=200, wood=200, gold=100,
               stone=200, pop=200, human=False, age=None):
        p = self.pm.players[pid]
        p.tribe_name = name
        p.civilization = civ
        p.lock_civ = True
        p.food, p.wood, p.gold, p.stone = food, wood, gold, stone
        p.population_cap = pop
        p.human = human
        if color is not None:
            # PlayerColorId is 1-based (BLUE=1..ORANGE=8); the scenario file stores 0-7.
            # Writing the raw id gave ORANGE an invalid index 8 and crashed the game.
            cv = int(getattr(color, "value", color))
            p.color = max(0, min(7, cv - 1))
        if age is not None:
            p.starting_age = age
        return p

    def players(self, n):
        self.pm.active_players = n

    def diplomacy(self, a, b, state):
        self.pm.players[a].set_player_diplomacy(b, state)
        self.pm.players[b].set_player_diplomacy(a, state)

    def camera(self, pid, x, y):
        if pid == 1:
            self._home_cam = (int(x), int(y))
        p = self.pm.players[pid]
        p.initial_camera_x, p.initial_camera_y = x, y

    # ------------------------------------------------------------ units
    def unit(self, pid, const, x, y, rot=0.0, name=None):
        cid = const.ID if hasattr(const, "ID") else int(const)
        x = max(1, min(self.size - 2, x))     # keep every object inside the map
        y = max(1, min(self.size - 2, y))
        u = self.um.add_unit(pid, cid, x + 0.5, y + 0.5, rotation=rot)
        if const in SHIPS or const in (B.DOCK, B.HARBOR):
            self._ship_units.append((x, y))
        else:
            self._land_units.append((x, y, FOOT.get(const, 0)))
        if name:
            self.rename(pid, u, name)
        return u

    def group(self, pid, const, n, cx, cy, cols=None, spacing=1.2):
        cols = cols or max(1, int(math.sqrt(n) + 0.5))
        out = []
        for i in range(n):
            out.append(self.unit(pid, const, cx + (i % cols) * spacing - cols * spacing / 2,
                                 cy + (i // cols) * spacing))
        return out

    def ring_walls(self, pid, cx, cy, r, wall=B.STONE_WALL, gaps=()):
        """Approximate circular wall, leaving gap angles (degrees) open."""
        seen = set()
        for a in range(0, 360, 2):
            if any(abs(((a - g + 180) % 360) - 180) < 12 for g in gaps):
                continue
            x = round(cx + r * math.cos(math.radians(a)))
            y = round(cy + r * math.sin(math.radians(a)))
            if (x, y) not in seen:
                seen.add((x, y))
                self.unit(pid, wall, x, y)

    def rename(self, pid, unit, name):
        """Rename a placed unit at scenario start (custom hero names)."""
        if not hasattr(self, "_rename_trigger"):
            self._rename_trigger = self.tm.add_trigger("Setup: names")
        self._rename_trigger.new_effect.change_object_name(
            source_player=pid, message=name, selected_object_ids=[unit.reference_id])
        self.heroes[name] = (pid, unit)

    # ------------------------------------------------------------ triggers
    def trig(self, name, **kw):
        return self.tm.add_trigger(name, **kw)

    def _portrait(self, who):
        """Unit type id whose portrait is shown next to a line of dialogue."""
        if who is None:
            return None
        if isinstance(who, int):
            return who
        if hasattr(who, "ID"):
            return who.ID
        if who in self.heroes:
            return self.heroes[who][1].unit_const
        return PORTRAITS.get(who)

    def _cam_move(self, trig, x, y):
        trig.new_effect.create_object(
            source_player=1, object_list_unit_id=O.MAP_REVEALER.ID,
            location_x=int(x), location_y=int(y)
        )

    def line(self, trig, who, text, secs=None, cam=None, panel=PanelLocation.TOP, named=True):
        """One line of narration/dialogue: portrait + speaker name, optional map reveal at cam.
        named=False shows the portrait without a 'Name:' prefix (narration about someone)."""
        speaker = who if isinstance(who, str) else "Narrator"
        vo_hash = _hashlib.md5(f"{speaker}|{text}".encode("utf-8")).hexdigest()[:10]
        vo_name = f"sw_vo_{vo_hash}"
        VO_REGISTRY[vo_name] = (speaker, text)
        base_secs = secs or max(7, min(16, len(text) // 13 + 3))
        vo_dur = VO_DURATIONS.get(vo_name, 0)
        secs = max(base_secs, int(math.ceil(vo_dur)) + 2) if vo_dur else base_secs
        msg = f"{who}: {text}" if (isinstance(who, str) and named) else text
        kw = {"sound_name": vo_name, "play_sound": 1}
        pid = self._portrait(who)
        if pid is not None:
            kw["object_list_unit_id"] = pid
        trig.new_effect.display_instructions(source_player=1, message=msg, display_time=secs,
                                             instruction_panel_position=panel, **kw)
        trig.new_effect.send_chat(source_player=1, message=msg)
        if cam is not None:
            self._cam_move(trig, cam[0], cam[1])
        return secs

    def story(self, lines, start_delay=1, gap=None, first_trigger_name="Story", enabled=True):
        """Chain of timed narration lines. Each line is a string (narrator) or a tuple
        (speaker, text) / (speaker, text, (cam_x, cam_y)). Returns (first, last) trigger."""
        first = prev = None
        prev_secs = start_delay
        for i, item in enumerate(lines):
            if isinstance(item, str):
                who, text, cam = None, item, None
            else:
                who, text = item[0], item[1]
                cam = item[2] if len(item) > 2 else None
            t = self.trig(f"{first_trigger_name} {i + 1}", enabled=(i == 0 and enabled))
            t.new_condition.timer(timer=start_delay if i == 0 else prev_secs)
            prev_secs = self.line(t, who, text, gap, cam)
            if prev is not None:
                prev.new_effect.activate_trigger(trigger_id=t.trigger_id)
            else:
                first = t
            prev = t
        return first, prev

    def mood(self, color_mood, after=0, name="Setup: atmosphere"):
        """Change lighting (night raids, monsoon, twilight)."""
        t = self.trig(name)
        t.new_condition.timer(timer=after)
        t.new_effect.change_color_mood(quantity=3, color_mood=color_mood)
        return t

    def hero_setup(self, name, hp=0, attack=0, melee_armor=0, pierce_armor=0, desc=None):
        """Give a named hero extra strength and a lore description."""
        pid, u = self.heroes[name]
        if not hasattr(self, "_hero_trigger"):
            self._hero_trigger = self.tm.add_trigger("Setup: heroes")
        t = self._hero_trigger
        ids = [u.reference_id]
        if hp:
            t.new_effect.change_object_hp(quantity=hp, source_player=pid, operation=Operation.ADD,
                                          selected_object_ids=ids)
            t.new_effect.heal_object(source_player=pid, selected_object_ids=ids)
        if attack:
            t.new_effect.change_object_attack(armour_attack_quantity=attack, armour_attack_class=4,
                                              source_player=pid, operation=Operation.ADD,
                                              selected_object_ids=ids)
        if melee_armor:
            t.new_effect.change_object_armor(armour_attack_quantity=melee_armor, armour_attack_class=4,
                                             source_player=pid, operation=Operation.ADD,
                                             selected_object_ids=ids)
        if pierce_armor:
            t.new_effect.change_object_armor(armour_attack_quantity=pierce_armor, armour_attack_class=3,
                                             source_player=pid, operation=Operation.ADD,
                                             selected_object_ids=ids)
        if desc:
            # Descriptions apply per unit type: only use them when the hero's type is unique.
            same = [x for x in self.um.get_all_units()
                    if x.player == pid and x.unit_const == u.unit_const]
            if len(same) == 1:
                t.new_effect.change_object_description(object_list_unit_id=u.unit_const,
                                                       source_player=pid, message=desc)

    def reveal(self, trig, points, big=False):
        """Bahirji Naik's intelligence: permanently reveal map areas for the player."""
        const = O.MAP_REVEALER_GIANT if big else O.MAP_REVEALER
        for x, y in points:
            trig.new_effect.create_object(object_list_unit_id=const.ID, source_player=1,
                                          location_x=int(x), location_y=int(y))

    def objective(self, name, text, order, enabled=True):
        return self.trig(name, display_as_objective=True, description=text,
                         short_description=text, display_on_screen=True,
                         description_order=order, enabled=enabled)

    def say(self, trig, msg, time=10):
        trig.new_effect.display_instructions(
            source_player=1, message=msg, display_time=time,
            instruction_panel_position=PanelLocation.TOP)
        trig.new_effect.send_chat(source_player=1, message=msg)

    def victory(self, trig, msg=None, epilogue=None):
        """Declare victory, optionally after a chain of epilogue lines (post-mission narration)."""
        lines = ([msg] if msg else []) + list(epilogue or [])
        if not lines:
            trig.new_effect.declare_victory(source_player=1, enabled=1)
            return trig
        self._chain_ix += 1
        first, last = self.story(lines, start_delay=1, first_trigger_name=f"Epilogue {self._chain_ix}",
                                 enabled=False)
        trig.new_effect.activate_trigger(trigger_id=first.trigger_id)
        fin = self.trig(f"Epilogue {self._chain_ix} end", enabled=False)
        fin.new_condition.timer(timer=8)
        fin.new_effect.declare_victory(source_player=1, enabled=1)
        last.new_effect.activate_trigger(trigger_id=fin.trigger_id)
        return fin

    def hero_loss(self, hero, enemy_pid, who):
        t = self.trig(f"Loss: {who} has fallen")
        t.new_condition.destroy_object(unit_object=hero.reference_id)
        self.say(t, f"{who} has fallen. Swarajya cannot survive this loss.")
        t.new_effect.declare_victory(source_player=enemy_pid, enabled=1)
        return t

    def spawn(self, trig, pid, const, n, x, y):
        cid = const.ID if hasattr(const, "ID") else int(const)
        for i in range(n):
            trig.new_effect.create_object(object_list_unit_id=cid, source_player=pid,
                                          location_x=x + (i % 4), location_y=y + (i // 4))

    def attack_move(self, trig, pid, area, tx, ty):
        x1, y1, x2, y2 = area
        trig.new_effect.task_object(source_player=pid, area_x1=x1, area_y1=y1,
                                    area_x2=x2, area_y2=y2, location_x=tx, location_y=ty,
                                    action_type=ActionType.ATTACK_MOVE)

    def wave(self, name, pid, after, comp, sx, sy, tx, ty, enabled=True, msg=None,
             repeat_every=None):
        """Spawn a war band at (sx,sy) after `after` seconds and send it to (tx,ty)."""
        gate = None
        if repeat_every and after > repeat_every:
            gate = self.trig(name + " (start)", enabled=enabled)
            gate.new_condition.timer(timer=after - repeat_every)
            enabled = False
        t = self.trig(name, enabled=enabled, looping=bool(repeat_every))
        t.new_condition.timer(timer=after if not repeat_every else repeat_every)
        if gate is not None:
            gate.new_effect.activate_trigger(trigger_id=t.trigger_id)
        off = 0
        for const, n in comp:
            self.spawn(t, pid, const, n, sx, sy + off)
            off += (n + 3) // 4 + 1
        if msg:
            self.say(t, msg, 8)
        go = self.trig(name + " (march)", enabled=False, looping=bool(repeat_every))
        go.new_condition.timer(timer=2)
        self.attack_move(go, pid, (sx - 2, sy - 2, sx + 6, sy + off + 2), tx, ty)
        t.new_effect.activate_trigger(trigger_id=go.trigger_id)
        if repeat_every:
            go.new_effect.deactivate_trigger(trigger_id=go.trigger_id)
        return gate if gate is not None else t

    def area_task(self, trig, pid, area, tx, ty, action=ActionType.ATTACK_MOVE):
        x1, y1, x2, y2 = area
        trig.new_effect.task_object(source_player=pid, area_x1=x1, area_y1=y1,
                                    area_x2=x2, area_y2=y2, location_x=tx,
                                    location_y=ty, action_type=action)

    def gold(self, trig, pid, amount):
        trig.new_effect.modify_resource(quantity=amount, tribute_list=Attribute.GOLD_STORAGE,
                                        source_player=pid, operation=Operation.ADD)

    def resource(self, trig, pid, attr, amount):
        trig.new_effect.modify_resource(quantity=amount, tribute_list=attr,
                                        source_player=pid, operation=Operation.ADD)

    def dead(self, trig, unit):
        trig.new_condition.destroy_object(unit_object=unit.reference_id)

    def cleared(self, trig, pid, area, otype=ObjectType.MILITARY, const=None):
        """Condition: player pid has no objects of otype (or const) left in area."""
        x1, y1, x2, y2 = area
        kw = {"object_list": const.ID} if const is not None else {"object_type": otype}
        trig.new_condition.objects_in_area(quantity=1, source_player=pid, area_x1=x1,
                                           area_y1=y1, area_x2=x2, area_y2=y2,
                                           inverted=1, **kw)

    def timer_display(self, trig, seconds, msg, slot=0):
        trig.new_effect.display_timer(display_time=seconds, time_unit=TimeUnit.MINUTES_AND_SECONDS,
                                      timer=slot, message=msg)

    def set_var(self, trig, var, value):
        trig.new_effect.change_variable(quantity=value, operation=Operation.SET, variable=var)

    def need_var(self, trig, var, value=1):
        trig.new_condition.variable_value(quantity=value, variable=var, comparison=Comparison.EQUAL)

    def hp_below(self, trig, unit, hp):
        trig.new_condition.object_hp(quantity=hp, unit_object=unit.reference_id,
                                     comparison=Comparison.LESS)

    def set_hp(self, trig, pid, unit, hp):
        trig.new_effect.change_object_hp(quantity=hp, source_player=pid, operation=Operation.SET,
                                         selected_object_ids=[unit.reference_id])

    def teleport(self, trig, pid, unit, x, y):
        trig.new_effect.teleport_object(source_player=pid, location_x=x, location_y=y,
                                        selected_object_ids=[unit.reference_id])

    def teleport_area(self, trig, pid, area, x, y):
        x1, y1, x2, y2 = area
        trig.new_effect.teleport_object(source_player=pid, location_x=x, location_y=y,
                                        area_x1=x1, area_y1=y1, area_x2=x2, area_y2=y2,
                                        object_type=ObjectType.MILITARY)

    def give(self, trig, src, dst, unit):
        trig.new_effect.change_ownership(source_player=src, target_player=dst,
                                         selected_object_ids=[unit.reference_id])

    def kill(self, trig, pid, unit):
        trig.new_effect.kill_object(source_player=pid, selected_object_ids=[unit.reference_id])

    def move(self, trig, pid, unit, x, y):
        trig.new_effect.task_object(source_player=pid, location_x=x, location_y=y,
                                    selected_object_ids=[unit.reference_id],
                                    action_type=ActionType.MOVE)

    def holding_cell(self, x=2, y=2):
        """A one-tile island in a moat: safe storage for teleported heroes."""
        self.rect(T.WATER_DEEP, x - 2, y - 2, x + 3, y + 3)
        self.unit(0, O.FLAG_A, x, y)
        return (x, y)

    def present(self, trig, pid, area, const=None, otype=None, qty=1):
        x1, y1, x2, y2 = area
        kw = {}
        if const is not None:
            kw["object_list"] = const.ID if hasattr(const, "ID") else int(const)
        if otype is not None:
            kw["object_type"] = otype
        trig.new_condition.objects_in_area(quantity=qty, source_player=pid, area_x1=x1,
                                           area_y1=y1, area_x2=x2, area_y2=y2, **kw)

    def arrive(self, trig, unit, area):
        x1, y1, x2, y2 = area
        trig.new_condition.bring_object_to_area(unit_object=unit.reference_id, area_x1=x1,
                                                area_y1=y1, area_x2=x2, area_y2=y2)

    def handover(self, trig, src, dst, area, otype=None):
        x1, y1, x2, y2 = area
        kw = {"object_type": otype} if otype else {}
        trig.new_effect.change_ownership(source_player=src, target_player=dst, area_x1=x1,
                                         area_y1=y1, area_x2=x2, area_y2=y2, **kw)

    def set_diplo(self, trig, a, b, state):
        trig.new_effect.change_diplomacy(diplomacy=state, source_player=a, target_player=b)
        trig.new_effect.change_diplomacy(diplomacy=state, source_player=b, target_player=a)

    def chain(self, a, b):
        a.new_effect.activate_trigger(trigger_id=b.trigger_id)

    # ------------------------------------------------------------ messages
    def texts(self, instructions, history, hints, victory, loss, scouts=""):
        mm = self.s.message_manager
        mm.instructions = instructions
        mm.history = history
        mm.hints = hints
        mm.victory = victory
        mm.loss = loss
        mm.scouts = scouts

    # ------------------------------------------------------------ finish
    def finish(self, outdir):
        # Clear impassable terrain beneath land units and buildings
        land = self.base if self.base not in WATER | FOREST else T.GRASS_1
        for x, y, r in self._land_units:
            for dx in range(-r - 1, r + 2):
                for dy in range(-r - 1, r + 2):
                    t = self.tile(x + dx, y + dy)
                    if t is not None and (t.terrain_id in WATER or t.terrain_id in FOREST):
                        t.terrain_id = T.DIRT_3 if r else land
        for x, y in self._ship_units:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    t = self.tile(x + dx, y + dy)
                    if t is not None and t.terrain_id not in WATER:
                        t.terrain_id = T.WATER_MEDIUM
                        t.elevation = 0
        # Water must be flat
        for t in self.s.map_manager.terrain:
            if t.terrain_id in WATER or t.terrain_id in (T.SHALLOWS, T.BEACH):
                t.elevation = 0
        self.smooth()
        # Populate safe Gaia resource clusters (Gold, Stone, Forage, Deer) on open land
        occupied = set()
        for u in self.um.get_all_units():
            ux, uy = int(u.x), int(u.y)
            for dx in range(-5, 6):
                for dy in range(-5, 6):
                    occupied.add((ux + dx, uy + dy))
        for rtype, count, cluster in (
            (O.GOLD_MINE, 4, 5),
            (O.STONE_MINE, 3, 4),
            (O.FORAGE_BUSH, 3, 6),
            (U.DEER, 3, 4),
        ):
            placed = 0
            for _ in range(200):
                if placed >= count:
                    break
                rx = self.rng.randint(14, self.size - 16)
                ry = self.rng.randint(14, self.size - 16)
                if (rx, ry) in occupied:
                    continue
                t0 = self.tile(rx, ry)
                if t0 is None or t0.terrain_id in WATER or t0.terrain_id in FOREST or t0.elevation > 2:
                    continue
                ok = True
                pts = []
                for k in range(cluster):
                    px, py = rx + (k % 3), ry + (k // 3)
                    tk = self.tile(px, py)
                    if tk is None or (px, py) in occupied or tk.terrain_id in WATER or tk.terrain_id in FOREST:
                        ok = False
                        break
                    pts.append((px, py))
                if not ok:
                    continue
                cid = rtype.ID if hasattr(rtype, "ID") else int(rtype)
                for px, py in pts:
                    self.um.add_unit(0, cid, px + 0.5, py + 0.5, rotation=0.0)
                    for dx in range(-4, 5):
                        for dy in range(-4, 5):
                            occupied.add((px + dx, py + dy))
                placed += 1
        # Put pre-placed AI units into Defensive Stance at t=1 so they hold their posts
        # without requiring a custom AI script file that blocks scenario load/teardown.
        hold_trig = self.trig("AI Defensive Stance", enabled=True)
        hold_trig.new_condition.timer(timer=1)
        for pid in range(2, self.pm.active_players + 1):
            hold_trig.new_effect.change_object_stance(
                source_player=pid,
                attack_stance=AttackStance.DEFENSIVE_STANCE,
            )
        # Sanitize unused effect fields to -1 to match official DE campaign binaries
        from AoE2ScenarioParser.datasets import effects as _asp_effects
        for trig in self.tm.triggers:
            for eff in trig.effects:
                used = _asp_effects.attributes.get(eff.effect_type, ())
                if "operation" not in used:
                    eff.operation = -1
                if "variable" not in used:
                    eff.variable = -1
        # Campaign naming: final filename + chapter heading on the briefing screen
        if self.filename in RENAME:
            new, heading = RENAME[self.filename]
            self.filename = new
            mm = self.s.message_manager
            mm.instructions = heading + "\n\n" + (mm.instructions or "")
        path = f"{outdir}/{self.filename}"
        self.s.write_to_file(path)
        return path
