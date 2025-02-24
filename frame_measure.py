import cv2
import numpy as np
# Load image
image_path = "/home/citriot-nano/Downloads/Image.jpeg"
#/mnt/data/F0E5FE47-3552-46A5-B917-447696FB0BAE.jpeg"
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
yellow_detected = False
# Process detected contours
for cnt in contours:
   area = cv2.contourArea(cnt)
   if area > 50:  # Filter small noise
       yellow_detected = True
       (x, y), radius = cv2.minEnclosingCircle(cnt)
       diameter = 2 * radius
       # Draw detected circle
       cv2.circle(image, (int(x), int(y)), int(radius), (0, 255, 0), 2)
    #    cv2.putText(image, f"Diameter: {int(diameter)}px", (int(x)-20, int(y)-20),
    #                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
       cv2.putText(image, f"D:{int(diameter)}px", (int(x)-20, int(y)-20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
       print(f"Diameter: {int(diameter)}px")
# Display yellow presence
text = "Yellow Detected" if yellow_detected else "No Yellow Detected"
cv2.putText(image, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
# Show result
cv2.imshow("Result", image)
cv2.waitKey(0)
cv2.destroyAllWindows()