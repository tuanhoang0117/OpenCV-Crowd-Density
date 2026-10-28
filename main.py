import cv2
import numpy as np
import time

print("Starting Grid Occupancy Detection...")

# Parameters 
GRID_ROWS = 6
GRID_COLS = 6
OCCUPANCY_THRESHOLD = 0.1  # 10% of pixels in a cell must be dark to count as occupied

# Load from camera 
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Failed to open camera.")
else:
    print("Camera opened successfully.")

while True:
    print("Loop running")  # debug statement

    ret, frame = cap.read()

    print(f"ret: {ret}")   # debug statement
    if not ret:
        print("Failed to read frame from camera.")
        break
    print(f"Frame shape: {frame.shape}")  # debug statement

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    cell_h = h // GRID_ROWS
    cell_w = w // GRID_COLS

    # Convert to grayscale and blur slightly to reduce noise
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    # Apply adaptive threshold (more lighting-resistant)
    thresh = cv2.adaptiveThreshold(blurred, 255,
                                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY_INV, 11, 2)

    occupied_count = 0
    cell_number = 1

    # Draw grid and detect occupancy
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x1 = col * cell_w
            y1 = row * cell_h
            x2 = x1 + cell_w
            y2 = y1 + cell_h

            cell = thresh[y1:y2, x1:x2]
            dark_pixels = cv2.countNonZero(cell)
            total_pixels = cell.shape[0] * cell.shape[1]
            darkness_ratio = dark_pixels / total_pixels

            # Draw rectangles
            color = (0, 255, 0)
            if darkness_ratio > OCCUPANCY_THRESHOLD:
                color = (0, 0, 255)
                occupied_count += 1
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            # Draw a number in the top left corner of each cell
            text = str(cell_number)
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.7
            thickness = 2
            text_x = x1 + 5
            text_y = y1 + 25
            cv2.putText(frame, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness)
            cell_number += 1    

    # Show occupied count
    cv2.putText(frame, f"Occupied: {occupied_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow("Grid Occupancy", frame)
    cv2.imshow("Threshold", thresh)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
print("Released camera and closed all windows.")