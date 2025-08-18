from gtts import gTTS
from pydub import AudioSegment
from pydub.utils import which

AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")
from pydub import AudioSegment
import os

def generate_audio(text, output="examples/driven_audio/audio.wav"):
    mp3_path = "temp_audio.mp3"
    tts = gTTS(text=text, lang='en', slow=False, tld="co.in")
    tts.save(mp3_path)

    # Convert to WAV
    sound = AudioSegment.from_mp3(mp3_path)
    sound.export(output, format="wav")

    os.remove(mp3_path)
    print(f"✅ Audio saved at: {output}")

# CLI mode
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, required=True)
    parser.add_argument("--voice", type=str, default="male")
    parser.add_argument("--output", type=str, default="examples/driven_audio/audio.wav")
    args = parser.parse_args()

    generate_audio(args.text, args.output)