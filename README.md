# 🚦 Crowd-Reactive Flow Control System

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Framework](https://img.shields.io/badge/Framework-PyTorch-red?logo=pytorch)
![Model](https://img.shields.io/badge/Detection%20Model-YOLOv5-green)
![Status](https://img.shields.io/badge/status-Stable-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## 🚀 Project Overview

This project implements an **intelligent, real-time flow control system** designed to dynamically adjust signal durations based on the volumetric density of objects (people, vehicles, general items) within a controlled observation zone. It transitions traffic management from purely static timing to a data-driven, adaptive model.

### 💡 Core Innovation: Hybrid State Stabilization
Unlike purely reactive systems that risk instability and rapid signal 'chattering', this system utilizes a **Hybrid State Stabilization** logic. It consumes continuous, real-time density input but stabilizes the control decision (e.g., Green Light Duration) into a fixed-cycle output, guaranteeing **predictability** and **efficiency** simultaneously.

---

## ✨ Features & Technical Highlights

* **Total Object Density Metric:** Leverages the **YOLOv5 Deep Learning Model** to detect and count all 80 COCO classes, providing a robust, general-purpose metric for calculating volumetric congestion.
* **Modular Architecture:** Structured with decoupled modules (`config.py`, `detector.py`, `logic.py`) to maximize **maintainability**, allow for rapid updates to AI models, and facilitate independent auditing of business rules.
* **Real-Time Visualization:** Displays the live object count, the calculated density `STATUS`, and the determined **Next Green Duration** directly overlaid on the video feed.
* **Event-Driven Auditing:** Implements highly efficient CSV logging by recording data **only when the density status transitions** (e.g., from `LOW` to `HIGH`), minimizing storage while providing a clean, auditable record for performance analysis.
* **Zero-Code Tuning:** All critical system parameters are stored in `config.py`, allowing easy adjustment of thresholds and durations without modifying core logic.

---

## ⚙️ System Architecture: Separation of Concerns

The project adheres to industry best practices by separating functional concerns into dedicated Python modules:

| File | Role | Responsibility |
| :--- | :--- | :--- |
| `main.py` | **Orchestrator** | Manages the camera I/O, runs the primary processing loop, and handles application lifecycle and cleanup. |
| `config.py` | **Configuration** | Stores all tunable parameters (`THRESHOLDS`, `DURATIONS`, `CAMERA_INDEX`). |
| `detector.py` | **AI Core** | Loads the YOLOv5 model, runs inference on frames, and calculates the **Total Object Count**. |
| `logic.py` | **Business Logic** | Determines the crowd `STATUS` based on thresholds, calculates the **Next Green Duration**, and manages the state-change logging to `crowd_control_log.csv`. |

---

## 🚦 Control Logic: Status-Based Duration

The system dynamically calculates the required flow duration based on three defined density zones, ensuring that resource allocation is proportionate to congestion.

| Density Status | Rule (Object Count) | Default Duration | Calculated Logged Action |
| :--- | :--- | :--- | :--- |
| **LOW** | Count $\le 3$ | $7s - 1s = \mathbf{6}$ seconds | Decreases wait time (faster cycle). |
| **DEFAULT** | $3 <$ Count $\le 7$ | $\mathbf{7}$ seconds | Standard flow time. |
| **HIGH** | Count $> 7$ | $7s + 2s = \mathbf{9}$ seconds | Increases flow time (clear congestion). |

> **Note:** These thresholds and durations are fully configurable within the `config.py` file.

---

## 📦 Getting Started

### Prerequisites

1. **Python 3.8+**
2. **`pip`** (Python package installer)

### Installation

Clone the repository and install the required libraries. This project requires PyTorch and OpenCV dependencies that are managed via `requirements.txt`.

```bash
# 1. Clone the repository
git clone [https://github.com/YourUsername/Crowd-Reactive-Flow-Control.git](https://github.com/YourUsername/Crowd-Reactive-Flow-Control.git)
cd Crowd-Reactive-Flow-Control

# 2. Install Dependencies
pip install -r requirements.txt
