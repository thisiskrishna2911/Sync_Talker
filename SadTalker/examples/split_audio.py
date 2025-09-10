from pydub import AudioSegment
import os

def split_audio(file_path, split_time_sec, output_dir=None):
    # Load the audio
    audio = AudioSegment.from_file(file_path)

    # Calculate split time in milliseconds
    split_time_ms = split_time_sec * 1000

    # Split the audio into two parts
    first_part = audio[:split_time_ms]
    second_part = audio[split_time_ms:]

    # Output directory handling
    if output_dir is None:
        output_dir = os.path.dirname(file_path)
    
    # Output file names
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    ext = os.path.splitext(file_path)[1]

    first_part_path = os.path.join(output_dir, f"{base_name}_part1{ext}")
    second_part_path = os.path.join(output_dir, f"{base_name}_part2{ext}")

    # Export both parts
    first_part.export(first_part_path, format=ext[1:])
    second_part.export(second_part_path, format=ext[1:])

    print(f"Audio split successfully:\n - First part: {first_part_path}\n - Second part: {second_part_path}")

# Example usage
split_audio("output0.wav", split_time_sec=88)  # Splits at 30 seconds
