from moviepy.editor import (
    VideoFileClip, TextClip, CompositeVideoClip,
    ColorClip, clips_array
)
from moviepy.config import change_settings
import re
import os

# Set ImageMagick path if required
change_settings({
    "IMAGEMAGICK_BINARY": r"D:\Installations\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
})

# Load video
face_clip = VideoFileClip("SadTalker/results/2025_07_24_12.28.49.mp4")
video_width, video_height = face_clip.size
caption_panel_width = video_width
font_size = 30

# Dummy WhisperX output (simulate transcript with code triggers)
raw_word_segments = [
    {'word': 'Hello', 'start': 0.5, 'end': 0.8},
    {'word': 'world', 'start': 0.8, 'end': 1.0},
    {'word': 'this', 'start': 1.1, 'end': 1.3},
    {'word': 'is', 'start': 1.3, 'end': 1.5},
    {'word': 'coden{code1,code2}', 'start': 1.6, 'end': 1.8},
    {'word': 'code#', 'start': 5.0, 'end': 5.2},
    {'word': 'resuming', 'start': 5.3, 'end': 5.5},
    {'word': 'captions', 'start': 5.6, 'end': 5.9},
]

# Preprocess: Separate words and code blocks
word_segments, code_segments = [], []
showing_code = False
current_code_start, current_code_names = None, []

for seg in raw_word_segments:
    word = seg['word']
    if re.match(r'coden\{.*?\}', word):
        showing_code = True
        current_code_start = seg['start']
        current_code_names = re.findall(r'coden\{(.*?)\}', word)[0].split(',')
        current_code_names = [c.strip() for c in current_code_names]
        continue
    elif word == 'code#':
        showing_code = False
        code_segments.append({
            "start": current_code_start,
            "end": seg['end'],
            "codes": current_code_names
        })
        current_code_start, current_code_names = None, []
        continue
    if not showing_code:
        word_segments.append(seg)

# Caption layout setup
dummy_clip = TextClip("Xg", fontsize=font_size, color='white')
line_height = dummy_clip.h + 5
space_width = TextClip(" ", fontsize=font_size, color='white').w

# Group words into pages
pages = []
current_page_words = []
x_pos, y_pos = 0, 0

for seg in word_segments:
    word_clip_for_size = TextClip(seg['word'], fontsize=font_size, color='white')
    word_w = word_clip_for_size.w

    if x_pos + word_w > caption_panel_width:
        x_pos = 0
        y_pos += line_height

    if y_pos + line_height > video_height:
        pages.append(current_page_words)
        current_page_words = []
        x_pos, y_pos = 0, 0

    current_page_words.append({
        "text": seg['word'],
        "start": seg['start'],
        "x": x_pos,
        "y": y_pos
    })
    x_pos += word_w + space_width

if current_page_words:
    pages.append(current_page_words)

# Generate caption pages
caption_pages = []
for i, page in enumerate(pages):
    if not page: continue
    page_start_time = page[0]['start']
    page_end_time = pages[i + 1][0]['start'] if i + 1 < len(pages) else face_clip.duration
    page_duration = page_end_time - page_start_time
    if page_duration <= 0: continue

    clips_for_page = [ColorClip(size=(caption_panel_width, video_height), color=(0, 0, 0), duration=page_duration)]
    
    for word in page:
        word_clip = TextClip(word['text'], fontsize=font_size, color='white') \
            .set_position((word['x'], word['y'])) \
            .set_start(word['start'] - page_start_time) \
            .set_duration(page_duration - (word['start'] - page_start_time))
        clips_for_page.append(word_clip)

    page_clip = CompositeVideoClip(clips_for_page, size=(caption_panel_width, video_height)) \
        .set_start(page_start_time)
    caption_pages.append(page_clip)

# Generate code block clips
code_clips = []

for block in code_segments:
    combined_code = ""
    for name in block['codes']:
        file_path = f"code/{name}.txt"
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                combined_code += f.read() + "\n\n"
        else:
            combined_code += f"# Missing: {name}.txt\n"

    code_text_clip = TextClip(
        combined_code.strip(),
        fontsize=26,
        color='white',
        bg_color='black',
        align='West',
        size=(caption_panel_width, video_height),
        method='caption'
    ).set_duration(block['end'] - block['start']) \
     .set_start(block['start']) \
     .set_position("center")

    code_clips.append(code_text_clip)

# Combine all
caption_video = CompositeVideoClip(caption_pages + code_clips, size=(caption_panel_width, video_height)) \
    .set_duration(face_clip.duration)

final_video = clips_array([[face_clip, caption_video]])
final_video.write_videofile("final_output_code_aware.mp4", fps=24, codec="libx264")
