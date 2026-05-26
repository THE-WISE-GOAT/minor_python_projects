```markdown
# Balanced Traffic Intersection Simulator

A graphical 2D simulation environment monitoring multi-directional vehicle routing, approaching grid traffic bottlenecks, and localized collision-avoidance vectors.

## 🧠 Technical Highlights
* **Cyclic Signal Profiles:** Runs an automatic background timer loop tracking traffic light phase intervals through exact transitions (`GREEN` ➡️ `YELLOW` ➡️ `ALL_RED`).
* **Proximity Avoidance Matrix:** Each spawned vehicle implements a forward-scanning raycast check. Cars dynamically evaluate the distance coordinates of any asset directly in front of them, instantly scaling down deceleration vectors to match stopping triggers.

## 🚀 Execution
Ensure you are inside the directory and your virtual environment is active:
```bash
python traffic.py