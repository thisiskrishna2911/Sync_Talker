import subprocess
import os

def download_and_clip(url, start_time, end_time, output_path="clipped_video.mp4"):
    # Ensure ffmpeg and yt-dlp exist
    if not shutil.which("yt-dlp"):
        raise SystemExit("Error: yt-dlp not installed. Run: pip install yt-dlp")
    if not shutil.which("ffmpeg"):
        raise SystemExit("Error: ffmpeg not installed. Install it via your package manager.")

    print("[INFO] Downloading best video + audio...")
    subprocess.run([
        "yt-dlp",
        "-f", "bestvideo+bestaudio/best",
        "-o", "temp_video.%(ext)s",
        url
    ], check=True)

    # Find the downloaded file (yt-dlp names vary)
    temp_file = next((f for f in os.listdir() if f.startswith("temp_video.")), None)
    if not temp_file:
        raise FileNotFoundError("Video download failed!")

    print("[INFO] Clipping using ffmpeg...")
    subprocess.run([
        "ffmpeg", "-y", "-i", temp_file,
        "-ss", str(start_time),
        "-to", str(end_time),
        "-c", "copy",
        output_path
    ], check=True)

    os.remove(temp_file)
    print(f"[SUCCESS] Saved clipped video → {output_path}")


if __name__ == "__main__":
    import shutil
    url = input("Enter YouTube URL: ").strip()
    start = float(input("Enter start time (in seconds): "))
    end = float(input("Enter end time (in seconds): "))
    download_and_clip(url, start, end)
