from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ColorClip
import moviepy.editor as mp
import numpy as np
from moviepy.config import change_settings

# Set the path to your ImageMagick binary.
# This is necessary for TextClip to work on some systems.
change_settings({
    "IMAGEMAGICK_BINARY": r"D:\Installations\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
})

# Load your SadTalker video
path = "SadTalker\\results\\2025_07_28_16.39.39.mp4"
face_clip = VideoFileClip(path)

# Setup dimensions for the video and caption area
video_width, video_height = face_clip.size
half_width = video_width // 2

# Placeholder for word_segments from WhisperX
# This contains the word, start time, and end time.
word_segments = [{'word': 'Machine', 'start': np.float64(0.031), 'end': np.float64(0.552), 'score': np.float64(0.831)}, {'word': 'learning', 'start': np.float64(0.612), 'end': np.float64(0.972), 'score': np.float64(0.749)}, {'word': 'is', 'start': np.float64(1.072), 'end': np.float64(1.152), 'score': np.float64(0.896)}, {'word': 'a', 'start': np.float64(1.233), 'end': np.float64(1.253), 'score': np.float64(0.626)}, {'word': 'branch', 'start': np.float64(1.333), 'end': np.float64(1.693), 'score': np.float64(0.897)}, {'word': 'of', 'start': np.float64(1.773), 'end': np.float64(1.813), 'score': np.float64(0.814)}, {'word': 'artificial', 'start': np.float64(1.853), 'end': np.float64(2.634), 'score': np.float64(0.858)}, {'word': 'intelligence', 'start': np.float64(2.714), 'end': np.float64(3.395), 'score': np.float64(0.856)}, {'word': 'that', 'start': np.float64(3.475), 'end': np.float64(3.616), 'score': np.float64(0.93)}, {'word': 'enables', 'start': np.float64(3.776), 'end': np.float64(4.216), 'score': np.float64(0.857)}, {'word': 'computers', 'start': np.float64(4.316), 'end': np.float64(4.997), 'score': np.float64(0.902)}, {'word': 'to', 'start': np.float64(5.057), 'end': np.float64(5.177), 'score': np.float64(0.788)}, {'word': 'learn', 'start': np.float64(5.218), 'end': np.float64(5.438), 'score': np.float64(0.671)}, {'word': 'from', 'start': np.float64(5.518), 'end': np.float64(5.678), 'score': np.float64(0.994)}, {'word': 'data', 'start': np.float64(5.758), 'end': np.float64(6.179), 'score': np.float64(0.913)}, {'word': 'and', 'start': np.float64(7.14), 'end': np.float64(7.24), 'score': np.float64(0.95)}, {'word': 'improve', 'start': np.float64(7.28), 'end': np.float64(7.801), 'score': np.float64(0.842)}, {'word': 'their', 'start': np.float64(7.841), 'end': np.float64(8.001), 'score': np.float64(0.79)}, {'word': 'performance', 'start': np.float64(8.061), 'end': np.float64(8.662), 'score': np.float64(0.862)}, {'word': 'without', 'start': np.float64(8.742), 'end': np.float64(9.122), 'score': np.float64(0.776)}, {'word': 'being', 'start': np.float64(9.203), 'end': np.float64(9.423), 'score': np.float64(0.561)}, {'word': 'explicitly', 'start': np.float64(9.523), 'end': np.float64(10.264), 'score': np.float64(0.844)}, {'word': 'programmed.', 'start': np.float64(10.364), 'end': np.float64(10.945), 'score': np.float64(0.914)}, {'word': 'Instead', 'start': np.float64(11.565), 'end': np.float64(11.966), 'score': np.float64(0.786)}, {'word': 'of', 'start': np.float64(12.046), 'end': np.float64(12.106), 'score': np.float64(0.845)}, {'word': 'writing', 'start': np.float64(12.226), 'end': np.float64(12.627), 'score': np.float64(0.918)}, {'word': 'specific', 'start': np.float64(12.687), 'end': np.float64(13.248), 'score': np.float64(0.931)}, {'word': 'instructions,', 'start': np.float64(13.348), 'end': np.float64(14.089), 'score': np.float64(0.906)}, {'word': 'we', 'start': np.float64(14.709), 'end': np.float64(14.87), 'score': np.float64(0.98)}, {'word': 'give', 'start': np.float64(14.93), 'end': np.float64(15.11), 'score': np.float64(0.993)}, {'word': 'machines', 'start': np.float64(15.21), 'end': np.float64(15.691), 'score': np.float64(0.729)}, {'word': 'large', 'start': np.float64(15.811), 'end': np.float64(16.131), 'score': np.float64(0.86)}, {'word': 'amounts', 'start': np.float64(16.171), 'end': np.float64(16.532), 'score': np.float64(0.746)}, {'word': 'of', 'start': np.float64(16.632), 'end': np.float64(16.672), 'score': np.float64(1.0)}, {'word': 'data', 'start': np.float64(16.752), 'end': np.float64(17.132), 'score': np.float64(0.942)}, {'word': 'and', 'start': np.float64(17.213), 'end': np.float64(17.293), 'score': np.float64(0.98)}, {'word': 'let', 'start': np.float64(17.353), 'end': np.float64(17.533), 'score': np.float64(0.912)}, {'word': 'them', 'start': np.float64(17.593), 'end': np.float64(17.753), 'score': np.float64(0.881)}, {'word': 'find', 'start': np.float64(17.833), 'end': np.float64(18.094), 'score': np.float64(0.801)}, {'word': 'patterns', 'start': np.float64(18.214), 'end': np.float64(18.674), 'score': np.float64(0.931)}, {'word': 'or', 'start': np.float64(18.855), 'end': np.float64(18.915), 'score': np.float64(0.998)}, {'word': 'make', 'start': np.float64(18.975), 'end': np.float64(19.175), 'score': np.float64(0.865)}, {'word': 'predictions.', 'start': np.float64(19.235), 'end': np.float64(20.757), 'score': np.float64(0.819)}, {'word': 'For', 'start': np.float64(20.737), 'end': np.float64(21.097), 'score': np.float64(0.67)}, {'word': 'example,', 'start': np.float64(21.197), 'end': np.float64(21.818), 'score': np.float64(0.91)}, {'word': 'in', 'start': np.float64(21.858), 'end': np.float64(22.419), 'score': np.float64(0.877)}, {'word': 'spam', 'start': np.float64(22.499), 'end': np.float64(22.919), 'score': np.float64(0.962)}, {'word': 'detection,', 'start': np.float64(22.959), 'end': np.float64(23.58), 'score': np.float64(0.935)}, {'word': 'a', 'start': np.float64(24.08), 'end': np.float64(24.12), 'score': np.float64(0.989)}, {'word': 'machine', 'start': np.float64(24.16), 'end': np.float64(24.581), 'score': np.float64(0.822)}, {'word': 'learning', 'start': np.float64(24.641), 'end': np.float64(24.961), 'score': np.float64(0.889)}, {'word': 'model', 'start': np.float64(25.041), 'end': np.float64(25.422), 'score': np.float64(0.87)}, {'word': 'can', 'start': np.float64(25.482), 'end': np.float64(25.642), 'score': np.float64(0.998)}, {'word': 'learn', 'start': np.float64(25.702), 'end': np.float64(25.942), 'score': np.float64(0.717)}, {'word': 'to', 'start': np.float64(26.002), 'end': np.float64(26.082), 'score': np.float64(0.99)}, {'word': 'recognize', 'start': np.float64(26.163), 'end': np.float64(26.763), 'score': np.float64(0.779)}, {'word': 'spam', 'start': np.float64(26.823), 'end': np.float64(27.224), 'score': np.float64(0.901)}, {'word': 'emails', 'start': np.float64(27.244), 'end': np.float64(27.644), 'score': np.float64(0.809)}, {'word': 'by', 'start': np.float64(27.764), 'end': np.float64(27.904), 'score': np.float64(0.999)}, {'word': 'analyzing', 'start': np.float64(28.044), 'end': np.float64(28.605), 'score': np.float64(0.933)}, {'word': 'thousands', 'start': np.float64(28.685), 'end': np.float64(29.166), 'score': np.float64(0.71)}, {'word': 'of', 'start': np.float64(29.266), 'end': np.float64(29.346), 'score': np.float64(0.981)}, {'word': 'labeled', 'start': np.float64(29.466), 'end': np.float64(29.906), 'score': np.float64(0.818)}, {'word': 'messages.', 'start': np.float64(30.847), 'end': np.float64(31.468), 'score': np.float64(0.973)}, {'word': 'There', 'start': np.float64(32.009), 'end': np.float64(32.209), 'score': np.float64(0.666)}, {'word': 'are', 'start': np.float64(32.289), 'end': np.float64(32.369), 'score': np.float64(0.921)}, {'word': 'different', 'start': np.float64(32.449), 'end': np.float64(32.829), 'score': np.float64(0.921)}, {'word': 'types', 'start': np.float64(32.929), 'end': np.float64(33.23), 'score': np.float64(0.867)}, {'word': 'of', 'start': np.float64(33.33), 'end': np.float64(33.41), 'score': np.float64(0.957)}, {'word': 'machine', 'start': np.float64(33.45), 'end': np.float64(33.89), 'score': np.float64(0.664)}, {'word': 'learning,', 'start': np.float64(33.93), 'end': np.float64(34.331), 'score': np.float64(0.837)}, {'word': 'including', 'start': np.float64(34.952), 'end': np.float64(35.492), 'score': np.float64(0.939)}, {'word': 'supervised', 'start': np.float64(35.572), 'end': np.float64(36.233), 'score': np.float64(0.895)}, {'word': 'learning,', 'start': np.float64(36.333), 'end': np.float64(36.713), 'score': np.float64(0.831)}, {'word': 'where', 'start': np.float64(37.174), 'end': np.float64(37.394), 'score': np.float64(0.854)}, {'word': 'the', 'start': np.float64(37.454), 'end': np.float64(37.534), 'score': np.float64(0.936)}, {'word': 'model', 'start': np.float64(37.614), 'end': np.float64(37.975), 'score': np.float64(0.861)}, {'word': 'learns', 'start': np.float64(38.055), 'end': np.float64(38.335), 'score': np.float64(0.746)}, {'word': 'from', 'start': np.float64(38.355), 'end': np.float64(38.575), 'score': np.float64(0.741)}, {'word': 'labeled', 'start': np.float64(38.615), 'end': np.float64(39.056), 'score': np.float64(0.613)}, {'word': 'data,', 'start': np.float64(39.136), 'end': np.float64(39.556), 'score': np.float64(0.931)}, {'word': 'unsupervised', 'start': np.float64(40.157), 'end': np.float64(40.998), 'score': np.float64(0.903)}, {'word': 'learning,', 'start': np.float64(41.078), 'end': np.float64(41.498), 'score': np.float64(0.821)}, {'word': 'where', 'start': np.float64(41.939), 'end': np.float64(42.179), 'score': np.float64(0.925)}, {'word': 'it', 'start': np.float64(42.259), 'end': np.float64(42.319), 'score': np.float64(0.994)}, {'word': 'finds', 'start': np.float64(42.439), 'end': np.float64(42.78), 'score': np.float64(0.84)}, {'word': 'hidden', 'start': np.float64(42.8), 'end': np.float64(43.16), 'score': np.float64(0.901)}, {'word': 'patterns', 'start': np.float64(43.22), 'end': np.float64(43.7), 'score': np.float64(0.865)}, {'word': 'without', 'start': np.float64(43.781), 'end': np.float64(44.141), 'score': np.float64(0.864)}, {'word': 'labels.', 'start': np.float64(44.261), 'end': np.float64(45.242), 'score': np.float64(0.907)}, {'word': 'and', 'start': np.float64(45.222), 'end': np.float64(45.542), 'score': np.float64(0.829)}, {'word': 'reinforcement', 'start': np.float64(45.623), 'end': np.float64(46.504), 'score': np.float64(0.909)}, {'word': 'learning,', 'start': np.float64(46.584), 'end': np.float64(46.984), 'score': np.float64(0.8)}, {'word': 'where', 'start': np.float64(47.445), 'end': np.float64(47.685), 'score': np.float64(0.968)}, {'word': 'it', 'start': np.float64(47.745), 'end': np.float64(47.846), 'score': np.float64(0.993)}, {'word': 'learns', 'start': np.float64(47.926), 'end': np.float64(48.226), 'score': np.float64(0.722)}, {'word': 'through', 'start': np.float64(48.326), 'end': np.float64(48.546), 'score': np.float64(0.958)}, {'word': 'trial', 'start': np.float64(48.607), 'end': np.float64(49.007), 'score': np.float64(0.787)}, {'word': 'and', 'start': np.float64(49.067), 'end': np.float64(49.147), 'score': np.float64(0.969)}, {'word': 'error.', 'start': np.float64(49.267), 'end': np.float64(49.528), 'score': np.float64(0.998)}, {'word': 'Machine', 'start': np.float64(50.048), 'end': np.float64(50.449), 'score': np.float64(0.675)}, {'word': 'learning', 'start': np.float64(50.509), 'end': np.float64(50.83), 'score': np.float64(0.886)}, {'word': 'powers', 'start': np.float64(50.91), 'end': np.float64(51.31), 'score': np.float64(0.837)}, {'word': 'many', 'start': np.float64(51.41), 'end': np.float64(51.671), 'score': np.float64(0.913)}, {'word': 'technologies', 'start': np.float64(51.731), 'end': np.float64(52.532), 'score': np.float64(0.925)}, {'word': 'we', 'start': np.float64(52.612), 'end': np.float64(52.752), 'score': np.float64(0.954)}, {'word': 'use', 'start': np.float64(52.932), 'end': np.float64(53.073), 'score': np.float64(0.8)}, {'word': 'every', 'start': np.float64(53.273), 'end': np.float64(53.533), 'score': np.float64(0.777)}, {'word': 'day,', 'start': np.float64(53.573), 'end': np.float64(53.773), 'score': np.float64(0.989)}, {'word': 'like', 'start': np.float64(54.374), 'end': np.float64(54.615), 'score': np.float64(0.802)}, {'word': 'recommendation', 'start': np.float64(54.735), 'end': np.float64(55.576), 'score': np.float64(0.927)}, {'word': 'systems,', 'start': np.float64(55.656), 'end': np.float64(56.177), 'score': np.float64(0.927)}, {'word': 'voice', 'start': np.float64(56.697), 'end': np.float64(57.078), 'score': np.float64(0.905)}, {'word': 'assistants,', 'start': np.float64(57.178), 'end': np.float64(57.819), 'score': np.float64(0.932)}, {'word': 'and', 'start': np.float64(58.32), 'end': np.float64(58.42), 'score': np.float64(0.907)}, {'word': 'facial', 'start': np.float64(58.52), 'end': np.float64(58.96), 'score': np.float64(0.924)}, {'word': 'recognition.', 'start': np.float64(59.041), 'end': np.float64(59.741), 'score': np.float64(0.953)}, {'word': 'As', 'start': np.float64(60.262), 'end': np.float64(60.402), 'score': np.float64(0.677)}, {'word': 'data', 'start': np.float64(60.482), 'end': np.float64(60.883), 'score': np.float64(0.882)}, {'word': 'grows,', 'start': np.float64(60.943), 'end': np.float64(61.324), 'score': np.float64(0.836)}, {'word': 'so', 'start': np.float64(61.844), 'end': np.float64(62.004), 'score': np.float64(1.0)}, {'word': 'does', 'start': np.float64(62.065), 'end': np.float64(62.265), 'score': np.float64(0.599)}, {'word': 'the', 'start': np.float64(62.345), 'end': np.float64(62.445), 'score': np.float64(0.999)}, {'word': 'power', 'start': np.float64(62.505), 'end': np.float64(62.846), 'score': np.float64(0.815)}, {'word': 'and', 'start': np.float64(62.926), 'end': np.float64(63.006), 'score': np.float64(0.913)}, {'word': 'potential', 'start': np.float64(63.066), 'end': np.float64(63.667), 'score': np.float64(0.878)}, {'word': 'of', 'start': np.float64(63.747), 'end': np.float64(63.807), 'score': np.float64(0.997)}, {'word': 'machine', 'start': np.float64(63.927), 'end': np.float64(64.328), 'score': np.float64(0.777)}, {'word': 'learning', 'start': np.float64(64.368), 'end': np.float64(64.728), 'score': np.float64(0.728)}, {'word': 'in', 'start': np.float64(64.828), 'end': np.float64(64.908), 'score': np.float64(0.994)}, {'word': 'shaping', 'start': np.float64(65.008), 'end': np.float64(65.389), 'score': np.float64(0.957)}, {'word': 'our', 'start': np.float64(65.509), 'end': np.float64(65.609), 'score': np.float64(0.829)}, {'word': 'world.', 'start': np.float64(65.649), 'end': np.float64(66.15), 'score': np.float64(0.828)}]
# --- Caption Generation Logic ---

# REDUCED FONT SIZE to 75% (40 * 0.75 = 30)
font_size = 15 
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
    if x_pos + word_w > half_width:
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
    
    # A black background for the caption area of this page
    black_bg = ColorClip(size=(half_width, video_height), color=(0, 0, 0), duration=page_duration)
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

    # Composite all the word clips for the page onto its black background
    page_composite = CompositeVideoClip(clips_for_this_page, size=(half_width, video_height))
    # Set the absolute start time for this page clip
    page_composite = page_composite.set_start(page_start_time)
    caption_pages.append(page_composite)


# 3. Create the final caption video by compositing all the page clips
caption_video = CompositeVideoClip(caption_pages, size=(half_width, video_height))
caption_video = caption_video.set_duration(face_clip.duration)

# 4. Final assembly
# Resize the original video to fit the left half
face_clip_resized = face_clip.resize(width=half_width)

# Arrange the face video and the caption video side-by-side
final_video = mp.clips_array([[face_clip_resized, caption_video]])
final_video.write_videofile("final_output_karaoke_style.mp4", fps=24, codec="libx264")

print("Video generation complete!")