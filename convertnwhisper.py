import os
import subprocess
import logging

# Set up logging
logging.basicConfig(filename='conversion.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

# Directory containing the audio files
input_dir = ".." #edit this path
output_dir = ".." #edit this path
txt_output_dir = ".." #edit this path

# Create output directories if they don't exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs(txt_output_dir, exist_ok=True)

def get_sample_rate(file_path):
    """Get the sample rate of an audio file using ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=sample_rate", "-of", "default=noprint_wrappers=1:nokey=1", file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return int(result.stdout.strip())

def convert_to_16khz(input_file, output_file):
    """Convert an audio file to 16kHz using ffmpeg."""
    logging.debug(f"Starting conversion of {input_file} to {output_file}")
    process = subprocess.Popen(
        ["ffmpeg", "-i", input_file, "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000", output_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate()
    logging.debug(f"ffmpeg stdout: {stdout}")
    logging.debug(f"ffmpeg stderr: {stderr}")
    if process.returncode != 0:
        logging.error(f"Error converting {input_file} to 16kHz: {stderr}")
    else:
        logging.info(f"Successfully converted {input_file} to 16kHz. Output: {stdout}")

def run_whisper(file_path, output_dir):
    """Run the whisper command on an audio file and save the transcript to the output directory."""
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_file = os.path.join(output_dir, base_name + ".txt")
    logging.debug(f"Running whisper on {file_path}, output will be saved to {output_file}")
    process = subprocess.Popen(
        ["./main", "-m", "models/ggml-large-v3-q5_0.bin", "-f", file_path, "-l", "auto", "--output-txt", output_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate()
    logging.debug(f"whisper stdout: {stdout}")
    logging.debug(f"whisper stderr: {stderr}")
    if process.returncode != 0:
        logging.error(f"Error running whisper on {file_path}: {stderr}")
    else:
        logging.info(f"Successfully ran whisper on {file_path}. Output: {stdout}")

# Loop through all files in the input directory
for file_name in os.listdir(input_dir):
    input_file = os.path.join(input_dir, file_name)
    ext = os.path.splitext(file_name)[1]
    
    if ext.lower() not in ['.wav', '.mp3']:
        continue  # Skip non-audio files

    try:
        sample_rate = get_sample_rate(input_file)
    except ValueError:
        print(f"Could not determine sample rate for {input_file}, skipping.")
        continue

    if sample_rate == 16000:
        print(f"File {input_file} is already in 16kHz, skipping conversion.")
        converted_file = input_file
    else:
        converted_file = os.path.join(output_dir, os.path.splitext(file_name)[0] + "16khz.wav")
        print(f"Converting {input_file} to 16kHz...")
        convert_to_16khz(input_file, converted_file)

    print(f"Running whisper on {converted_file}...")
    run_whisper(converted_file, txt_output_dir)