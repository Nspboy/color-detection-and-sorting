# Real-Time Color Detection with Flask, OpenCV, and ESP32

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.0%2B-green)
![Flask](https://img.shields.io/badge/Flask-web%20app-orange)

A real-time color detection system that uses OpenCV for computer vision, communicates with an ESP32 over serial, and provides an interactive web dashboard using Flask.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Screenshots](#screenshots)
- [Architecture Diagram](#architecture-diagram)
- [Hardware Setup](#hardware-setup)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [License](#license)
- [Credits](#credits)

---

## Project Overview

This project detects red, green, and blue objects in real-time using your webcam, then:
- Updates a live count on a local web dashboard.
- Communicates detection results to an ESP32 over serial.
- Provides audible feedback via sound files.

---

## Screenshots

### 1. Web Dashboard

![Web Dashboard](images/dashboard_screenshot.png)

### 2. Real-Time Detection

![OpenCV Window with Detection](images/opencv_detection.png)

### 3. Hardware Setup

![Hardware Photo](D:\project\images\esp32.jpg)

---

## Architecture Diagram

A high-level overview of system components:

![Architecture Diagram](images/architecture.png)


## Installation

1. **Clone this repository:**
    ```
    git clone https://github.com/yourusername/yourrepo.git
    cd yourrepo
    ```

2. **Install Python dependencies:**
    ```
    pip install -r requirements.txt
    ```

3. **Download/add required sound files:**
    - Place `red.wav`, `green.wav`, `blue.wav`, `unknown.wav` in the root directory.

---

## Usage

1. Connect your ESP32 device and camera.
2. Run the Python script:
    ```
    python main.py
    ```
3. Open your browser at `http://localhost:5000` to access the dashboard.
4. Press `q` to close the OpenCV window.

---

## Features

- Real-time color tracking with OpenCV
- Visual dashboard with Flask
- ESP32 hardware communication via serial port
- Voice feedback for each detection event

---

## Tech Stack

- **Python** 3.8+
- **OpenCV** for computer vision
- **Flask** for web server
- **PySerial** for serial communication
- **NumPy** for efficient array handling
- **playsound** for audio feedback




