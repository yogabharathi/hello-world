import cv2
import numpy as np

# Load image
image_path = "/home/citriot-nano/Downloads/Image.jpeg"
image = cv2.imread(image_path)

# Convert to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define yellow color range
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])

# Create a mask for yellow
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

# Find contours
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.imshow("Contours", mask)
cv2.waitKey(0)
yellow_detected = False
pixel_to_mm_ratio = 0.1  # Example: 1 pixel = 0.1 mm (Replace with actual ratio)

# Process detected contours
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 50:  # Filter small noise
        yellow_detected = True
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        diameter_px = 2 * radius
        diameter_mm = diameter_px * pixel_to_mm_ratio  # Convert to mm
        
        # Draw detected circle
        cv2.circle(image, (int(x), int(y)), int(radius), (0, 255, 0), 2)
        
        # Display diameter in pixels and mm  {int(diameter_px)}px /
        cv2.putText(image, f"D:{diameter_mm:.2f}", 
                    (int(x)-40, int(y)- 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
        print(f"Diameter: {diameter_mm:.2f} mm")

# Display yellow presence
text = "Yellow Detected" if yellow_detected else "No Yellow Detected"
cv2.putText(image, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

# Show result
cv2.imshow("Result", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
