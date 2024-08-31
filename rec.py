import pyaudio
import wave
import tkinter as tk
from tkinter import filedialog

class AudioRecorder:
    def __init__(self, master):
        self.master = master
        self.master.title("Audio Recorder")

        self.recording = False
        self.frames = []

        # Set window size
        self.master.geometry("600x200")

        # Load images
        self.icon_image = tk.PhotoImage(file="icon.png")
        self.button_image = tk.PhotoImage(file="image.png")

        # Create a frame for buttons and labels
        self.frame = tk.Frame(master)
        self.frame.pack(expand=True, pady=20)

        # Create and place buttons with images
        self.start_button = tk.Button(self.frame, image=self.button_image, command=self.start_recording)
        self.start_button.grid(row=0, column=0, padx=20)
        self.start_label = tk.Label(self.frame, text="Start Recording", bg="#FEBAAD")
        self.start_label.grid(row=1, column=0)

        self.stop_button = tk.Button(self.frame, image=self.button_image, command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=20)
        self.stop_label = tk.Label(self.frame, text="Stop Recording", bg="#FEBAAD")
        self.stop_label.grid(row=1, column=1)

        self.save_button = tk.Button(self.frame, image=self.button_image, command=self.save_recording, state=tk.DISABLED)
        self.save_button.grid(row=0, column=2, padx=20)
        self.save_label = tk.Label(self.frame, text="Save Recording", bg="#FEBAAD")
        self.save_label.grid(row=1, column=2)

        # Set the window icon
        self.icon = tk.PhotoImage(file="icon.png")
        master.iconphoto(True, self.icon)

        # Label with custom font for the title
        self.label = tk.Label(master, text="Voice Recorder", font=("Arial", 16), bg="#FEBAAD", fg="#3B3024")
        self.label.pack(pady=10)

        self.chunk = 1024
        self.sample_rate = 44100
        self.p = pyaudio.PyAudio()

    def start_recording(self):
        self.recording = True
        self.frames = []
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.DISABLED)

        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.sample_rate,
                                  input=True,
                                  frames_per_buffer=self.chunk)

        self.record()

    def record(self):
        if self.recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)
            self.master.after(10, self.record)

    def stop_recording(self):
        self.recording = False
        self.stream.stop_stream()
        self.stream.close()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.NORMAL)

    def save_recording(self):
        filename = filedialog.asksaveasfilename(defaultextension=".wav",
                                               filetypes=[("WAV files", "*.wav"), ("All files", "*.*")])
        if filename:
            wf = wave.open(filename, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.frames))
            wf.close()

if __name__ == "__main__":
    root = tk.Tk()

    # Create and configure the application
    app = AudioRecorder(root)
    
    root.mainloop()
