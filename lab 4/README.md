# Lab 4: VibeCoding - Fruit Ninja Game Enhancement

**Student SRN:** `PES1UG24CS705`  
**Course:** Software Engineering Lab  
**Original Assigned Repository:** [SETAPESU26/41_fruit-ninja](https://github.com/SETAPESU26/41_fruit-ninja)  
**Destination Repository:** [Akshayarcot/openapi-mock-server-generator](https://github.com/Akshayarcot/openapi-mock-server-generator) (`lab 4/`)  
**AI Pair-Programming Partner:** Antigravity (Gemini 3.8 Flash)  

---

## 📋 Deliverables Summary

| Deliverable | File / Path | Status |
|---|---|:---:|
| **a. Videos (Before and After)** | [`before_gameplay.mp4`](./before_gameplay.mp4), [`after_gameplay.mp4`](./after_gameplay.mp4), [`videos/`](./videos/) | ✅ Complete (10s each, 30 FPS) |
| **b. Updated Code** | [`main.py`](./main.py), [`game/`](./game/) (`fruit.py`, `game_engine.py`, `audio.py`) | ✅ Complete & Verified |
| **c. Chat History (Doc & PDF)** | [`PES1UG24CS705_Lab4_Chat_History.pdf`](./PES1UG24CS705_Lab4_Chat_History.pdf), [`PES1UG24CS705_Lab4_Chat_History.docx`](./PES1UG24CS705_Lab4_Chat_History.docx), [`chat_history.md`](./chat_history.md) | ✅ Complete |

---

## 🎯 Tasks Completed

### Task 1: Refined Continuous Collision Detection
- **Problem:** Discrete collision detection evaluated `contains_point(x, y)` only at exact frame mouse coordinates. Fast swipes caused the cursor to "tunnel" from one side of the fruit to the other in a single frame without touching the circle radius, causing missed slices despite visual blade intersection.
- **Solution:** Implemented **Continuous Collision Detection (CCD)** via line segment vs circle intersection in `Fruit.intersects_segment(p1, p2)`:
  - Treats mouse movement between consecutive frames as line segment $P(t) = P_1 + t(P_2 - P_1)$ for $t \in [0, 1]$.
  - Projects circle center $C(x_c, y_c)$ onto the segment:
    $$t = \text{clamp}\left(\frac{(x_c - x_1)\Delta x + (y_c - y_1)\Delta y}{\Delta x^2 + \Delta y^2}, 0, 1\right)$$
  - Calculates distance from closest segment point $P_{closest}$ to circle center $C$.
  - Registers a slice if and only if $\text{dist} \le r$.
- **Visual Enhancement:** Added physics-driven splitting fruit halves (`FruitHalf`) that tumble apart with rotation and gravity, alongside colorful juice particles (`Particle`).

### Task 2: Implement Game Over Condition & Screen
- **Problem:** When lives reached 0 or a bomb was sliced, the original engine merely printed to console (`Game over! Final score: ...`) while leaving the screen frozen and uninformative.
- **Solution:** 
  - Created a dedicated game-over state with a darkened translucent backdrop (`overlay` with alpha 215).
  - Prominently displays:
    - **Header:** Large stylized `GAME OVER` title with shadow.
    - **Reason:** Specific cause of termination (`"Bomb Detonated!"` or `"Out of Lives!"`).
    - **Score Board:** Displays `"Final Score: {score}"` and persisted `"High Score: {high_score}"`.
  - Suspends fruit spawning while allowing existing slice particles and halves to gracefully fade out.

### Task 3: Add Replay Option & Difficulty Selection
- **Features Added:**
  - Dynamic replay menu allowing the player to restart without exiting the game.
  - Three distinct difficulty presets:
    - **Easy:** `spawn_interval = 65`, `bomb_chance = 0.08`, `speed_scale = 0.85`
    - **Medium:** `spawn_interval = 50`, `bomb_chance = 0.15`, `speed_scale = 1.0` (Default)
    - **Hard:** `spawn_interval = 36`, `bomb_chance = 0.25`, `speed_scale = 1.25`
  - Dual control inputs:
    - **Mouse:** Clickable on-screen difficulty buttons with dynamic hover highlights (`1. Easy`, `2. Medium`, `3. Hard`, `Q. Exit`).
    - **Keyboard:** Instant key shortcuts (`1`/`E`, `2`/`M`, `3`/`H`, `Q`/`ESC`).
  - `GameEngine.reset(difficulty)` cleanly reinitializes score, lives, entity lists, and timers while preserving the player's high score.

### Task 4: Add Sound Feedback
- **Sound Architecture:** Created `game/audio.py` (`SoundManager`) with built-in standalone 16-bit 44.1kHz PCM WAV assets generated in `game/assets/sounds/`:
  - `slice.wav`: Crisp high-speed blade whoosh with downward frequency modulation (1500Hz $\rightarrow$ 400Hz).
  - `bomb.wav`: Low-frequency 90Hz exponential rumbling explosion.
  - `game_over.wav`: Sad descending minor melodic triad ($A_4 \rightarrow F\#_4 \rightarrow D_4$).
- **Headless & Offline Resilience:** `SoundManager` safely detects audio driver availability and fails over gracefully into silent mode if no audio hardware is present.

---

## 🎬 Video Demonstrations

1. **Before Video (`before_gameplay.mp4` / `videos/before_gameplay.mp4`):**
   - Duration: 10 seconds (300 frames @ 30 FPS).
   - Demonstrates the tunneling bug where fast swipes cross the fruit without slicing it.
   - Shows fruit falling off screen, dropping lives to 0, and screen freezing with only console output.

2. **After Video (`after_gameplay.mp4` / `videos/after_gameplay.mp4`):**
   - Duration: 10 seconds (300 frames @ 30 FPS).
   - Demonstrates continuous collision detection cleanly slicing fast swipes.
   - Demonstrates fruit splitting into halves and juice splash particles.
   - Demonstrates bomb detonation, explosion effect, and Game Over screen.
   - Demonstrates hovering over replay buttons and launching a new game in Hard mode.

---

## 📁 Repository Structure

```
lab 4/
├── README.md                                # Lab documentation and task report
├── PES1UG24CS705_Lab4_Chat_History.pdf       # Exported chat history & prompts (PDF)
├── PES1UG24CS705_Lab4_Chat_History.docx      # Exported chat history & prompts (DOCX)
├── chat_history.md                          # Markdown transcript of prompt iterations
├── before_gameplay.mp4                      # 10s gameplay video before fixes
├── after_gameplay.mp4                       # 10s gameplay video after all features
├── main.py                                  # Pygame entry point
├── requirements.txt                         # Python dependencies
├── record_gameplay.py                       # Automated 10-second video recording script
├── generate_chat_docs.py                    # PDF/DOCX transcript generator
├── videos/
│   ├── before_gameplay.mp4
│   └── after_gameplay.mp4
└── game/
    ├── __init__.py
    ├── audio.py                             # Audio & SoundManager module
    ├── fruit.py                             # Continuous collision detection, FruitHalf, Particle
    ├── game_engine.py                       # Game loop, UI overlay, replay difficulty manager
    └── assets/
        └── sounds/
            ├── slice.wav
            ├── bomb.wav
            └── game_over.wav
```

---

## 🚀 Running the Game

### Prerequisites
```bash
pip install -r requirements.txt
```

### Launch Interactive Game
```bash
python main.py
```

### Controls
- **Mouse Swipe:** Slice fruits (and avoid bombs!)
- **Click:** Slice at cursor position / Click menu buttons
- **On Game Over:**
  - Press `1` or `E`: Replay on **Easy**
  - Press `2` or `M`: Replay on **Medium**
  - Press `3` or `H`: Replay on **Hard**
  - Press `Q` or `ESC`: Quit game
- **In-Game:** Press `R` to restart current session at any time.

### Re-generate Submission Videos
```bash
python record_gameplay.py
```
