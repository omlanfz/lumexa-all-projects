"""
Orbit Drop - Physics Puzzle Game
Lumexa Game Creator Path - Course 03, Project 08

A real physics-based puzzle game: launch a ball with gravity, velocity, and
collision response to reach a goal zone, across 6 hand-designed levels of
increasing difficulty loaded from a clean, data-driven level structure.

This is a single self-contained merged file combining:
settings.py, level_data.py, entities/ball.py, entities/obstacle.py,
level.py, ui.py, game_state.py, and main.py.
"""
import math
import sys
from enum import Enum, auto

import pygame

# ==========================================================================
# Settings and constants for Orbit Drop - Physics Puzzle Game.
# ==========================================================================

TITLE = "Orbit Drop"

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650
FPS = 60

GRAVITY = 900.0          # pixels / second^2
RESTITUTION = 0.55       # bounciness applied on collision (0 = no bounce, 1 = perfect bounce)
FRICTION = 0.995         # per-frame velocity damping to settle balls over time
MAX_LAUNCH_POWER = 620.0

BALL_RADIUS = 14

# ---- Colors ----
BG_COLOR = (10, 12, 28)
PANEL_COLOR = (20, 22, 44)
WALL_COLOR = (70, 80, 118)
STATIC_BOX_COLOR = (90, 100, 140)
BALL_COLOR = (90, 210, 255)
GOAL_COLOR = (110, 230, 150)
LAUNCHER_COLOR = (255, 190, 80)
AIM_LINE_COLOR = (255, 255, 255)
WHITE = (235, 235, 240)
ACCENT = (90, 220, 255)
DANGER_COLOR = (230, 80, 80)

FONT_NAME = "consolas"


# ==========================================================================
# Level data for Orbit Drop - Physics Puzzle Game.
#
# Each level is a plain dictionary (data-driven design, Course 03 Lesson 02):
#   - "launcher": (x, y) - where the ball starts and is launched from.
#   - "goal": (x, y, radius) - the target zone the ball must reach.
#   - "boxes": list of (x, y, width, height) static obstacle rectangles.
#   - "max_power_hint": a short string shown to the player for guidance.
#
# Levels increase in difficulty by adding more obstacles, narrower gaps, and
# goals that require the ball to bounce around barriers rather than go
# directly to the target - a "teach, test, twist" progression per Lesson 02.
# ==========================================================================

LEVELS = [
    # Level 1 - TEACH: a wide open shot straight to a big goal, no obstacles.
    {
        "name": "Open Sky",
        "launcher": (80, 500),
        "goal": (780, 560, 32),
        "boxes": [
            (0, 600, 900, 50),  # ground/floor
        ],
    },
    # Level 2 - TEACH: one simple obstacle to arc over.
    {
        "name": "First Wall",
        "launcher": (80, 500),
        "goal": (780, 560, 30),
        "boxes": [
            (0, 600, 900, 50),
            (420, 470, 40, 130),
        ],
    },
    # Level 3 - TEST: a narrow gap requiring an accurate bounce.
    {
        "name": "The Gap",
        "launcher": (60, 300),
        "goal": (800, 560, 28),
        "boxes": [
            (0, 600, 900, 50),
            (0, 0, 20, 650),
            (880, 0, 20, 650),
            (350, 350, 30, 250),
            (500, 0, 30, 300),
        ],
    },
    # Level 4 - TEST: a platform ledge the ball must land and settle on.
    {
        "name": "Ledge Landing",
        "launcher": (60, 150),
        "goal": (760, 260, 26),
        "boxes": [
            (0, 600, 900, 50),
            (0, 0, 20, 650),
            (880, 0, 20, 650),
            (620, 300, 260, 30),
            (300, 420, 220, 30),
        ],
    },
    # Level 5 - TWIST: a small pocket goal tucked behind two barriers,
    # requiring a bounce off the ceiling AND a side wall to reach it.
    {
        "name": "Twin Barriers",
        "launcher": (60, 550),
        "goal": (450, 120, 24),
        "boxes": [
            (0, 600, 900, 50),
            (0, 0, 20, 650),
            (880, 0, 20, 650),
            (0, 0, 900, 20),
            (250, 200, 30, 400),
            (600, 0, 30, 400),
        ],
    },
    # Level 6 - TWIST: a tight vertical shaft goal that punishes overshooting,
    # combining everything taught so far into the hardest layout.
    {
        "name": "The Vault",
        "launcher": (60, 300),
        "goal": (450, 560, 22),
        "boxes": [
            (0, 600, 900, 50),
            (0, 0, 20, 650),
            (880, 0, 20, 650),
            (0, 0, 900, 20),
            (200, 300, 30, 350),
            (380, 450, 140, 30),
            (620, 300, 30, 350),
            (300, 150, 300, 30),
        ],
    },
]


# ==========================================================================
# The physics-driven Ball entity for Orbit Drop.
# ==========================================================================

class Ball:
    """A circle with real position/velocity integration, gravity, and
    simple collision response against axis-aligned obstacles and screen
    bounds. This is the "real simple physics" required by Project 08:
    gravity, velocity, and collision response for a circle.
    """

    def __init__(self, x, y, radius=BALL_RADIUS):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.radius = radius
        self.launched = False
        self.settled = False
        self.color = BALL_COLOR

    def launch(self, vx, vy):
        self.vx = vx
        self.vy = vy
        self.launched = True
        self.settled = False

    def reset(self, x, y):
        self.x, self.y = float(x), float(y)
        self.vx = self.vy = 0.0
        self.launched = False
        self.settled = False

    @property
    def rect_bounds(self):
        """A bounding box, useful for quick broad-phase checks."""
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def update(self, dt, obstacles, screen_width, screen_height):
        if not self.launched or self.settled:
            return

        # --- Integrate physics: gravity affects vertical velocity ---
        self.vy += GRAVITY * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

        # --- Friction/damping so the ball naturally settles over time ---
        self.vx *= FRICTION
        self.vy *= FRICTION

        # --- Collide with screen bounds (acts as the puzzle box walls) ---
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx = -self.vx * RESTITUTION
        elif self.x + self.radius > screen_width:
            self.x = screen_width - self.radius
            self.vx = -self.vx * RESTITUTION

        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy = -self.vy * RESTITUTION
        elif self.y + self.radius > screen_height:
            self.y = screen_height - self.radius
            self.vy = -self.vy * RESTITUTION

        # --- Collide with each static obstacle (rectangle) ---
        for obstacle in obstacles:
            resolve_circle_rect_collision(self, obstacle.rect)

        # --- Consider the ball "settled" once it's basically stopped ---
        speed = math.hypot(self.vx, self.vy)
        if speed < 6 and self.y + self.radius >= screen_height - 1:
            self.settled = True

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius, width=2)


def resolve_circle_rect_collision(ball, rect):
    """Finds the closest point on an AABB rect to the ball's center, and if
    the ball overlaps that point, pushes it out and reflects its velocity
    along the collision normal, scaled by RESTITUTION - a compact, standard
    circle-vs-AABB collision response used in many simple physics engines.
    """
    closest_x = max(rect.left, min(ball.x, rect.right))
    closest_y = max(rect.top, min(ball.y, rect.bottom))

    dx = ball.x - closest_x
    dy = ball.y - closest_y
    distance_sq = dx * dx + dy * dy

    if distance_sq >= ball.radius * ball.radius or distance_sq == 0:
        return

    distance = math.sqrt(distance_sq)
    overlap = ball.radius - distance
    nx, ny = dx / distance, dy / distance

    # Push the ball out of the obstacle along the collision normal.
    ball.x += nx * overlap
    ball.y += ny * overlap

    # Reflect velocity along the normal (standard elastic-ish bounce formula).
    dot = ball.vx * nx + ball.vy * ny
    ball.vx -= 2 * dot * nx
    ball.vy -= 2 * dot * ny
    ball.vx *= RESTITUTION
    ball.vy *= RESTITUTION


# ==========================================================================
# Static obstacles and the goal zone for Orbit Drop.
# ==========================================================================

class StaticBox:
    """An immovable rectangular obstacle the ball bounces off of."""

    def __init__(self, x, y, width, height, color=STATIC_BOX_COLOR):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=4)
        pygame.draw.rect(surface, WALL_COLOR, self.rect, width=2, border_radius=4)


class Goal:
    """The target zone. The level is won when the ball settles inside it,
    or simply overlaps it while sufficiently slow (a "landed" condition).
    """

    def __init__(self, x, y, radius=26):
        self.x, self.y = x, y
        self.radius = radius

    def contains_ball(self, ball):
        dx = ball.x - self.x
        dy = ball.y - self.y
        distance = (dx * dx + dy * dy) ** 0.5
        return distance <= self.radius + ball.radius * 0.4

    def draw(self, surface, pulse=0.0):
        base_radius = self.radius + int(3 * pulse)
        pygame.draw.circle(surface, GOAL_COLOR, (self.x, self.y), base_radius, width=4)
        pygame.draw.circle(surface, GOAL_COLOR, (self.x, self.y), max(4, base_radius - 14))


# ==========================================================================
# Level loader - converts level_data dictionaries into real game objects.
# ==========================================================================

class Level:
    def __init__(self, index):
        self.index = index
        data = LEVELS[index]
        self.name = data["name"]
        self.launcher_pos = data["launcher"]
        self.boxes = [StaticBox(x, y, w, h) for (x, y, w, h) in data["boxes"]]
        gx, gy, gr = data["goal"]
        self.goal = Goal(gx, gy, gr)
        self.ball = Ball(*self.launcher_pos)
        self.attempts = 0
        self.won = False

    def reset_ball(self):
        self.ball.reset(*self.launcher_pos)

    def restart_level(self):
        self.reset_ball()
        self.attempts = 0
        self.won = False

    def launch_ball(self, vx, vy):
        if self.ball.launched and not self.ball.settled and not self.won:
            return  # a shot is already in flight; wait for it to settle
        self.reset_ball()
        self.ball.launch(vx, vy)
        self.attempts += 1

    def update(self, dt, screen_width, screen_height):
        self.ball.update(dt, self.boxes, screen_width, screen_height)
        if not self.won and self.ball.launched and self.goal.contains_ball(self.ball):
            self.won = True

    def draw(self, surface, pulse=0.0):
        for box in self.boxes:
            box.draw(surface)
        self.goal.draw(surface, pulse)
        self.ball.draw(surface)


def total_levels():
    return len(LEVELS)


# ==========================================================================
# UI/HUD module for Orbit Drop: buttons, title, level select, HUD, win screens.
# ==========================================================================

pygame.font.init()
_title_font = pygame.font.SysFont(FONT_NAME, 46, bold=True)
_heading_font = pygame.font.SysFont(FONT_NAME, 28, bold=True)
_body_font = pygame.font.SysFont(FONT_NAME, 20)
_small_font = pygame.font.SysFont(FONT_NAME, 16)


class Button:
    def __init__(self, rect, text, on_click, enabled=True):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.on_click = on_click
        self.hovered = False
        self.enabled = enabled

    def update(self, mouse_pos):
        self.hovered = self.enabled and self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if not self.enabled:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()

    def draw(self, surface):
        if not self.enabled:
            color = (40, 44, 66)
            text_color = (110, 112, 130)
        else:
            color = (70, 90, 160) if self.hovered else (46, 58, 110)
            text_color = WHITE
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, ACCENT, self.rect, width=2, border_radius=10)
        label = _body_font.render(self.text, True, text_color)
        surface.blit(label, (self.rect.centerx - label.get_width() // 2, self.rect.centery - label.get_height() // 2))


def draw_title_screen(surface, on_play, on_quit, mouse_pos, events):
    surface.fill(BG_COLOR)
    title = _title_font.render(TITLE, True, ACCENT)
    surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 140))
    subtitle = _body_font.render("A Physics Puzzle Game - Lumexa Game Creator Path", True, WHITE)
    surface.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 200))

    play_btn = Button((SCREEN_WIDTH // 2 - 110, 300, 220, 50), "Play", on_play)
    quit_btn = Button((SCREEN_WIDTH // 2 - 110, 370, 220, 50), "Quit", on_quit)
    for btn in (play_btn, quit_btn):
        btn.update(mouse_pos)
        for event in events:
            btn.handle_event(event)
        btn.draw(surface)


def draw_level_select(surface, level_names, unlocked_count, on_select, mouse_pos, events):
    surface.fill(BG_COLOR)
    heading = _heading_font.render("Select a Level", True, ACCENT)
    surface.blit(heading, (SCREEN_WIDTH // 2 - heading.get_width() // 2, 40))

    cols = 3
    btn_w, btn_h = 220, 70
    gap_x, gap_y = 30, 30
    start_x = SCREEN_WIDTH // 2 - (cols * btn_w + (cols - 1) * gap_x) // 2
    start_y = 120

    for i, name in enumerate(level_names):
        row, col = divmod(i, cols)
        x = start_x + col * (btn_w + gap_x)
        y = start_y + row * (btn_h + gap_y)
        unlocked = i <= unlocked_count
        label = f"{i + 1}. {name}" if unlocked else f"{i + 1}. Locked"
        btn = Button((x, y, btn_w, btn_h), label, (lambda idx=i: on_select(idx)), enabled=unlocked)
        btn.update(mouse_pos)
        for event in events:
            btn.handle_event(event)
        btn.draw(surface)

    hint = _small_font.render("Complete a level to unlock the next one.", True, WHITE)
    surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 40))


def draw_hud(surface, level, drag_start, drag_current):
    panel = pygame.Rect(0, 0, SCREEN_WIDTH, 46)
    pygame.draw.rect(surface, PANEL_COLOR, panel)
    name_label = _body_font.render(f"Level {level.index + 1}: {level.name}", True, ACCENT)
    surface.blit(name_label, (12, 12))
    attempts_label = _body_font.render(f"Attempts: {level.attempts}", True, WHITE)
    surface.blit(attempts_label, (SCREEN_WIDTH - attempts_label.get_width() - 12, 12))

    hint = _small_font.render(
        "Drag from the ball to aim, release to launch. R = retry level.", True, WHITE,
    )
    surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 26))

    if drag_start and drag_current:
        pygame.draw.line(surface, AIM_LINE_COLOR, drag_start, drag_current, 3)


def draw_win_overlay(surface, level, on_next, on_replay, on_menu, mouse_pos, events, is_last_level):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    surface.blit(overlay, (0, 0))

    msg = _heading_font.render(f"Level {level.index + 1} Complete!", True, GOAL_COLOR)
    surface.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 180))
    stats = _body_font.render(f"Solved in {level.attempts} attempt(s).", True, WHITE)
    surface.blit(stats, (SCREEN_WIDTH // 2 - stats.get_width() // 2, 230))

    buttons = []
    if not is_last_level:
        buttons.append(Button((SCREEN_WIDTH // 2 - 110, 280, 220, 46), "Next Level", on_next))
    buttons.append(Button((SCREEN_WIDTH // 2 - 110, 336, 220, 46), "Replay Level", on_replay))
    buttons.append(Button((SCREEN_WIDTH // 2 - 110, 392, 220, 46), "Level Select", on_menu))

    for btn in buttons:
        btn.update(mouse_pos)
        for event in events:
            btn.handle_event(event)
        btn.draw(surface)


def draw_all_complete(surface, on_menu, mouse_pos, events):
    surface.fill(BG_COLOR)
    title = _title_font.render("All Levels Complete!", True, GOAL_COLOR)
    surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 220))
    msg = _body_font.render("You solved every Orbit Drop puzzle. Great work, engineer!", True, WHITE)
    surface.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 280))

    btn = Button((SCREEN_WIDTH // 2 - 110, 340, 220, 50), "Level Select", on_menu)
    btn.update(mouse_pos)
    for event in events:
        btn.handle_event(event)
    btn.draw(surface)


# ==========================================================================
# Finite state machine governing Orbit Drop's overall flow.
# ==========================================================================

class AppState(Enum):
    TITLE = auto()
    LEVEL_SELECT = auto()
    PLAYING = auto()
    LEVEL_WIN = auto()
    ALL_COMPLETE = auto()


class GameStateMachine:
    ALLOWED_TRANSITIONS = {
        AppState.TITLE: {AppState.LEVEL_SELECT},
        AppState.LEVEL_SELECT: {AppState.PLAYING, AppState.TITLE},
        AppState.PLAYING: {AppState.LEVEL_WIN, AppState.LEVEL_SELECT},
        AppState.LEVEL_WIN: {AppState.PLAYING, AppState.LEVEL_SELECT, AppState.ALL_COMPLETE},
        AppState.ALL_COMPLETE: {AppState.LEVEL_SELECT, AppState.TITLE},
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


# ==========================================================================
# Main Game class and entry point (from main.py).
# ==========================================================================

AIM_SENSITIVITY = 2.6  # converts drag distance to launch speed


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.fsm = GameStateMachine()

        self.level_names = [Level(i).name for i in range(total_levels())]
        self.unlocked_count = 0  # index of the highest unlocked level
        self.current_level = None
        self.drag_start = None
        self.drag_current = None
        self.pulse_timer = 0.0

    # -----------------------------------------------------------------
    def go_to_level_select(self):
        self.fsm.change_state(AppState.LEVEL_SELECT)

    def start_level(self, index):
        self.current_level = Level(index)
        self.drag_start = None
        self.drag_current = None
        self.fsm.change_state(AppState.PLAYING)

    def replay_current_level(self):
        if self.current_level:
            self.current_level.restart_level()
            self.fsm.change_state(AppState.PLAYING)

    def go_to_next_level(self):
        next_index = self.current_level.index + 1
        if next_index < total_levels():
            self.start_level(next_index)
        else:
            self.fsm.change_state(AppState.ALL_COMPLETE)

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def _on_level_win(self):
        self.unlocked_count = max(self.unlocked_count, self.current_level.index + 1)
        self.fsm.change_state(AppState.LEVEL_WIN)

    # -----------------------------------------------------------------
    def handle_playing_event(self, event):
        level = self.current_level
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            level.restart_level()
            return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.fsm.change_state(AppState.LEVEL_SELECT)
            return

        if level.won or level.ball.launched and not level.ball.settled:
            return  # ignore new aiming while a shot is in flight or already won

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            bx, by = level.ball.x, level.ball.y
            if math.hypot(event.pos[0] - bx, event.pos[1] - by) <= level.ball.radius + 30:
                self.drag_start = (bx, by)
                self.drag_current = event.pos
        elif event.type == pygame.MOUSEMOTION and self.drag_start:
            self.drag_current = event.pos
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.drag_start:
            dx = self.drag_start[0] - event.pos[0]
            dy = self.drag_start[1] - event.pos[1]
            distance = math.hypot(dx, dy)
            if distance > 4:
                strength = min(distance * AIM_SENSITIVITY, MAX_LAUNCH_POWER)
                nx, ny = dx / distance, dy / distance
                level.launch_ball(nx * strength, ny * strength)
            self.drag_start = None
            self.drag_current = None

    def update(self, dt):
        self.pulse_timer += dt
        if self.fsm.is_in(AppState.PLAYING):
            level = self.current_level
            level.update(dt, SCREEN_WIDTH, SCREEN_HEIGHT)
            if level.won:
                self._on_level_win()

    def draw(self, events, mouse_pos):
        state = self.fsm.state
        if state == AppState.TITLE:
            draw_title_screen(self.screen, self.go_to_level_select, self.quit_game, mouse_pos, events)
        elif state == AppState.LEVEL_SELECT:
            draw_level_select(self.screen, self.level_names, self.unlocked_count, self.start_level, mouse_pos, events)
        elif state == AppState.PLAYING:
            self.screen.fill(BG_COLOR)
            pulse = (math.sin(self.pulse_timer * 4) + 1) / 2
            self.current_level.draw(self.screen, pulse)
            draw_hud(self.screen, self.current_level, self.drag_start, self.drag_current)
        elif state == AppState.LEVEL_WIN:
            self.screen.fill(BG_COLOR)
            pulse = (math.sin(self.pulse_timer * 4) + 1) / 2
            self.current_level.draw(self.screen, pulse)
            draw_hud(self.screen, self.current_level, None, None)
            is_last = self.current_level.index == total_levels() - 1
            draw_win_overlay(
                self.screen, self.current_level, self.go_to_next_level,
                self.replay_current_level, self.go_to_level_select, mouse_pos, events, is_last,
            )
        elif state == AppState.ALL_COMPLETE:
            draw_all_complete(self.screen, self.go_to_level_select, mouse_pos, events)

    def run(self):
        running = True
        while running:
            dt = min(self.clock.tick(FPS) / 1000.0, 1 / 30)  # clamp dt to avoid physics spikes
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()

            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif self.fsm.is_in(AppState.PLAYING):
                    self.handle_playing_event(event)

            self.update(dt)
            self.draw(events, mouse_pos)
            pygame.display.flip()

        pygame.quit()
        sys.exit()


def main():
    Game().run()


if __name__ == "__main__":
    main()
