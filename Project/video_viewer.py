import streamlit as st
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip

def concatenate_videos(input_files, output_file):
    if len(input_files) != 2:
        st.error("Please upload exactly two videos to concatenate.")
        return

    # Load the input video clips
    clips = [VideoFileClip(file) for file in input_files]

    # Concatenate the video clips
    final_clip = concatenate_videoclips(clips)

    # Write the concatenated video to a file
    final_clip.write_videofile(output_file)

    # Close all video clips
    for clip in clips:
        clip.close()
    final_clip.close()

def trim_video(input_file, output_file, start_time, end_time):
    # Load the video clip
    clip = VideoFileClip(input_file)

    # Trim the video clip
    trimmed_clip = clip.subclip(start_time, end_time)

    # Write the trimmed video to a file
    trimmed_clip.write_videofile(output_file)

    # Close the original clip and trimmed clip
    clip.close()
    trimmed_clip.close()

def add_text_to_video(input_file, output_file, text, start_time, end_time):
    # Load the video clip
    clip = VideoFileClip(input_file)

    # Generate a TextClip with the provided text
    text_clip = TextClip(text, fontsize=50, color='white')

    # Overlay the text clip on the video clip for the specified duration
    annotated_clip = clip.fl_time(lambda t: text_clip if start_time <= t <= end_time else None)

    # Write the annotated video to a file
    annotated_clip.write_videofile(output_file)

    # Close the original clip, text clip, and annotated clip
    clip.close()
    text_clip.close()
    annotated_clip.close()

def main():
    st.title("Online Video Editor")

    st.write("Select an operation:")
    operation = st.selectbox("Operation", ["Concatenate Videos", "Trim Video", "Add Text to Video"])

    st.write("Upload a video from your desktop:")
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi"])

    processing_complete = False

    if uploaded_file is not None:
        st.video(uploaded_file)
        output_filename = st.text_input("Enter output filename (without extension)")

        if operation == "Concatenate Videos":
            st.write("Upload another video to concatenate:")
            uploaded_file2 = st.file_uploader("Choose another video file", type=["mp4", "avi"])
            if uploaded_file2 is not None:
                st.video(uploaded_file2)
                if st.button("Process Video"):
                    process_concatenate_videos(uploaded_file, uploaded_file2, output_filename)
                    processing_complete = True
        elif operation == "Trim Video":
            start_time = st.number_input("Start Time", value=0.0)
            end_time = st.number_input("End Time", value=10.0)
            if st.button("Process Video"):
                process_trim_video(uploaded_file, start_time, end_time, output_filename)
                processing_complete = True
        elif operation == "Add Text to Video":
            text = st.text_input("Enter text to add")
            start_time = st.number_input("Start Time", value=0.0)
            end_time = st.number_input("End Time", value=10.0)
            if st.button("Process Video"):
                process_add_text_to_video(uploaded_file, text, start_time, end_time, output_filename)
                processing_complete = True

    # Display download button for processed video only if processing is complete
    if processing_complete:
        download_processed_video()

def process_concatenate_videos(uploaded_file1, uploaded_file2, output_filename):
    with open(os.path.join("temp_files", uploaded_file1.name), "wb") as f1:
        f1.write(uploaded_file1.getbuffer())
    with open(os.path.join("temp_files", uploaded_file2.name), "wb") as f2:
        f2.write(uploaded_file2.getbuffer())
    output_file = f"{output_filename}.mp4" if output_filename else "output.mp4"
    concatenate_videos([os.path.join("temp_files", uploaded_file1.name), os.path.join("temp_files", uploaded_file2.name)], output_file)

def process_trim_video(uploaded_file, start_time, end_time, output_filename):
    with open(os.path.join("temp_files", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    output_file = f"{output_filename}.mp4" if output_filename else "output.mp4"
    trim_video(os.path.join("temp_files", uploaded_file.name), output_file, start_time, end_time)

def process_add_text_to_video(uploaded_file, text, start_time, end_time, output_filename):
    with open(os.path.join("temp_files", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    output_file = f"{output_filename}.mp4" if output_filename else "output.mp4"
    add_text_to_video(os.path.join("temp_files", uploaded_file.name), output_file, text, start_time, end_time)

def download_processed_video():
    if os.path.exists("output.mp4"):
        with open("output.mp4", "rb") as f:
            video_bytes = f.read()
        st.download_button(label="Download Processed Video", data=video_bytes, file_name="output.mp4", mime="video/mp4")

if __name__ == "__main__":
    main()
