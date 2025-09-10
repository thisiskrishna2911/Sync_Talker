import os
import time
from text_to_audio import generate_audio

# Step 1: Your script
script = "Hello, I am your virtual internship mentor. Thank you!"

# Step 2: Convert text to audio
generate_audio(script)

# Step 3: Generate video with SadTalker
image_path = "examples/source_image/happy1.png"
audio_path = "examples/driven_audio/audio.wav"

# Measure start time
start_time = time.time()

# Optimized SadTalker command
exit_code = os.system(
    f'python inference.py '
    f'--driven_audio "{audio_path}" '
    f'--source_image "{image_path}" '
    f'--result_dir results '
    f'--checkpoint_dir checkpoints '
    f'--size 256 '
    f'--batch_size 1 '
    f'--still '
    f'--preprocess crop '
    f'--verbose '
)

# Measure end time
end_time = time.time()
duration = end_time - start_time

# Print result
if exit_code == 0:
    print(f"✅ Video generation completed in {duration:.2f} seconds.")
else:
    print(f"❌ Video generation failed after {duration:.2f} seconds.")