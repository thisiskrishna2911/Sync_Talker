import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'SadTalker/SadTalker/uploads'
app.config['OUTPUT_FOLDER'] = 'static/output'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

SAD_TALKER_PATH = "."  # path to your SadTalker repo

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image = request.files.get('image')
        audio = request.files.get('audio')
        res = result.form.get('res')
        print(res)
        if not image or not audio:
            return "Please upload both image and audio", 400

        img_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio.filename)

        image.save(img_path)
        audio.save(audio_path)

        # Output filename
        output_video = f"{os.path.splitext(image.filename)[0]}_talk.mp4"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_video)

        # Run SadTalker inference.py
        cmd = [
            "python", os.path.join(SAD_TALKER_PATH, "inference.py"),
            "--driven_audio", audio_path,
            "--source_image", img_path,
            "--result_dir", app.config['OUTPUT_FOLDER']
        ]
        subprocess.run(cmd, check=True, cwd=r"D:\SyncTalker\SadTalker\SadTalker")

        return redirect(url_for('result', filename=output_video))

    return render_template('index.html')

@app.route('/result/<filename>')
def result(filename):
    return render_template('result.html', filename=filename)

@app.route('/static/output/<filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
