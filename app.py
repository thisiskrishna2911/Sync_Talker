import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import glob
import sys

app = Flask(__name__)

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
app.config['OUTPUT_FOLDER'] = os.path.join(BASE_DIR, 'static', 'output')
SAD_TALKER_PATH = os.path.join(BASE_DIR, "SadTalker")

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image = request.files.get('image')
        audio = request.files.get('audio')

        if not image or not audio:
            return "Please upload both an image and an audio file.", 400

        img_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio.filename)

        image.save(img_path)
        audio.save(audio_path)

        abs_audio_path = os.path.abspath(audio_path)
        abs_img_path = os.path.abspath(img_path)
        abs_result_dir = os.path.abspath(app.config['OUTPUT_FOLDER'])

        # Use the same python interpreter that is running Flask
        python_executable = sys.executable
        
        cmd = [
            python_executable, "inference.py",
            "--driven_audio", abs_audio_path,
            "--source_image", abs_img_path,
            "--result_dir", abs_result_dir,
            "--enhancer", "gfpgan"
        ]

        try:
            subprocess.run(cmd, check=True, cwd=SAD_TALKER_PATH)
        except subprocess.CalledProcessError as e:
            print(f"Error running SadTalker: {e}")
            # You might want to add the debug code from the previous step here
            # to capture and display stderr if this fails again.
            return "An error occurred while processing the video.", 500

        # --- CORRECTED LOGIC: Find the newest MP4 file ---
        
        # 1. Get a list of all .mp4 files in the output directory
        all_videos = glob.glob(os.path.join(abs_result_dir, '*.mp4'))

        if not all_videos:
            return "Processing failed to produce a video file. Check the console for errors.", 500

        # 2. Find the most recently modified file among them
        latest_video = max(all_videos, key=os.path.getmtime)
        
        # 3. Get just the filename from the full path
        final_video_filename = os.path.basename(latest_video)

        # 4. Redirect to the result page with the correct filename
        return redirect(url_for('result', filename=final_video_filename))

    return render_template('index.html')


# --- Simplified Result and Serving Routes ---

@app.route('/result/<filename>')
def result(filename):
    # We only need the filename, no timestamp folder
    return render_template('result.html', filename=filename)


@app.route('/static/output/<filename>')
def download_file(filename):
    # Serve the file directly from the output folder
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)