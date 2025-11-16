import argparse
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ColorClip, VideoClip
import moviepy.editor as mp
import numpy as np
from moviepy.config import change_settings
import whisperx
import os
import sys

def get_time_stamp(path):
    # This function is stable and remains the same.
    print("Loading transcription model...")
    model = whisperx.load_model("large-v2", device="cpu", compute_type="float32")
    audio = whisperx.load_audio(path)
    print("Transcribing audio...")
    result = model.transcribe(audio, language='en')
    print("Loading alignment model...")
    alignment_model, metadata = whisperx.load_align_model(language_code=result["language"], device="cpu")
    print("Aligning transcription...")
    result_aligned = whisperx.align(result["segments"], alignment_model, metadata, audio, device="cpu")
    word_segments = result_aligned["word_segments"]
    print("Word-level timestamps generated.")
    return word_segments

def robust_manual_blit(background_rgb, overlay_rgb, overlay_mask, pos):
    """
    A completely rewritten, robust blitting function that handles any
    combination of input shapes from MoviePy to prevent all ValueErrors.
    """
    x, y = int(pos[0]), int(pos[1])

    # --- Data Sanitization ---
    # Ensure background is 3-channel RGB
    if background_rgb.ndim == 2:
        background_rgb = np.stack((background_rgb,) * 3, axis=-1)
    
    # Ensure overlay is 3-channel RGB
    if overlay_rgb.ndim == 2:
        overlay_rgb = np.stack((overlay_rgb,) * 3, axis=-1)

    # Ensure mask is a single channel (2D)
    if overlay_mask.ndim == 3 and overlay_mask.shape[2] == 3:
        # Convert RGB mask to single channel grayscale
        overlay_mask = overlay_mask[:, :, 0]

    h, w, _ = overlay_rgb.shape
    bg_h, bg_w, _ = background_rgb.shape

    # Boundary check
    if x >= bg_w or y >= bg_h:
        return background_rgb

    # Crop overlay if it goes out of bounds
    x_end = min(x + w, bg_w)
    y_end = min(y + h, bg_h)
    w = x_end - x
    h = y_end - y
    overlay_rgb = overlay_rgb[:h, :w]
    overlay_mask = overlay_mask[:h, :w]

    # --- Blitting Logic ---
    # Normalize mask to 0-1 range for blending
    mask_norm = overlay_mask / 255.0
    mask_norm = mask_norm[..., np.newaxis] # Add channel dimension for broadcasting

    # Get the region of interest from the background
    bg_region = background_rgb[y:y_end, x:x_end]

    # Perform the alpha blending
    composite = overlay_rgb * mask_norm + bg_region * (1 - mask_norm)

    # Place the blended region back into the background
    background_rgb[y:y_end, x:x_end] = composite.astype('uint8')
    return background_rgb

def make_karaoke_video(video_input, output_path, imagemagick_path,
                       background_color='black', text_color='white',
                       padding=20, margin=10, border_width=2,
                       border_color='white', margin_color='black'):
    if not os.path.exists(imagemagick_path):
        print(f"❌ ERROR: ImageMagick not found at '{imagemagick_path}'")
        sys.exit(1)
    change_settings({"IMAGEMAGICK_BINARY": imagemagick_path})

    face_clip = VideoFileClip(video_input)
    video_fps = face_clip.fps
    video_width, video_height = face_clip.size
    caption_panel_width = video_width

    word_segments = get_time_stamp(video_input)
    if not word_segments:
        print("❌ ERROR: No words were transcribed from the audio.")
        sys.exit(1)

    font_size = 30
    dummy_clip = TextClip("Xg", fontsize=font_size, color=text_color)
    line_height = dummy_clip.h + 5
    space_clip = TextClip(" ", fontsize=font_size, color=text_color)
    space_width = space_clip.w

    pages = []
    current_page_words = []
    x_pos, y_pos = padding, padding
    page_start_time = word_segments[0].get('start', 0)

    for seg in word_segments:
        word_clip_for_size = TextClip(seg['word'], fontsize=font_size, color=text_color)
        word_w = word_clip_for_size.w
        if x_pos + word_w > caption_panel_width - padding:
            x_pos, y_pos = padding, y_pos + line_height
        if y_pos + line_height > video_height - padding:
            page_end_time = seg['start']
            pages.append({'words': current_page_words, 'start': page_start_time, 'end': page_end_time})
            current_page_words = []
            x_pos, y_pos = padding, padding
            page_start_time = seg['start']
        current_page_words.append({"text": seg['word'], "x": x_pos, "y": y_pos})
        x_pos += word_w + space_width
    if current_page_words:
        pages.append({'words': current_page_words, 'start': page_start_time, 'end': face_clip.duration})

    print("Pre-rendering caption pages using robust manual blitting...")
    page_images = []
    for page in pages:
        # Create the border image as the base canvas
        canvas = ColorClip(size=(caption_panel_width, video_height), color=border_color, duration=1).get_frame(0)
        
        if border_width > 0:
            # Create the inner background
            inner_bg = ColorClip(size=(caption_panel_width - 2 * border_width, video_height - 2 * border_width), color=background_color, duration=1).get_frame(0)
            # Blit the background onto the border
            canvas = robust_manual_blit(canvas, inner_bg, np.full((inner_bg.shape[0], inner_bg.shape[1]), 255), (border_width, border_width))
        
        # Manually blit each word onto the canvas
        for word_info in page['words']:
            word_clip = TextClip(word_info['text'], fontsize=font_size, color=text_color, bg_color='transparent')
            word_rgb = word_clip.get_frame(0)
            word_mask = word_clip.mask.get_frame(0)
            # Correctly offset word position by border width
            pos = (word_info['x'] + border_width, word_info['y'] + border_width)
            canvas = robust_manual_blit(canvas, word_rgb, word_mask, pos)
        
        page_images.append(canvas)
    
    black_frame = np.zeros((video_height, caption_panel_width, 3), dtype="uint8")
    print(f"{len(page_images)} pages pre-rendered successfully.")

    def make_caption_frame(t):
        for i, page in enumerate(pages):
            if page['start'] <= t < page['end']:
                return page_images[i]
        return black_frame

    caption_video = VideoClip(make_caption_frame, duration=face_clip.duration)
    margin_clip = ColorClip(size=(margin, video_height), color=margin_color, duration=face_clip.duration)
    
    final_video = mp.clips_array([[face_clip, margin_clip, caption_video]])
    final_video.audio = face_clip.audio
    
    print("Writing final video file...")
    final_video.write_videofile(output_path, fps=video_fps, codec="libx264", audio_codec="aac")
    
    print(f"Video generation complete! Saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Create a karaoke-style video with side-by-side captions.")
    parser.add_argument("video_input", help="Path to the input video file.")
    parser.add_argument("-o", "--output", default="final_output_karaoke_style.mp4", help="Output video path.")
    
    imagemagick_path = r"D:\Installations\ImageMagick-7.1.2-Q16-HDRI\magick.exe"

    parser.add_argument("--background_color", default="black", help="Background color.")
    parser.add_argument("--text_color", default="white", help="Color of the caption text.")
    parser.add_argument("--padding", type=int, default=20, help="Padding around the text.")
    parser.add_argument("--margin", type=int, default=10, help="Margin between video and captions.")
    parser.add_argument("--margin_color", default="black", help="Color of the margin area.")
    parser.add_argument("--border_width", type=int, default=2, help="Width of the border.")
    parser.add_argument("--border_color", default="white", help="Color of the border.")

    args = parser.parse_args()

    make_karaoke_video(
        args.video_input, args.output, imagemagick_path,
        background_color=args.background_color, text_color=args.text_color,
        padding=args.padding, margin=args.margin,
        border_width=args.border_width, border_color=args.border_color,
        margin_color=args.margin_color
    )

if __name__ == "__main__":
    main()