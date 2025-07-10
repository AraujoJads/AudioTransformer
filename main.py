import customtkinter as ctk
from tabs.tab_converter import TabConverter
from tabs.tab_compressor import TabCompressor
from tabs.tab_preview import TabPreview

class AudioConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🎵 Conversor de Áudio Premium")
        self.geometry("720x600")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark")  # Improved theme to dark mode for modern look
        ctk.set_default_color_theme("blue")

        self.create_tabs()
        self.bind_shortcuts()

    def create_tabs(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(expand=True, fill="both", padx=20, pady=20)

        # Cria e adiciona abas como classes separadas
        self.converter_tab = TabConverter(self.tabview.add("Conversor"))
        self.compressor_tab = TabCompressor(self.tabview.add("Compressor"))
        self.preview_tab = TabPreview(self.tabview.add("Preview"))

    def bind_shortcuts(self):
        # Keyboard shortcuts to switch tabs: Ctrl+1, Ctrl+2, Ctrl+3
        self.bind("<Control-1>", lambda e: self.tabview.set("Conversor"))
        self.bind("<Control-2>", lambda e: self.tabview.set("Compressor"))
        self.bind("<Control-3>", lambda e: self.tabview.set("Preview"))


if __name__ == "__main__":
    app = AudioConverterApp()
    app.mainloop()
