"""
Lumexa Maze Runner Timer - single-file merged version.

Run with: python maze-runner-timer.py   (from the project root)

This file merges (in order): settings, maze layouts/parsing, audio,
scores persistence, hazard/player sprites, UI helpers, the Game state
machine, and the main entry point - all originally split across
src/settings.py, src/mazes.py, src/maze.py, src/audio.py, src/scores.py,
src/hazard.py, src/player.py, src/ui.py, src/game.py, and src/main.py.
"""

import json
import os
import random
import sys

import pygame


# ======================================================================
# Settings / constants (from settings.py)
# ======================================================================

TILE_SIZE = 40
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GAME_TITLE = "Lumexa Maze Runner Timer"

# --- Colors ---
BLACK = (10, 10, 20)
WALL_COLOR = (60, 70, 110)
FLOOR_COLOR = (20, 24, 40)
WHITE = (255, 255, 255)
GRAY = (150, 150, 165)
CYAN = (80, 220, 255)
YELLOW = (255, 220, 80)
RED = (230, 70, 70)
GREEN = (100, 230, 130)
PURPLE = (190, 120, 255)

PLAYER_SPEED = 220
HAZARD_SPEED = 110

LEVEL_TIME_LIMITS = {
    1: 45,
    2: 60,
}

# BASE_DIR now points at the project root (this file's directory), since
# everything used to live inside src/ and has been merged up one level.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_DIR = os.path.join(BASE_DIR, "sounds")
SCORES_FILE = os.path.join(BASE_DIR, "best_times.json")


# ======================================================================
# Maze layouts (from mazes.py)
# ======================================================================

# Each maze is a list of equal-length strings, one character per tile:
#   '#' = wall
#   '.' = open floor
#   'S' = player start
#   'E' = exit (goal)
#   'H' = hazard start position (floor tile, hazard spawns here)
#
# Grid is 20 columns x 15 rows, matching an 800x600 screen at 40px tiles.

MAZE_LEVEL_1 = [
    "####################",
    "#S..#..............#",
    "#.#.#.############.#",
    "#.#.#.#..........#.#",
    "#.#.#.#.########.#.#",
    "#.#...#.#......#.#.#",
    "#.#####.#.####.#.#.#",
    "#.......#.#..#.#.#.#",
    "#######.#.#.##.#.#.#",
    "#....H..#.#....#.#.#",
    "#.#####.#.######.#.#",
    "#.#.....#........#.#",
    "#.#.################",
    "#..................E",
    "####################",
]

MAZE_LEVEL_2 = [
    "####################",
    "#S....#....#.......#",
    "#.###.#.##.#.#####.#",
    "#.#H..#.##.#.#...#.#",
    "#.#.####.#.#.#.#.#.#",
    "#.#......#.#.#.#.#.#",
    "#.########.#.#.#.#.#",
    "#..........#...#.#.#",
    "#.###########.##.#.#",
    "#.#.....#...#....#.#",
    "#.#.###.#.#.####.#.#",
    "#.#.#H..#.#......#.#",
    "#.#.#.#####.######.#",
    "#...#..............E",
    "####################",
]

MAZE_LEVELS = {
    1: MAZE_LEVEL_1,
    2: MAZE_LEVEL_2,
}


def normalize_maze(rows):
    """Pad every row to the same length with walls, defensively."""
    width = max(len(r) for r in rows)
    return [r.ljust(width, "#") for r in rows]


# ======================================================================
# Maze class (from maze.py)
# Parses a text-based maze layout into wall rects, start position,
# exit rect, and hazard spawn points, and draws the maze.
# ======================================================================

class Maze:
    def __init__(self, layout):
        self.layout = normalize_maze(layout)
        self.rows = len(self.layout)
        self.cols = len(self.layout[0])

        self.wall_rects = []
        self.start_pos = (TILE_SIZE + TILE_SIZE // 2, TILE_SIZE + TILE_SIZE // 2)
        self.exit_rect = None
        self.hazard_spawns = []

        self._parse()

    def _parse(self):
        for row_index, row in enumerate(self.layout):
            for col_index, char in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if char == "#":
                    self.wall_rects.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
                elif char == "S":
                    self.start_pos = (x + TILE_SIZE // 2, y + TILE_SIZE // 2)
                elif char == "E":
                    self.exit_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                elif char == "H":
                    self.hazard_spawns.append((x + TILE_SIZE // 2, y + TILE_SIZE // 2))

        if self.exit_rect is None:
            # Defensive fallback: put exit at bottom-right open tile
            self.exit_rect = pygame.Rect(
                (self.cols - 2) * TILE_SIZE, (self.rows - 2) * TILE_SIZE, TILE_SIZE, TILE_SIZE
            )

    def collides_with_wall(self, rect):
        return rect.collidelist(self.wall_rects) != -1

    def draw(self, screen):
        pixel_width = self.cols * TILE_SIZE
        pixel_height = self.rows * TILE_SIZE
        screen.fill(FLOOR_COLOR, pygame.Rect(0, 0, pixel_width, pixel_height))

        for wall in self.wall_rects:
            pygame.draw.rect(screen, WALL_COLOR, wall)
            pygame.draw.rect(screen, (30, 36, 60), wall, 1)

        pygame.draw.rect(screen, GREEN, self.exit_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.exit_rect, 2)


# ======================================================================
# Sound manager (from audio.py)
# Defensive loading: missing files or no audio device never crash the game.
# ======================================================================

class SoundManager:
    def __init__(self):
        self.enabled = True
        try:
            pygame.mixer.init()
        except pygame.error:
            self.enabled = False

        self.sounds = {}
        if self.enabled:
            self._load_sound("step", "step.wav", volume=0.2)
            self._load_sound("win", "win.wav", volume=0.6)
            self._load_sound("hurt", "hurt.wav", volume=0.6)
            self._load_sound("timeout", "timeout.wav", volume=0.6)

    def _load_sound(self, name, filename, volume=0.5):
        path = os.path.join(SOUND_DIR, filename)
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            self.sounds[name] = sound
        except (pygame.error, FileNotFoundError):
            self.sounds[name] = None

    def play(self, name):
        if not self.enabled:
            return
        sound = self.sounds.get(name)
        if sound is not None:
            sound.play()

    def play_music(self, filename="theme.ogg", volume=0.2, loop=True):
        if not self.enabled:
            return
        path = os.path.join(SOUND_DIR, filename)
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loops=-1 if loop else 0)
        except (pygame.error, FileNotFoundError):
            pass


# ======================================================================
# Best-time persistence (from scores.py)
# Reads/writes a small JSON file next to the source code. All file
# operations are wrapped defensively so a missing or corrupt file
# never crashes the game - it just falls back to "no best time yet."
# ======================================================================

def load_best_times():
    """Return a dict like {"1": 23.4, "2": 40.1} of best completion times per level."""
    if not os.path.exists(SCORES_FILE):
        return {}
    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
        return {}
    except (json.JSONDecodeError, OSError):
        return {}


def save_best_time(level_number, time_seconds):
    """Save a new best time for a level if it beats the existing one."""
    best_times = load_best_times()
    key = str(level_number)
    current_best = best_times.get(key)

    if current_best is None or time_seconds < current_best:
        best_times[key] = round(time_seconds, 2)
        try:
            with open(SCORES_FILE, "w", encoding="utf-8") as f:
                json.dump(best_times, f, indent=2)
        except OSError:
            pass  # If we can't write the file, just skip saving silently
        return True  # new best time achieved
    return False


def get_best_time(level_number):
    best_times = load_best_times()
    return best_times.get(str(level_number))


# ======================================================================
# Hazard sprite (from hazard.py)
# Patrols back and forth in a straight line, bouncing off walls
# detected via the same Maze wall-collision check the player uses.
# ======================================================================

class Hazard(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((26, 26), pygame.SRCALPHA)
        pygame.draw.polygon(
            self.image, RED, [(13, 0), (26, 13), (13, 26), (0, 13)]
        )
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.speed = HAZARD_SPEED

    def update(self, dt, maze):
        dx = self.direction[0] * self.speed * dt
        dy = self.direction[1] * self.speed * dt

        self.rect.x += dx
        self.rect.y += dy

        if maze.collides_with_wall(self.rect):
            self.rect.x -= dx
            self.rect.y -= dy
            # bounce: reverse direction on collision
            self.direction = (-self.direction[0], -self.direction[1])

    def reset(self, x, y):
        self.rect.center = (x, y)


# ======================================================================
# Player sprite (from player.py)
# Movement is axis-separated (move X, resolve X collisions, then move Y,
# resolve Y collisions) so the player can slide along a wall instead of
# getting fully stuck when moving diagonally into a corner.
# ======================================================================

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(self.image, CYAN, (12, 12), 11)
        pygame.draw.circle(self.image, (255, 255, 255), (12, 12), 11, 2)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = PLAYER_SPEED

    def update(self, dt, keys, maze):
        dx = 0
        dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1

        if dx != 0 and dy != 0:
            # normalize diagonal speed so it isn't faster than straight movement
            dx *= 0.7071
            dy *= 0.7071

        move_x = dx * self.speed * dt
        move_y = dy * self.speed * dt

        # Move on the X axis, then revert exactly if it caused a wall collision
        self.rect.x += move_x
        if maze.collides_with_wall(self.rect):
            self.rect.x -= move_x

        # Move on the Y axis independently, same correction approach
        self.rect.y += move_y
        if maze.collides_with_wall(self.rect):
            self.rect.y -= move_y

    def reset(self, x, y):
        self.rect.center = (x, y)


# ======================================================================
# UI helpers: HUD and screens (from ui.py)
# ======================================================================

def draw_text_centered(screen, font, text, color, y):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(SCREEN_WIDTH // 2, y))
    screen.blit(surface, rect)


def draw_hud(screen, font, level_number, time_left, best_time):
    timer_color = RED if time_left <= 10 else WHITE
    timer_text = font.render(f"Time Left: {time_left:.1f}s", True, timer_color)
    screen.blit(timer_text, (10, 10))

    level_text = font.render(f"Level {level_number}", True, WHITE)
    screen.blit(level_text, (10, 36))

    best_str = f"{best_time:.1f}s" if best_time is not None else "--"
    best_text = font.render(f"Best: {best_str}", True, GRAY)
    screen.blit(best_text, (10, 62))


def draw_menu(screen, font, big_font):
    draw_text_centered(screen, big_font, "LUMEXA MAZE RUNNER", CYAN, 220)
    draw_text_centered(screen, font, "Press ENTER or SPACE to start", WHITE, 300)
    draw_text_centered(
        screen, font, "Arrows/WASD to move - reach the green exit before time runs out!",
        GRAY, 340,
    )


def draw_win(screen, font, big_font, level_number, time_taken, best_time, is_new_best, final_level):
    draw_text_centered(screen, big_font, "LEVEL COMPLETE!", GREEN, 200)
    draw_text_centered(screen, font, f"Time: {time_taken:.1f}s", WHITE, 270)
    if is_new_best:
        draw_text_centered(screen, font, "NEW BEST TIME!", YELLOW, 300)
    elif best_time is not None:
        draw_text_centered(screen, font, f"Best: {best_time:.1f}s", GRAY, 300)

    if final_level:
        draw_text_centered(screen, font, "You cleared every level!", CYAN, 340)
        draw_text_centered(screen, font, "Press R to play again or ESC to quit", WHITE, 380)
    else:
        draw_text_centered(screen, font, "Press SPACE for the next level", WHITE, 380)


def draw_timeout(screen, font, big_font, level_number):
    draw_text_centered(screen, big_font, "TIME'S UP!", RED, 220)
    draw_text_centered(screen, font, f"You ran out of time on Level {level_number}", WHITE, 290)
    draw_text_centered(screen, font, "Press R to retry or ESC to quit", GRAY, 330)


def draw_hazard_hit(screen, font):
    draw_text_centered(screen, font, "Hazard hit! Sent back to start.", RED, 90)


# ======================================================================
# Game state machine (from game.py)
# States: MENU -> PLAYING -> WIN / TIMEOUT -> restart to MENU/PLAYING
# ======================================================================

class GameState:
    MENU = "menu"
    PLAYING = "playing"
    WIN = "win"
    TIMEOUT = "timeout"


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 26)
        self.big_font = pygame.font.SysFont(None, 52)

        self.sound = SoundManager()
        self.sound.play_music("theme.ogg")

        self.state = GameState.MENU
        self.level_number = 1
        self.max_level = max(MAZE_LEVELS.keys())

        self.maze = None
        self.player = None
        self.hazards = None

        self.time_left = 0.0
        self.time_taken = 0.0
        self.hit_flash_timer = 0.0
        self.is_new_best = False

    # ------------------------------------------------------------------
    def start_level(self, level_number):
        self.level_number = level_number
        layout = MAZE_LEVELS[level_number]
        self.maze = Maze(layout)

        self.player = Player(*self.maze.start_pos)

        self.hazards = pygame.sprite.Group()
        # Defensive fallback: if a maze defines no 'H' markers, spawn a single
        # hazard near the exit rather than on top of the player's start tile.
        fallback_spawn = [self.maze.exit_rect.center] if self.maze.exit_rect else [self.maze.start_pos]
        spawns = self.maze.hazard_spawns or fallback_spawn
        for spawn in spawns:
            self.hazards.add(Hazard(*spawn))

        self.time_left = float(LEVEL_TIME_LIMITS.get(level_number, 60))
        self.time_taken = 0.0
        self.hit_flash_timer = 0.0
        self.is_new_best = False
        self.state = GameState.PLAYING

    def restart_from_menu(self):
        self.state = GameState.MENU

    # ------------------------------------------------------------------
    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return True

        if event.key == pygame.K_ESCAPE:
            if self.state == GameState.PLAYING:
                self.state = GameState.MENU
            else:
                return False
            return True

        if self.state == GameState.MENU:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.start_level(1)

        elif self.state == GameState.WIN:
            if self.level_number >= self.max_level:
                if event.key == pygame.K_r:
                    self.start_level(1)
            else:
                if event.key == pygame.K_SPACE:
                    self.start_level(self.level_number + 1)

        elif self.state == GameState.TIMEOUT:
            if event.key == pygame.K_r:
                self.start_level(self.level_number)

        return True

    # ------------------------------------------------------------------
    def update(self, dt, keys):
        if self.state != GameState.PLAYING:
            return

        self.player.update(dt, keys, self.maze)
        self.hazards.update(dt, self.maze)

        self.time_left -= dt
        self.time_taken += dt

        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= dt

        # Hazard contact: send player back to start, small time penalty
        hit_list = pygame.sprite.spritecollide(self.player, self.hazards, False)
        if hit_list:
            self.player.reset(*self.maze.start_pos)
            self.time_left = max(0.0, self.time_left - 3.0)
            self.hit_flash_timer = 1.0
            self.sound.play("hurt")

        # Reached the exit?
        if self.player.rect.colliderect(self.maze.exit_rect):
            new_best = save_best_time(self.level_number, self.time_taken)
            self.is_new_best = new_best
            self.sound.play("win")
            self.state = GameState.WIN
            return

        # Out of time?
        if self.time_left <= 0:
            self.time_left = 0.0
            self.sound.play("timeout")
            self.state = GameState.TIMEOUT

    # ------------------------------------------------------------------
    def draw(self):
        self.screen.fill(BLACK)

        if self.state == GameState.MENU:
            draw_menu(self.screen, self.font, self.big_font)
        elif self.state == GameState.PLAYING:
            self._draw_playing()
        elif self.state == GameState.WIN:
            best_time = get_best_time(self.level_number)
            final_level = self.level_number >= self.max_level
            draw_win(
                self.screen, self.font, self.big_font, self.level_number,
                self.time_taken, best_time, self.is_new_best, final_level,
            )
        elif self.state == GameState.TIMEOUT:
            draw_timeout(self.screen, self.font, self.big_font, self.level_number)

        pygame.display.flip()

    def _draw_playing(self):
        self.maze.draw(self.screen)
        self.hazards.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        best_time = get_best_time(self.level_number)
        draw_hud(self.screen, self.font, self.level_number, max(0.0, self.time_left), best_time)
        if self.hit_flash_timer > 0:
            draw_hazard_hit(self.screen, self.font)


# ======================================================================
# Entry point (from main.py)
# ======================================================================

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()

    game = Game(screen)
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                if not game.handle_event(event):
                    running = False

        keys = pygame.key.get_pressed()
        game.update(dt, keys)
        game.draw()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
