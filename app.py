import streamlit as st
import cv2
import time
import os
import tempfile
from datetime import datetime

st.title("Video 2 Frames Converter")
st.divider()

# Clear session state on app restart
if 'app_initialized' not in st.session_state:
    st.session_state.clear()  # This clears the cache when the app is restarted
    st.session_state.app_initialized = True  # Mark the session as initialized

# Initialize session state for output directory
if 'output_dir' not in st.session_state:
    st.session_state.output_dir = None

# Function to create output directory
def create_output_directory():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(os.getcwd(), f"output_directory_{timestamp}")
    try:
        os.makedirs(output_dir, exist_ok=True)
        st.session_state.output_dir = output_dir
        return True
    except Exception as e:
        st.error(f"Error creating directory: {str(e)}")
        return False

# Function to upload video
def upload_video():
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])
    if uploaded_file:
        # Validate file type
        if not uploaded_file.name.endswith(('.mp4', '.avi', '.mov')):
            st.error("Invalid file type. Please upload an mp4, avi, or mov video.")
            return None, None
        try:
            temp_dir = tempfile.mkdtemp()
            temp_video_path = os.path.join(temp_dir, "temp_video.mp4")
            file_bytes = uploaded_file.read()
            with open(temp_video_path, "wb") as f:
                f.write(file_bytes)
            return temp_video_path, cv2.VideoCapture(temp_video_path)
        except Exception as e:
            st.error(f"Error processing video: {str(e)}")
            return None, None
    return None, None

# Function to handle frame extraction
def frame_capture(path, frame_rate, num_frames_to_download, output_dir):
    if not output_dir:
        st.error("Please create an output directory first!")
        return False

    vid_obj = cv2.VideoCapture(path)
    fps = int(vid_obj.get(cv2.CAP_PROP_FPS))
    
    if fps <= 0:
        st.error("Error: FPS (Frames per Second) is zero or could not be determined.")
        return False

    if frame_rate <= 0:
        st.error("Error: Frame rate must be greater than zero.")
        return False

    total_frames = int(vid_obj.get(cv2.CAP_PROP_FRAME_COUNT))
    frames_to_extract = min(num_frames_to_download, total_frames)  # Limit extraction to total frames if needed

    # Calculate the interval of frames to skip based on the desired frame rate
    frame_interval = max(fps // frame_rate, 1)
    extracted_frames = 0
    start_time = time.time()

    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        for frame_num in range(0, total_frames, frame_interval):
            if extracted_frames >= frames_to_extract:  # Stop once we've extracted enough frames
                break

            vid_obj.set(cv2.CAP_PROP_POS_FRAMES, frame_num)  # Jump to the needed frame
            success, image = vid_obj.read()
            if not success:
                st.warning("Frame extraction stopped early due to failure.")
                break

            # Save the extracted frame
            frame_path = os.path.join(output_dir, f"frame_{extracted_frames:04d}.jpg")
            try:
                cv2.imwrite(frame_path, image)
                extracted_frames += 1
            except Exception as e:
                st.error(f"Error saving frame: {str(e)}")
                return False

            # Update the progress bar
            progress = extracted_frames / frames_to_extract
            progress_bar.progress(progress)

            # Update remaining time estimation
            elapsed_time = time.time() - start_time
            remaining_time = (elapsed_time / extracted_frames) * (frames_to_extract - extracted_frames)
            status_text.write(f"Estimated time remaining: {remaining_time:.2f} seconds")

        return True

    finally:
        vid_obj.release()
        # Cleanup temporary file
        try:
            os.remove(path)
            os.rmdir(os.path.dirname(path))
        except:
            pass

# Function to reset directory with confirmation
def reset_directory():
    if st.session_state.output_dir:
        if st.button("Confirm Reset Directory"):
            st.session_state.output_dir = None
            st.experimental_rerun()
        else:
            st.warning("Press the button below to confirm resetting the directory.")
    else:
        st.warning("No directory to reset.")

# Main app workflow
st.header("Step 1: Upload Video")
video_path, vid_obj = upload_video()

if vid_obj is not None:
    total_frames = int(vid_obj.get(cv2.CAP_PROP_FRAME_COUNT))
    st.success(f"Video uploaded successfully! Total frames: {total_frames}")
    st.divider()

    st.header("Step 2: Configure Settings")
    col1, col2 = st.columns(2)
    with col1:
        num_frames_to_download = st.number_input("Number of frames to extract", min_value=1, max_value=total_frames, value=total_frames)
    with col2:
        frame_rate = st.number_input("Frame rate (frames per second)", min_value=1, value=5)

    st.divider()

    st.header("Step 3: Select Output Directory")
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.session_state.output_dir:
            st.success(f"✓ Output directory ready: {st.session_state.output_dir}")
        else:
            st.warning("⚠ Please create an output directory")
    with col2:
        if st.button("Create Output Directory"):
            if create_output_directory():
                st.rerun()

    if st.button("Reset Directory"):
        reset_directory()

    st.divider()

    st.header("Step 4: Start Extraction")
    can_extract = all([video_path, st.session_state.output_dir, os.path.exists(st.session_state.output_dir)])
    if not can_extract:
        st.error("⚠ Please complete all previous steps before extracting frames.")
    
    if st.button("▶ Start Frame Extraction", type="primary", disabled=not can_extract):
        with st.spinner("Extracting frames..."):
            success = frame_capture(video_path, frame_rate, num_frames_to_download, st.session_state.output_dir)
            if success:
                st.success("✓ Frames extracted successfully!")
                if os.path.exists(st.session_state.output_dir):
                    num_files = len([f for f in os.listdir(st.session_state.output_dir) if f.endswith('.jpg')])
                    st.info(f"📊 Number of frames extracted: {num_files}")
                    st.write("📁 Frames saved in:")
                    st.code(st.session_state.output_dir)
# To run this code use this command: streamlit run app.py --server.maxUploadSize=2048