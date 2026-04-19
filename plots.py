import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =========================================================
# SETTINGS
# =========================================================
file_path = "/home/aghilas/tello_twin_logs/twin_compare_15_secned_.csv"
output_dir = os.path.dirname(file_path)
output_png = os.path.join(output_dir, "trajectory_comparison_15_second_cleaner.png")

meas_x_col = "gz_x"
meas_y_col = "gz_y"
meas_z_col = "gz_z"   # if missing, zeros used
time_col = "time"

jump_threshold = 0.10
median_window = 9
mean_window = 21
downsample_step = 8

# remove noisy beginning/end if needed
trim_start = 10
trim_end = 10

# =========================================================
# HELPERS
# =========================================================
def get_col_or_zeros(df, col):
    if col in df.columns:
        return df[col].to_numpy()
    return np.zeros(len(df))

def remove_big_jumps(x, y, z, t, threshold=0.10):
    keep = [0]
    for i in range(1, len(x)):
        d = np.sqrt((x[i] - x[i-1])**2 + (y[i] - y[i-1])**2 + (z[i] - z[i-1])**2)
        if d <= threshold:
            keep.append(i)
    keep = np.array(keep)
    return x[keep], y[keep], z[keep], t[keep]

def smooth_median(arr, window):
    return pd.Series(arr).rolling(window=window, center=True, min_periods=1).median().to_numpy()

def smooth_mean(arr, window):
    return pd.Series(arr).rolling(window=window, center=True, min_periods=1).mean().to_numpy()

def fit_circle_simple(x, y):
    cx = np.mean(x)
    cy = np.mean(y)
    r = np.mean(np.sqrt((x - cx)**2 + (y - cy)**2))
    return cx, cy, r

# =========================================================
# MAIN
# =========================================================
def main():
    df = pd.read_csv(file_path).dropna().copy()
    df = df.sort_values(time_col).reset_index(drop=True)

    t = df[time_col].to_numpy()
    t = t - t[0]

    x = df[meas_x_col].to_numpy()
    y = df[meas_y_col].to_numpy()
    z = get_col_or_zeros(df, meas_z_col)

    # remove impossible jumps
    x, y, z, t = remove_big_jumps(x, y, z, t, threshold=jump_threshold)

    # trim edges
    if len(x) > (trim_start + trim_end + 20):
        x = x[trim_start:len(x)-trim_end]
        y = y[trim_start:len(y)-trim_end]
        z = z[trim_start:len(z)-trim_end]
        t = t[trim_start:len(t)-trim_end]

    # stronger smoothing
    x = smooth_median(x, median_window)
    y = smooth_median(y, median_window)
    z = smooth_median(z, median_window)

    x = smooth_mean(x, mean_window)
    y = smooth_mean(y, mean_window)
    z = smooth_mean(z, mean_window)

    # downsample
    x = x[::downsample_step]
    y = y[::downsample_step]
    z = z[::downsample_step]

    if len(x) < 10:
        raise ValueError("Too few valid points after filtering.")

    # theoretical circle from filtered data
    cx, cy, r = fit_circle_simple(x, y)
    cz = np.median(z)

    theta = np.linspace(0, 2*np.pi, 400)
    x_ref = cx + r * np.cos(theta)
    y_ref = cy + r * np.sin(theta)
    z_ref = np.full_like(theta, cz)

    # plot
    fig = plt.figure(figsize=(14, 7))

    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax1.plot(x_ref, y_ref, z_ref, label="Trajectoire théorique", linewidth=2)
    ax1.plot(x, y, z, label="Trajectoire réelle", linewidth=1.5)
    ax1.scatter(x[0], y[0], z[0], s=20, label="Départ")
    ax1.scatter(x[-1], y[-1], z[-1], s=20, label="Arrivée")
    ax1.set_title("(a) Trajectoire vue de dessus")
    ax1.set_xlabel("X [m]")
    ax1.set_ylabel("Y [m]")
    ax1.set_zlabel("Z [m]")
    ax1.view_init(elev=60, azim=120)
    ax1.legend(fontsize=8)
    ax1.grid(True)

    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    ax2.plot(x_ref, y_ref, z_ref, label="Trajectoire théorique", linewidth=2)
    ax2.plot(x, y, z, label="Trajectoire réelle", linewidth=1.5)
    ax2.scatter(x[0], y[0], z[0], s=20, label="Départ")
    ax2.scatter(x[-1], y[-1], z[-1], s=20, label="Arrivée")
    ax2.set_title("(b) Trajectoire vue latérale")
    ax2.set_xlabel("X [m]")
    ax2.set_ylabel("Y [m]")
    ax2.set_zlabel("Z [m]")
    ax2.view_init(elev=10, azim=-120)
    ax2.legend(fontsize=8)
    ax2.grid(True)

    fig.suptitle("Comparaison des trajectoires théorique et réelle du drone", fontsize=16)
    plt.tight_layout()
    plt.savefig(output_png, dpi=300, bbox_inches="tight")
    plt.show()

    print(f"Saved: {output_png}")
    print(f"Circle center: ({cx:.3f}, {cy:.3f}, {cz:.3f})")
    print(f"Radius: {r:.3f} m")

if __name__ == "__main__":
    main()
