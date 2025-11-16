# Sync_Talker

Sync_Talker is an advanced talking-head video generation toolkit inspired by the SadTalker project. It enables photorealistic talking head generation with multiple additional features focused on accessibility and ease of use.

## Features

- **Mouth Synchronization**: Generate realistic talking-head videos synced with input audio.
- **Script Generation**: Instantly generate scripts for custom topics using built-in tools.
- **Custom Script & Audio**: Use your own scripts and voice recordings, or generate AI-powered audio versions.
- **Caption Support**: Automatically adds captions to the right side of videos for greater accessibility.
- **Flexible Input Options**: Supports uploading your source image, choosing or generating scripts, and providing custom videos for eyeblink and pose reference.
- **Accessible Interface**: Built with accessibility in mind, offering a user-friendly web interface.

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/thisiskrishna2911/Sync_Talker.git
cd Sync_Talker
```

### 2. Install dependencies
It is recommended to use a virtual environment.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Download required models

Make sure you download the pre-trained models for SadTalker and any voice cloning models as specified in their respective documentation. Place them in the appropriate directories as described in the repo.

### 4. Run the app

```bash
python app.py
```

Then open your browser at [http://localhost:5000](http://localhost:5000).

## Usage

1. **Upload a Source Image**: Choose a clear photo to animate.
2. **Script Generation**: Enter a topic to generate a script, or provide your own script.
3. **Audio Input**: Record your voice or upload a custom audio file, or use AI to generate one from the script.
4. **Customize Animation**: Optionally upload a reference video for fine-grained eye-blink or head pose control.
5. **Generate Video**: Click to generate your talking-head video. Captions will display on the right side for enhanced accessibility.
6. **Download & Share**: Download your video or share it easily.

## Credits

- Built upon [SadTalker](https://github.com/OpenTalker/SadTalker)
- Script and caption tools inspired by accessibility best practices.

## License

See [LICENSE](LICENSE) file for details.

