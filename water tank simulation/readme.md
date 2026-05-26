```markdown
# Smart Fluid Reservoir Feedback Model

An automated closed-loop fluid simulation tracking environmental volume changes against system discharge infrastructure.

## 🧠 Technical Highlights
* **Closed-Loop Feedback:** Employs a classic dual-threshold automated controller system to maintain fluid levels.
* **Automated Guardrails:** If simulated rainfall inputs drive the overall volume beyond the high safety threshold (80%), automated discharge pumps are triggered. Once the level is drawn back down past the low boundary line (30%), the system automatically deactivates the pumps to protect the physical hardware from running dry.

## 🚀 Execution
Ensure you are inside the directory and your virtual environment is active:
```bash
python water.py