import cv2
import os

def extract_frames(video_path, output_folder, frame_interval=1):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Check if the video was opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    frame_count = 0  # Counter for frame numbers
    
    while True:
        # Read a frame from the video
        ret, frame = cap.read()
        
        # If frame was not successfully read, we have reached the end of the video
        if not ret:
            break
        
        # Save the frame at the specified interval
        if frame_count % frame_interval == 0:
            # Create the output file path
            frame_filename = os.path.join(output_folder, f"frame_{frame_count}.jpg")
            
            # Write the frame as an image file
            cv2.imwrite(frame_filename, frame)
            print(f"Saved {frame_filename}")
        
        # Increment the frame counter
        frame_count += 1
    
    # Release the video capture object
    cap.release()
    print("Frame extraction completed.")

# Example usage
video_path = "/home/citriot-nano/citriot-project/Nhisika/weight_bridge/ch8_output.mp4"  # Path to the video file
output_folder = "ch8-frame"  # Folder to save extracted frames
frame_interval = 30  # Save every 30th frame (adjustable)

extract_frames(video_path, output_folder, frame_interval)
