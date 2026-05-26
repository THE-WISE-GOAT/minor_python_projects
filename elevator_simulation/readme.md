```markdown
# Multi-Elevator Dispatch Logic Simulation

An interactive visual workbench designed to model multi-car elevator motion metrics, scheduling heuristics, and dynamic passenger queue allocations using Pygame.

## 🧠 Technical Highlights
* **Discrete State-Machine:** Each elevator car independently steps through explicit operational conditional flags (`IDLE`, `MOVING`, `OPENING`, `BOARDING`, `CLOSING`).
* **Heuristic Routing:** Intercepts real-time floor demand calls and processes geometric vector metrics. The system evaluates current directions and car occupation numbers to delegate passenger requests to the most efficient asset.
* **Priority Sorting:** Sorts passenger requests relative to current directional vectors to maximize car throughput and limit unneeded reverse-travel intervals.

## 🚀 Execution
Ensure you are inside the directory and your virtual environment is active:
```bash
python elevator.py