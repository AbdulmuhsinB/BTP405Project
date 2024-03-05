# from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip
# from moviepy.video import fx

# def concatenate_videos(input_files, output_file):
#     # Load all input video clips
#     clips = [VideoFileClip(file) for file in input_files]
    
#     # Concatenate the video clips
#     final_clip = concatenate_videoclips(clips)
    
#     # Write the concatenated video to a file
#     final_clip.write_videofile(output_file)
    
#     # Close all video clips
#     for clip in clips:
#         clip.close()
#     final_clip.close()

# def trim_video(input_file, output_file, start_time, end_time):
#     # Load the video clip
#     clip = VideoFileClip(input_file)
    
#     # Trim the video clip
#     trimmed_clip = clip.subclip(start_time, end_time)
    
#     # Write the trimmed video to a file
#     trimmed_clip.write_videofile(output_file)
    
#     # Close the original clip and trimmed clip
#     clip.close()
#     trimmed_clip.close()

# def add_text_to_video(input_file, output_file, text, start_time, end_time):
#     # Load the video clip
#     clip = VideoFileClip(input_file)
    
#     # Generate a TextClip with the provided text
#     text_clip = TextClip(text, fontsize=50, color='white')
    
#     # Overlay the text clip on the video clip for the specified duration
#     annotated_clip = clip.fl_time(lambda t: text_clip if start_time <= t <= end_time else None)
    
#     # Write the annotated video to a file
#     annotated_clip.write_videofile(output_file)
    
#     # Close the original clip, text clip, and annotated clip
#     clip.close()
#     text_clip.close()
#     annotated_clip.close()
