import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_path = "/home/aghilas/tello_twin_logs/twin_compare_1_minute_.csv"

df = pd.read_csv(file_path)
df = df.dropna()

t = df["time"] - df["time"].iloc[0]

output_dir = "plots"
os.makedirs(output_dir, exist_ok=True)

# 1. Position comparison X
plt.figure()
plt.plot(t, df["twin_x"], label="twin_x")
plt.plot(t, df["gz_x"], label="gz_x")
plt.xlabel("Time (s)")
plt.ylabel("X Position (m)")
plt.title("Twin vs Gazebo - X Position")
plt.legend()
plt.grid()
plt.savefig(os.path.join(output_dir, "x_position_comparison.png"), dpi=300, bbox_inches="tight")

# 2. Trajectory XY
plt.figure()
plt.plot(df["twin_x"], df["twin_y"], label="Twin")
plt.plot(df["gz_x"], df["gz_y"], label="Gazebo")
plt.xlabel("X Position (m)")
plt.ylabel("Y Position (m)")
plt.title("Trajectory Comparison")
plt.legend()
plt.axis("equal")
plt.grid()
plt.savefig(os.path.join(output_dir, "trajectory_comparison.png"), dpi=300, bbox_inches="tight")

# 3. Position error
error_x = df["twin_x"] - df["gz_x"]
error_y = df["twin_y"] - df["gz_y"]

plt.figure()
plt.plot(t, error_x, label="error_x")
plt.plot(t, error_y, label="error_y")
plt.xlabel("Time (s)")
plt.ylabel("Error (m)")
plt.title("Position Error")
plt.legend()
plt.grid()
plt.savefig(os.path.join(output_dir, "position_error.png"), dpi=300, bbox_inches="tight")

# 4. Yaw comparison
def quat_to_yaw(qz, qw):
    return 2 * np.arctan2(qz, qw)

twin_yaw = quat_to_yaw(df["twin_qz"], df["twin_qw"])
gz_yaw = quat_to_yaw(df["gz_qz"], df["gz_qw"])

plt.figure()
plt.plot(t, twin_yaw, label="twin_yaw")
plt.plot(t, gz_yaw, label="gz_yaw")
plt.xlabel("Time (s)")
plt.ylabel("Yaw (rad)")
plt.title("Yaw Comparison")
plt.legend()
plt.grid()
plt.savefig(os.path.join(output_dir, "yaw_comparison.png"), dpi=300, bbox_inches="tight")

# 5. Yaw error
yaw_error = twin_yaw - gz_yaw

plt.figure()
plt.plot(t, yaw_error, label="yaw_error")
plt.xlabel("Time (s)")
plt.ylabel("Error (rad)")
plt.title("Yaw Error")
plt.legend()
plt.grid()
plt.savefig(os.path.join(output_dir, "yaw_error.png"), dpi=300, bbox_inches="tight")

plt.show()
