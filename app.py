import logging
import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import glob
import sys
import uuid
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)


app = Flask(__name__)

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
app.config['OUTPUT_FOLDER'] = os.path.join(BASE_DIR, 'static', 'output')
# Assumes inference.py is in the same directory as app.py
SAD_TALKER_PATH = f"{BASE_DIR}/SadTalker" 

# Create directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

def save_file(file):
    """Saves a file to the upload folder with a unique name and returns the absolute path."""
    if not file or file.filename == '':
        return None
    # Generate a unique filename to prevent overwriting and conflicts
    filename = file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return os.path.abspath(filepath)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # --- 1. Handle File Uploads ---
        source_image_file = request.files.get('source_image')
        driven_audio_file = request.files.get('driven_audio')

        # Optional reference video uploads
        ref_eyeblink_file = request.files.get('ref_eyeblink')
        ref_pose_file = request.files.get('ref_pose')

        if not source_image_file or not driven_audio_file:
            return "Please upload both a source image and a driven audio file.", 400

        source_image_path = save_file(source_image_file)
        driven_audio_path = save_file(driven_audio_file)
        ref_eyeblink_path = save_file(ref_eyeblink_file)
        ref_pose_path = save_file(ref_pose_file)

        abs_result_dir = os.path.abspath(app.config['OUTPUT_FOLDER'])
        python_executable = "D:\Installations\Anaconda\envs\sad\python.exe"

        # --- 2. Build the SadTalker Command ---
        # Start with the mandatory arguments
        cmd = [
            python_executable, "inference.py",
            "--driven_audio", driven_audio_path,
            "--source_image", source_image_path,
            "--result_dir", abs_result_dir,
        ]

        # --- Add arguments to the command only if they have a value ---

        # Add optional reference videos if they were uploaded
        if ref_eyeblink_path:
            cmd.extend(["--ref_eyeblink", ref_eyeblink_path])
        if ref_pose_path:
            cmd.extend(["--ref_pose", ref_pose_path])

        # Preprocessing and Size will always have a value from the dropdown
        cmd.extend(["--preprocess", request.form.get('preprocess', 'crop')])
        cmd.extend(["--size", request.form.get('size', '256')])
        
        # Add numeric/text inputs only if the user has provided a non-empty value
        pose_style = request.form.get('pose_style')
        if pose_style:
            cmd.extend(["--pose_style", pose_style])
            
        expression_scale = request.form.get('expression_scale')
        if expression_scale:
            cmd.extend(["--expression_scale", expression_scale])
        
        # Add enhancers only if a specific option other than 'None' is chosen
        enhancer = request.form.get('enhancer')
        if enhancer and enhancer != 'None':
            cmd.extend(["--enhancer", enhancer])
            
        background_enhancer = request.form.get('background_enhancer')
        if background_enhancer and background_enhancer != 'None':
            cmd.extend(["--background_enhancer", background_enhancer])
            
        # Add flags (checkboxes) only if they are checked in the form
        if request.form.get('still'):
            cmd.append("--still")
        if request.form.get('face3dvis'):
            cmd.append("--face3dvis")
        if request.form.get('verbose'):
            cmd.append("--verbose")
        if request.form.get('cpu'):
            cmd.append("--cpu")

        # Handle head rotation inputs. Use strip() to ignore empty spaces.
        input_yaw = request.form.get('input_yaw')
        if input_yaw and input_yaw.strip():
            cmd.extend(['--input_yaw'] + input_yaw.strip().split())

        input_pitch = request.form.get('input_pitch')
        if input_pitch and input_pitch.strip():
            cmd.extend(['--input_pitch'] + input_pitch.strip().split())
            
        input_roll = request.form.get('input_roll')
        if input_roll and input_roll.strip():
            cmd.extend(['--input_roll'] + input_roll.strip().split())

        # --- 3. Run the Command ---
        try:
            print("Running command:", " ".join(cmd))
            subprocess.run(cmd, check=True, cwd=SAD_TALKER_PATH)
        except subprocess.CalledProcessError as e:
            print(f"Error running SadTalker: {e}")
            # Consider capturing stderr to show more detailed errors to the user
            return "An error occurred while processing the video. Check the server console for details.", 500
        except FileNotFoundError:
            return "Error: 'inference.py' not found. Make sure it's in the correct directory.", 500

        # --- 4. Find the result and redirect ---
        # Get a list of all .mp4 files in the output directory
        all_videos = glob.glob(os.path.join(abs_result_dir, '*.mp4'))
        if not all_videos:
            return "Processing failed to produce a video file. Check the server console for errors.", 500

        # Find the most recently modified video file
        latest_video = max(all_videos, key=os.path.getmtime)
        final_video_filename = os.path.basename(latest_video)

        # Redirect to the result page with the correct filename
        return redirect(url_for('result', filename=final_video_filename))

    # For a GET request, just render the main page
    return render_template('index.html')


@app.route('/result/<filename>')
def result(filename):
    """Renders the page to display the generated video."""
    return render_template('result.html', filename=filename)


@app.route('/static/output/<filename>')
def serve_output_file(filename):
    """Serves the generated video file for viewing/downloading."""
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)


if __name__ == '__main__':
    # Set host to '0.0.0.0' to make it accessible on your local network
    app.run(debug=True, host='0.0.0.0', port=5000)