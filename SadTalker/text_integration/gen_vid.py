from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ColorClip
import moviepy.editor as mp
import numpy as np
from moviepy.config import change_settings

# Set the path to your ImageMagick binary.
# Install ImageMagic in your system if it works remove following, If doesn't then put your relative path.
change_settings({
    "IMAGEMAGICK_BINARY": r"D:\Installations\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
})

# Load your SadTalker video
path = "text_integration\\vid1\\2025_07_31_17.29.43.mp4"
face_clip = VideoFileClip(path)

# Setup dimensions for the video and caption area
video_width, video_height = face_clip.size
half_width = video_width // 2

# Placeholder for word_segments from WhisperX
# Run time_stamp and get word stamp for your audio paste it here.
word_segments = [{'word': 'I', 'start': 0.031, 'end': 0.334, 'score': 0.811}, {'word': 'am', 'start': 0.354, 'end': 0.455, 'score': 0.995}, {'word': 'Sneha.', 'start': 0.515, 'end': 1.06, 'score': 0.872}, {'word': 'I', 'start': 1.483, 'end': 1.544, 'score': 0.804}, {'word': 'am', 'start': 1.584, 'end': 1.665, 'score': 0.951}, {'word': 'learning', 'start': 1.746, 'end': 2.129, 'score': 0.877}, {'word': 'AI', 'start': 2.29, 'end': 2.654, 'score': 0.882}, {'word': 'and', 'start': 2.694, 'end': 2.795, 'score': 0.782}, {'word': 'ML.', 'start': 2.855, 'end': 3.521, 'score': 0.825}, {'word': 'I', 'start': 4.106, 'end': 4.187, 'score': 0.997}, {'word': 'have', 'start': 4.227, 'end': 4.409, 'score': 0.788}, {'word': 'to', 'start': 4.469, 'end': 4.59, 'score': 0.989}, {'word': 'say', 'start': 4.651, 'end': 4.852, 'score': 0.997}, {'word': 'it', 'start': 4.893, 'end': 5.054, 'score': 0.782}, {'word': 'takes', 'start': 5.115, 'end': 5.397, 'score': 0.757}, {'word': 'long', 'start': 5.498, 'end': 5.74, 'score': 0.772}, {'word': 'to', 'start': 5.801, 'end': 5.901, 'score': 0.97}, {'word': 'run', 'start': 5.962, 'end': 6.123, 'score': 0.843}, {'word': 'this', 'start': 6.184, 'end': 6.365, 'score': 0.775}, {'word': 'file.', 'start': 6.466, 'end': 7.273, 'score': 0.912}]

# --- Caption Generation Logic ---

font_size = 30 # 75% of 40
dummy_clip = TextClip("Xg", fontsize=font_size, color='white')
line_height = dummy_clip.h + 5
space_clip = TextClip(" ", fontsize=font_size, color='white')
space_width = space_clip.w

# 1. Group words into pages, calculating the height of each page
pages = []
current_page_words = []
x_pos, y_pos = 0, 0

for seg in word_segments:
    word_clip_for_size = TextClip(seg['word'], fontsize=font_size, color='white')
    word_w = word_clip_for_size.w

    if x_pos + word_w > half_width:
        x_pos = 0
        y_pos += line_height

    # If the text block is about to exceed the available height, finalize the current page.
    if y_pos + line_height > video_height:
        page_height = y_pos + line_height  # Calculate total height of this text block
        pages.append({'words': current_page_words, 'height': page_height})
        # Reset for the new page
        current_page_words = []
        x_pos, y_pos = 0, 0

    current_page_words.append({
        "text": seg['word'],
        "start": seg['start'],
        "x": x_pos,
        "y": y_pos
    })
    x_pos += word_w + space_width

# Append the final page of words after the loop finishes
if current_page_words:
    page_height = y_pos + line_height
    pages.append({'words': current_page_words, 'height': page_height})

# 2. Create a list to hold the final, centered caption video clips
caption_pages = []

for i, page_data in enumerate(pages):
    page_words = page_data['words']
    page_height = page_data['height']
    if not page_words: continue

    page_start_time = page_words[0]['start']
    page_end_time = face_clip.duration if i + 1 >= len(pages) else pages[i+1]['words'][0]['start']
    page_duration = page_end_time - page_start_time
    if page_duration <= 0: continue

    # NEW: Calculate the vertical offset to center the text block
    y_offset = (video_height - page_height) / 2

    # A list to hold all clips for the current page, starting with the background
    clips_for_this_page = [
        ColorClip(size=(half_width, video_height), color=(0,0,0), duration=page_duration)
    ]

    for word_info in page_words:
        word_start_in_page = word_info['start'] - page_start_time
        word_duration = page_duration - word_start_in_page
        if word_duration <= 0: continue
        
        # Create the TextClip and apply the y_offset to its position
        clip = TextClip(
            word_info['text'],
            fontsize=font_size,
            color='white'
        ).set_position(
            (word_info['x'], word_info['y'] + y_offset) # Centering adjustment
        ).set_start(word_start_in_page).set_duration(word_duration)
        
        clips_for_this_page.append(clip)

    page_composite = CompositeVideoClip(clips_for_this_page, size=(half_width, video_height))
    page_composite = page_composite.set_start(page_start_time)
    caption_pages.append(page_composite)

# 3. Create the final caption video by compositing all the page clips
caption_video = CompositeVideoClip(caption_pages, size=(half_width, video_height))
caption_video = caption_video.set_duration(face_clip.duration)

# 4. Final assembly
# MoviePy will automatically center the resized face_clip vertically
# if its new height is less than the composition height.
face_clip_resized = face_clip.resize(width=half_width)

# Arrange the vertically centered video and the vertically centered captions side-by-side
final_video = mp.clips_array([[face_clip_resized, caption_video]])
final_video.write_videofile("final_output_centered.mp4", fps=24, codec="libx264")

print("Video generation complete!")