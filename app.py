import logging
import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import glob
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
app.config['OUTPUT_FOLDER'] = os.path.join(BASE_DIR, 'static', 'output')

# Paths to script locations
CLONE_VOICE_PATH = os.path.join(BASE_DIR, 'AudioMaker')
SAD_TALKER_PATH = os.path.join(BASE_DIR, 'SadTalker')
CAPTION_SCRIPT_PATH = os.path.join(BASE_DIR, 'Caption', 'gen_cap_og.py')

# Create directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

def save_file(file):
    """Saves a file to the upload folder with a unique name and returns the absolute path."""
    if not file or file.filename == '':
        return None
    filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return os.path.abspath(filepath)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # --- 1. Handle File Uploads and Pre-generated Audio ---
        source_image_file = request.files.get('source_image')
        driven_audio_path = None

        # Check if we're using audio generated from the previous step
        generated_audio_filename = request.form.get('generated_audio_filename')
        
        if generated_audio_filename:
            driven_audio_path = os.path.abspath(os.path.join(app.config['OUTPUT_FOLDER'], generated_audio_filename))
        else:
            # Fallback to file upload if no pre-generated audio is provided
            driven_audio_file = request.files.get('driven_audio')
            if not driven_audio_file:
                 return "Please provide a driven audio file.", 400
            driven_audio_path = save_file(driven_audio_file)

        if not source_image_file:
            return "Please upload a source image.", 400
            
        source_image_path = save_file(source_image_file)

        # Optional reference video uploads
        ref_eyeblink_file = request.files.get('ref_eyeblink')
        ref_pose_file = request.files.get('ref_pose')
        ref_eyeblink_path = save_file(ref_eyeblink_file)
        ref_pose_path = save_file(ref_pose_file)

        abs_result_dir = os.path.abspath(app.config['OUTPUT_FOLDER'])
        python_executable = "D:\\Installations\\Anaconda\\envs\\sad\\python.exe"

        # --- 2. Build the SadTalker Command ---
        cmd = [
            python_executable, "inference.py",
            "--driven_audio", driven_audio_path,
            "--source_image", source_image_path,
            "--result_dir", abs_result_dir,
        ]
        
        if ref_eyeblink_path: cmd.extend(["--ref_eyeblink", ref_eyeblink_path])
        if ref_pose_path: cmd.extend(["--ref_pose", ref_pose_path])
        cmd.extend(["--preprocess", request.form.get('preprocess', 'crop')])
        cmd.extend(["--size", request.form.get('size', '256')])
        pose_style = request.form.get('pose_style'); 
        if pose_style: cmd.extend(["--pose_style", pose_style])
        expression_scale = request.form.get('expression_scale'); 
        if expression_scale: cmd.extend(["--expression_scale", expression_scale])
        enhancer = request.form.get('enhancer'); 
        if enhancer and enhancer != 'None': cmd.extend(["--enhancer", enhancer])
        background_enhancer = request.form.get('background_enhancer'); 
        if background_enhancer and background_enhancer != 'None': cmd.extend(["--background_enhancer", background_enhancer])
        if request.form.get('still'): cmd.append("--still")
        if request.form.get('face3dvis'): cmd.append("--face3dvis")
        if request.form.get('verbose'): cmd.append("--verbose")
        if request.form.get('cpu'): cmd.append("--cpu")
        input_yaw = request.form.get('input_yaw'); 
        if input_yaw and input_yaw.strip(): cmd.extend(['--input_yaw'] + input_yaw.strip().split())
        input_pitch = request.form.get('input_pitch'); 
        if input_pitch and input_pitch.strip(): cmd.extend(['--input_pitch'] + input_pitch.strip().split())
        input_roll = request.form.get('input_roll'); 
        if input_roll and input_roll.strip(): cmd.extend(['--input_roll'] + input_roll.strip().split())

        # --- 3. Run the Command ---
        try:
            print("Running command:", " ".join(cmd))
            subprocess.run(cmd, check=True, cwd=SAD_TALKER_PATH)
        except subprocess.CalledProcessError as e:
            print(f"Error running SadTalker: {e}")
            return "An error occurred while processing the video.", 500
        except FileNotFoundError:
            return "Error: 'inference.py' not found.", 500

        # --- 4. Find the result and redirect ---
        all_videos = glob.glob(os.path.join(abs_result_dir, '*.mp4'))
        if not all_videos:
            return "Processing failed to produce a video file.", 500
        latest_video = max(all_videos, key=os.path.getmtime)
        final_video_filename = os.path.basename(latest_video)
        return redirect(url_for('result', filename=final_video_filename))

    # --- Handle GET request for the index page ---
    # Check if an audio filename was passed from the audio generator
    audio_filename = request.args.get('audio_filename')
    return render_template('index.html', audio_filename=audio_filename)

@app.route('/audio', methods=['GET', 'POST'])
def audio():
    if request.method == 'POST':
        audio_file = request.files.get('driven_audio')
        text = request.form.get('input_text')
        if not audio_file or not text:
            return "Please upload a sample audio file and provide the input text.", 400
        
        sample_audio_path = save_file(audio_file)
        output_filename = f"{uuid.uuid4()}.wav"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        python_executable = "D:\\Installations\\Anaconda\\envs\\text\\python.exe"

        cmd = [
            python_executable, "clone_voice.py",
            "--audio", sample_audio_path,
            "--text", text,
            "--output", output_path,
        ]

        try:
            print("Running command:", " ".join(cmd))
            # IMPORTANT: The CWD should be the folder where clone_voice.py is
            subprocess.run(cmd, check=True, cwd=CLONE_VOICE_PATH) 
        except subprocess.CalledProcessError as e:
            print(f"Error running voice cloning: {e}")
            return "An error occurred while processing the audio.", 500
        except FileNotFoundError:
            return "Error: 'clone_voice.py' not found.", 500

        return redirect(url_for('audio_success', filename=output_filename))

    return render_template("audio.html")

@app.route('/audio_success/<filename>')
def audio_success(filename):
    """Renders a page with options after audio is successfully generated."""
    return render_template('audio_success.html', filename=filename)

@app.route('/result/<filename>')
def result(filename):
    """Renders the page to display the generated video or audio."""
    return render_template('result.html', filename=filename)

@app.route('/static/output/<filename>')
def serve_output_file(filename):
    """Serves the generated video or audio file."""
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

# --- Caption Maker Route ---
@app.route('/caption', methods=['GET', 'POST'])
def caption():
    """
    Route to generate and serve a video with side-by-side captions using 'Caption/gen_cap_og.py'.
    Expects a video file upload from the user.
    """
    if request.method == 'POST':
        video_file = request.files.get('video_input')
        if not video_file:
            return "Please upload a video file for captioning.", 400
        video_path = save_file(video_file)

        output_filename = f"{uuid.uuid4()}_karaoke.mp4"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

        # Set the path to ImageMagick executable; adjust as needed for your environment
        imagemagick_path = request.form.get('imagemagick_path', r"D:\Installations\ImageMagick-7.1.2-Q16-HDRI\magick.exe")

        python_executable = "D:\\Installations\\Anaconda\\envs\\sad\\python.exe"

        cmd = [
            python_executable, CAPTION_SCRIPT_PATH,
            video_path,
            "-o", output_path,
            "--imagemagick", imagemagick_path
        ]
        try:
            print("Running caption command:", " ".join(map(str, cmd)))
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running caption generation: {e}")
            return "An error occurred while generating captions.", 500
        except FileNotFoundError:
            return "Error: Caption maker file not found.", 500
        
        return redirect(url_for('caption_result', filename=output_filename))
    return render_template('caption.html')
    
@app.route('/caption_result/<filename>')
def caption_result(filename):
    """Render the result page for the generated captioned video."""
    return render_template('caption_result.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)