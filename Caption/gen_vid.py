import argparse
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ColorClip
import moviepy.editor as mp
import numpy as np
from moviepy.config import change_settings
import whisperx
import os

def get_time_stamp(path):
    # 1. Load model and transcribe
    model = whisperx.load_model("large-v2", device="cpu", compute_type="float32")
    audio = whisperx.load_audio(path)
    result = model.transcribe(audio, language='en')

    # 2. Load alignment model
    alignment_model, metadata = whisperx.load_align_model(language_code=result["language"], device="cpu")

    # 3. Perform alignment to get word-level timestamps
    result_aligned = whisperx.align(result["segments"], alignment_model, metadata, audio, device="cpu")

    # 4. Extract word-level segments
    word_segments = result_aligned["word_segments"]
    print("Word segments:", word_segments)
    return word_segments

def make_karaoke_video(video_input, output_path, imagemagick_path):
    # Fix: Only allow known video formats as output
    ALLOWED_VIDEO_EXTS = [".mp4", ".avi", ".mov", ".mkv", ".webm"]
    out_ext = os.path.splitext(output_path)[1].lower()
    if out_ext not in ALLOWED_VIDEO_EXTS:
        # If output file does not end with one of the allowed video file extensions, use .mp4 instead and warn user
        safe_output_path = os.path.splitext(output_path)[0] + ".mp4"
        print(f"⚠️ Output file extension '{out_ext}' is not a standard video format. Changing output file to: '{safe_output_path}'")
        output_path = safe_output_path

    # Set the path to your ImageMagick binary.
    change_settings({
        "IMAGEMAGICK_BINARY": imagemagick_path
    })

    face_clip = VideoFileClip(video_input)
    video_width, video_height = face_clip.size
    caption_panel_width = video_width  # Caption panel is same width as video (side-by-side)
    total_width = video_width * 2

    print("Transcribing and aligning audio...")
    word_segments = get_time_stamp(video_input)

    # --- Caption Generation Logic ---
    font_size = 30  # 75% as before
    dummy_clip = TextClip("Xg", fontsize=font_size, color='white')
    line_height = dummy_clip.h + 5
    space_clip = TextClip(" ", fontsize=font_size, color='white')
    space_width = space_clip.w

    # 1. Group words into pages based on new layout (caption_panel_width)
    pages = []
    current_page_words = []
    x_pos, y_pos = 0, 0

    for seg in word_segments:
        word_clip_for_size = TextClip(seg['word'], fontsize=font_size, color='white')
        word_w = word_clip_for_size.w

        # Wrap to next line if necessary
        if x_pos + word_w > caption_panel_width:
            x_pos = 0
            y_pos += line_height

        # If the next line of text would go off-screen, create a new page
        if y_pos + line_height > video_height:
            page_height = y_pos + line_height
            pages.append({'words': current_page_words, 'height': page_height})
            current_page_words = []
            x_pos, y_pos = 0, 0

        current_page_words.append({
            "text": seg['word'],
            "start": seg['start'],
            "x": x_pos,
            "y": y_pos
        })
        x_pos += word_w + space_width

    # Add the last page of words
    if current_page_words:
        page_height = y_pos + line_height
        pages.append({'words': current_page_words, 'height': page_height})

    # 2. Create list of caption video clips (each with width=caption_panel_width)
    caption_pages = []

    for i, page in enumerate(pages):
        page_words = page['words']
        if not page_words:
            continue

        page_start_time = page_words[0]['start']
        if i + 1 < len(pages):
            page_end_time = pages[i+1]['words'][0]['start']
        else:
            page_end_time = face_clip.duration

        page_duration = page_end_time - page_start_time
        if page_duration <= 0:
            continue

        # Compose all word clips over a black bg
        clips_for_this_page = []
        black_bg = ColorClip(size=(caption_panel_width, video_height), color=(0, 0, 0), duration=page_duration)
        clips_for_this_page.append(black_bg)

        for word_info in page_words:
            word_start_in_page = word_info['start'] - page_start_time
            word_duration = page_duration - word_start_in_page
            if word_duration <= 0:
                continue
            clip = TextClip(
                word_info['text'],
                fontsize=font_size,
                color='white'
            ).set_position((word_info['x'], word_info['y'])) \
                .set_start(word_start_in_page) \
                .set_duration(word_duration)
            clips_for_this_page.append(clip)

        page_composite = CompositeVideoClip(clips_for_this_page, size=(caption_panel_width, video_height))
        page_composite = page_composite.set_start(page_start_time)
        caption_pages.append(page_composite)

    # 3. Final caption video: width = caption_panel_width
    caption_video = CompositeVideoClip(caption_pages, size=(caption_panel_width, video_height))
    caption_video = caption_video.set_duration(face_clip.duration)

    # 4. Final assembly: arrange original video (left), captions (right)
    # Keep the full original video (not cropped/resized), and put caption video right of it
    final_video = mp.clips_array([[face_clip, caption_video]])
    final_video = final_video.set_duration(face_clip.duration)
    final_video.write_videofile(output_path, fps=24, codec="libx264")

    print(f"Video generation complete! Saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Create a karaoke-style video with side-by-side captions.")
    parser.add_argument("video_input", help="Path to the input video file.")
    parser.add_argument("-o", "--output", default="final_output_karaoke_style.mp4", help="Output video path.")
    parser.add_argument("--imagemagick", default=r"D:\Installations\ImageMagick-7.1.2-Q16-HDRI\magick.exe", help="Path to the ImageMagick executable.")
    args = parser.parse_args()

    make_karaoke_video(args.video_input, args.output, args.imagemagick)

if __name__ == "__main__":
    main()