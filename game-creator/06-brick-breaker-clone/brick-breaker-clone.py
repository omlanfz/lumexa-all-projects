"""
Lumexa Brick Breaker Clone - single-file merged version.

Run with: python brick-breaker-clone.py

This file merges the original src/ modules (settings, audio, ball, paddle,
bricks, ui, game, main) into one self-contained script. All internal
imports between those modules have been removed since everything now
lives in a single namespace; external imports (pygame, os, sys, random)
are kept and deduplicated at the top.
"""

import os
import sys
import random
import pygame

# ==========================================================================
# settings.py - shared constants
# ==========================================================================

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GAME_TITLE = "Lumexa Brick Breaker"

# --- Colors ---
BLACK = (10, 10, 20)
WHITE = (255, 255, 255)
GRAY = (150, 150, 165)
CYAN = (80, 220, 255)
YELLOW = (255, 220, 80)
RED = (230, 70, 70)
GREEN = (100, 230, 130)
ORANGE = (255, 150, 60)
PURPLE = (190, 120, 255)
SILVER = (200, 205, 215)

# --- Paddle ---
PADDLE_WIDTH = 110
PADDLE_HEIGHT = 16
PADDLE_SPEED = 480
PADDLE_Y_OFFSET = 40  # distance from bottom of screen

# --- Ball ---
BALL_RADIUS = 8
BALL_BASE_SPEED = 320
BALL_MAX_SPEED = 620
BALL_SPEEDUP_PER_HIT = 6

# --- Bricks ---
BRICK_ROWS = 6
BRICK_COLS = 10
BRICK_WIDTH = 68
BRICK_HEIGHT = 24
BRICK_TOP_OFFSET = 70
BRICK_SPACING = 6
# Side margin is computed so BRICK_COLS bricks + spacing fit centered on screen
BRICK_SIDE_MARGIN = (SCREEN_WIDTH - (BRICK_COLS * BRICK_WIDTH + (BRICK_COLS - 1) * BRICK_SPACING)) // 2
TOUGH_BRICK_HEALTH = 2

# --- Gameplay ---
START_LIVES = 3
SCORE_NORMAL_BRICK = 10
SCORE_TOUGH_BRICK = 25

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_DIR = os.path.join(BASE_DIR, "sounds")


# ==========================================================================
# audio.py - Sound manager
# Defensive loading: missing files or no audio device never crash the game.
# ==========================================================================

class SoundManager:
    def __init__(self):
        self.enabled = True
        try:
            pygame.mixer.init()
        except pygame.error:
            self.enabled = False

        self.sounds = {}
        if self.enabled:
            self._load_sound("bounce", "bounce.wav", volume=0.4)
            self._load_sound("brick_break", "brick_break.wav", volume=0.6)
            self._load_sound("brick_hit", "brick_hit.wav", volume=0.4)
            self._load_sound("lose_life", "lose_life.wav", volume=0.6)
            self._load_sound("win", "win.wav", volume=0.6)

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


# ==========================================================================
# ball.py - Ball sprite.
# Rect-based (AABB) collision with proper reflection: walls bounce
# by flipping the relevant velocity component; the paddle reflects
# the ball based on where it was struck; bricks reflect based on
# which side (top/bottom vs left/right) was hit, determined by
# comparing overlap depth on each axis.
# ==========================================================================

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = BALL_BASE_SPEED
        angle = random.uniform(-0.6, 0.6)
        self.vx = self.speed * (1 if random.random() < 0.5 else -1)
        self.vy = -self.speed
        self._apply_angle(angle)

        self.launched = True

    def _apply_angle(self, angle_offset):
        """Nudge the current direction by an angle offset (radians-ish, simplified)."""
        speed = max(1.0, (self.vx ** 2 + self.vy ** 2) ** 0.5)
        direction_x = 1 if self.vx >= 0 else -1
        self.vx = direction_x * speed * (0.5 + abs(angle_offset))
        self.vy = -abs(speed)
        self._normalize_speed(speed)

    def _normalize_speed(self, target_speed):
        magnitude = max(1.0, (self.vx ** 2 + self.vy ** 2) ** 0.5)
        scale = target_speed / magnitude
        self.vx *= scale
        self.vy *= scale

    def update(self, dt, keys=None):
        self.rect.x += self.vx * dt
        self.rect.y += self.vy * dt

        # Bounce off left/right walls
        if self.rect.left <= 0:
            self.rect.left = 0
            self.vx = abs(self.vx)
        elif self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.vx = -abs(self.vx)

        # Bounce off the top wall
        if self.rect.top <= 0:
            self.rect.top = 0
            self.vy = abs(self.vy)

    def bounce_off_paddle(self, paddle_rect):
        """Reflect based on where the ball struck the paddle (angle varies by offset)."""
        offset = (self.rect.centerx - paddle_rect.centerx) / (paddle_rect.width / 2)
        offset = max(-1.0, min(1.0, offset))

        current_speed = min(
            BALL_MAX_SPEED, (self.vx ** 2 + self.vy ** 2) ** 0.5 + BALL_SPEEDUP_PER_HIT
        )
        max_angle_ratio = 0.8  # limits how horizontal the bounce can become
        self.vx = current_speed * offset * max_angle_ratio
        self.vy = -abs(current_speed * (1 - abs(offset) * max_angle_ratio))
        self._normalize_speed(current_speed)
        self.rect.bottom = paddle_rect.top

    def bounce_off_brick(self, brick_rect):
        """Determine which side of the brick was hit using overlap depth,
        and reflect the corresponding velocity component. Also speeds up
        slightly on every brick hit, capped at BALL_MAX_SPEED."""
        overlap_left = self.rect.right - brick_rect.left
        overlap_right = brick_rect.right - self.rect.left
        overlap_top = self.rect.bottom - brick_rect.top
        overlap_bottom = brick_rect.bottom - self.rect.top

        min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

        if min_overlap in (overlap_left, overlap_right):
            self.vx = -self.vx
        else:
            self.vy = -self.vy

        current_speed = min(
            BALL_MAX_SPEED, (self.vx ** 2 + self.vy ** 2) ** 0.5 + BALL_SPEEDUP_PER_HIT
        )
        self._normalize_speed(current_speed)

    def reset(self, x, y):
        self.rect.center = (x, y)
        self.speed = BALL_BASE_SPEED
        self.vx = self.speed * (1 if random.random() < 0.5 else -1) * 0.6
        self.vy = -self.speed
        self._normalize_speed(self.speed)


# ==========================================================================
# paddle.py - Paddle sprite.
# ==========================================================================

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(
            self.image, CYAN, self.image.get_rect(), border_radius=6
        )
        self.rect = self.image.get_rect(
            centerx=SCREEN_WIDTH // 2, bottom=SCREEN_HEIGHT - PADDLE_Y_OFFSET
        )
        self.speed = PADDLE_SPEED

    def update(self, dt, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed * dt
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(SCREEN_WIDTH, self.rect.right)

    def reset(self):
        self.rect.centerx = SCREEN_WIDTH // 2


# ==========================================================================
# bricks.py - Brick sprites and grid construction.
# Two brick types:
#   - Normal brick: destroyed in one hit.
#   - Tough brick:   requires two hits, changes color after the first hit.
# ==========================================================================

ROW_COLORS = [
    (230, 70, 70),
    (255, 150, 60),
    (255, 220, 80),
    (100, 230, 130),
    (80, 220, 255),
    (190, 120, 255),
]


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, row, tough=False):
        super().__init__()
        self.tough = tough
        self.health = TOUGH_BRICK_HEALTH if tough else 1
        self.max_health = self.health
        self.color = SILVER if tough else ROW_COLORS[row % len(ROW_COLORS)]
        self.score_value = SCORE_TOUGH_BRICK if tough else SCORE_NORMAL_BRICK

        self.image = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.rect = self.image.get_rect(topleft=(x, y))
        self._redraw()

    def _redraw(self):
        self.image.fill(self.color)
        pygame.draw.rect(self.image, (20, 20, 30), self.image.get_rect(), 2)
        if self.tough and self.health < self.max_health:
            # Show a crack line once the tough brick has been hit once
            pygame.draw.line(
                self.image, (60, 60, 70),
                (4, BRICK_HEIGHT // 2), (BRICK_WIDTH - 4, BRICK_HEIGHT // 2), 2,
            )

    def take_hit(self):
        """Return True if this hit destroyed the brick."""
        self.health -= 1
        if self.health <= 0:
            self.kill()
            return True
        self._redraw()
        return False


def build_brick_grid(bricks_group, all_sprites_group, level_number=1):
    """Build a full grid of bricks. Later levels include more tough bricks."""
    tough_row_threshold = 1 if level_number == 1 else 2

    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            x = BRICK_SIDE_MARGIN + col * (BRICK_WIDTH + BRICK_SPACING)
            y = BRICK_TOP_OFFSET + row * (BRICK_HEIGHT + BRICK_SPACING)
            is_tough = row < tough_row_threshold
            brick = Brick(x, y, row, tough=is_tough)
            bricks_group.add(brick)
            all_sprites_group.add(brick)


# ==========================================================================
# ui.py - UI helpers: HUD and screens.
# ==========================================================================

def draw_text_centered(screen, font, text, color, y):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(SCREEN_WIDTH // 2, y))
    screen.blit(surface, rect)


def draw_hud(screen, font, score, lives, level_number):
    hud_text = font.render(
        f"Score: {score}    Lives: {lives}    Level: {level_number}", True, WHITE
    )
    screen.blit(hud_text, (10, 10))


def draw_menu(screen, font, big_font):
    draw_text_centered(screen, big_font, "LUMEXA BRICK BREAKER", CYAN, 200)
    draw_text_centered(screen, font, "Press ENTER or SPACE to start", WHITE, 280)
    draw_text_centered(
        screen, font, "Arrows/A-D to move paddle, SPACE to launch the ball", GRAY, 320,
    )


def draw_serve_prompt(screen, font):
    draw_text_centered(screen, font, "Press SPACE to launch the ball", WHITE, 480)


def draw_level_clear(screen, font, big_font, score, final_level):
    draw_text_centered(screen, big_font, "LEVEL CLEAR!", GREEN, 220)
    draw_text_centered(screen, font, f"Score: {score}", WHITE, 290)
    if final_level:
        draw_text_centered(screen, font, "You cleared every level!", CYAN, 330)
        draw_text_centered(screen, font, "Press R to play again or ESC to quit", WHITE, 370)
    else:
        draw_text_centered(screen, font, "Press SPACE for the next level", WHITE, 370)


def draw_game_over(screen, font, big_font, score):
    draw_text_centered(screen, big_font, "GAME OVER", RED, 220)
    draw_text_centered(screen, font, f"Final Score: {score}", WHITE, 290)
    draw_text_centered(screen, font, "Press R to restart or ESC to quit", GRAY, 330)


# ==========================================================================
# game.py - Game state machine.
# States: MENU -> SERVE -> PLAYING -> LEVEL_CLEAR / GAME_OVER -> restart
# ==========================================================================

MAX_LEVEL = 2


class GameState:
    MENU = "menu"
    SERVE = "serve"
    PLAYING = "playing"
    LEVEL_CLEAR = "level_clear"
    GAME_OVER = "game_over"


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 26)
        self.big_font = pygame.font.SysFont(None, 52)

        self.sound = SoundManager()
        self.sound.play_music("theme.ogg")

        self.state = GameState.MENU
        self.level_number = 1
        self.score = 0
        self.lives = START_LIVES

        self.paddle = None
        self.ball = None
        self.bricks = None
        self.all_sprites = None

    # ------------------------------------------------------------------
    def start_new_game(self):
        self.level_number = 1
        self.score = 0
        self.lives = START_LIVES
        self._start_level(self.level_number)

    def _start_level(self, level_number):
        self.level_number = level_number
        self.paddle = Paddle()
        self.ball = Ball(self.paddle.rect.centerx, self.paddle.rect.top - 10)
        self.bricks = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.paddle)

        build_brick_grid(self.bricks, self.all_sprites, level_number)
        self.state = GameState.SERVE

    def _reset_ball_on_paddle(self):
        self.ball.rect.midbottom = (self.paddle.rect.centerx, self.paddle.rect.top - 2)

    # ------------------------------------------------------------------
    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return True

        if event.key == pygame.K_ESCAPE:
            if self.state in (GameState.PLAYING, GameState.SERVE):
                self.state = GameState.MENU
            else:
                return False
            return True

        if self.state == GameState.MENU:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.start_new_game()

        elif self.state == GameState.SERVE:
            if event.key == pygame.K_SPACE:
                self.state = GameState.PLAYING

        elif self.state == GameState.LEVEL_CLEAR:
            if self.level_number >= MAX_LEVEL:
                if event.key == pygame.K_r:
                    self.start_new_game()
            else:
                if event.key == pygame.K_SPACE:
                    self._start_level(self.level_number + 1)

        elif self.state == GameState.GAME_OVER:
            if event.key == pygame.K_r:
                self.start_new_game()

        return True

    # ------------------------------------------------------------------
    def update(self, dt, keys):
        if self.state == GameState.SERVE:
            self.paddle.update(dt, keys)
            self._reset_ball_on_paddle()
            return

        if self.state != GameState.PLAYING:
            return

        self.paddle.update(dt, keys)
        self.ball.update(dt)

        # Ball vs paddle
        if self.ball.rect.colliderect(self.paddle.rect) and self.ball.vy > 0:
            self.ball.bounce_off_paddle(self.paddle.rect)
            self.sound.play("bounce")

        # Ball vs bricks: only resolve the single closest brick per frame
        # to avoid double-bounce glitches when the ball clips a corner.
        hit_bricks = pygame.sprite.spritecollide(self.ball, self.bricks, False)
        if hit_bricks:
            closest_brick = min(
                hit_bricks,
                key=lambda b: (
                    (self.ball.rect.centerx - b.rect.centerx) ** 2
                    + (self.ball.rect.centery - b.rect.centery) ** 2
                ),
            )
            self.ball.bounce_off_brick(closest_brick.rect)
            destroyed = closest_brick.take_hit()
            if destroyed:
                self.score += closest_brick.score_value
                self.sound.play("brick_break")
            else:
                self.sound.play("brick_hit")

        # Ball fell below the screen: lose a life
        if self.ball.rect.top > SCREEN_HEIGHT:
            self.lives -= 1
            self.sound.play("lose_life")
            if self.lives > 0:
                self.paddle.reset()
                self.ball = Ball(self.paddle.rect.centerx, self.paddle.rect.top - 10)
                self._reset_ball_on_paddle()
                self.state = GameState.SERVE
            else:
                self.state = GameState.GAME_OVER

        # Level cleared: no bricks remaining
        if len(self.bricks) == 0 and self.state == GameState.PLAYING:
            self.sound.play("win")
            self.state = GameState.LEVEL_CLEAR

    # ------------------------------------------------------------------
    def draw(self):
        self.screen.fill(BLACK)

        if self.state == GameState.MENU:
            draw_menu(self.screen, self.font, self.big_font)
        elif self.state in (GameState.SERVE, GameState.PLAYING):
            self._draw_playing()
            if self.state == GameState.SERVE:
                draw_serve_prompt(self.screen, self.font)
        elif self.state == GameState.LEVEL_CLEAR:
            final_level = self.level_number >= MAX_LEVEL
            draw_level_clear(self.screen, self.font, self.big_font, self.score, final_level)
        elif self.state == GameState.GAME_OVER:
            draw_game_over(self.screen, self.font, self.big_font, self.score)

        pygame.display.flip()

    def _draw_playing(self):
        self.bricks.draw(self.screen)
        self.screen.blit(self.paddle.image, self.paddle.rect)
        self.screen.blit(self.ball.image, self.ball.rect)
        draw_hud(self.screen, self.font, self.score, self.lives, self.level_number)


# ==========================================================================
# main.py - entry point.
# Run with: python brick-breaker-clone.py
# ==========================================================================

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
