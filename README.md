# Interactive Python Simulations & Algorithmic Engines Portfolio

A centralized showcase of self-contained Python applications exploring discrete state-machine design, automated feedback loops, kinematic modeling, and real-time computer vision tracking interfaces.

---

## 📂 Repository Architecture

This repository functions as an integrated portfolio. Every simulation is fully modularized into its own directory alongside a dedicated technical brief:

* **[`/computer-vision-blink-trigger`](./computer-vision-blink-trigger)**: MediaPipe-driven gesture tracking interface. Handles real-time spatial coordinate evaluation.
* **[`/elevator-dispatch-system`](./elevator-dispatch-system)**: Pygame-driven multi-car dispatch logic engine. Explores scheduling optimization and transit state-machines.
* **[`/traffic-intersection-flow`](./traffic-intersection-flow)**: Fixed-phase balanced traffic grid coordinator. Implements relative-distance collision avoidance logic.
* **[`/fluid-reservoir-control`](./fluid-reservoir-control)**: Automated dual-threshold pump feedback model simulating environmental inflows against mechanical discharge thresholds.
* **[`/ball-trajectory-kinematics`](./ball-trajectory-kinematics)**: Explicit time-stepped trajectory physics generator with automatic Excel reporting profiles.

---

## 🛠️ Environment Setup

### Prerequisites
* Python 3.10 or higher
* An active webcam assembly (required exclusively for the Computer Vision module)

### Installation & Initialization
1. Clone the workspace layout:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/python-simulations-portfolio.git](https://github.com/YOUR_USERNAME/python-simulations-portfolio.git)
   cd python-simulations-portfolio
   
2. Establish and initialize an isolated local virtual environment:

    ```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install all cross-project external dependencies at once:

    ```bash
pip install -r requirements.txt

💡 Maintained as an ongoing engineering exploration into programmatic simulations, real-time feedback loops, and interactive UI systems.