import os
import subprocess
import pysrt
from deep_translator import GoogleTranslator
import imageio_ffmpeg

def extract_subtitles(video_path, output_srt_path):
    """
    Extracts embedded English subtitles from a video file using ffmpeg.
    """
    try:
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        
        # First, try to extract the English subtitle stream
        command_eng = [
            ffmpeg_exe,
            '-y',
            '-i', video_path,
            '-map', '0:s:m:language:eng', # Maps English subtitle streams
            '-c:s', 'srt',
            output_srt_path
        ]
        
        print(f"Extracting English subtitles to {output_srt_path}...")
        result = subprocess.run(command_eng, capture_output=True, text=True)
        
        # If it failed (maybe no English stream), fallback to the first subtitle stream
        if result.returncode != 0:
            print("English stream not found explicitly, falling back to first available subtitle stream...")
            command_fallback = [
                ffmpeg_exe,
                '-y',
                '-i', video_path,
                '-map', '0:s:0', # Fallback to the first subtitle stream
                '-c:s', 'srt',
                output_srt_path
            ]
            result = subprocess.run(command_fallback, capture_output=True, text=True)
        
        if result.returncode != 0:
            print("Error extracting subtitles. Ensure ffmpeg is installed and the video has subtitles.")
            print(result.stderr)
            return False
            
        print("Subtitles extracted successfully.")
        return True
    except Exception as e:
        print(f"An unexpected error occurred during extraction: {e}")
        return False

def translate_srt(input_srt_path, output_srt_path, target_lang='si'):
    """
    Translates an SRT file using deep-translator.
    """
    try:
        print(f"Translating {input_srt_path} to Sinhala...")
        subs = pysrt.open(input_srt_path, encoding='utf-8')
        translator = GoogleTranslator(source='auto', target=target_lang)
        
        total_subs = len(subs)
        for i, sub in enumerate(subs):
            # Show progress
            if i % 10 == 0:
                 print(f"Translating: {i}/{total_subs} ({int(i/total_subs*100)}%)")
                 
            # Translate text
            if sub.text.strip():
                try:
                    translated_text = translator.translate(sub.text)
                    sub.text = translated_text
                except Exception as trans_err:
                     print(f"Error translating subtitle {i}: {trans_err}")
                     # Keep original text if translation fails
        
        subs.save(output_srt_path, encoding='utf-8')
        print(f"Translation complete. Saved to {output_srt_path}")
        return True
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return False

def process_video(video_path):
    """
    Main pipeline: Extract -> Translate
    """
    base_name, _ = os.path.splitext(video_path)
    temp_english_srt = f"{base_name}_extracted_eng.srt"
    final_sinhala_srt = f"{base_name}_si.srt"
    
    if extract_subtitles(video_path, temp_english_srt):
        if translate_srt(temp_english_srt, final_sinhala_srt):
             print("\n--- Success ---")
             print(f"Translated subtitles are ready at: {final_sinhala_srt}")
             print("You can now open your video player and load this subtitle file.")
             
             # Clean up the temporary english extracted file
             try:
                 os.remove(temp_english_srt)
             except OSError:
                 pass
             return True
        else:
             print("Pipeline failed at translation stage.")
             return False
    else:
        print("Pipeline failed at extraction stage.")
        return False

if __name__ == "__main__":
    # Example usage for testing without UI
    import sys
    if len(sys.argv) > 1:
        process_video(sys.argv[1])
    else:
        print("Please provide a video file path as an argument.")
