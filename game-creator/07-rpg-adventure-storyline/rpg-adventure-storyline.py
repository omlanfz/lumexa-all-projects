"""
Starlight Relic - RPG Adventure Storyline
Lumexa Game Creator Path - Course 03, Project 07

A top-down RPG-lite adventure: explore a village, talk to two NPCs whose
dialogue advances a branching storyline, collect and use an inventory item,
complete a simple quest, and reach a clear win/ending state. Story progress
is tracked by an explicit QuestManager state machine and can be saved to /
loaded from a checkpoint file (F5 to save, F9 to load).

This is a single-file merge of the original multi-module project:
  settings.py, map_data.py, quest.py, dialogue.py, inventory.py,
  entities/entity.py, entities/item.py, entities/npc.py, entities/player.py,
  world.py, ui.py, game_state.py, main.py
All internal imports between those modules have been removed since
everything now lives in this one file. External imports (pygame, sys, json)
are kept below.
"""
import sys
import json
from enum import Enum, auto

import pygame


# =====================================================================
# SETTINGS / CONSTANTS  (from settings.py)
# =====================================================================
TITLE = "Starlight Relic"

TILE_SIZE = 48
MAP_COLS = 16
MAP_ROWS = 11
SCREEN_WIDTH = TILE_SIZE * MAP_COLS
SCREEN_HEIGHT = TILE_SIZE * MAP_ROWS + 140  # extra room for dialogue box / HUD
FPS = 60

PLAYER_SPEED = 180  # pixels per second

# ---- Colors ----
BG_COLOR = (12, 14, 30)
GRASS_COLOR = (34, 82, 52)
PATH_COLOR = (120, 108, 78)
WALL_COLOR = (58, 62, 90)
WATER_COLOR = (40, 90, 140)
PLAYER_COLOR = (80, 200, 255)
NPC_COLOR_ELDER = (230, 190, 90)
NPC_COLOR_GUARD = (200, 100, 100)
ITEM_COLOR = (255, 215, 90)
RELIC_COLOR = (200, 140, 255)
WHITE = (235, 235, 240)
BLACK = (10, 10, 14)
PANEL_COLOR = (20, 22, 44)
ACCENT_COLOR = (90, 220, 255)
QUEST_COLOR = (120, 230, 150)

FONT_NAME = "consolas"
FONT_SIZE_SMALL = 18
FONT_SIZE_MEDIUM = 22
FONT_SIZE_LARGE = 34


# =====================================================================
# MAP DATA  (from map_data.py)
# =====================================================================
# Map data for Starlight Relic.
# Data-driven world layout: a grid of characters converted into tiles/objects
# by the World loader, following the data-driven design pattern
# taught in Course 03, Lesson 02 (Level Design Theory and Practice).
#
# Legend:
#   '#' = wall (impassable)
#   '.' = grass (walkable)
#   'P' = stone path (walkable, purely cosmetic difference from grass)
#   '~' = water (impassable)
#   'S' = player start position
#   'E' = Elder NPC (gives the main quest)
#   'G' = Guard NPC (blocks the corridor to the relic room until the quest
#         item has been delivered - see Guard.blocking below)
#   'I' = Ancient Key item on the ground (inventory pickup)
#   'R' = the Starlight Relic (final quest item / triggers the win state)
#
# All rows are exactly MAP_COLS (16) characters wide and there are exactly
# MAP_ROWS (11) rows, matching the settings above.
WORLD_MAP = [
    "################",
    "#S.....P.......#",
    "#.....PP.......#",
    "#.....P....E...#",
    "#~~...P........#",
    "#~~...P........#",
    "#.....P..I.....#",
    "#.....P........#",
    "#.....P........#",
    "#.....G......R.#",
    "################",
]


# =====================================================================
# QUEST SYSTEM  (from quest.py)
# =====================================================================
class QuestStage(Enum):
    NOT_STARTED = auto()
    ACTIVE = auto()          # quest accepted, key not yet found
    KEY_FOUND = auto()       # key found, guard not yet convinced
    GUARD_PASSED = auto()    # guard convinced, relic not yet retrieved
    COMPLETE = auto()        # relic retrieved - win condition met


class QuestManager:
    """Tracks the single main quest's progress and exposes simple flags/methods
    that other modules (NPCs, World, Game) read to make decisions.
    """

    def __init__(self):
        self.stage = QuestStage.NOT_STARTED
        self._guard_passed_flag = False

    # --- story progress transitions -------------------------------------
    def start_quest(self):
        if self.stage == QuestStage.NOT_STARTED:
            self.stage = QuestStage.ACTIVE

    def collect_key(self):
        if self.stage == QuestStage.ACTIVE:
            self.stage = QuestStage.KEY_FOUND

    @property
    def guard_passed(self):
        return self._guard_passed_flag

    @guard_passed.setter
    def guard_passed(self, value):
        self._guard_passed_flag = value
        if value and self.stage == QuestStage.KEY_FOUND:
            self.stage = QuestStage.GUARD_PASSED

    def collect_relic(self):
        if self.stage == QuestStage.GUARD_PASSED:
            self.stage = QuestStage.COMPLETE

    # --- read-only convenience properties used by NPCs/UI ----------------
    @property
    def has_key(self):
        return self.stage.value >= QuestStage.KEY_FOUND.value

    @property
    def is_complete(self):
        return self.stage == QuestStage.COMPLETE

    def objective_text(self):
        """A single human-readable line describing what the player should do
        next - shown in the HUD, giving constant visual guidance (Lesson 5)."""
        return {
            QuestStage.NOT_STARTED: "Find Elder Mira in the village.",
            QuestStage.ACTIVE: "Find the Ancient Key.",
            QuestStage.KEY_FOUND: "Show the key to Guard Talos.",
            QuestStage.GUARD_PASSED: "Retrieve the Starlight Relic from the vault.",
            QuestStage.COMPLETE: "Quest complete! You saved the village.",
        }[self.stage]


# =====================================================================
# BASE ENTITY  (from entities/entity.py)
# =====================================================================
class Entity:
    """Base class for any object placed in the game world.

    Follows the Course 03 Lesson 03 architecture pattern: shared position/rect
    and update/draw hooks live here; subclasses override only what differs.
    """

    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.active = True

    def update(self, dt, world):
        pass

    def draw(self, surface, camera_offset=(0, 0)):
        draw_rect = self.rect.move(camera_offset)
        pygame.draw.rect(surface, self.color, draw_rect, border_radius=4)


# =====================================================================
# ITEM ENTITIES  (from entities/item.py)
# =====================================================================
class Item(Entity):
    """A collectible item on the ground. `item_id` is used by Inventory/Quest."""

    def __init__(self, x, y, item_id, color):
        size = TILE_SIZE - 22
        super().__init__(x, y, size, size, color)
        self.item_id = item_id

    def draw(self, surface, camera_offset=(0, 0)):
        cx, cy = self.rect.move(camera_offset).center
        pygame.draw.circle(surface, self.color, (cx, cy), self.rect.width // 2)
        pygame.draw.circle(surface, WHITE, (cx, cy), self.rect.width // 2, width=2)


class AncientKey(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "ancient_key", ITEM_COLOR)


class StarlightRelic(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "starlight_relic", RELIC_COLOR)


# =====================================================================
# NPC ENTITIES  (from entities/npc.py)
# =====================================================================
class NPC(Entity):
    """Base NPC: has a name and a dialogue tree (see DialogueBox below for format)."""

    def __init__(self, x, y, color, name, dialogue_tree):
        size = TILE_SIZE - 14
        super().__init__(x, y, size, size, color)
        self.name = name
        self.dialogue_tree = dialogue_tree

    def draw(self, surface, camera_offset=(0, 0)):
        super().draw(surface, camera_offset)
        pygame.draw.rect(surface, WHITE, self.rect.move(camera_offset), width=2, border_radius=4)


class Elder(NPC):
    """Gives the player the main quest: retrieve the Starlight Relic."""

    def __init__(self, x, y, quest_manager):
        tree = build_elder_dialogue(quest_manager)
        super().__init__(x, y, NPC_COLOR_ELDER, "Elder Mira", tree)


class Guard(NPC):
    """Blocks the corridor to the relic room until the quest is complete.

    While `blocking` is True, the Guard's rect is treated as an obstacle by
    the World's collision check, just like a wall tile.
    """

    def __init__(self, x, y, quest_manager):
        tree = build_guard_dialogue(quest_manager)
        super().__init__(x, y, NPC_COLOR_GUARD, "Guard Talos", tree)
        self.quest_manager = quest_manager

    @property
    def blocking(self):
        return not self.quest_manager.has_key


def build_elder_dialogue(quest_manager):
    """Returns a branching dialogue tree (a dict of node_id -> node data).
    Each node has 'text' and 'options': a list of (label, next_node_id, effect)
    tuples. `effect` is an optional callable applied when that option is chosen.
    """

    def start_quest():
        quest_manager.start_quest()

    return {
        "root": {
            "text": (
                "Elder Mira: Traveler! The Starlight Relic has been stolen "
                "from our shrine. Will you help us recover it?"
            ),
            "options": [
                ("Yes, I'll help.", "accept", start_quest),
                ("Tell me more first.", "lore", None),
                ("Not right now.", "decline", None),
            ],
        },
        "lore": {
            "text": (
                "Elder Mira: Long ago the Relic protected our village from the "
                "void between stars. Guard Talos holds the Ancient Key needed "
                "to reach the vault - find him, but he trusts no one without proof."
            ),
            "options": [
                ("I'll help.", "accept", start_quest),
                ("Not right now.", "decline", None),
            ],
        },
        "accept": {
            "text": (
                "Elder Mira: Thank you! Find the Ancient Key nearby, then show "
                "it to Guard Talos so he lets you through to the vault."
            ),
            "options": [("Understood.", "END", None)],
        },
        "decline": {
            "text": "Elder Mira: I understand. Return if you change your mind.",
            "options": [("Okay.", "END", None)],
        },
        "quest_active_reminder": {
            "text": "Elder Mira: Have you found the Ancient Key yet? Guard Talos guards the vault.",
            "options": [("I'll keep looking.", "END", None)],
        },
        "quest_complete": {
            "text": (
                "Elder Mira: You found the Starlight Relic! Our village is safe "
                "once more, thanks to you, traveler."
            ),
            "options": [("It was an honor.", "END", None)],
        },
    }


def build_guard_dialogue(quest_manager):
    def give_key_and_pass():
        quest_manager.guard_passed = True

    return {
        "root": {
            "text": "Guard Talos: Halt! None may pass to the vault without the Ancient Key.",
            "options": [("I don't have it yet.", "END", None)],
        },
        "has_key": {
            "text": "Guard Talos: Ah, you found the Key! Very well - the vault is yours to enter.",
            "options": [("Thank you.", "END", give_key_and_pass)],
        },
    }


# =====================================================================
# INVENTORY SYSTEM  (from inventory.py)
# =====================================================================
class Inventory:
    """A simple item-counting inventory, owned by the Player via composition."""

    def __init__(self):
        self.items = {}

    def add(self, item_id, amount=1):
        self.items[item_id] = self.items.get(item_id, 0) + amount

    def has(self, item_id):
        return self.items.get(item_id, 0) > 0

    def count(self, item_id):
        return self.items.get(item_id, 0)

    def remove(self, item_id, amount=1):
        if self.has(item_id):
            self.items[item_id] = max(0, self.items[item_id] - amount)

    def as_list(self):
        """Returns a readable list of (item_id, count) for HUD display."""
        return [(item_id, count) for item_id, count in self.items.items() if count > 0]


# =====================================================================
# PLAYER ENTITY  (from entities/player.py)
# =====================================================================
class Player(Entity):
    def __init__(self, x, y):
        size = TILE_SIZE - 14
        super().__init__(x, y, size, size, PLAYER_COLOR)
        self.speed = PLAYER_SPEED
        self.inventory = Inventory()
        self.facing = "down"

    def handle_input(self, keys, dt, world):
        dx = dy = 0.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
            self.facing = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
            self.facing = "right"
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
            self.facing = "up"
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1
            self.facing = "down"

        if dx and dy:
            dx *= 0.7071
            dy *= 0.7071

        move_x = dx * self.speed * dt
        move_y = dy * self.speed * dt

        self.rect.x += move_x
        if world.collides(self.rect):
            self.rect.x -= move_x

        self.rect.y += move_y
        if world.collides(self.rect):
            self.rect.y -= move_y

    def interaction_point(self):
        """Returns a small probe rect in front of the player, used to detect
        which NPC/item the player is trying to interact with."""
        probe_size = 20
        if self.facing == "left":
            return pygame.Rect(self.rect.left - probe_size, self.rect.centery - probe_size // 2, probe_size, probe_size)
        if self.facing == "right":
            return pygame.Rect(self.rect.right, self.rect.centery - probe_size // 2, probe_size, probe_size)
        if self.facing == "up":
            return pygame.Rect(self.rect.centerx - probe_size // 2, self.rect.top - probe_size, probe_size, probe_size)
        return pygame.Rect(self.rect.centerx - probe_size // 2, self.rect.bottom, probe_size, probe_size)

    def draw(self, surface, camera_offset=(0, 0)):
        super().draw(surface, camera_offset)
        # Small facing indicator so players can see their orientation clearly.
        cx, cy = self.rect.move(camera_offset).center
        marker_offsets = {"up": (0, -14), "down": (0, 14), "left": (-14, 0), "right": (14, 0)}
        ox, oy = marker_offsets[self.facing]
        pygame.draw.circle(surface, WHITE, (cx + ox, cy + oy), 4)


# =====================================================================
# DIALOGUE SYSTEM  (from dialogue.py)
# =====================================================================
# Tree format (see build_elder_dialogue / build_guard_dialogue above):
#     {
#         "node_id": {
#             "text": "...",
#             "options": [(label, next_node_id, effect_or_None), ...],
#         },
#         ...
#     }
# A next_node_id of "END" closes the dialogue box.
pygame.font.init()
_text_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_MEDIUM)
_name_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_MEDIUM, bold=True)
_option_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SMALL)


def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if font.size(trial)[0] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


class DialogueBox:
    """Manages an active conversation: current node, selected option, input."""

    def __init__(self):
        self.npc_name = ""
        self.tree = None
        self.node_id = None
        self.selected_index = 0
        self.active = False

    def start(self, npc_name, tree, start_node="root"):
        self.npc_name = npc_name
        self.tree = tree
        self.node_id = start_node if start_node in tree else "root"
        self.selected_index = 0
        self.active = True

    def current_node(self):
        return self.tree[self.node_id]

    def handle_event(self, event):
        """Returns True if the dialogue box consumed this event."""
        if not self.active:
            return False
        node = self.current_node()
        options = node["options"]

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_index = (self.selected_index - 1) % len(options)
                return True
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_index = (self.selected_index + 1) % len(options)
                return True
            if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_e):
                self._choose(options[self.selected_index])
                return True
            if pygame.K_1 <= event.key <= pygame.K_9:
                index = event.key - pygame.K_1
                if index < len(options):
                    self._choose(options[index])
                return True
        return True  # dialogue box swallows all input while active

    def _choose(self, option):
        label, next_node, effect = option
        if effect is not None:
            effect()
        if next_node == "END" or next_node not in self.tree:
            self.active = False
        else:
            self.node_id = next_node
            self.selected_index = 0

    def draw(self, surface):
        if not self.active:
            return
        node = self.current_node()
        box_height = 150
        box_rect = pygame.Rect(20, SCREEN_HEIGHT - box_height - 10, SCREEN_WIDTH - 40, box_height)
        pygame.draw.rect(surface, PANEL_COLOR, box_rect, border_radius=10)
        pygame.draw.rect(surface, ACCENT_COLOR, box_rect, width=2, border_radius=10)

        name_surface = _name_font.render(self.npc_name, True, ACCENT_COLOR)
        surface.blit(name_surface, (box_rect.x + 16, box_rect.y + 10))

        lines = wrap_text(node["text"], _text_font, box_rect.width - 32)
        for i, line in enumerate(lines[:2]):
            line_surface = _text_font.render(line, True, WHITE)
            surface.blit(line_surface, (box_rect.x + 16, box_rect.y + 40 + i * 24))

        option_y = box_rect.y + 40 + min(len(lines), 2) * 24 + 12
        for i, (label, _next, _effect) in enumerate(node["options"]):
            prefix = "> " if i == self.selected_index else "  "
            color = ACCENT_COLOR if i == self.selected_index else WHITE
            option_surface = _option_font.render(f"{prefix}{label}", True, color)
            surface.blit(option_surface, (box_rect.x + 16, option_y + i * 22))


# =====================================================================
# WORLD LOADER  (from world.py)
# =====================================================================
class World:
    """Converts WORLD_MAP into real game objects.

    Follows the data-driven level design pattern from Course 03, Lesson 02:
    the grid is pure data, and this one loader builds real entities from it.
    """

    def __init__(self, quest_manager):
        self.walls = []
        self.grass_tiles = []
        self.path_tiles = []
        self.water_tiles = []
        self.player_start = (TILE_SIZE * 1, TILE_SIZE * 1)
        self.npcs = []
        self.items = []
        self.quest_manager = quest_manager

        self._parse(WORLD_MAP)

    def _parse(self, grid):
        for row_index, row in enumerate(grid):
            for col_index, char in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

                if char == "#":
                    self.walls.append(rect)
                elif char == "~":
                    self.walls.append(rect)  # water is also impassable
                    self.water_tiles.append(rect)
                elif char == ".":
                    self.grass_tiles.append(rect)
                elif char == "P":
                    self.path_tiles.append(rect)
                elif char == "S":
                    self.grass_tiles.append(rect)
                    self.player_start = rect.center
                elif char == "E":
                    self.grass_tiles.append(rect)
                    self.npcs.append(Elder(x + 7, y + 7, self.quest_manager))
                elif char == "G":
                    self.grass_tiles.append(rect)
                    self.npcs.append(Guard(x + 7, y + 7, self.quest_manager))
                elif char == "I":
                    self.grass_tiles.append(rect)
                    self.items.append(AncientKey(x + 11, y + 11))
                elif char == "R":
                    self.grass_tiles.append(rect)
                    self.items.append(StarlightRelic(x + 11, y + 11))
                else:
                    self.grass_tiles.append(rect)

    def collides(self, rect):
        """Checks a rect against all impassable walls AND any currently
        blocking NPC (e.g., the Guard before the quest key is found)."""
        for wall in self.walls:
            if rect.colliderect(wall):
                return True
        for npc in self.npcs:
            if getattr(npc, "blocking", False) and rect.colliderect(npc.rect):
                return True
        return False

    def draw(self, surface, camera_offset=(0, 0)):
        for tile in self.grass_tiles:
            pygame.draw.rect(surface, GRASS_COLOR, tile.move(camera_offset))
        for tile in self.path_tiles:
            pygame.draw.rect(surface, PATH_COLOR, tile.move(camera_offset))
        for tile in self.water_tiles:
            pygame.draw.rect(surface, WATER_COLOR, tile.move(camera_offset))
        for wall in self.walls:
            if wall not in self.water_tiles:
                pygame.draw.rect(surface, WALL_COLOR, wall.move(camera_offset))
        for item in self.items:
            if item.active:
                item.draw(surface, camera_offset)
        for npc in self.npcs:
            npc.draw(surface, camera_offset)


# =====================================================================
# UI / HUD  (from ui.py)
# =====================================================================
pygame.font.init()
_hud_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SMALL)
_title_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_LARGE, bold=True)
_button_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_MEDIUM)


class Button:
    def __init__(self, rect, text, on_click):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.on_click = on_click
        self.hovered = False

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            pass  # keyboard confirm handled by caller for menus with one primary action

    def draw(self, surface):
        color = (70, 90, 160) if self.hovered else (46, 58, 110)
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, ACCENT_COLOR, self.rect, width=2, border_radius=10)
        label = _button_font.render(self.text, True, WHITE)
        surface.blit(label, (self.rect.centerx - label.get_width() // 2, self.rect.centery - label.get_height() // 2))


class HUD:
    """Persistent in-game overlay: quest objective and inventory contents."""

    def draw(self, surface, quest_manager, inventory):
        panel_rect = pygame.Rect(0, SCREEN_HEIGHT - 140, SCREEN_WIDTH, 140)
        pygame.draw.rect(surface, PANEL_COLOR, panel_rect)
        pygame.draw.rect(surface, ACCENT_COLOR, panel_rect, width=2)

        objective_label = _hud_font.render(f"Objective: {quest_manager.objective_text()}", True, QUEST_COLOR)
        surface.blit(objective_label, (16, panel_rect.y + 10))

        items = inventory.as_list()
        item_text = "Inventory: " + (", ".join(f"{name} x{count}" for name, count in items) if items else "empty")
        item_label = _hud_font.render(item_text, True, WHITE)
        surface.blit(item_label, (16, panel_rect.y + 34))

        hint_label = _hud_font.render(
            "Move: WASD/Arrows   Interact: E / Space   (near an NPC or item)",
            True, WHITE,
        )
        surface.blit(hint_label, (16, panel_rect.y + 58))


def draw_title_screen(surface, on_start, on_quit, mouse_pos, events):
    surface.fill(BG_COLOR)
    title = _title_font.render(TITLE, True, ACCENT_COLOR)
    surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

    subtitle = _button_font.render("An RPG Adventure - Lumexa Game Creator Path", True, WHITE)
    surface.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 160))

    start_button = Button((SCREEN_WIDTH // 2 - 110, 260, 220, 50), "Start Adventure", on_start)
    quit_button = Button((SCREEN_WIDTH // 2 - 110, 330, 220, 50), "Quit", on_quit)
    for button in (start_button, quit_button):
        button.update(mouse_pos)
        for event in events:
            button.handle_event(event)
        button.draw(surface)


def draw_win_screen(surface, on_restart, mouse_pos, events):
    surface.fill(BG_COLOR)
    title = _title_font.render("Quest Complete!", True, QUEST_COLOR)
    surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 140))
    msg = _button_font.render(
        "You recovered the Starlight Relic and saved the village.", True, WHITE,
    )
    surface.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 200))

    restart_button = Button((SCREEN_WIDTH // 2 - 110, 280, 220, 50), "Play Again", on_restart)
    restart_button.update(mouse_pos)
    for event in events:
        restart_button.handle_event(event)
    restart_button.draw(surface)


# =====================================================================
# GAME STATE MACHINE  (from game_state.py)
# =====================================================================
class AppState(Enum):
    TITLE = auto()
    EXPLORING = auto()
    DIALOGUE = auto()
    WIN = auto()


class GameStateMachine:
    ALLOWED_TRANSITIONS = {
        AppState.TITLE: {AppState.EXPLORING},
        AppState.EXPLORING: {AppState.DIALOGUE, AppState.WIN, AppState.TITLE},
        AppState.DIALOGUE: {AppState.EXPLORING},
        AppState.WIN: {AppState.TITLE, AppState.EXPLORING},
    }

    def __init__(self, initial=AppState.TITLE):
        self.state = initial

    def change_state(self, new_state):
        if new_state in self.ALLOWED_TRANSITIONS.get(self.state, set()):
            self.state = new_state
            return True
        return False

    def is_in(self, *states):
        return self.state in states


# =====================================================================
# MAIN GAME CLASS  (from main.py)
# =====================================================================
SAVE_FILE = "starlight_relic_save.json"


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.fsm = GameStateMachine()
        self.hud = HUD()
        self.dialogue_box = DialogueBox()
        self.quest_manager = None
        self.world = None
        self.player = None
        self._new_world()

    # -----------------------------------------------------------------
    def _new_world(self):
        self.quest_manager = QuestManager()
        self.world = World(self.quest_manager)
        self.player = Player(*self.world.player_start)

    def start_game(self):
        self._new_world()
        self.fsm.change_state(AppState.EXPLORING)

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def return_to_title(self):
        self.fsm.change_state(AppState.TITLE)

    # -----------------------------------------------------------------
    def save_game(self):
        data = {
            "quest_stage": self.quest_manager.stage.name,
            "guard_passed": self.quest_manager.guard_passed,
            "inventory": self.quest_manager and self.player.inventory.items,
            "player_pos": [self.player.rect.x, self.player.rect.y],
            "items_collected": [item.item_id for item in self.world.items if not item.active],
        }
        try:
            with open(SAVE_FILE, "w") as f:
                json.dump(data, f)
            print("Game saved.")
        except OSError as e:
            print(f"Could not save game: {e}")

    def load_game(self):
        try:
            with open(SAVE_FILE) as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError):
            print("No valid save file found.")
            return

        self._new_world()
        self.quest_manager.stage = QuestStage[data["quest_stage"]]
        self.quest_manager.guard_passed = data["guard_passed"]
        self.player.inventory.items = data["inventory"]
        self.player.rect.x, self.player.rect.y = data["player_pos"]
        for item_id in data["items_collected"]:
            for item in self.world.items:
                if item.item_id == item_id:
                    item.active = False
        self.fsm.change_state(AppState.EXPLORING)
        print("Game loaded.")

    # -----------------------------------------------------------------
    def _nearby_npc(self):
        probe = self.player.interaction_point()
        for npc in self.world.npcs:
            if probe.colliderect(npc.rect):
                return npc
        return None

    def _try_interact(self):
        npc = self._nearby_npc()
        if npc is None:
            return

        start_node = "root"
        if npc.name == "Elder Mira":
            if self.quest_manager.is_complete:
                start_node = "quest_complete"
            elif self.quest_manager.stage != QuestStage.NOT_STARTED:
                start_node = "quest_active_reminder"
        elif npc.name == "Guard Talos":
            start_node = "has_key" if self.quest_manager.has_key else "root"

        self.dialogue_box.start(npc.name, npc.dialogue_tree, start_node)
        self.fsm.change_state(AppState.DIALOGUE)

    def _try_pickup(self):
        for item in self.world.items:
            if not item.active:
                continue
            if not self.player.rect.colliderect(item.rect):
                continue
            if item.item_id == "ancient_key":
                item.active = False
                self.player.inventory.add("Ancient Key")
                self.quest_manager.collect_key()
            elif item.item_id == "starlight_relic":
                if self.quest_manager.guard_passed:
                    item.active = False
                    self.player.inventory.add("Starlight Relic")
                    self.quest_manager.collect_relic()
                    self.fsm.change_state(AppState.WIN)

    # -----------------------------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F5:
                self.save_game()
            elif event.key == pygame.K_F9:
                self.load_game()

        if self.fsm.is_in(AppState.DIALOGUE):
            consumed = self.dialogue_box.handle_event(event)
            if not self.dialogue_box.active and consumed:
                self.fsm.change_state(AppState.EXPLORING)
            return

        if self.fsm.is_in(AppState.EXPLORING):
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_e, pygame.K_RETURN):
                self._try_interact()

    def update(self, dt):
        if self.fsm.is_in(AppState.EXPLORING):
            keys = pygame.key.get_pressed()
            self.player.handle_input(keys, dt, self.world)
            self._try_pickup()

    def draw(self):
        if self.fsm.is_in(AppState.TITLE):
            mouse_pos = pygame.mouse.get_pos()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit_game()
            draw_title_screen(self.screen, self.start_game, self.quit_game, mouse_pos, events)
            for event in events:
                self.handle_event(event)
            return

        if self.fsm.is_in(AppState.WIN):
            mouse_pos = pygame.mouse.get_pos()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit_game()
            draw_win_screen(self.screen, self.start_game, mouse_pos, events)
            return

        self.screen.fill(BG_COLOR)
        self.world.draw(self.screen)
        self.player.draw(self.screen)
        self.hud.draw(self.screen, self.quest_manager, self.player.inventory)
        self.dialogue_box.draw(self.screen)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0

            if self.fsm.is_in(AppState.TITLE, AppState.WIN):
                self.draw()
                pygame.display.flip()
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.handle_event(event)

            self.update(dt)
            self.draw()
            pygame.display.flip()

        pygame.quit()
        sys.exit()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
