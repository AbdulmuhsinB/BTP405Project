from moviepy.editor import * 
from moviepy.video.fx import all as vfx 
import streamlit as st 

# Function to concatenate two videos
def concatenate_videos(input_files, output_file):
    if len(input_files) != 2:  # Checking if exactly two videos are uploaded
        st.error("Please upload exactly two videos to concatenate.")  # Displaying an error message if the condition is not met
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

# Function to trim a video
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

# Function to invert colors of a video
def invert_colors(input_file, output_file):
    # Load the video clip
    clip = VideoFileClip(input_file)

    # Invert the colors of the video clip
    inverted_clip = vfx.invert_colors(clip)

    # Write the inverted video to a file
    inverted_clip.write_videofile(output_file)

    # Close the original clip and inverted clip
    clip.close()
    inverted_clip.close()

# Function to adjust the speed of a video
def adjust_speed(input_file, output_file, speed_factor):
    # Load the video clip
    clip = VideoFileClip(input_file)

    # Adjust the speed of the video clip
    new_clip = clip.fx(vfx.speedx, speed_factor)

    # Write the adjusted speed video to a file
    new_clip.write_videofile(output_file)

    # Close the original clip and new clip
    clip.close()
    new_clip.close()

# Function to mirror a video horizontally
def mirror_video(input_file, output_file):
    # Load the video clip
    clip = VideoFileClip(input_file)

    # Mirror the video clip horizontally
    mirrored_clip = vfx.mirror_x(clip)

    # Write the mirrored video to a file
    mirrored_clip.write_videofile(output_file)

    # Close the original clip and mirrored clip
    clip.close()
    mirrored_clip.close()
