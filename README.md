# Interactive Python Simulations & Small Utilities

This repository is a collection of compact, self-contained Python projects demonstrating simulation techniques, simple controllers, and lightweight computer-vision utilities.

---

## Projects

Each project lives in its own folder with a short technical brief and a runnable script. To run a project, open a terminal in the project's directory and run the command shown.

- **[`/blink_key_press`](./blink_key_press)** — Eye-Blink Event Keypress Controller: uses MediaPipe Face Mesh to detect deliberate eye blinks and emit local keystrokes. Run:

   ```bash
   python blink_to_key.py
   ```

- **[`/hand_sign_screenlock`](./hand_sign_screenlock)** — Hand-gesture Screen Lock: uses MediaPipe Hands + OpenCV to detect a closed fist and lock the host screen (cross-platform helpers). Run:

   ```bash
   python hand_lock.py
   ```

- **[`/elevator_simulation`](./elevator_simulation)** — Multi-Elevator Dispatch Logic Simulation: Pygame visual workbench modeling multi-car dispatch heuristics and state-machine behaviors. Run:

   ```bash
   python elevator.py
   ```

- **[`/traffic_simulation`](./traffic_simulation)** — Balanced Traffic Intersection Simulator: 2D vehicle routing with signal phases and proximity-based avoidance. Run:

   ```bash
   python traffic.py
   ```

- **[`/water_tank_simulation`](./water_tank_simulation)** — Smart Fluid Reservoir Feedback Model: dual-threshold automated pump controller simulation. Run:

   ```bash
   python water.py
   ```

- **[`/ball-bounce_simulation`](./ball-bounce_simulation)** — Kinematic Trajectory & Attenuation Engine: time-stepped physics simulation that logs trajectories to an Excel file. Run:

   ```bash
   python bounce.py
   ```

---

## Setup

### Prerequisites
- Python 3.10 or newer
- A webcam is required for the computer-vision utilities (`blink_key_press` and `hand_sign_screenlock`).

### Install
1. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Notes
- If you only want to run non-CV projects (Pygame / numeric sims), OpenCV and MediaPipe are optional.
- The `hand_sign_screenlock` attempts platform-specific lock commands; depending on your OS you may need elevated permissions or minor adjustments.

---

If you'd like, I can also:
- add missing `readme.md` for `hand_sign_screenlock`,
- generate short usage examples per project, or
- run a quick smoke test for one of the scripts.