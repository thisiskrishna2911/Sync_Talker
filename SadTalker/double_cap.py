from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ColorClip
import moviepy.editor as mp
import numpy as np
from moviepy.config import change_settings
from text_integration import time_stamp
# Set the path to your ImageMagick binary.
# This is necessary for TextClip to work on some systems.
change_settings({
    "IMAGEMAGICK_BINARY": r"D:\Installations\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
})

# Load your SadTalker video
path = "text_integration\sneha_output.mp4"
face_clip = VideoFileClip(path)

# --- MODIFICATION START ---
# The width of the caption panel will be the same as the original video's width.
# The final video will have a total width of video_width * 2.
video_width, video_height = face_clip.size
caption_panel_width = video_width 
# --- MODIFICATION END ---

    
# Placeholder for word_segments from WhisperX
# This contains the word, start time, and end time.
# In a real scenario, you would populate this list from your transcription data.
# Example:
# word_segments = [
#     {'word': 'This', 'start': 0.5, 'end': 0.8},
#     {'word': 'is', 'start': 0.8, 'end': 1.0},
#     {'word': 'a', 'start': 1.0, 'end': 1.1},
#     {'word': 'test', 'start': 1.2, 'end': 1.6},
#     # ... and so on
# ]
word_segments = time_stamp.get_time_stamp("Animate characters project.mp4")

# --- Caption Generation Logic ---

# REDUCED FONT SIZE to 75% (40 * 0.75 = 30)
font_size = 30
# Create dummy clips to get the height of a line and the width of a space.
dummy_clip = TextClip("Xg", fontsize=font_size, color='white')
line_height = dummy_clip.h + 5  # Add a 5-pixel gap between lines
space_clip = TextClip(" ", fontsize=font_size, color='white')
space_width = space_clip.w

# 1. Group words into pages based on layout
pages = []
current_page_words = []
x_pos, y_pos = 0, 0

for seg in word_segments:
    word_clip_for_size = TextClip(seg['word'], fontsize=font_size, color='white')
    word_w = word_clip_for_size.w

    # If the current word doesn't fit horizontally, wrap to the next line
    # --- MODIFICATION START ---
    # Use the new caption_panel_width for layout calculations instead of half_width
    if x_pos + word_w > caption_panel_width:
    # --- MODIFICATION END ---
        x_pos = 0
        y_pos += line_height

    # If the next line of text would go off-screen, create a new page
    if y_pos + line_height > video_height:
        pages.append(current_page_words)
        current_page_words = []
        x_pos, y_pos = 0, 0

    # Add the word with its calculated position to the current page
    current_page_words.append({
        "text": seg['word'],
        "start": seg['start'],
        "x": x_pos,
        "y": y_pos
    })
    # Update the x-position for the next word
    x_pos += word_w + space_width

# Add the last page of words
if current_page_words:
    pages.append(current_page_words)

# 2. Create a list to hold the final caption video clips (one for each page)
caption_pages = []

for i, page in enumerate(pages):
    if not page:
        continue

    # The start time of this page is the start time of its first word
    page_start_time = page[0]['start']
    
    # The end time of this page is the start of the next page, or the end of the video
    if i + 1 < len(pages):
        page_end_time = pages[i+1][0]['start']
    else:
        page_end_time = face_clip.duration

    page_duration = page_end_time - page_start_time

    if page_duration <= 0: continue

    # Create a list to hold all the word clips for the current page
    clips_for_this_page = []
    
    # --- MODIFICATION START ---
    # A black background for the caption area of this page, sized to the new panel width
    black_bg = ColorClip(size=(caption_panel_width, video_height), color=(0, 0, 0), duration=page_duration)
    # --- MODIFICATION END ---
    clips_for_this_page.append(black_bg)

    for word_info in page:
        # The word appears at its start time and stays visible for the rest of the page.
        word_start_in_page = word_info['start'] - page_start_time
        
        # Clip starts when word is spoken and lasts until the page ends
        word_duration = page_duration - word_start_in_page

        if word_duration <= 0: continue
        
        clip = TextClip(
            word_info['text'],
            fontsize=font_size,
            color='white'
        ).set_position((word_info['x'], word_info['y'])) \
         .set_start(word_start_in_page) \
         .set_duration(word_duration)
        
        clips_for_this_page.append(clip)

    # --- MODIFICATION START ---
    # Composite all the word clips for the page onto its black background using the new panel width
    page_composite = CompositeVideoClip(clips_for_this_page, size=(caption_panel_width, video_height))
    # --- MODIFICATION END ---
    # Set the absolute start time for this page clip
    page_composite = page_composite.set_start(page_start_time)
    caption_pages.append(page_composite)


# 3. Create the final caption video by compositing all the page clips
# --- MODIFICATION START ---
# The final caption video now has the same dimensions as the original video
caption_video = CompositeVideoClip(caption_pages, size=(caption_panel_width, video_height))
# --- MODIFICATION END ---
caption_video = caption_video.set_duration(face_clip.duration)

# 4. Final assembly
# --- MODIFICATION START ---
# NO LONGER NEEDED: face_clip_resized = face_clip.resize(width=half_width)

# Arrange the ORIGINAL face video and the new caption video side-by-side.
# MoviePy will automatically create a final canvas wide enough to hold both.
final_video = mp.clips_array([[face_clip, caption_video]])
# --- MODIFICATION END ---
final_video.write_videofile("final_output_karaoke_style_double_width.mp4", fps=24, codec="libx264")

print("Video generation complete!")