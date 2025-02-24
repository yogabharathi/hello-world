import os
import subprocess

# Input and output paths
input_video = "/home/citriot-nano/Videos/Screencasts/cylinder.webm"  # Replace with the path to your .webm video file
output_video = "cylinder.mp4"  # Replace with the desired output file path

# Check if the input file exists
if not os.path.exists(input_video):
    print(f"Error: Input file '{input_video}' not found.")
    exit()

# Command to convert the video using FFmpeg
ffmpeg_command = f"ffmpeg -i {input_video} -c:v libx264 -c:a aac -strict experimental {output_video}"

# Run the FFmpeg command
try:
    print("Converting video...")
    subprocess.run(ffmpeg_command, shell=True, check=True)
    print(f"Conversion complete. Saved as '{output_video}'.")
except subprocess.CalledProcessError as e:
    print(f"Error during conversion: {e}")
