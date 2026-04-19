# Data-Driven Digital Twin of a Te# Data-Driven Digital Twin of a Tello Drone
**ROS2 | Gazebo | LSTM Sequence Learning**

This repository contains a **Digital Twin** framework for the DJI Tello drone. The project bridges the gap between traditional physics-based simulation and data-driven state estimation by synchronizing a ROS2-based kinematic model with a high-fidelity Gazebo environment.

---

## 🎯 Project Objectives

* **Baseline Twin:** Develop a real-time ROS2 dynamics node that mirrors drone behavior.
* **Data Acquisition:** Log synchronized datasets containing control inputs (`Twist`) and ground-truth states.
* **Behavioral Analysis:** Compare the trajectory of the mathematical twin against Gazebo’s physics engine.
* **State Prediction:** Train a **Long Short-Term Memory (LSTM)** network to predict future states and account for non-linear residuals.

---

## 🏗 System Architecture

The system follows a modular ROS2 design where the "Digital Twin" and the "Physical Entity" (Gazebo) consume the same command stream simultaneously.

```text
                +-------------------------+
                |       cmd_test          |
                | (Publishes Twist Cmds)  |
                +------------+------------+
                             |
                    Topic: /tello_cmd
                             |
              +--------------+--------------+
              v                             v
    +-----------------------+     +-----------------------+
    |    simple_dynamics    |     |   Gazebo Simulator    |
    | (Baseline Twin Model) |     |    (Ground Truth)     |
    +-----------+-----------+     +-----------+-----------+
                |                             |
         Topic: /tello_state           Topic: /model_pose
                |                             |
                +------------+----------------+
                             v
                +-------------------------+
                |       logger_node       |
                |  (Syncs & Writes CSV)   |
                +------------+------------+
                             |
                             v
                +-------------------------+
                |   Offline LSTM Model    |
                | (Future State Predict)  |
                +-------------------------+
📂 Repository StructurePlaintexttello_twin_ws/
├── src/
│   ├── tello_twin_bringup/    # Launch files, Gazebo worlds, and URDF models
│   ├── tello_twin_control/    # Baseline dynamics and kinematic twin node
│   ├── tello_twin_logging/    # Data synchronization and CSV serialization
│   └── tello_twin_msgs/       # Custom interfaces for state/command sync
├── scripts/                   # Python scripts for LSTM training (PyTorch/TF)
└── data/                      # Recorded flight logs for ML training
🛠 Technical Implementation1. Kinematic BaselineThe twin node calculates state updates by integrating velocity commands over time. For a state vector $\mathbf{x} = [x, y, z, \psi]^T$ and input $\mathbf{u}$, the transition is defined as:$$x_{t+1} = x_t + \int_{t}^{t+\Delta t} f(x, u) \, dt$$2. LSTM Sequence ModelingTo capture complex dynamics (drag, inertia, motor latency), we utilize an LSTM network:Input Window: A sequence of the last $N$ commands and states.Output: Predicted state at $T + \Delta t$.Loss Function: Mean Squared Error (MSE) between Gazebo ground truth and the LSTM prediction.🚀 Getting StartedPrerequisitesROS2: Humble or FoxySimulator: Gazebo 11Python Libraries: pandas, numpy, torch or tensorflowInstallation & BuildBashmkdir -p ~/tello_twin_ws/src
cd ~/tello_twin_ws/src
# git clone <your-repo-link> .
cd ~/tello_twin_ws
colcon build --symlink-install
source install/setup.bash
Running the ProjectLaunch Simulation & Twin:Bashros2 launch tello_twin_bringup complete_twin.launch.py
Start Data Logging:Bashros2 run tello_twin_logging logger_nodello Drone
**ROS2 | Gazebo | LSTM Sequence Learning**

This repository contains a **Digital Twin** framework for the DJI Tello drone. The project bridges the gap between traditional physics-based simulation and data-driven state estimation by synchronizing a ROS2-based kinematic model with a high-fidelity Gazebo environment.

---

## 🎯 Project Objectives

* **Baseline Twin:** Develop a real-time ROS2 dynamics node that mirrors drone behavior.
* **Data Acquisition:** Log synchronized datasets containing control inputs (`Twist`) and ground-truth states.
* **Behavioral Analysis:** Compare the trajectory of the mathematical twin against Gazebo’s physics engine.
* **State Prediction:** Train a **Long Short-Term Memory (LSTM)** network to predict future states and account for non-linear residuals.

---

## 🏗 System Architecture

The system follows a modular ROS2 design where the "Digital Twin" and the "Physical Entity" (Gazebo) consume the same command stream simultaneously.

```text
                +-------------------------+
                |       cmd_test          |
                | (Publishes Twist Cmds)  |
                +------------+------------+
# Data-Driven Digital Twin of a Tello Drone
**ROS2 | Gazebo | LSTM Sequence Learning**

This repository contains a **Digital Twin** framework for the DJI Tello drone. The project bridges the gap between traditional physics-based simulation and data-driven state estimation by synchronizing a ROS2-based kinematic model with a high-fidelity Gazebo environment.

---

## 🎯 Project Objectives

* **Baseline Twin:** Develop a real-time ROS2 dynamics node that mirrors drone behavior.
* **Data Acquisition:** Log synchronized datasets containing control inputs (`Twist`) and ground-truth states.
* **Behavioral Analysis:** Compare the trajectory of the mathematical twin against Gazebo’s physics engine.
* **State Prediction:** Train a **Long Short-Term Memory (LSTM)** network to predict future states and account for non-linear residuals.

---

## 🏗 System Architecture

The system follows a modular ROS2 design where the "Digital Twin" and the "Physical Entity" (Gazebo) consume the same command stream simultaneously.

```text
                +-------------------------+
                |       cmd_test          |
                | (Publishes Twist Cmds)  |
                +------------+------------+
                             |
                    Topic: /tello_cmd
                             |
              +--------------+--------------+
              v                             v
    +-----------------------+     +-----------------------+
    |    simple_dynamics    |     |   Gazebo Simulator    |
    | (Baseline Twin Model) |     |    (Ground Truth)     |
    +-----------+-----------+     +-----------+-----------+
                |                             |
         Topic: /tello_state           Topic: /model_pose
                |                             |
                +------------+----------------+
                             v
                +-------------------------+
                |       logger_node       |
                |  (Syncs & Writes CSV)   |
                +------------+------------+
                             |
                             v
                +-------------------------+
                |   Offline LSTM Model    |
                | (Future State Predict)  |
                +-------------------------+
📂 Repository StructurePlaintexttello_twin_ws/
├── src/
│   ├── tello_twin_bringup/    # Launch files, Gazebo worlds, and URDF models
│   ├── tello_twin_control/    # Baseline dynamics and kinematic twin node
│   ├── tello_twin_logging/    # Data synchronization and CSV serialization
│   └── tello_twin_msgs/       # Custom interfaces for state/command sync
├── scripts/                   # Python scripts for LSTM training (PyTorch/TF)
└── data/                      # Recorded flight logs for ML training
🛠 Technical Implementation1. Kinematic BaselineThe twin node calculates state updates by integrating velocity commands over time. For a state vector $\mathbf{x} = [x, y, z, \psi]^T$ and input $\mathbf{u}$, the transition is defined as:$$x_{t+1} = x_t + \int_{t}^{t+\Delta t} f(x, u) \, dt$$2. LSTM Sequence ModelingTo capture complex dynamics (drag, inertia, motor latency), we utilize an LSTM network:Input Window: A sequence of the last $N$ commands and states.Output: Predicted state at $T + \Delta t$.Loss Function: Mean Squared Error (MSE) between Gazebo ground truth and the LSTM prediction.🚀 Getting StartedPrerequisitesROS2: Humble or FoxySimulator: Gazebo 11Python Libraries: pandas, numpy, torch or tensorflowInstallation & BuildBashmkdir -p ~/tello_twin_ws/src
cd ~/tello_twin_ws/src
# git clone <your-repo-link> .
cd ~/tello_twin_ws
colcon build --symlink-install
source install/setup.bash
Running the ProjectLaunch Simulation & Twin:Bashros2 launch tello_twin_bringup complete_twin.launch.py
Start Data Logging:Bashros2 run tello_twin_logging logger_node                             |
                    Topic: /tello_cmd
                             |
              +--------------+--------------+
              v                             v
    +-----------------------+     +-----------------------+
    |    simple_dynamics    |     |   Gazebo Simulator    |
    | (Baseline Twin Model) |     |    (Ground Truth)     |
    +-----------+-----------+     
         Topic: /tello_state           Topic: /model_pose
                |                             |
                +------------+----------------+
                             v
                +-------------------------+
                |       logger_node       |
                |  (Syncs & Writes CSV)   |
                +------------+------------+
                             |
                             v
                +-------------------------+
                |   Offline LSTM Model    |
                | (Future State Predict)  |
                +-------------------------+
