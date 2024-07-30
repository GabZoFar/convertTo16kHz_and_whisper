# Audio Conversion and Transcription Script

This script converts audio files to 16kHz and transcribes them using the Whisper model. The transcriptions are saved as text files.

## Prerequisites

- Python 3.x
- `ffmpeg` and `ffprobe` installed and available in your system's PATH
- Whisper model and its dependencies

## Setup

1. **Clone the repository:**

    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Install dependencies:**

    Ensure you have `ffmpeg` and `ffprobe` installed. You can download them from [FFmpeg's official website](https://ffmpeg.org/download.html).

3. **Download the Whisper model:**

    Place the Whisper model file (`ggml-large-v3-q5_0.bin`) in the `models` directory.

## Configuration

Edit the script to set the correct paths for your input, output, and text output directories:

## Directory containing the audio files
input_dir = "path/to/input_directory"
output_dir = "path/to/output_directory"
txt_output_dir = "path/to/txt_output_directory"


## Usage

Run the script:
python convertnwhisper.py


## How it works

The script will:

1. Loop through all audio files in the input directory.
2. Convert audio files to 16kHz if they are not already.
3. Transcribe the audio files using the Whisper model.
4. Save the transcriptions as text files in the specified output directory.

## Logging

The script logs its operations to `conversion.log`. You can check this file for detailed information about the conversion and transcription processes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [FFmpeg](https://ffmpeg.org/)
- [Whisper](https://github.com/openai/whisper)

Make sure to replace <repository_url> and <repository_directory> with the actual URL and directory name of your repository.