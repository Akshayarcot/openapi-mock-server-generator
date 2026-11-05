import os
import sys
import math
import random
import numpy as np
import cv2
import pygame

# Set up offscreen SDL driver
os.environ["SDL_VIDEODRIVER"] = "dummy"

# Import enhanced engine
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from game.game_engine import GameEngine as EnhancedEngine
from game.fruit import Fruit as EnhancedFruit

# Import original engine cleanly using importlib
import importlib.util
SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "fruit-ninja-src"))

# Set up package namespace for original modules
import types
orig_pkg = types.ModuleType("orig_game")
orig_pkg.__path__ = [os.path.join(SRC_PATH, "game")]
sys.modules["orig_game"] = orig_pkg

spec_orig_fruit = importlib.util.spec_from_file_location("orig_game.fruit", os.path.join(SRC_PATH, "game", "fruit.py"))
orig_fruit_mod = importlib.util.module_from_spec(spec_orig_fruit)
sys.modules["orig_game.fruit"] = orig_fruit_mod
spec_orig_fruit.loader.exec_module(orig_fruit_mod)
OriginalFruit = orig_fruit_mod.Fruit

spec_orig_engine = importlib.util.spec_from_file_location("orig_game.game_engine", os.path.join(SRC_PATH, "game", "game_engine.py"))
orig_engine_mod = importlib.util.module_from_spec(spec_orig_engine)
sys.modules["orig_game.game_engine"] = orig_engine_mod
spec_orig_engine.loader.exec_module(orig_engine_mod)
OriginalEngine = orig_engine_mod.GameEngine


def record_before_video(output_path, duration_sec=10, fps=30):
    print(f"[Recorder] Recording BEFORE video to {output_path}...")
    pygame.init()
    width, height = 700, 600
    surf = pygame.Surface((width, height))
    clock = pygame.time.Clock()

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_path, fourcc, float(fps), (width, height))

    engine = OriginalEngine(width, height)
    engine.spawn_interval = 45

    font_hud = pygame.font.SysFont("Arial", 18, bold=True)
    font_alert = pygame.font.SysFont("Arial", 22, bold=True)

    total_frames = int(duration_sec * fps)
    
    # Controlled fruit launch for reproducible demonstration of the bug
    # We will spawn a fruit right in the center arc and perform a fast swipe that jumps across it
    for frame_idx in range(total_frames):
        surf.fill((20, 25, 45))

        # Scripted events:
        # At frame 20, spawn fruit
        if frame_idx == 20:
            f = OriginalFruit(350, height + 20, 0, -14, 0.35, kind="fruit")
            f.color = (230, 60, 60)
            engine.fruits.append(f)

        # At frame 60: fast swipe across (150, 280) -> (550, 280) jumping right over fruit at (350, 280)
        if frame_idx == 60:
            # First position far left
            engine._handle_motion((160, 270))
        elif frame_idx == 61:
            # Second position far right (fast jump!)
            # In original code, contains_point only checks (540, 270), so it MISSES!
            engine._handle_motion((540, 270))
        elif 62 <= frame_idx <= 75:
            # Trail fades
            if engine.trail:
                engine.trail.pop(0)

        # At frame 120, spawn another fruit
        if frame_idx == 120:
            f2 = OriginalFruit(250, height + 20, 1.0, -13, 0.35, kind="fruit")
            f2.color = (240, 140, 30)
            engine.fruits.append(f2)

        # At frame 160: another fast swipe jumping across f2
        if frame_idx == 155:
            engine._handle_motion((120, 310))
        elif frame_idx == 156:
            engine._handle_motion((480, 310))
        elif 157 <= frame_idx <= 170:
            if engine.trail:
                engine.trail.pop(0)

        # Let fruits fall off screen to trigger lives drop to 0
        if frame_idx == 180:
            # Force lives to 0 to show the broken game over state
            engine.lives = 0

        engine.update()
        engine.render(surf)

        # Overlay descriptive watermark for submission video
        banner = pygame.Surface((width, 36), pygame.SRCALPHA)
        banner.fill((180, 20, 20, 220))
        surf.blit(banner, (0, height - 36))
        txt = font_hud.render("BEFORE: Fast Swipe Bug (Slice Missed) & Frozen Terminal Game Over", True, (255, 255, 255))
        surf.blit(txt, (width // 2 - txt.get_width() // 2, height - 28))

        if 60 <= frame_idx <= 90:
            alert = font_alert.render("FAST SWIPE JUMPED OVER FRUIT -> SLICE MISSED!", True, (255, 220, 50))
            surf.blit(alert, (width // 2 - alert.get_width() // 2, 80))

        if frame_idx >= 180:
            alert2 = font_alert.render("GAME OVER: Screen frozen! Only printed to terminal", True, (255, 100, 100))
            surf.blit(alert2, (width // 2 - alert2.get_width() // 2, 280))

        # Convert pygame surface to OpenCV BGR frame
        frame_rgb = pygame.surfarray.array3d(surf)
        frame_bgr = cv2.cvtColor(np.transpose(frame_rgb, (1, 0, 2)), cv2.COLOR_RGB2BGR)
        writer.write(frame_bgr)

    writer.release()
    print(f"[Recorder] Finished BEFORE video: {output_path} ({total_frames} frames)")


def record_after_video(output_path, duration_sec=10, fps=30):
    print(f"[Recorder] Recording AFTER video to {output_path}...")
    pygame.init()
    width, height = 700, 600
    surf = pygame.Surface((width, height))
    clock = pygame.time.Clock()

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_path, fourcc, float(fps), (width, height))

    engine = EnhancedEngine(width, height)
    total_frames = int(duration_sec * fps)

    font_hud = pygame.font.SysFont("Arial", 18, bold=True)
    font_alert = pygame.font.SysFont("Arial", 22, bold=True)

    for frame_idx in range(total_frames):
        surf.fill((20, 25, 45))

        # 1. First Fruit Spawn at frame 15
        if frame_idx == 15:
            f1 = EnhancedFruit(350, height + 20, 0, -14, 0.35, kind="fruit")
            f1.color = (235, 65, 65)
            engine.fruits.append(f1)

        # 2. Fast swipe across fruit at frame 48 (jumping across 160 -> 540)
        # Continuous line segment detection intercepts and slices cleanly!
        if frame_idx == 48:
            engine._handle_motion((160, 270))
        elif frame_idx == 49:
            engine._handle_motion((540, 270))

        # 3. Spawn multi fruits at frame 70
        if frame_idx == 70:
            f2 = EnhancedFruit(240, height + 20, 1.2, -14.5, 0.35, kind="fruit")
            f2.color = (245, 140, 35)
            f3 = EnhancedFruit(460, height + 20, -1.2, -14.5, 0.35, kind="fruit")
            f3.color = (80, 200, 90)
            engine.fruits.extend([f2, f3])

        # Slice both fruits with smooth swipe at frame 102
        if frame_idx == 100:
            engine._handle_motion((180, 320))
        elif frame_idx == 102:
            engine._handle_motion((320, 240))
        elif frame_idx == 104:
            engine._handle_motion((520, 320))

        # 4. Spawn Bomb at frame 125
        if frame_idx == 125:
            bomb = EnhancedFruit(350, height + 20, 0, -13.5, 0.35, kind="bomb")
            engine.fruits.append(bomb)

        # 5. Fast slice through bomb at frame 155
        if frame_idx == 155:
            engine._handle_motion((200, 300))
        elif frame_idx == 156:
            engine._handle_motion((500, 300))

        # 6. Game over screen active from frame 156+
        # Simulate mouse hovering over replay difficulty buttons
        if 200 <= frame_idx < 240:
            # Hover over Medium button
            engine.mouse_pos = (350, 390)
        elif 240 <= frame_idx < 265:
            # Hover over Hard button
            engine.mouse_pos = (500, 390)
        elif frame_idx == 265:
            # Click Hard difficulty to restart game
            engine.reset("Hard")

        # 7. Post-restart action in Hard mode
        if frame_idx == 275:
            f_hard = EnhancedFruit(320, height + 20, 1.5, -16, 0.35, kind="fruit")
            f_hard.color = (240, 215, 45)
            engine.fruits.append(f_hard)

        engine.update()
        engine.render(surf)

        # Overlay descriptive banner
        banner = pygame.Surface((width, 36), pygame.SRCALPHA)
        banner.fill((20, 140, 60, 220))
        surf.blit(banner, (0, height - 36))
        txt = font_hud.render("AFTER: Continuous Line Slicing + Splitting Halves + Game Over Replay", True, (255, 255, 255))
        surf.blit(txt, (width // 2 - txt.get_width() // 2, height - 28))

        if 48 <= frame_idx <= 65:
            alert = font_alert.render("FAST SWIPE DETECTED -> PERFECT SLICE & JUICE SPLASH!", True, (120, 255, 140))
            surf.blit(alert, (width // 2 - alert.get_width() // 2, 80))

        if 156 <= frame_idx <= 190:
            alert2 = font_alert.render("BOMB EXPLOSION TRIGGERED GAME OVER SCREEN!", True, (255, 120, 120))
            surf.blit(alert2, (width // 2 - alert2.get_width() // 2, 80))

        if 240 <= frame_idx <= 265:
            alert3 = font_alert.render("SELECTING HARD DIFFICULTY TO REPLAY...", True, (255, 220, 50))
            surf.blit(alert3, (width // 2 - alert3.get_width() // 2, 80))

        if frame_idx > 265:
            alert4 = font_alert.render("NEW GAME STARTED IN HARD MODE!", True, (100, 220, 255))
            surf.blit(alert4, (width // 2 - alert4.get_width() // 2, 80))

        frame_rgb = pygame.surfarray.array3d(surf)
        frame_bgr = cv2.cvtColor(np.transpose(frame_rgb, (1, 0, 2)), cv2.COLOR_RGB2BGR)
        writer.write(frame_bgr)

    writer.release()
    print(f"[Recorder] Finished AFTER video: {output_path} ({total_frames} frames)")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    videos_dir = os.path.join(base_dir, "videos")
    os.makedirs(videos_dir, exist_ok=True)

    before_path = os.path.join(videos_dir, "before_gameplay.mp4")
    after_path = os.path.join(videos_dir, "after_gameplay.mp4")

    record_before_video(before_path, duration_sec=10, fps=30)
    record_after_video(after_path, duration_sec=10, fps=30)

    # Also copy to root of lab 4 for easy access
    import shutil
    shutil.copyfile(before_path, os.path.join(base_dir, "before_gameplay.mp4"))
    shutil.copyfile(after_path, os.path.join(base_dir, "after_gameplay.mp4"))
    print("[Recorder] Videos successfully generated and saved!")
