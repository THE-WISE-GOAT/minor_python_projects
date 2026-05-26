```markdown
# Kinematic Trajectory & Attenuation Engine

A mathematical simulation modeling object displacement vectors under explicit gravitational loads, featuring real-time animation plotting and automated data recording.

## 🧠 Technical Highlights
* **Kinematic Solver:** Implements time-stepped differential integration loops (`dt = 0.01`) to calculate velocity attenuation and physical coordinates frame by frame.
* **Energy Dissipation:** Applies a Coefficient of Restitution (`e`) to instantly compute kinetic energy drops and vertical vector flips upon ground plane contact.
* **Data Logging Workspace:** Automatically structures every mathematical calculation into a unified Pandas Dataframe, outputting a data tracking file directly to `files/ball_trajectory.xlsx`.

## 🚀 Execution
Ensure you are inside the directory and your virtual environment is active:
```bash
python bounce.py