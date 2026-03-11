# Sinhala Video Subtitle Translator

A desktop Python application that extracts embedded English subtitles from video files (like MP4, MKV) and translates them into a standalone Sinhala `.srt` subtitle track. It uses a modern GUI built with Tkinter for easy file selection.

## Features
- **Embedded Subtitle Extraction**: Automatically pulls the English subtitle stream from your video files without requiring hardcoded OCR.
- **Bulk Processing**: Select one or multiple video files at once to queue them up for translation.
- **Automated Translation**: Uses `deep-translator` (Google Translate) to translate English SRT blocks into Sinhala (`si`), preserving precise timestamps.
- **Built-in FFmpeg**: Integrates `imageio-ffmpeg` to automatically download and utilize the required FFmpeg components without any manual system installations or PATH configurations.

## Requirements
- Python 3.8+ 

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sankethabilas21/sub2sinhala_script.git
   cd sub2sinhala_script
   ```

2. **Create a virtual environment (Optional but Recommended):**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *This will install `deep-translator`, `pysrt`, and `imageio-ffmpeg`.*

## Usage

1. **Run the Application:**
   ```bash
   python main.py
   ```
   
2. **Translate Subtitles:**
   - Click the "Browse Video" button in the GUI.
   - Select one or more video files (e.g., standard `.mkv` or `.mp4` files with embedded English tracks).
   - Click "Start Translation". 
   - Wait for the pipeline to finish. You can view the live progress logs inside the application window.

3. **Result:**
   - Once completed, the translated subtitle files will be saved in the same directory as your original video files with `_si.srt` appended to the name. You can then load these `.srt` files manually into media players like PotPlayer or VLC.

## Note
- This tool requires a live internet connection to perform the translations via Google Translate.
- If your video file has *hardcoded* (burned-in) subtitles instead of embedded text tracks, this tool will not be able to extract them.
