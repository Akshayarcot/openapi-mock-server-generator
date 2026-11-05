import math
import random
import pygame
from .fruit import Fruit, Particle
from .audio import SoundManager

WHITE = (255, 255, 255)
DARK_BLUE = (20, 25, 45)
BOMB_BLACK = (30, 30, 30)
FRUIT_COLORS = [
    (235, 65, 65),    # Watermelon / Apple Red
    (245, 140, 35),   # Orange
    (240, 215, 45),   # Banana / Lemon Yellow
    (80, 200, 90),    # Kiwi / Lime Green
    (170, 75, 220),   # Plum / Grape Purple
]

DIFFICULTY_PRESETS = {
    "Easy": {
        "spawn_interval": 65,
        "bomb_chance": 0.08,
        "speed_scale": 0.85,
        "label": "Easy"
    },
    "Medium": {
        "spawn_interval": 50,
        "bomb_chance": 0.15,
        "speed_scale": 1.0,
        "label": "Medium"
    },
    "Hard": {
        "spawn_interval": 36,
        "bomb_chance": 0.25,
        "speed_scale": 1.25,
        "label": "Hard"
    }
}


class GameEngine:
    def __init__(self, width, height, sounds_dir=None):
        self.width = width
        self.height = height

        # Audio manager
        self.sound_mgr = SoundManager(sounds_dir=sounds_dir)

        # Game entity collections
        self.fruits = []
        self.halves = []
        self.particles = []
        self.trail = []  # Recent blade swipe positions
        self.last_pos = None

        # Difficulty & Progression
        self.difficulty = "Medium"
        self._apply_difficulty(self.difficulty)
        self._spawn_timer = 0

        # Stats
        self.lives = 3
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.game_over_reason = ""
        self._game_over_sound_played = False

        # Fonts
        self._init_fonts()

        # Replay UI buttons
        self.buttons = {}
        self.mouse_pos = (0, 0)

    def _init_fonts(self):
        try:
            self.font_score = pygame.font.SysFont("Helvetica, Arial", 26, bold=True)
            self.font_title = pygame.font.SysFont("Helvetica, Arial", 52, bold=True)
            self.font_subtitle = pygame.font.SysFont("Helvetica, Arial", 24)
            self.font_btn = pygame.font.SysFont("Helvetica, Arial", 20, bold=True)
        except Exception:
            self.font_score = pygame.font.Font(None, 30)
            self.font_title = pygame.font.Font(None, 60)
            self.font_subtitle = pygame.font.Font(None, 28)
            self.font_btn = pygame.font.Font(None, 24)

    def _apply_difficulty(self, diff_name):
        preset = DIFFICULTY_PRESETS.get(diff_name, DIFFICULTY_PRESETS["Medium"])
        self.difficulty = diff_name
        self.spawn_interval = preset["spawn_interval"]
        self.bomb_chance = preset["bomb_chance"]
        self.speed_scale = preset["speed_scale"]

    def reset(self, difficulty=None):
        """Reset game state for a new game session with chosen difficulty."""
        if difficulty:
            self._apply_difficulty(difficulty)
        self.fruits.clear()
        self.halves.clear()
        self.particles.clear()
        self.trail.clear()
        self.last_pos = None
        self._spawn_timer = 0
        self.lives = 3
        self.score = 0
        self.game_over = False
        self.game_over_reason = ""
        self._game_over_sound_played = False

    def spawn_fruit(self):
        x = random.randint(70, self.width - 70)
        vy = -random.uniform(13.5, 16.5) * self.speed_scale
        vx = random.uniform(-2.5, 2.5)
        gravity = 0.35
        kind = "bomb" if random.random() < self.bomb_chance else "fruit"

        fruit = Fruit(x, self.height + 30, vx, vy, gravity, radius=28, kind=kind)
        fruit.color = BOMB_BLACK if kind == "bomb" else random.choice(FRUIT_COLORS)
        self.fruits.append(fruit)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
            self._handle_motion(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.mouse_pos = event.pos
            self._handle_click(event.pos)
        elif event.type == pygame.KEYDOWN:
            self._handle_keypress(event.key)

    def _handle_motion(self, pos):
        if self.game_over:
            return

        # Continuous Collision Detection (Task 1)
        # Check both line segment from last_pos -> pos AND point containment
        for fruit in self.fruits:
            if not fruit.sliced:
                hit = False
                if self.last_pos is not None:
                    hit = fruit.intersects_segment(self.last_pos, pos)
                if not hit:
                    hit = fruit.contains_point(pos[0], pos[1])
                if hit:
                    self._slice(fruit)

        self.last_pos = pos
        self.trail.append(pos)
        if len(self.trail) > 12:
            self.trail.pop(0)

    def _handle_click(self, pos):
        if self.game_over:
            # Check clicks on difficulty buttons
            for diff, rect in self.buttons.items():
                if rect.collidepoint(pos):
                    if diff == "Quit":
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
                    else:
                        self.reset(diff)
                    return
        else:
            # Single click slice attempt
            for fruit in self.fruits:
                if not fruit.sliced and fruit.contains_point(pos[0], pos[1]):
                    self._slice(fruit)

    def _handle_keypress(self, key):
        if self.game_over:
            if key in (pygame.K_1, pygame.K_e):
                self.reset("Easy")
            elif key in (pygame.K_2, pygame.K_m, pygame.K_SPACE, pygame.K_RETURN):
                self.reset("Medium")
            elif key in (pygame.K_3, pygame.K_h):
                self.reset("Hard")
            elif key in (pygame.K_q, pygame.K_ESCAPE):
                pygame.event.post(pygame.event.Event(pygame.QUIT))
        else:
            if key == pygame.K_r:
                self.reset(self.difficulty)

    def _slice(self, fruit):
        fruit.sliced = True
        halves, particles = fruit.split()
        self.halves.extend(halves)
        self.particles.extend(particles)

        if fruit.kind == "bomb":
            # Task 4: Bomb sound
            self.sound_mgr.play_bomb()
            self._trigger_game_over("Bomb Detonated!")
        else:
            # Task 4: Slice sound
            self.sound_mgr.play_slice()
            self.score += 1
            if self.score > self.high_score:
                self.high_score = self.score

    def _trigger_game_over(self, reason):
        self.game_over = True
        self.game_over_reason = reason
        if not self._game_over_sound_played:
            self.sound_mgr.play_game_over()
            self._game_over_sound_played = True
        print(f"Game over! [{reason}] Final score: {self.score}")

    def handle_input(self):
        pass

    def update(self):
        # Always update particles & halves even during game-over for smooth decay
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if not p.is_dead()]

        for h in self.halves:
            h.update()
        self.halves = [h for h in self.halves if not h.off_screen(self.height)]

        if self.game_over:
            return

        # Gradually fade trail when mouse is stationary
        if self.trail and random.random() < 0.2:
            self.trail.pop(0)

        # Spawn fruit
        self._spawn_timer += 1
        if self._spawn_timer >= self.spawn_interval:
            self._spawn_timer = 0
            self.spawn_fruit()

        still_alive = []
        for fruit in self.fruits:
            fruit.update()
            if fruit.sliced:
                continue
            if fruit.off_screen(self.height):
                if fruit.kind == "fruit":
                    self.lives -= 1
                    # Small red penalty splash
                    for _ in range(8):
                        self.particles.append(Particle(fruit.x, self.height - 10, (220, 60, 60)))
                continue
            still_alive.append(fruit)
        self.fruits = still_alive

        if self.lives <= 0 and not self.game_over:
            self._trigger_game_over("Out of Lives!")

    def render(self, screen):
        # 1. Render active fruits
        for fruit in self.fruits:
            fruit.render(screen)

        # 2. Render sliced halves
        for half in self.halves:
            half.render(screen)

        # 3. Render splash and explosion particles
        for p in self.particles:
            if p is not None:
                p.render(screen)

        # 4. Render blade trail (glowing white / cyan slash)
        if len(self.trail) >= 2:
            for i in range(len(self.trail) - 1):
                progress = (i + 1) / len(self.trail)
                width = max(1, int(progress * 6))
                color = (
                    int(180 + 75 * progress),
                    int(220 + 35 * progress),
                    255
                )
                pygame.draw.line(screen, color, self.trail[i], self.trail[i + 1], width)

        # 5. Render HUD (Score, Lives, High Score, Difficulty)
        self._render_hud(screen)

        # 6. Render Game Over Screen (Task 2 & 3)
        if self.game_over:
            self._render_game_over(screen)

    def _render_hud(self, screen):
        score_text = self.font_score.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (16, 14))

        high_text = self.font_subtitle.render(f"Best: {self.high_score}", True, (180, 200, 220))
        screen.blit(high_text, (16, 44))

        diff_badge = self.font_subtitle.render(f"Diff: {self.difficulty}", True, (240, 200, 100))
        screen.blit(diff_badge, (self.width // 2 - diff_badge.get_width() // 2, 14))

        # Hearts for lives
        lives_label = self.font_score.render("Lives:", True, WHITE)
        screen.blit(lives_label, (self.width - 200, 14))
        for i in range(3):
            heart_color = (240, 60, 60) if i < self.lives else (80, 80, 90)
            hx = self.width - 110 + i * 30
            hy = 26
            pygame.draw.circle(screen, heart_color, (hx, hy), 9)

    def _render_game_over(self, screen):
        # Dark translucent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((10, 12, 25, 215))
        screen.blit(overlay, (0, 0))

        # Game Over Banner
        title_surf = self.font_title.render("GAME OVER", True, (245, 60, 60))
        title_shadow = self.font_title.render("GAME OVER", True, (20, 20, 20))
        screen.blit(title_shadow, (self.width // 2 - title_surf.get_width() // 2 + 2, 112))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 110))

        # Subtitle / Reason
        reason_surf = self.font_subtitle.render(self.game_over_reason, True, (240, 210, 90))
        screen.blit(reason_surf, (self.width // 2 - reason_surf.get_width() // 2, 175))

        # Score Summary Card
        score_box = pygame.Rect(self.width // 2 - 160, 215, 320, 90)
        pygame.draw.rect(screen, (30, 36, 60), score_box, border_radius=10)
        pygame.draw.rect(screen, (70, 85, 140), score_box, width=2, border_radius=10)

        final_surf = self.font_score.render(f"Final Score: {self.score}", True, WHITE)
        best_surf = self.font_subtitle.render(f"High Score: {self.high_score}", True, (160, 220, 160))
        screen.blit(final_surf, (self.width // 2 - final_surf.get_width() // 2, 230))
        screen.blit(best_surf, (self.width // 2 - best_surf.get_width() // 2, 265))

        # Prompt for Replay
        prompt_surf = self.font_subtitle.render("Select Difficulty to Play Again:", True, (220, 225, 235))
        screen.blit(prompt_surf, (self.width // 2 - prompt_surf.get_width() // 2, 325))

        # Replay buttons: Easy, Medium, Hard, Quit
        btn_configs = [
            ("Easy", "1. Easy", (40, 160, 90), (60, 200, 120)),
            ("Medium", "2. Medium", (210, 140, 30), (240, 175, 50)),
            ("Hard", "3. Hard", (200, 50, 50), (240, 80, 80)),
            ("Quit", "Q. Exit", (80, 85, 100), (120, 125, 145)),
        ]

        btn_w, btn_h = 135, 42
        spacing = 16
        total_w = len(btn_configs) * btn_w + (len(btn_configs) - 1) * spacing
        start_x = (self.width - total_w) // 2
        btn_y = 370

        self.buttons = {}
        for idx, (diff_key, label, base_col, hover_col) in enumerate(btn_configs):
            bx = start_x + idx * (btn_w + spacing)
            rect = pygame.Rect(bx, btn_y, btn_w, btn_h)
            self.buttons[diff_key] = rect

            is_hovered = rect.collidepoint(self.mouse_pos)
            color = hover_col if is_hovered else base_col
            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, WHITE if is_hovered else (200, 200, 200), rect, width=2, border_radius=8)

            txt = self.font_btn.render(label, True, WHITE)
            screen.blit(txt, (bx + (btn_w - txt.get_width()) // 2, btn_y + (btn_h - txt.get_height()) // 2))

        # Bottom Hint
        hint = self.font_subtitle.render("Keyboard: [1] Easy  [2] Medium  [3] Hard  [Q] Quit", True, (150, 160, 180))
        screen.blit(hint, (self.width // 2 - hint.get_width() // 2, 440))
