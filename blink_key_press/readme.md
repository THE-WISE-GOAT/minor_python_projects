```markdown
# Eye-Blink Event Keypress Controller

A computer vision engine that monitors human gestures in real-time and maps deliberate eye-blink configurations directly into localized system keystroke inputs.

## 🧠 Technical Highlights
* **Landmark Tracking:** Leverages Google MediaPipe Face Mesh to capture and parse high-fidelity 3D facial coordinate arrays.
* **Mathematical Mapping:** Extracts coordinate matrices to isolate human eye dimensions and systematically verify the Eye Aspect Ratio (EAR) based on vertical vs. horizontal pixel intervals.
* **State Debouncing:** Utilizes a consecutiveframe filter tracking threshold (`CONSEC_FRAMES = 2`) along with an explicit internal cooldown timer (`COOLDOWN_SEC = 0.9`) to filter out unconscious micro-blinks and prevent signal bouncing.

## 🚀 Execution
Ensure you are inside the directory and your virtual environment is active:
```bash
python blink_to_key.py

Optional CLI Configuration:

```bash
python blink_to_key.py --key down --threshold 0.21