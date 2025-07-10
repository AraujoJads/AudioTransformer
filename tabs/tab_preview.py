# tabs/tab_preview.py
import os
import threading
import simpleaudio as sa
import customtkinter as ctk
from tkinter import filedialog, messagebox

class TabPreview:
    def __init__(self, master):
        self.master = master
        self.current_wave = None
        self.play_thread = None
        self.playing = False

        self.setup_ui()

    def setup_ui(self):
        ctk.CTkLabel(self.master, text="Preview de Áudio", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=10)

        self.select_button = ctk.CTkButton(self.master, text="Selecionar Arquivo de Áudio", command=self.select_file)
        self.select_button.pack(pady=10)

        self.play_button = ctk.CTkButton(self.master, text="▶️ Play", command=self.toggle_playback, state="disabled")
        self.play_button.pack(pady=5)

        self.status_label = ctk.CTkLabel(self.master, text="Nenhum arquivo carregado.")
        self.status_label.pack(pady=10)

    def select_file(self):
        filetypes = [("Áudio", "*.wav")]
        path = filedialog.askopenfilename(filetypes=filetypes)
        if path:
            if not path.lower().endswith(".wav"):
                messagebox.showwarning("Formato não suportado", "Por enquanto, apenas arquivos .wav podem ser reproduzidos.")
                return
            self.audio_path = path
            self.status_label.configure(text=f"Carregado: {os.path.basename(path)}")
            self.play_button.configure(state="normal")

    def toggle_playback(self):
        if self.playing:
            self.stop_audio()
        else:
            self.play_audio()

    def play_audio(self):
        if not hasattr(self, "audio_path") or not self.audio_path:
            return

        self.playing = True
        self.play_button.configure(text="⏹ Stop")
        self.play_thread = threading.Thread(target=self._play_wav, daemon=True)
        self.play_thread.start()

    def stop_audio(self):
        self.playing = False
        if self.current_wave:
            self.current_wave.stop()
        self.play_button.configure(text="▶️ Play")

    def _play_wav(self):
        try:
            wave_obj = sa.WaveObject.from_wave_file(self.audio_path)
            self.current_wave = wave_obj.play()
            self.current_wave.wait_done()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao tocar o áudio: {e}")
        finally:
            self.playing = False
            self.play_button.configure(text="▶️ Play")