import os
import argparse
import logging
import torch
import tempfile
from pydub import AudioSegment
from TTS.api import TTS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def convert_to_wav_if_needed(audio_path: str) -> str:
    """Convert non-WAV audio (e.g. .m4a, .mp3) to WAV temporarily."""
    ext = os.path.splitext(audio_path)[1].lower()
    if ext != ".wav":
        logger.info(f"Converting {audio_path} to WAV...")
        audio = AudioSegment.from_file(audio_path)
        tmp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        audio.export(tmp_wav.name, format="wav")
        return tmp_wav.name
    return audio_path


def get_device():
    return "cuda" if torch.cuda.is_available() else "cpu"


def clone_voice(reference_audio: str, text: str, output_file: str = "output.wav", model_name: str = None, language: str = "en"):
    """Clone a voice from a reference audio and generate the given text."""
    model_name = model_name or "tts_models/multilingual/multi-dataset/xtts_v2"
    device = get_device()

    reference_audio = convert_to_wav_if_needed(reference_audio)

    logger.info(f"Using device: {device}")
    tts = TTS(model_name=model_name, progress_bar=True).to(device)

    logger.info(f"Cloning from: {reference_audio}")
    logger.info(f"Generating text: \"{text}\"")

    tts.tts_to_file(
        text=text,
        speaker_wav=reference_audio,
        language=language,
        file_path=output_file
    )

    logger.info(f"[SUCCESS] Voice cloned and saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="🎙️ Voice Cloning CLI using Coqui TTS (XTTS v2)")
    parser.add_argument("--audio", "-a", required=True, help="Path to reference voice audio file")
    parser.add_argument("--text", "-t", required=True, help="Text to be spoken by the cloned voice")
    parser.add_argument("--output", "-o", default="cloned_voice.wav", help="Output file path")
    parser.add_argument("--model", "-m", default=None, help="Optional TTS model name (default: xtts_v2)")
    parser.add_argument("--lang", "-l", default="en", help="Language code (e.g., 'en', 'fr', 'de')")

    args = parser.parse_args()
    clone_voice(args.audio, args.text, args.output, args.model, args.lang)


if __name__ == "__main__":
    main()
