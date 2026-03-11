import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import sys
import os

from subtitle_processor import process_video

class SubtitleTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sinhala Video Subtitle Translator")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        self.video_path = tk.StringVar()
        self.video_files = []
        
        self.create_widgets()

    def create_widgets(self):
        # Main Frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="Extract & Translate Subtitles to Sinhala", font=("Helvetica", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # File Selection Area
        file_frame = tk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=10)
        
        path_entry = tk.Entry(file_frame, textvariable=self.video_path, width=50, state='readonly')
        path_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        browse_btn = tk.Button(file_frame, text="Browse Video", command=self.browse_file)
        browse_btn.pack(side=tk.LEFT)
        
        # Translate Button
        self.translate_btn = tk.Button(main_frame, text="Start Translation", command=self.start_translation_thread, 
                                     bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), pady=10)
        self.translate_btn.pack(fill=tk.X, pady=20)
        
        # Log Output Area
        log_label = tk.Label(main_frame, text="Process Logs:")
        log_label.pack(anchor=tk.W)
        
        self.log_text = tk.Text(main_frame, height=10, width=70, state=tk.DISABLED, bg="#f0f0f0")
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Redirect stdout to the text widget
        sys.stdout = PrintLogger(self.log_text)

    def browse_file(self):
        filenames = filedialog.askopenfilenames(
            title="Select Video Files",
            filetypes=(
                ("Video Files", "*.mp4 *.mkv *.avi *.mov"),
                ("All Files", "*.*")
            )
        )
        if filenames:
            self.video_files = list(filenames)
            self.video_path.set("; ".join(self.video_files))

    def start_translation_thread(self):
        video_str = self.video_path.get()
        if not video_str:
            messagebox.showwarning("No File", "Please select video files first.")
            return

        # Use the stored list or parse from the entry if typed manually
        if not hasattr(self, 'video_files') or not self.video_files or "; ".join(self.video_files) != video_str:
            self.video_files = [f.strip() for f in video_str.split(';') if f.strip()]
            
        for vf in self.video_files:
            if not os.path.exists(vf):
                messagebox.showerror("Error", f"Selected file does not exist:\n{vf}")
                return

        # Disable button during processing
        self.translate_btn.config(state=tk.DISABLED, text="Processing...")
        
        # Clear previous logs
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        print(f"Starting pipeline for {len(self.video_files)} file(s)...\n")
        
        # Run in separate thread to prevent UI freezing
        thread = threading.Thread(target=self.run_process, args=(self.video_files,))
        thread.daemon = True
        thread.start()

    def run_process(self, video_files):
        success_count = 0
        try:
            for i, video_file in enumerate(video_files):
                print(f"--- Processing file {i+1} of {len(video_files)} ---")
                print(f"File: {os.path.basename(video_file)}")
                success = process_video(video_file)
                if success:
                    success_count += 1
                print("-" * 40 + "\n")
                
            if success_count == len(video_files):
                 print("\nDone! All files processed successfully. You can close this window now.")
                 messagebox.showinfo("Success", "All subtitles translated successfully!")
            elif success_count > 0:
                 print(f"\nDone! {success_count}/{len(video_files)} files processed successfully.")
                 messagebox.showwarning("Partial Success", f"Translated {success_count} out of {len(video_files)} files. Check logs for details.")
            else:
                 messagebox.showerror("Failed", "Translation process failed for all files. Check the logs.")
        except Exception as e:
            print(f"\nCRITICAL ERROR: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")
        finally:
            # Re-enable button
            self.root.after(0, lambda: self.translate_btn.config(state=tk.NORMAL, text="Start Translation"))

class PrintLogger:
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, text):
        self.textbox.config(state=tk.NORMAL)
        self.textbox.insert(tk.END, text)
        self.textbox.see(tk.END)
        self.textbox.config(state=tk.DISABLED)

    def flush(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = SubtitleTranslatorApp(root)
    root.mainloop()
