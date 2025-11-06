#!/usr/bin/env python3
import cv2
from pygrabber.dshow_graph import FilterGraph
import sys

# --- Configuration ---
TARGET_CAMERA_NAME = "Nearstream VM33"  # Default camera name

# --- Parse Zoom Value from Command-Line Argument ---
if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <zoom_value>")
    sys.exit(1)

try:
    ZOOM_AMOUNT = float(sys.argv[1])
except ValueError:
    print(f"Error: Invalid zoom value '{sys.argv[1]}'. Must be a number.")
    sys.exit(1)

# --- Find Camera Index ---
device_names = FilterGraph().get_input_devices()
target_index = None

for i, name in enumerate(device_names):
    if name.lower() == TARGET_CAMERA_NAME.lower():
        target_index = i
        break

if target_index is None:
    print(f"Error: Camera '{TARGET_CAMERA_NAME}' not found.")
    print("Available cameras:")
    for name in device_names:
        print(f"  {name}")
    sys.exit(1)

print(f"Found target camera '{TARGET_CAMERA_NAME}' at index {target_index}")

# --- Open Camera and Set Zoom ---
cap = cv2.VideoCapture(target_index, cv2.CAP_DSHOW)
if not cap.isOpened():
    print(f"Error: Could not open camera index {target_index}")
    sys.exit(1)

# Set zoom if supported
if hasattr(cv2, 'CAP_PROP_ZOOM'):
    if cap.set(cv2.CAP_PROP_ZOOM, ZOOM_AMOUNT):
        print(f"Zoom set to {ZOOM_AMOUNT}")
    else:
        print("Failed to set zoom. Camera might not support it.")
else:
    print("CAP_PROP_ZOOM not available in your OpenCV version.")

# Close camera
cap.release()
print("Camera released. Done.")
