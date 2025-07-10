import os
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pydub import AudioSegment

class TabCompressor:
    def __init__(self, master):
        self.master = master
        self.input_files = []
        self.output_dir = ""
        self.cancel_requested = False
        self.is_compressing = False

        self.compression_map = {
            "Leve (192k)": "192k",
            "Média (128k)": "128k",
            "Forte (96k)": "96k"
        }

        self.setup_ui()

    def setup_ui(self):
        ctk.CTkLabel(self.master, text="Compressor Inteligente", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=10)

        buttons_frame = ctk.CTkFrame(self.master)
        buttons_frame.pack(pady=10)

        self.select_input_button = ctk.CTkButton(buttons_frame, text="Selecionar Arquivos", command=self.select_input_files)
        self.select_input_button.grid(row=0, column=0, padx=10)
        self.select_input_button.tooltip = "Selecione arquivos de áudio para compressão."

        self.select_output_button = ctk.CTkButton(buttons_frame, text="Selecionar Pasta de Saída", command=self.select_output_dir)
        self.select_output_button.grid(row=0, column=1, padx=10)
        self.select_output_button.tooltip = "Selecione a pasta onde os arquivos comprimidos serão salvos."

        ctk.CTkLabel(self.master, text="Nível de compressão:").pack(pady=(10, 0))

        self.compression_level = ctk.CTkOptionMenu(self.master, values=list(self.compression_map.keys()))
        self.compression_level.set("Média (128k)")
        self.compression_level.pack(pady=5)
        self.compression_level.tooltip = "Selecione o nível de compressão."

        self.compress_button = ctk.CTkButton(self.master, text="Comprimir", command=self.start_compression)
        self.compress_button.pack(pady=10)

        self.cancel_button = ctk.CTkButton(self.master, text="Cancelar", command=self.cancel_compression, fg_color="red")
        self.cancel_button.pack()

        self.progress_bar = ctk.CTkProgressBar(self.master, width=500)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        self.status_text = ctk.CTkTextbox(self.master, width=680, height=180, state="disabled", fg_color="#1e1e1e", text_color="#dcdcdc", font=ctk.CTkFont(size=12))
        self.status_text.pack(pady=10)

        # Keyboard shortcuts
        self.master.bind("<Control-c>", lambda e: self.start_compression())
        self.master.bind("<Control-x>", lambda e: self.cancel_compression())

    def select_input_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Áudio", "*.mp3 *.wav *.flac *.ogg *.aac")])
        if files:
            self.input_files = list(files)
            self.log(f"[✔] {len(files)} arquivos selecionados para compressão.")
        else:
            self.log("[⚠] Nenhum arquivo selecionado.")

    def select_output_dir(self):
        self.output_dir = filedialog.askdirectory(title="Selecionar pasta de saída")
        if self.output_dir:
            self.log(f"[✔] Pasta de saída: {self.output_dir}")
        else:
            self.log("[⚠] Nenhuma pasta selecionada.")

    def start_compression(self):
        if self.is_compressing:
            return
        if not self.input_files or not self.output_dir:
            messagebox.showwarning("Aviso", "Escolha arquivos e a pasta de saída.")
            return

        self.is_compressing = True
        self.update_ui_state()
        self.cancel_requested = False
        self.progress_bar.set(0)
        self.status_text.configure(state="normal")
        self.status_text.delete("1.0", "end")
        self.status_text.configure(state="disabled")

        threading.Thread(target=self.compress_files, daemon=True).start()

    def compress_files(self):
        bitrate = self.compression_map[self.compression_level.get()]
        total = len(self.input_files)

        for i, file_path in enumerate(self.input_files, start=1):
            if self.cancel_requested:
                self.log("[⛔] Compressão cancelada.")
                break

            try:
                audio = AudioSegment.from_file(file_path)
                base = os.path.splitext(os.path.basename(file_path))[0]
                ext = os.path.splitext(file_path)[1][1:].lower()
                out_path = os.path.join(self.output_dir, f"{base}_compressed.{ext}")

                audio.export(out_path, format=ext, bitrate=bitrate)
                self.log(f"[✔] {base} comprimido → {bitrate}")
            except Exception as e:
                self.log(f"[✖] Erro ao comprimir {file_path}: {e}")

            self.progress_bar.set(i / total)

        self.is_compressing = False
        self.update_ui_state()

    def cancel_compression(self):
        if not self.is_compressing:
            return
        self.cancel_requested = True
        self.log("[⛔] Cancelamento solicitado...")

    def update_ui_state(self):
        state = "disabled" if self.is_compressing else "normal"
        self.compress_button.configure(state=state)
        self.cancel_button.configure(state="normal" if self.is_compressing else "disabled")
        self.select_input_button.configure(state=state)
        self.select_output_button.configure(state=state)
        self.compression_level.configure(state=state)

    def log(self, text):
        self.status_text.configure(state="normal")
        self.status_text.insert("end", text + "\n")
        self.status_text.configure(state="disabled")
        self.status_text.see("end")
