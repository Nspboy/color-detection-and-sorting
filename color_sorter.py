import cv2
import serial
import time
from flask import Flask, render_template, jsonify
import threading
from playsound import playsound
import os
import sys
import numpy as np

# ----- Flask App -----
app = Flask(__name__)
counts = {"RED": 0, "GREEN": 0, "BLUE": 0, "UNKNOWN": 0}

@app.route('/')
def index():
    """Renders the main HTML dashboard."""
    return render_template('index.html')

@app.route('/counts')
def get_counts():
    """Returns the current color counts as a JSON object."""
    return jsonify(counts)

# ----- Detection Code -----
def detection_loop():
    # Serial connection to ESP32
    try:
        esp32 = serial.Serial('COM4', 115200, timeout=1)   # Update COM port as needed
        time.sleep(2)
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        print("Please check the COM port and ensure the ESP32 is connected.")
        return

    # OS-specific webcam backend
    if sys.platform == "win32":
        backend = cv2.CAP_DSHOW
    elif sys.platform == "darwin":
        backend = cv2.CAP_AVFOUNDATION
    else:
        backend = cv2.CAP_V4L2

    cap = cv2.VideoCapture(1, backend)  # Change device index if needed
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)

    # Pre-check for sound files
    sound_files = ["red.wav", "green.wav", "blue.wav", "unknown.wav"]
    for sound_file in sound_files:
        if not os.path.exists(sound_file):
            print(f"Warning: Sound file '{sound_file}' not found. Voice feedback will be disabled.")

    detection_interval = 0.5
    last_detection_time = time.time()

    # HSV ranges for colors
    hsv_ranges = {
        "RED": [(np.array([0, 100, 50]), np.array([10, 255, 255])),
                (np.array([160, 100, 50]), np.array([179, 255, 255]))],  # red (two ranges)
        "GREEN": [(np.array([35, 100, 50]), np.array([85, 255, 255]))],
        "BLUE": [(np.array([90, 100, 50]), np.array([130, 255, 255]))]
    }

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Warning: Failed to grab frame. Re-attempting...")
            cap.release()
            time.sleep(1)
            cap = cv2.VideoCapture(1, backend)
            if not cap.isOpened():
                print("Error: Could not re-open camera. Exiting loop.")
                break
            continue

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        detected_color = "UNKNOWN"
        detected_areas = []

        for color, ranges in hsv_ranges.items():
            mask = None
            for lower, upper in ranges:
                current_mask = cv2.inRange(hsv, lower, upper)
                mask = current_mask if mask is None else cv2.bitwise_or(mask, current_mask)

            # Noise removal
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 1000:  # Minimum area threshold to filter noise
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    detected_areas.append(color)

        if detected_areas:
            detected_color = detected_areas[0]

        current_time = time.time()
        if current_time - last_detection_time >= detection_interval:
            counts[detected_color] += 1
            try:
                esp32.write((detected_color + "\n").encode())
            except Exception as e:
                print(f"Error writing to serial: {e}")
            print(f"Detected {detected_color} | Totals: {counts}")

            sound_file = f"{detected_color.lower()}.wav"
            if os.path.exists(sound_file):
                playsound(sound_file)
            last_detection_time = current_time

        cv2.imshow('Real-Time Color Tracking', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    esp32.close()

# ----- Start Threads -----
if __name__ == "__main__":
    detection_thread = threading.Thread(target=detection_loop)
    detection_thread.daemon = True
    detection_thread.start()

    app.run(host="0.0.0.0", port=5000, debug=False)
