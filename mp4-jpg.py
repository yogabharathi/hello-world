import cv2
import os

def extract_frames(video_path, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    video_capture = cv2.VideoCapture(video_path)
    
    if not video_capture.isOpened():
        print(f"Error: Unable to open video file: {video_path}")
        return

    frame_count = 0

    while True:
        # Read a frame from the video
        ret, frame = video_capture.read()

        # Break the loop if there are no frames left to read
        if not ret:
            break

        # Construct the file name for the frame
        frame_filename = os.path.join(output_folder, f"frame_{frame_count:05d}.jpg")

        # Save the frame as a JPEG file
        cv2.imwrite(frame_filename, frame)

        print(f"Saved: {frame_filename}")

        frame_count += 1

    # Release the video capture object
    video_capture.release()
    print(f"Extraction completed. Total frames saved: {frame_count}")

if __name__ == "__main__":
    video_file_path = "/home/citriot-nano/citriot-project/Nhisika/cylinder_type_count/new-cylinder-data/load-1.mp4"
    output_folder_name = "/home/citriot-nano/citriot-project/Nhisika/cylinder_type_count/new-cylinder-data/frame/load-1/"

    extract_frames(video_file_path, output_folder_name)
