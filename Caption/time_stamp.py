import whisperx

def get_time_stamp(path):
    # 1. Load model and transcribe
    model = whisperx.load_model("large-v2", device="cpu", compute_type="float32")
    audio = whisperx.load_audio(path)  # Replace with your actual path
    result = model.transcribe(audio, language='en')

    # 2. Load alignment model
    alignment_model, metadata = whisperx.load_align_model(language_code=result["language"], device="cpu")

    # 3. Perform alignment to get word-level timestamps
    result_aligned = whisperx.align(result["segments"], alignment_model, metadata, audio, device="cpu")

    # 4. Extract word-level segments
    word_segments = result_aligned["word_segments"]
    print(word_segments)
    return word_segments

get_time_stamp("text_integration\\vid1\\2025_07_24_12.28.49.mp4")