import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd

def input_float(prompt: str, default: float) -> float:
    text = input(f"{prompt} [{default}]: ").strip()
    if text == "":
        return default
    return float(text)

DEFAULT_H0  = 5.0      
DEFAULT_VX0 = 3.0      
DEFAULT_VY0 = 0.0      
DEFAULT_G   = 9.81     
DEFAULT_E   = 0.85     
DEFAULT_DT    = 0.01   
DEFAULT_T_MAX = 30.0   

h0  = input_float("Initial height h0 (m)", DEFAULT_H0)
vx0 = input_float("Initial horizontal velocity vx0 (m/s)", DEFAULT_VX0)
vy0 = input_float("Initial vertical velocity vy0 (m/s)", DEFAULT_VY0)
g   = input_float("Gravity g (m/s^2)", DEFAULT_G)
e   = input_float("Coefficient of restitution e (0-1)", DEFAULT_E)

dt    = DEFAULT_DT
t_max = DEFAULT_T_MAX
ground_y = 0.0

vy_stop_thresh      = 0.02    
straight_line_ratio = 0.02    

t_vals, x_vals, y_vals, vx_vals, vy_vals = [], [], [], [], []

t = 0.0
x = 0.0
y = h0
vx = vx0
vy = vy0

while t <= t_max:
    t_vals.append(t)
    x_vals.append(x)
    y_vals.append(y)
    vx_vals.append(vx)
    vy_vals.append(vy)

    vy = vy - g * dt
    x = x + vx * dt
    y = y + vy * dt

    if y < ground_y:
        y = ground_y
        vy = -e * vy
        if abs(vy) < vy_stop_thresh:
            t += dt
            t_vals.append(t)
            x_vals.append(x)
            y_vals.append(y)
            vx_vals.append(vx)
            vy_vals.append(vy)
            break
        
    if abs(vy) < straight_line_ratio * max(abs(vx), 1e-6) and y <= ground_y + 0.01:
        t += dt
        t_vals.append(t)
        x_vals.append(x)
        y_vals.append(y)
        vx_vals.append(vx)
        vy_vals.append(vy)
        break

    t += dt

os.makedirs("files", exist_ok=True)
df = pd.DataFrame({
    "time_s": t_vals,
    "x_m": x_vals,
    "y_m": y_vals,
    "vx_m_s": vx_vals,
    "vy_m_s": vy_vals,
})
excel_path = os.path.join("files", "ball_trajectory.xlsx")
df.to_excel(excel_path, index=False)
print("Saved data to:", excel_path)

fig, ax = plt.subplots(figsize=(10, 6))
ax.set_aspect("equal", "box")

x_min, x_max = min(x_vals), max(x_vals)
y_min, y_max = 0.0, max(y_vals) * 1.1 if y_vals else 1.0
ax.set_xlim(x_min - 1.0, x_max + 0.5)
ax.set_ylim(y_min, y_max)

path_line, = ax.plot([], [], "b-", linewidth=1, alpha=0.0)

ball, = ax.plot([], [], "ro", markersize=8)

ax.axhline(ground_y, color="black", linewidth=1)

speed_text = ax.text(0.02, 0.95, "", transform=ax.transAxes, fontsize=10, color="black", va="top", ha="left")

def init():
    ball.set_data([], [])
    path_line.set_data([], [])
    path_line.set_alpha(0.0)
    speed_text.set_text("")
    return ball, path_line, speed_text

def update(frame):
    x = x_vals[frame]
    y = y_vals[frame]
    vx = vx_vals[frame]
    vy = vy_vals[frame]

    ball.set_data([x], [y])
    speed = np.sqrt(vx ** 2 + vy ** 2)
    speed_text.set_text(f"Speed: {speed:.2f} m/s")

    if frame == len(t_vals) - 1:
        path_line.set_data(x_vals, y_vals)
        path_line.set_alpha(1.0)

    return ball, path_line, speed_text

ani = FuncAnimation(
    fig,
    update,
    frames=len(t_vals),
    init_func=init,
    blit=True,
    interval=int(dt * 1000),
    repeat=False
)

plt.title("Bouncing Ball (path appears after motion)")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.show()
