"""
Lumexa Space Shooter - single-file edition.

This file merges the original src/ modules (settings, audio, bullet, enemy,
effects, player, ui, game, main) into one self-contained script.

Run with: python space-shooter.py
"""

import os
import random
import sys

import pygame

# ======================================================================
# Settings / constants  (was: settings.py)
# ======================================================================

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GAME_TITLE = "Lumexa Space Shooter"

# --- Colors ---
BLACK = (8, 8, 20)
DARK_BLUE = (14, 18, 40)
WHITE = (255, 255, 255)
GRAY = (150, 150, 165)
CYAN = (80, 220, 255)
YELLOW = (255, 220, 80)
ORANGE = (255, 150, 60)
RED = (230, 70, 70)
GREEN = (100, 230, 130)
PURPLE = (190, 120, 255)

# --- Player ---
PLAYER_START_HEALTH = 100
PLAYER_SPEED = 320
PLAYER_START_LIVES = 3
PLAYER_SHOOT_COOLDOWN = 0.25  # seconds between shots
PLAYER_INVULNERABLE_TIME = 2.0  # seconds of invulnerability after respawn

# --- Bullets ---
PLAYER_BULLET_SPEED = 560
ENEMY_BULLET_SPEED = 260

# --- Enemies / waves ---
ENEMY_BASE_SPEED = 60
ENEMY_BASE_SHOOT_INTERVAL = 2.2
WAVE_INTERVAL = 18.0  # seconds before a new wave spawns automatically
MAX_ENEMIES_PER_WAVE = 14

# --- Scoring ---
SCORE_PER_KILL = 25

# --- Paths ---
# Kept relative to this file's location (project root), same behavior as
# before where SOUND_DIR was relative to the module's own directory.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_DIR = os.path.join(BASE_DIR, "sounds")


# ======================================================================
# Sound manager  (was: audio.py)
# ======================================================================

class SoundManager:
    def __init__(self):
        self.enabled = True
        try:
            pygame.mixer.init()
        except pygame.error:
            self.enabled = False

        self.sounds = {}
        self.muted = False

        if self.enabled:
            self._load_sound("shoot", "shoot.wav", volume=0.4)
            self._load_sound("explosion", "explosion.wav", volume=0.6)
            self._load_sound("hit", "hit.wav", volume=0.6)
            self._load_sound("powerup", "powerup.wav", volume=0.5)
            self._load_sound("gameover", "gameover.wav", volume=0.6)

    def _load_sound(self, name, filename, volume=0.5):
        path = os.path.join(SOUND_DIR, filename)
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            self.sounds[name] = sound
        except (pygame.error, FileNotFoundError):
            self.sounds[name] = None

    def play(self, name):
        if not self.enabled or self.muted:
            return
        sound = self.sounds.get(name)
        if sound is not None:
            sound.play()

    def play_music(self, filename="theme.ogg", volume=0.25, loop=True):
        if not self.enabled:
            return
        path = os.path.join(SOUND_DIR, filename)
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0 if self.muted else volume)
            pygame.mixer.music.play(loops=-1 if loop else 0)
        except (pygame.error, FileNotFoundError):
            pass

    def toggle_mute(self):
        self.muted = not self.muted
        if self.enabled:
            try:
                pygame.mixer.music.set_volume(0 if self.muted else 0.25)
            except pygame.error:
                pass


# ======================================================================
# Bullet sprite  (was: bullet.py)
# ======================================================================

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction=-1, color=(255, 220, 80), speed=None):
        super().__init__()
        self.image = pygame.Surface((5, 16), pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, self.image.get_rect(), border_radius=2)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction  # -1 = moving up (player), 1 = moving down (enemy)
        self.speed = speed if speed is not None else PLAYER_BULLET_SPEED

    def update(self, dt, keys=None):
        self.rect.y += self.direction * self.speed * dt
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or \
           self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()


# ======================================================================
# Enemy sprite and wave spawning  (was: enemy.py)
# ======================================================================

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, wave):
        super().__init__()
        self.image = pygame.Surface((36, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, RED, [(0, 0), (36, 0), (18, 30)])
        pygame.draw.circle(self.image, ORANGE, (18, 10), 4)
        self.rect = self.image.get_rect(center=(x, y))

        self.direction = random.choice([-1, 1])
        self.horizontal_speed = ENEMY_BASE_SPEED + wave * 8
        self.shoot_timer = random.uniform(0, ENEMY_BASE_SHOOT_INTERVAL)
        self.shoot_interval = max(0.7, ENEMY_BASE_SHOOT_INTERVAL - wave * 0.12)
        self.health = 1 if wave < 4 else 2  # tougher enemies from wave 4 onward
        self.want_to_shoot = False

    def update(self, dt, keys=None):
        self.rect.x += self.direction * self.horizontal_speed * dt
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.direction *= -1
            self.rect.left = max(0, self.rect.left)
            self.rect.right = min(SCREEN_WIDTH, self.rect.right)

        self.shoot_timer += dt
        if self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0.0
            self.want_to_shoot = True
        else:
            self.want_to_shoot = False

    def take_hit(self):
        """Return True if this hit destroyed the enemy."""
        self.health -= 1
        if self.health <= 0:
            self.kill()
            return True
        return False

    def make_bullet(self):
        return Bullet(
            self.rect.centerx,
            self.rect.bottom,
            direction=1,
            color=ORANGE,
            speed=ENEMY_BULLET_SPEED,
        )


def spawn_wave(wave_number, enemies_group, all_sprites_group):
    """Spawn a formation of enemies scaled to the current wave number."""
    enemy_count = min(4 + wave_number, MAX_ENEMIES_PER_WAVE)
    cols = min(enemy_count, 7)
    spacing_x = SCREEN_WIDTH // (cols + 1)

    for i in range(enemy_count):
        row = i // cols
        col = i % cols
        x = spacing_x * (col + 1)
        y = 50 + row * 55
        enemy = Enemy(x, y, wave_number)
        enemies_group.add(enemy)
        all_sprites_group.add(enemy)


# ======================================================================
# Visual effects  (was: effects.py)
# ======================================================================

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, max_radius=28, duration=0.35):
        super().__init__()
        self.x = x
        self.y = y
        self.max_radius = max_radius
        self.duration = duration
        self.age = 0.0
        self.image = pygame.Surface((max_radius * 2, max_radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, dt, keys=None):
        self.age += dt
        if self.age >= self.duration:
            self.kill()
            return

        progress = self.age / self.duration
        radius = max(1, int(self.max_radius * progress))
        alpha = max(0, 255 - int(255 * progress))

        self.image.fill((0, 0, 0, 0))
        color_outer = (*ORANGE, alpha)
        color_inner = (*YELLOW, alpha)
        pygame.draw.circle(self.image, color_outer, (self.max_radius, self.max_radius), radius)
        pygame.draw.circle(
            self.image, color_inner, (self.max_radius, self.max_radius), max(1, radius // 2)
        )


class Starfield:
    """A simple procedurally-drawn scrolling starfield background."""

    def __init__(self, width, height, count=80):
        self.width = width
        self.height = height
        self.stars = []
        for _ in range(count):
            self.stars.append(
                {
                    "x": random.randint(0, width),
                    "y": random.randint(0, height),
                    "speed": random.uniform(30, 140),
                    "size": random.randint(1, 3),
                }
            )

    def update(self, dt):
        for star in self.stars:
            star["y"] += star["speed"] * dt
            if star["y"] > self.height:
                star["y"] = 0
                star["x"] = random.randint(0, self.width)

    def draw(self, screen):
        for star in self.stars:
            brightness = 150 + star["size"] * 30
            color = (min(255, brightness), min(255, brightness), 255)
            pygame.draw.circle(
                screen, color, (int(star["x"]), int(star["y"])), star["size"]
            )


# ======================================================================
# Player sprite  (was: player.py)
# ======================================================================

class Player(pygame.sprite.Sprite):
    """The player's ship: movement, shooting cooldown, health, and
    brief invulnerability after taking damage."""

    def __init__(self, x, y):
        super().__init__()
        self.image_normal = self._build_image(CYAN)
        self.image_hit = self._build_image((255, 255, 255))
        self.image = self.image_normal
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = PLAYER_SPEED
        self.health = PLAYER_START_HEALTH
        self.max_health = PLAYER_START_HEALTH
        self.shoot_timer = 0.0
        self.invulnerable_timer = 0.0
        self.flicker_timer = 0.0

    @staticmethod
    def _build_image(color):
        image = pygame.Surface((44, 36), pygame.SRCALPHA)
        pygame.draw.polygon(image, color, [(22, 0), (0, 36), (44, 36)])
        pygame.draw.polygon(image, (255, 255, 255), [(22, 6), (12, 30), (32, 30)], width=1)
        return image

    def update(self, dt, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed * dt
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed * dt
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed * dt

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(SCREEN_WIDTH, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(SCREEN_HEIGHT, self.rect.bottom)

        if self.shoot_timer > 0:
            self.shoot_timer -= dt

        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= dt
            self.flicker_timer += dt
            # Flicker between normal and hit-flash art while invulnerable
            self.image = self.image_hit if int(self.flicker_timer * 10) % 2 == 0 else self.image_normal
        else:
            self.image = self.image_normal

    def can_shoot(self):
        return self.shoot_timer <= 0

    def shoot(self):
        """Create and return a new Bullet if the cooldown allows it, else None."""
        if not self.can_shoot():
            return None
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        return Bullet(self.rect.centerx, self.rect.top, direction=-1, color=(255, 220, 80))

    def take_damage(self, amount):
        if self.invulnerable_timer > 0:
            return False  # damage ignored while invulnerable
        self.health = max(0, self.health - amount)
        self.invulnerable_timer = PLAYER_INVULNERABLE_TIME
        return True

    def is_alive(self):
        return self.health > 0

    def reset(self):
        self.health = self.max_health
        self.shoot_timer = 0.0
        self.invulnerable_timer = 0.0
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)


# ======================================================================
# UI helpers: HUD and text screens  (was: ui.py)
# ======================================================================

def draw_text_centered(screen, font, text, color, y):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(SCREEN_WIDTH // 2, y))
    screen.blit(surface, rect)


def draw_hud(screen, font, score, lives, health, max_health, wave):
    hud_text = font.render(
        f"Score: {score}    Lives: {lives}    Wave: {wave}", True, WHITE
    )
    screen.blit(hud_text, (10, 10))

    # Health bar
    bar_width = 200
    bar_height = 16
    bar_x = 10
    bar_y = 40
    pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height), 1)
    fill_width = int(bar_width * max(0, health) / max_health)
    color = GREEN if health > max_health * 0.3 else RED
    pygame.draw.rect(screen, color, (bar_x + 2, bar_y + 2, max(0, fill_width - 4), bar_height - 4))


def draw_menu(screen, font, big_font, high_score):
    draw_text_centered(screen, big_font, "LUMEXA SPACE SHOOTER", CYAN, 200)
    draw_text_centered(screen, font, "Press ENTER or SPACE to launch", WHITE, 280)
    draw_text_centered(
        screen, font, "Arrows/WASD to move, SPACE to fire, M to mute, ESC to quit",
        GRAY, 320,
    )
    draw_text_centered(screen, font, f"Best Score: {high_score}", GRAY, 360)


def draw_game_over(screen, font, big_font, score, high_score):
    draw_text_centered(screen, big_font, "SHIP DESTROYED", RED, 210)
    draw_text_centered(screen, font, f"Final Score: {score}", WHITE, 280)
    draw_text_centered(screen, font, f"Best Score: {high_score}", GRAY, 310)
    draw_text_centered(screen, font, "Press R to restart or ESC to quit", WHITE, 350)


def draw_paused(screen, font, big_font):
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))
    draw_text_centered(screen, big_font, "PAUSED", WHITE, 260)
    draw_text_centered(screen, font, "Press P to resume", GRAY, 320)


# ======================================================================
# Game state machine  (was: game.py)
# States: MENU -> PLAYING -> (PAUSED) -> GAME_OVER -> restart to MENU/PLAYING
# ======================================================================

class GameState:
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 28)
        self.big_font = pygame.font.SysFont(None, 56)

        self.sound = SoundManager()
        self.sound.play_music("theme.ogg")

        self.starfield = Starfield(SCREEN_WIDTH, SCREEN_HEIGHT, count=90)

        self.state = GameState.MENU
        self.high_score = 0
        self.final_score = 0

        self.player = None
        self.all_sprites = None
        self.player_bullets = None
        self.enemy_bullets = None
        self.enemies = None
        self.effects = None

        self.score = 0
        self.lives = PLAYER_START_LIVES
        self.wave_number = 1
        self.wave_timer = 0.0

    # ------------------------------------------------------------------
    def start_new_game(self):
        """(Re)initialize every piece of mutable session state."""
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)
        self.all_sprites = pygame.sprite.Group(self.player)
        self.player_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()

        self.score = 0
        self.lives = PLAYER_START_LIVES
        self.wave_number = 1
        self.wave_timer = 0.0

        spawn_wave(self.wave_number, self.enemies, self.all_sprites)
        self.state = GameState.PLAYING

    # ------------------------------------------------------------------
    def handle_event(self, event):
        """Returns False if the game should quit, True otherwise."""
        if event.type != pygame.KEYDOWN:
            return True

        if event.key == pygame.K_ESCAPE:
            if self.state == GameState.PLAYING or self.state == GameState.PAUSED:
                self.state = GameState.MENU
            else:
                return False
            return True

        if event.key == pygame.K_m:
            self.sound.toggle_mute()

        if self.state == GameState.MENU:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.start_new_game()

        elif self.state == GameState.PLAYING:
            if event.key == pygame.K_SPACE:
                bullet = self.player.shoot()
                if bullet is not None:
                    self.player_bullets.add(bullet)
                    self.all_sprites.add(bullet)
                    self.sound.play("shoot")
            elif event.key == pygame.K_p:
                self.state = GameState.PAUSED

        elif self.state == GameState.PAUSED:
            if event.key == pygame.K_p:
                self.state = GameState.PLAYING

        elif self.state == GameState.GAME_OVER:
            if event.key == pygame.K_r:
                self.start_new_game()

        return True

    # ------------------------------------------------------------------
    def update(self, dt, keys):
        self.starfield.update(dt)

        if self.state != GameState.PLAYING:
            return

        self.player.update(dt, keys)
        self.enemies.update(dt)
        self.player_bullets.update(dt)
        self.enemy_bullets.update(dt)
        self.effects.update(dt)

        # Continuous fire while holding SPACE, gated by the player's cooldown
        if keys[pygame.K_SPACE]:
            bullet = self.player.shoot()
            if bullet is not None:
                self.player_bullets.add(bullet)
                self.all_sprites.add(bullet)
                self.sound.play("shoot")

        # Enemy "AI decisions" -> spawn bullets
        for enemy in list(self.enemies):
            if getattr(enemy, "want_to_shoot", False):
                bullet = enemy.make_bullet()
                self.enemy_bullets.add(bullet)
                self.all_sprites.add(bullet)

        # Player bullets vs enemies
        hits = pygame.sprite.groupcollide(self.player_bullets, self.enemies, True, False)
        for bullet, hit_enemies in hits.items():
            for enemy in hit_enemies:
                destroyed = enemy.take_hit()
                if destroyed:
                    self.score += SCORE_PER_KILL
                    self._spawn_explosion(enemy.rect.center)
                    self.sound.play("explosion")

        # Enemy bullets vs player
        hit_list = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
        for _ in hit_list:
            if self.player.take_damage(15):
                self.sound.play("hit")

        # Enemies ramming the player
        rammed = pygame.sprite.spritecollide(self.player, self.enemies, True)
        for enemy in rammed:
            self._spawn_explosion(enemy.rect.center)
            if self.player.take_damage(30):
                self.sound.play("hit")

        # Wave progression
        self.wave_timer += dt
        if len(self.enemies) == 0 or self.wave_timer >= WAVE_INTERVAL:
            self.wave_timer = 0.0
            self.wave_number += 1
            spawn_wave(self.wave_number, self.enemies, self.all_sprites)

        # Player death -> lose a life or game over
        if not self.player.is_alive():
            self.lives -= 1
            if self.lives > 0:
                self.player.reset()
            else:
                self.final_score = self.score
                self.high_score = max(self.high_score, self.score)
                self.sound.play("gameover")
                self.state = GameState.GAME_OVER

    def _spawn_explosion(self, pos):
        explosion = Explosion(pos[0], pos[1])
        self.effects.add(explosion)

    # ------------------------------------------------------------------
    def draw(self):
        self.screen.fill(BLACK)
        self.starfield.draw(self.screen)

        if self.state == GameState.MENU:
            draw_menu(self.screen, self.font, self.big_font, self.high_score)
        elif self.state in (GameState.PLAYING, GameState.PAUSED):
            self._draw_playing()
            if self.state == GameState.PAUSED:
                draw_paused(self.screen, self.font, self.big_font)
        elif self.state == GameState.GAME_OVER:
            draw_game_over(self.screen, self.font, self.big_font, self.final_score, self.high_score)

        pygame.display.flip()

    def _draw_playing(self):
        self.all_sprites.draw(self.screen)
        self.effects.draw(self.screen)
        draw_hud(
            self.screen,
            self.font,
            self.score,
            self.lives,
            self.player.health,
            self.player.max_health,
            self.wave_number,
        )


# ======================================================================
# Entry point  (was: main.py)
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
