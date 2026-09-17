"""
Nova Drift - Published Portfolio Game
Lumexa Game Creator Path - Course 03, Project 09 (Capstone)

A side-scrolling platformer combining every lesson of the course: clean OOP
architecture (Lesson 03), data-driven level design across 3 levels (Lesson
02), a polished title/UI/HUD (Lesson 05), tuned difficulty and a full
menu -> playing -> win/lose -> restart state machine (Lessons 01, 03, 06),
and performance-conscious code including object pooling for popups
(Lesson 07) and a final "juice" polish pass (Lesson 08).

Optional sound effects are loaded defensively - if no sound files are
present (which is the case in this environment), the game runs silently
without crashing, per Lesson 08's edge-case discipline.

This file is a single self-contained merge of the original multi-file
project (settings.py, level_data.py, juice.py, entities/*.py, level.py,
ui.py, game_state.py, main.py) - all internal imports between those
modules have been removed since everything now lives in one namespace.
"""
import sys
import math
import random
from enum import Enum, auto

import pygame

# =====================================================================
# SETTINGS / CONSTANTS  (from settings.py)
# =====================================================================
TITLE = "Nova Drift"

TILE_SIZE = 40
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
FPS = 60

GRAVITY = 1500.0
JUMP_VELOCITY = -620.0
PLAYER_MOVE_SPEED = 260.0
MAX_FALL_SPEED = 900.0
PLAYER_MAX_HEALTH = 3
INVINCIBILITY_DURATION = 1.2

# ---- Colors ----
BG_TOP = (14, 12, 40)
BG_BOTTOM = (30, 18, 60)
PLATFORM_COLOR = (90, 100, 140)
MOVING_PLATFORM_COLOR = (140, 110, 180)
HAZARD_COLOR = (230, 70, 90)
COLLECTIBLE_COLOR = (255, 210, 70)
CHECKPOINT_COLOR = (110, 230, 170)
GOAL_COLOR = (120, 240, 200)
PLAYER_COLOR = (90, 210, 255)
ENEMY_COLOR = (230, 120, 90)
WHITE = (235, 235, 240)
ACCENT = (110, 230, 255)
PANEL_COLOR = (18, 16, 40)
HEALTH_GOOD = (90, 220, 130)
HEALTH_LOW = (230, 80, 80)

FONT_NAME = "consolas"

STAR_COUNT = 60  # decorative parallax starfield particle count


# =====================================================================
# LEVEL DATA  (from level_data.py)
# =====================================================================
"""
Level data for Nova Drift - a side-scrolling platformer.

Each level is a plain dictionary (data-driven design, Course 03 Lesson 02):
  - "width": total level width in pixels (the camera scrolls up to this).
  - "platforms": list of (x, y, w, h) static solid rectangles.
  - "moving_platforms": list of dicts: {rect:(x,y,w,h), axis, travel, speed}.
  - "hazards": list of (x, y, w, h) spike rectangles.
  - "enemies": list of dicts: {x, y, patrol_range, speed}.
  - "collectibles": list of (x, y) star-shard positions.
  - "checkpoints": list of (x, y) - the first is the level's start position.
  - "goal": (x, y) - reaching this ends the level in victory.

Levels escalate in difficulty following "teach, test, twist" (Lesson 02):
Level 1 teaches jumping/collecting on solid ground; Level 2 tests moving
platforms and a patrolling enemy; Level 3 twists all of it together with
tighter timing and more hazards.
"""

LEVELS = [
    {
        "name": "Launch Pad",
        "width": 2200,
        "platforms": [
            (0, 560, 500, 80),
            (600, 560, 300, 80),
            (980, 480, 200, 40),
            (1260, 560, 500, 80),
            (1840, 400, 360, 40),
            (300, 400, 120, 20),
        ],
        "moving_platforms": [],
        "hazards": [
            (500, 600, 100, 40),
            (900, 600, 80, 40),
        ],
        "enemies": [],
        "collectibles": [(340, 350), (1020, 420), (1300, 500), (1900, 340), (2000, 340)],
        "checkpoints": [(40, 480), (1000, 400)],
        "goal": (2120, 320),
    },
    {
        "name": "Drifting Platforms",
        "width": 2600,
        "platforms": [
            (0, 560, 400, 80),
            (700, 560, 260, 80),
            (1600, 560, 300, 80),
            (2200, 560, 400, 80),
            (450, 380, 100, 20),
        ],
        "moving_platforms": [
            {"rect": (420, 460, 120, 24), "axis": "x", "travel": 220, "speed": 90},
            {"rect": (1050, 420, 120, 24), "axis": "y", "travel": 140, "speed": 70},
            {"rect": (1900, 460, 140, 24), "axis": "x", "travel": 180, "speed": 100},
        ],
        "hazards": [
            (400, 600, 300, 40),
            (960, 600, 640, 40),
            (1900, 600, 300, 40),
        ],
        "enemies": [
            {"x": 750, "y": 520, "patrol_range": 120, "speed": 70},
            {"x": 2250, "y": 520, "patrol_range": 100, "speed": 90},
        ],
        "collectibles": [(480, 330), (1080, 360), (1650, 500), (1950, 400), (2350, 500)],
        "checkpoints": [(40, 480), (1650, 500)],
        "goal": (2500, 480),
    },
    {
        "name": "Nova's Edge",
        "width": 3000,
        "platforms": [
            (0, 560, 340, 80),
            (600, 560, 200, 80),
            (1050, 480, 160, 20),
            (1500, 560, 220, 80),
            (2050, 400, 200, 20),
            (2500, 560, 500, 80),
        ],
        "moving_platforms": [
            {"rect": (360, 470, 110, 24), "axis": "x", "travel": 200, "speed": 110},
            {"rect": (820, 430, 110, 24), "axis": "y", "travel": 160, "speed": 90},
            {"rect": (1240, 500, 110, 24), "axis": "x", "travel": 220, "speed": 120},
            {"rect": (1740, 340, 110, 24), "axis": "y", "travel": 180, "speed": 100},
            {"rect": (2280, 480, 130, 24), "axis": "x", "travel": 180, "speed": 130},
        ],
        "hazards": [
            (340, 600, 260, 40),
            (800, 600, 250, 40),
            (1270, 600, 230, 40),
            (1720, 600, 330, 40),
            (2180, 600, 320, 40),
        ],
        "enemies": [
            {"x": 650, "y": 520, "patrol_range": 60, "speed": 100},
            {"x": 1550, "y": 520, "patrol_range": 80, "speed": 110},
            {"x": 2600, "y": 520, "patrol_range": 150, "speed": 120},
        ],
        "collectibles": [
            (400, 420), (860, 380), (1090, 430), (1290, 450), (1780, 290),
            (2100, 350), (2700, 500), (2850, 500),
        ],
        "checkpoints": [(40, 480), (1050, 430), (2050, 350)],
        "goal": (2960, 480),
    },
]


# =====================================================================
# JUICE / POLISH EFFECTS  (from juice.py)
# =====================================================================
"""Polish/"juice" effects for Nova Drift: screen shake and floating text
popups (Course 03, Lesson 08 pattern). These are purely visual feedback -
they never affect game logic, collisions, or scoring math.
"""
pygame.font.init()
_popup_font = pygame.font.SysFont(FONT_NAME, 20, bold=True)


class ScreenShake:
    def __init__(self):
        self.timer = 0.0
        self.magnitude = 0

    def trigger(self, duration=0.15, magnitude=6):
        self.timer = duration
        self.magnitude = magnitude

    def update(self, dt):
        if self.timer > 0:
            self.timer -= dt

    def get_offset(self):
        if self.timer <= 0:
            return (0, 0)
        return (random.randint(-self.magnitude, self.magnitude), random.randint(-self.magnitude, self.magnitude))


class FloatingText:
    def __init__(self, x, y, text, color, lifetime=0.7):
        self.x, self.y = x, y
        self.text = text
        self.color = color
        self.lifetime = lifetime
        self.age = 0.0

    def update(self, dt):
        self.age += dt
        self.y -= 36 * dt

    @property
    def alive(self):
        return self.age < self.lifetime

    def draw(self, surface, camera_x=0):
        alpha = max(0, 255 - int((self.age / self.lifetime) * 255))
        label = _popup_font.render(self.text, True, self.color)
        label.set_alpha(alpha)
        surface.blit(label, (self.x - camera_x, self.y))


class JuiceManager:
    """A small pool-friendly manager for all active floating-text popups.

    Uses a fixed-size reusable pool (Course 03, Lesson 07: object pooling)
    instead of creating/destroying FloatingText objects every pickup, since
    a platformer can generate many popups quickly (collectibles, damage).
    """

    POOL_SIZE = 64

    def __init__(self):
        self.shake = ScreenShake()
        self._pool = [FloatingText(0, 0, "", (0, 0, 0)) for _ in range(self.POOL_SIZE)]
        for popup in self._pool:
            popup.age = popup.lifetime  # start all as "expired"/inactive

    def spawn_text(self, x, y, text, color=COLLECTIBLE_COLOR):
        for popup in self._pool:
            if not popup.alive:
                popup.x, popup.y = x, y
                popup.text = text
                popup.color = color
                popup.age = 0.0
                popup.lifetime = 0.7
                return

    def update(self, dt):
        self.shake.update(dt)
        for popup in self._pool:
            if popup.alive:
                popup.update(dt)

    def draw(self, surface, camera_x=0):
        for popup in self._pool:
            if popup.alive:
                popup.draw(surface, camera_x)


# =====================================================================
# BASE ENTITY  (from entities/entity.py)
# =====================================================================
class Entity:
    """Base Entity class shared across Nova Drift's game objects (Lesson 03 pattern)."""

    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.active = True

    def update(self, dt, level):
        pass

    def draw(self, surface, camera_x=0):
        pygame.draw.rect(surface, self.color, self.rect.move(-camera_x, 0), border_radius=4)


# =====================================================================
# PLATFORMS  (from entities/platform.py)
# =====================================================================
class Platform:
    """A static, solid platform/ground segment."""

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def update(self, dt):
        pass

    @property
    def velocity(self):
        return (0.0, 0.0)

    def draw(self, surface, camera_x=0):
        r = self.rect.move(-camera_x, 0)
        pygame.draw.rect(surface, PLATFORM_COLOR, r, border_radius=3)
        pygame.draw.rect(surface, ACCENT, (r.x, r.y, r.width, 4))


class MovingPlatform:
    """A platform that oscillates back and forth along one axis.

    The player is carried along by adding this platform's per-frame delta to
    the player's position whenever the player is standing on top of it -
    the standard technique for "riding" moving platforms in a 2D platformer.
    """

    def __init__(self, x, y, width, height, axis="x", travel=120, speed=60):
        self.rect = pygame.Rect(x, y, width, height)
        self.origin = pygame.Vector2(x, y)
        self.axis = axis
        self.travel = travel
        self.speed = speed
        self.t = 0.0
        self._last_pos = pygame.Vector2(x, y)
        self._velocity = pygame.Vector2(0, 0)

    def update(self, dt):
        self._last_pos = pygame.Vector2(self.rect.x, self.rect.y)
        self.t += dt * self.speed / max(self.travel, 1)
        wave = (math.sin(self.t) + 1) / 2  # 0..1 smooth oscillation
        if self.axis == "x":
            self.rect.x = int(self.origin.x + wave * self.travel)
        else:
            self.rect.y = int(self.origin.y + wave * self.travel)

        self._velocity = pygame.Vector2(self.rect.x, self.rect.y) - self._last_pos

    @property
    def velocity(self):
        return (self._velocity.x, self._velocity.y)

    def draw(self, surface, camera_x=0):
        r = self.rect.move(-camera_x, 0)
        pygame.draw.rect(surface, MOVING_PLATFORM_COLOR, r, border_radius=3)
        pygame.draw.rect(surface, ACCENT, (r.x, r.y, r.width, 4))


# =====================================================================
# HAZARDS  (from entities/hazard.py)
# =====================================================================
class Hazard(Entity):
    """Static hazards for Nova Drift - spikes that damage the player on contact."""

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, HAZARD_COLOR)

    def draw(self, surface, camera_x=0):
        r = self.rect.move(-camera_x, 0)
        spike_width = 12
        count = max(1, r.width // spike_width)
        for i in range(count):
            x0 = r.x + i * spike_width
            pygame.draw.polygon(
                surface, self.color,
                [(x0, r.bottom), (x0 + spike_width // 2, r.top), (x0 + spike_width, r.bottom)],
            )


# =====================================================================
# COLLECTIBLES  (from entities/collectible.py)
# =====================================================================
class Collectible(Entity):
    """Collectible star-shard entities for Nova Drift."""

    def __init__(self, x, y):
        super().__init__(x, y, 22, 22, COLLECTIBLE_COLOR)
        self.bob_timer = 0.0

    def update(self, dt, level):
        self.bob_timer += dt * 4

    def draw(self, surface, camera_x=0):
        if not self.active:
            return
        r = self.rect.move(-camera_x, 0)
        offset_y = int(math.sin(self.bob_timer) * 4)
        cx, cy = r.centerx, r.centery + offset_y
        points = []
        for i in range(8):
            angle = math.pi / 4 * i
            radius = 11 if i % 2 == 0 else 5
            points.append((cx + math.cos(angle) * radius, cy + math.sin(angle) * radius))
        pygame.draw.polygon(surface, self.color, points)


# =====================================================================
# CHECKPOINTS / GOAL  (from entities/checkpoint.py)
# =====================================================================
class Checkpoint(Entity):
    """Checkpoint flag entity for Nova Drift."""

    def __init__(self, x, y):
        super().__init__(x, y, 28, 56, PLATFORM_COLOR)
        self.activated = False

    def draw(self, surface, camera_x=0):
        r = self.rect.move(-camera_x, 0)
        color = CHECKPOINT_COLOR if self.activated else PLATFORM_COLOR
        pygame.draw.rect(surface, color, (r.x + r.width // 2 - 2, r.y, 4, r.height))
        flag_color = CHECKPOINT_COLOR if self.activated else (110, 110, 130)
        pygame.draw.polygon(
            surface, flag_color,
            [(r.x + r.width // 2 + 2, r.y), (r.x + r.width // 2 + 22, r.y + 10), (r.x + r.width // 2 + 2, r.y + 20)],
        )


class Goal(Entity):
    """Goal flag entity for Nova Drift - reaching it ends the level."""

    def __init__(self, x, y):
        super().__init__(x, y, 32, 64, GOAL_COLOR)

    def draw(self, surface, camera_x=0):
        r = self.rect.move(-camera_x, 0)
        pygame.draw.rect(surface, (140, 140, 160), (r.x + r.width // 2 - 3, r.y, 6, r.height))
        pygame.draw.polygon(
            surface, self.color,
            [(r.x + r.width // 2 + 3, r.y), (r.x + r.width // 2 + 30, r.y + 12), (r.x + r.width // 2 + 3, r.y + 24)],
        )


# =====================================================================
# ENEMY  (from entities/enemy.py)
# =====================================================================
class Enemy(Entity):
    """A simple patrolling enemy for Nova Drift - moves back and forth and damages
    the player on contact, demonstrating the Entity inheritance pattern from
    Course 03, Lesson 03 applied to a new hazard type without touching collision
    logic elsewhere.
    """

    def __init__(self, x, y, patrol_range=100, speed=70):
        size = 30
        super().__init__(x, y, size, size, ENEMY_COLOR)
        self.origin_x = x
        self.patrol_range = patrol_range
        self.speed = speed
        self.direction = 1

    def update(self, dt, level):
        self.rect.x += int(self.direction * self.speed * dt)
        if self.rect.x > self.origin_x + self.patrol_range:
            self.rect.x = self.origin_x + self.patrol_range
            self.direction = -1
        elif self.rect.x < self.origin_x - self.patrol_range:
            self.rect.x = self.origin_x - self.patrol_range
            self.direction = 1

    def draw(self, surface, camera_x=0):
        r = self.rect.move(-camera_x, 0)
        pygame.draw.rect(surface, self.color, r, border_radius=8)
        eye_offset = 8 if self.direction > 0 else -8
        pygame.draw.circle(surface, WHITE, (r.centerx + eye_offset, r.centery - 4), 4)


# =====================================================================
# PLAYER  (from entities/player.py)
# =====================================================================
class Player:
    """Player entity for Nova Drift - platformer movement, health, and collision."""

    def __init__(self, x, y):
        size = 32
        self.rect = pygame.Rect(x, y, size, size)
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self.facing = 1
        self.health = PLAYER_MAX_HEALTH
        self.lives = 3
        self.invincible_timer = 0.0
        self.score = 0
        self.color = PLAYER_COLOR

    def handle_input(self, keys):
        self.vx = 0.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -PLAYER_MOVE_SPEED
            self.facing = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = PLAYER_MOVE_SPEED
            self.facing = 1
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vy = JUMP_VELOCITY
            self.on_ground = False

    def update(self, dt, platforms):
        if self.invincible_timer > 0:
            self.invincible_timer -= dt

        self.vy += GRAVITY * dt
        self.vy = min(self.vy, MAX_FALL_SPEED)

        # --- Horizontal movement + collision ---
        self.rect.x += int(self.vx * dt)
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vx > 0:
                    self.rect.right = platform.rect.left
                elif self.vx < 0:
                    self.rect.left = platform.rect.right

        # --- Vertical movement + collision ---
        self.rect.y += int(self.vy * dt)
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vy > 0:
                    self.rect.bottom = platform.rect.top
                    self.vy = 0
                    self.on_ground = True
                    # Ride moving platforms: carry the player horizontally
                    # by the platform's own per-frame delta (Lesson 03/07
                    # composition idea applied to physics carrying).
                    vel = getattr(platform, "velocity", (0.0, 0.0))
                    self.rect.x += int(vel[0])
                elif self.vy < 0:
                    self.rect.top = platform.rect.bottom
                    self.vy = 0

    def take_damage(self, amount=1):
        """Encapsulates all damage logic including invincibility frames -
        outside code should never touch self.health directly (Lesson 03)."""
        if self.invincible_timer > 0:
            return False
        self.health -= amount
        self.invincible_timer = INVINCIBILITY_DURATION
        return True

    def respawn_at(self, x, y):
        self.rect.topleft = (x, y)
        self.vx = self.vy = 0.0
        self.health = PLAYER_MAX_HEALTH
        self.invincible_timer = INVINCIBILITY_DURATION

    def draw(self, surface, camera_x=0):
        flicker_hidden = self.invincible_timer > 0 and int(self.invincible_timer * 12) % 2 == 0
        if flicker_hidden:
            return
        r = self.rect.move(-camera_x, 0)
        pygame.draw.rect(surface, self.color, r, border_radius=6)
        eye_x = r.centerx + (6 if self.facing > 0 else -6)
        pygame.draw.circle(surface, WHITE, (eye_x, r.centery - 6), 4)


# =====================================================================
# LEVEL LOADER  (from level.py)
# =====================================================================
class Level:
    """Level loader for Nova Drift - converts level_data dictionaries into real
    game objects (Course 03, Lesson 02 data-driven design pattern)."""

    def __init__(self, index):
        data = LEVELS[index]
        self.index = index
        self.name = data["name"]
        self.width = data["width"]

        self.static_platforms = [Platform(*p) for p in data["platforms"]]
        self.moving_platforms = [
            MovingPlatform(*mp["rect"], axis=mp["axis"], travel=mp["travel"], speed=mp["speed"])
            for mp in data["moving_platforms"]
        ]
        self.all_platforms = self.static_platforms + self.moving_platforms

        self.hazards = [Hazard(*h) for h in data["hazards"]]
        self.enemies = [Enemy(e["x"], e["y"], e["patrol_range"], e["speed"]) for e in data["enemies"]]
        self.collectibles = [Collectible(x, y) for (x, y) in data["collectibles"]]
        self.checkpoints = [Checkpoint(x, y) for (x, y) in data["checkpoints"]]
        self.checkpoints[0].activated = True
        self.goal = Goal(*data["goal"])

        self.start_pos = data["checkpoints"][0]
        self.active_checkpoint_index = 0

    def current_checkpoint_pos(self):
        cp = self.checkpoints[self.active_checkpoint_index]
        return (cp.rect.x, cp.rect.y)

    def update(self, dt):
        for platform in self.moving_platforms:
            platform.update(dt)
        for enemy in self.enemies:
            enemy.update(dt, self)
        for collectible in self.collectibles:
            collectible.update(dt, self)

    def check_checkpoints(self, player_rect):
        for i, cp in enumerate(self.checkpoints):
            if not cp.activated and player_rect.colliderect(cp.rect):
                cp.activated = True
                self.active_checkpoint_index = i

    def draw(self, surface, camera_x):
        for platform in self.all_platforms:
            platform.draw(surface, camera_x)
        for hazard in self.hazards:
            hazard.draw(surface, camera_x)
        for cp in self.checkpoints:
            cp.draw(surface, camera_x)
        self.goal.draw(surface, camera_x)
        for collectible in self.collectibles:
            if collectible.active:
                collectible.draw(surface, camera_x)
        for enemy in self.enemies:
            enemy.draw(surface, camera_x)


def total_levels():
    return len(LEVELS)


# =====================================================================
# UI / HUD  (from ui.py)
# =====================================================================
_title_font = pygame.font.SysFont(FONT_NAME, 50, bold=True)
_heading_font = pygame.font.SysFont(FONT_NAME, 30, bold=True)
_body_font = pygame.font.SysFont(FONT_NAME, 20)
_small_font = pygame.font.SysFont(FONT_NAME, 16)


class Button:
    def __init__(self, rect, text, on_click):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.on_click = on_click
        self.hovered = False

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            self.on_click()

    def draw(self, surface):
        color = (80, 100, 180) if self.hovered else (50, 60, 120)
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, ACCENT, self.rect, width=2, border_radius=10)
        label = _body_font.render(self.text, True, WHITE)
        surface.blit(label, (self.rect.centerx - label.get_width() // 2, self.rect.centery - label.get_height() // 2))


def draw_vertical_gradient(surface, top_color, bottom_color):
    height = surface.get_height()
    for y in range(height):
        ratio = y / height
        color = tuple(int(top_color[i] + (bottom_color[i] - top_color[i]) * ratio) for i in range(3))
        pygame.draw.line(surface, color, (0, y), (surface.get_width(), y))


def draw_title_screen(surface, on_play, on_quit, mouse_pos, events):
    draw_vertical_gradient(surface, BG_TOP, BG_BOTTOM)
    title = _title_font.render(TITLE, True, ACCENT)
    surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
    subtitle = _body_font.render("A Side-Scrolling Platformer - Lumexa Game Creator Path Capstone", True, WHITE)
    surface.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 215))

    play_btn = Button((SCREEN_WIDTH // 2 - 110, 300, 220, 50), "Start Game", on_play)
    quit_btn = Button((SCREEN_WIDTH // 2 - 110, 370, 220, 50), "Quit", on_quit)
    for btn in (play_btn, quit_btn):
        btn.update(mouse_pos)
        for event in events:
            btn.handle_event(event)
        btn.draw(surface)

    hint = _small_font.render("Arrows/WASD to move, Space/Up to jump, P to pause.", True, WHITE)
    surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 440))


def draw_hud(surface, player, level):
    panel = pygame.Rect(0, 0, SCREEN_WIDTH, 46)
    pygame.draw.rect(surface, PANEL_COLOR, panel)

    # Health bar
    bar_x, bar_y, bar_w, bar_h = 12, 12, 140, 20
    pygame.draw.rect(surface, (40, 42, 66), (bar_x - 2, bar_y - 2, bar_w + 4, bar_h + 4), border_radius=6)
    ratio = max(0, player.health) / PLAYER_MAX_HEALTH
    color = HEALTH_GOOD if ratio > 0.4 else HEALTH_LOW
    pygame.draw.rect(surface, color, (bar_x, bar_y, int(bar_w * ratio), bar_h), border_radius=4)
    hp_label = _small_font.render(f"HP {player.health}/{PLAYER_MAX_HEALTH}", True, WHITE)
    surface.blit(hp_label, (bar_x + bar_w + 10, bar_y))

    lives_label = _small_font.render(f"Lives: {player.lives}", True, WHITE)
    surface.blit(lives_label, (bar_x + bar_w + 120, bar_y))

    score_label = _body_font.render(f"Shards: {player.score}", True, COLLECTIBLE_COLOR)
    surface.blit(score_label, (SCREEN_WIDTH - score_label.get_width() - 200, 10))

    name_label = _body_font.render(f"Level {level.index + 1}: {level.name}", True, ACCENT)
    surface.blit(name_label, (SCREEN_WIDTH - name_label.get_width() - 12, 10))


def draw_pause_overlay(surface, on_resume, on_quit_to_title, mouse_pos, events):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    surface.blit(overlay, (0, 0))
    heading = _heading_font.render("Paused", True, ACCENT)
    surface.blit(heading, (SCREEN_WIDTH // 2 - heading.get_width() // 2, 200))

    resume_btn = Button((SCREEN_WIDTH // 2 - 110, 270, 220, 46), "Resume", on_resume)
    quit_btn = Button((SCREEN_WIDTH // 2 - 110, 326, 220, 46), "Quit to Title", on_quit_to_title)
    for btn in (resume_btn, quit_btn):
        btn.update(mouse_pos)
        for event in events:
            btn.handle_event(event)
        btn.draw(surface)


def draw_level_complete(surface, level, player, on_continue, mouse_pos, events, is_last_level):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    surface.blit(overlay, (0, 0))

    heading = _heading_font.render(f"{level.name} Complete!", True, GOAL_COLOR)
    surface.blit(heading, (SCREEN_WIDTH // 2 - heading.get_width() // 2, 220))
    stats = _body_font.render(f"Shards collected this run: {player.score}", True, WHITE)
    surface.blit(stats, (SCREEN_WIDTH // 2 - stats.get_width() // 2, 270))

    label = "Finish Adventure" if is_last_level else "Next Level"
    btn = Button((SCREEN_WIDTH // 2 - 110, 320, 220, 46), label, on_continue)
    btn.update(mouse_pos)
    for event in events:
        btn.handle_event(event)
    btn.draw(surface)


def draw_game_over(surface, on_retry, on_quit_to_title, mouse_pos, events):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((30, 0, 0, 170))
    surface.blit(overlay, (0, 0))
    heading = _heading_font.render("Game Over", True, HEALTH_LOW)
    surface.blit(heading, (SCREEN_WIDTH // 2 - heading.get_width() // 2, 220))

    retry_btn = Button((SCREEN_WIDTH // 2 - 110, 290, 220, 46), "Retry Level", on_retry)
    title_btn = Button((SCREEN_WIDTH // 2 - 110, 346, 220, 46), "Quit to Title", on_quit_to_title)
    for btn in (retry_btn, title_btn):
        btn.update(mouse_pos)
        for event in events:
            btn.handle_event(event)
        btn.draw(surface)


def draw_game_complete(surface, total_score, on_title, mouse_pos, events):
    draw_vertical_gradient(surface, BG_TOP, BG_BOTTOM)
    title = _title_font.render("Adventure Complete!", True, GOAL_COLOR)
    surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
    msg = _body_font.render(f"Total shards collected: {total_score}", True, WHITE)
    surface.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 260))

    btn = Button((SCREEN_WIDTH // 2 - 110, 330, 220, 50), "Back to Title", on_title)
    btn.update(mouse_pos)
    for event in events:
        btn.handle_event(event)
    btn.draw(surface)


# =====================================================================
# GAME STATE MACHINE  (from game_state.py)
# =====================================================================
class AppState(Enum):
    TITLE = auto()
    PLAYING = auto()
    PAUSED = auto()
    LEVEL_COMPLETE = auto()
    GAME_OVER = auto()
    GAME_COMPLETE = auto()


class GameStateMachine:
    """Finite state machine governing Nova Drift's overall flow (Lesson 03 pattern)."""

    ALLOWED_TRANSITIONS = {
        AppState.TITLE: {AppState.PLAYING},
        AppState.PLAYING: {AppState.PAUSED, AppState.LEVEL_COMPLETE, AppState.GAME_OVER},
        AppState.PAUSED: {AppState.PLAYING, AppState.TITLE},
        AppState.LEVEL_COMPLETE: {AppState.PLAYING, AppState.GAME_COMPLETE},
        AppState.GAME_OVER: {AppState.PLAYING, AppState.TITLE},
        AppState.GAME_COMPLETE: {AppState.TITLE},
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
# MAIN GAME / ENTRY POINT  (from main.py)
# =====================================================================
try:
    pygame.mixer.init()
    SOUND_ENABLED = True
except pygame.error:
    SOUND_ENABLED = False


def _try_load_sound(path):
    """Defensive sound loading: returns None (never crashes) if the sound
    file is missing or the mixer is unavailable - Lesson 08 edge-case rule."""
    if not SOUND_ENABLED:
        return None
    try:
        return pygame.mixer.Sound(path)
    except (pygame.error, FileNotFoundError):
        return None


def _play(sound):
    if sound is not None:
        try:
            sound.play()
        except pygame.error:
            pass


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.fsm = GameStateMachine()
        self.juice = JuiceManager()

        self.sfx_collect = _try_load_sound("assets/collect.wav")
        self.sfx_hurt = _try_load_sound("assets/hurt.wav")
        self.sfx_win = _try_load_sound("assets/win.wav")

        self.level = None
        self.player = None
        self.camera_x = 0.0
        self.total_score = 0

    # -----------------------------------------------------------------
    def start_new_game(self):
        self.total_score = 0
        self._load_level(0)
        self.fsm.change_state(AppState.PLAYING)

    def _load_level(self, index):
        self.level = Level(index)
        start_x, start_y = self.level.start_pos
        self.player = Player(start_x, start_y)
        self.camera_x = 0.0

    def retry_level(self):
        self._load_level(self.level.index)
        self.fsm.change_state(AppState.PLAYING)

    def go_to_next_level(self):
        next_index = self.level.index + 1
        if next_index < total_levels():
            self._load_level(next_index)
            self.fsm.change_state(AppState.PLAYING)
        else:
            self.fsm.change_state(AppState.GAME_COMPLETE)

    def quit_to_title(self):
        self.fsm.change_state(AppState.TITLE)

    def quit_game(self):
        pygame.quit()
        sys.exit()

    # -----------------------------------------------------------------
    def _respawn_player(self):
        x, y = self.level.current_checkpoint_pos()
        self.player.respawn_at(x, y - 24)

    def _handle_damage(self):
        took_damage = self.player.take_damage(1)
        if took_damage:
            self.juice.shake.trigger(duration=0.2, magnitude=8)
            self.juice.spawn_text(self.player.rect.centerx, self.player.rect.top - 10, "-1 HP", HEALTH_LOW)
            _play(self.sfx_hurt)
            if self.player.health <= 0:
                self.player.lives -= 1
                if self.player.lives <= 0:
                    self.fsm.change_state(AppState.GAME_OVER)
                else:
                    self._respawn_player()

    def _update_gameplay(self, dt):
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        self.player.update(dt, self.level.all_platforms)

        if self.player.rect.top > SCREEN_HEIGHT + 200:
            self._handle_damage()  # falling off the bottom counts as a hit

        self.level.update(dt)
        self.level.check_checkpoints(self.player.rect)

        for hazard in self.level.hazards:
            if self.player.rect.colliderect(hazard.rect):
                self._handle_damage()

        for enemy in self.level.enemies:
            if enemy.active and self.player.rect.colliderect(enemy.rect):
                self._handle_damage()

        for collectible in self.level.collectibles:
            if collectible.active and self.player.rect.colliderect(collectible.rect):
                collectible.active = False
                self.player.score += 1
                self.total_score += 1
                self.juice.spawn_text(collectible.rect.centerx, collectible.rect.y - 10, "+1", COLLECTIBLE_COLOR)
                _play(self.sfx_collect)

        if self.player.rect.colliderect(self.level.goal.rect):
            _play(self.sfx_win)
            self.fsm.change_state(AppState.LEVEL_COMPLETE)

        self.juice.update(dt)

        # --- Camera follows the player horizontally, clamped to level bounds ---
        target_camera_x = self.player.rect.centerx - SCREEN_WIDTH // 2
        target_camera_x = max(0, min(target_camera_x, self.level.width - SCREEN_WIDTH))
        self.camera_x += (target_camera_x - self.camera_x) * 0.15  # smoothed follow

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and self.fsm.is_in(AppState.PLAYING):
                self.fsm.change_state(AppState.PAUSED)
            elif event.key == pygame.K_p and self.fsm.is_in(AppState.PAUSED):
                self.fsm.change_state(AppState.PLAYING)
            elif event.key == pygame.K_ESCAPE and self.fsm.is_in(AppState.PAUSED):
                self.fsm.change_state(AppState.TITLE)

    def update(self, dt):
        if self.fsm.is_in(AppState.PLAYING):
            self._update_gameplay(dt)

    def draw(self, events, mouse_pos):
        state = self.fsm.state
        if state == AppState.TITLE:
            draw_title_screen(self.screen, self.start_new_game, self.quit_game, mouse_pos, events)
            return
        if state == AppState.GAME_COMPLETE:
            draw_game_complete(self.screen, self.total_score, self.quit_to_title, mouse_pos, events)
            return

        # All remaining states render the game world underneath their overlay.
        offset = self.juice.shake.get_offset()
        cam = int(self.camera_x) - offset[0]
        draw_vertical_gradient(self.screen, BG_TOP, BG_BOTTOM)
        self.level.draw(self.screen, cam)
        self.player.draw(self.screen, cam)
        self.juice.draw(self.screen, cam)
        draw_hud(self.screen, self.player, self.level)

        if state == AppState.PAUSED:
            draw_pause_overlay(self.screen, self._resume, self.quit_to_title, mouse_pos, events)
        elif state == AppState.LEVEL_COMPLETE:
            is_last = self.level.index == total_levels() - 1
            draw_level_complete(self.screen, self.level, self.player, self.go_to_next_level, mouse_pos, events, is_last)
        elif state == AppState.GAME_OVER:
            draw_game_over(self.screen, self.retry_level, self.quit_to_title, mouse_pos, events)

    def _resume(self):
        self.fsm.change_state(AppState.PLAYING)

    def run(self):
        running = True
        while running:
            dt = min(self.clock.tick(FPS) / 1000.0, 1 / 30)
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()

            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.handle_event(event)

            self.update(dt)
            self.draw(events, mouse_pos)
            pygame.display.flip()

        pygame.quit()
        sys.exit()


def main():
    Game().run()


if __name__ == "__main__":
    main()
