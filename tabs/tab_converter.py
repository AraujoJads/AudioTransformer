import os
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pydub import AudioSegment

SUPPORTED_FORMATS = ('.mp3', '.wav', '.flac', '.ogg', '.aac')
BITRATES = ["64k", "128k", "192k", "256k", "320k"]
FORMATS = ["mp3", "wav", "flac", "ogg", "aac"]

class TabConverter:
    def __init__(self, master):
        self.master = master
        self.input_paths = []
        self.output_dir = ""
        self.cancel_requested = False

        self.setup_ui()

    def setup_ui(self):
        ctk.CTkLabel(self.master, text="Conversor de Áudio", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=10)

        frame = ctk.CTkFrame(self.master)
        frame.pack(pady=10)

        ctk.CTkButton(frame, text="Selecionar Arquivos ou Pasta", command=self.select_input).grid(row=0, column=0, padx=10)
        ctk.CTkButton(frame, text="Selecionar Pasta de Saída", command=self.select_output_dir).grid(row=0, column=1, padx=10)

        # Bitrate e formato
        options_frame = ctk.CTkFrame(self.master)
        options_frame.pack(pady=10)

        self.bitrate_option = ctk.CTkOptionMenu(options_frame, values=BITRATES)
        self.bitrate_option.set("192k")
        self.bitrate_option.grid(row=0, column=0, padx=10)

        self.format_option = ctk.CTkOptionMenu(options_frame, values=FORMATS)
        self.format_option.set("mp3")
        self.format_option.grid(row=0, column=1, padx=10)

        # Botões
        self.convert_button = ctk.CTkButton(self.master, text="Converter", command=self.start_conversion)
        self.convert_button.pack(pady=10)

        self.cancel_button = ctk.CTkButton(self.master, text="Cancelar", command=self.cancel_conversion, fg_color="red")
        self.cancel_button.pack()

        # Barra de progresso
        self.progress_bar = ctk.CTkProgressBar(self.master, width=500)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        # Área de status
        self.status_text = ctk.CTkTextbox(self.master, width=680, height=180, state="disabled")
        self.status_text.pack(pady=10)

    def select_input(self):
        paths = filedialog.askopenfilenames(filetypes=[("Áudio", "*.mp3 *.wav *.flac *.ogg *.aac")])
        if not paths:
            directory = filedialog.askdirectory(title="Ou escolha uma pasta")
            if directory:
                self.input_paths = self.find_audio_files(directory)
                self.log(f"[✔] Pasta selecionada: {directory}")
        else:
            self.input_paths = list(paths)
            self.log(f"[✔] {len(paths)} arquivos adicionados.")

    def select_output_dir(self):
        self.output_dir = filedialog.askdirectory(title="Selecionar pasta de saída")
        if self.output_dir:
            self.log(f"[✔] Pasta de saída: {self.output_dir}")

    def find_audio_files(self, root_dir):
        audio_files = []
        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.lower().endswith(SUPPORTED_FORMATS):
                    audio_files.append(os.path.join(root, file))
        return audio_files

    def start_conversion(self):
        if not self.input_paths or not self.output_dir:
            messagebox.showwarning("Aviso", "Escolha arquivos/pasta e pasta de saída.")
            return

        self.cancel_requested = False
        self.progress_bar.set(0)
        self.status_text.configure(state="normal")
        self.status_text.delete("1.0", "end")
        self.status_text.configure(state="disabled")

        threading.Thread(target=self.convert_files, daemon=True).start()

    def convert_files(self):
        bitrate = self.bitrate_option.get()
        out_format = self.format_option.get()

        files = self.input_paths
        total = len(files)

        for i, file_path in enumerate(files, start=1):
            if self.cancel_requested:
                self.log("[⛔] Conversão cancelada.")
                break

            try:
                audio = AudioSegment.from_file(file_path)
                base = os.path.splitext(os.path.basename(file_path))[0]
                out_path = os.path.join(self.output_dir, f"{base}_converted.{out_format}")

                if os.path.exists(out_path):
                    self.log(f"[⚠] Ignorado (duplicado): {base}")
                    continue

                audio.export(out_path, format=out_format, bitrate=bitrate)
                self.log(f"[✔] {base} convertido → {out_format} @ {bitrate}")
            except Exception as e:
                self.log(f"[✖] Erro ao converter {file_path}: {e}")

            self.progress_bar.set(i / total)

    def cancel_conversion(self):
        self.cancel_requested = True
        self.log("[⛔] Cancelamento solicitado...")

    def log(self, text):
        self.status_text.configure(state="normal")
        self.status_text.insert("end", text + "\n")
        self.status_text.configure(state="disabled")
        self.status_text.see("end")
