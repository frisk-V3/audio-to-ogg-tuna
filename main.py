import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path
from pydub import AudioSegment
import threading

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Universal OGG Tuna GUI")
        self.geometry("500x350")
        ctk.set_appearance_mode("dark")

        # UI要素
        self.label = ctk.CTkLabel(self, text="音声ファイルをOGGに一括変換", font=("Hiragino Sans", 20, "bold"))
        self.label.pack(pady=20)

        self.file_list_label = ctk.CTkLabel(self, text="ファイルを選択してください", text_color="gray")
        self.file_list_label.pack(pady=5)

        self.select_btn = ctk.CTkButton(self, text="ファイルを選択", command=self.select_files)
        self.select_btn.pack(pady=10)

        self.convert_btn = ctk.CTkButton(self, text="変換開始", command=self.start_conversion, state="disabled", fg_color="green")
        self.convert_btn.pack(pady=10)

        self.progress = ctk.CTkProgressBar(self)
        self.progress.set(0)
        self.progress.pack(pady=20, padx=20, fill="x")

        self.files = []

    def select_files(self):
        self.files = filedialog.askopenfilenames(
            filetypes=[("Audio Files", "*.mp3 *.webm *.m4a *.wav *.flac")]
        )
        if self.files:
            self.file_list_label.configure(text=f"{len(self.files)} 個のファイルを選択中", text_color="white")
            self.convert_btn.configure(state="normal")

    def start_conversion(self):
        self.convert_btn.configure(state="disabled")
        self.select_btn.configure(state="disabled")
        # メインスレッドを止めないよう別スレッドで実行
        threading.Thread(target=self.convert_process).start()

    def convert_process(self):
        total = len(self.files)
        for i, file_path in enumerate(self.files):
            try:
                p = Path(file_path)
                audio = AudioSegment.from_file(str(p))
                out_dir = p.parent / "converted_ogg"
                out_dir.mkdir(exist_ok=True)
                audio.export(str(out_dir / f"{p.stem}.ogg"), format="ogg", codec="libvorbis")
            except Exception as e:
                print(f"Error: {e}")
            
            self.progress.set((i + 1) / total)
        
        self.label.configure(text="変換完了！", text_color="cyan")
        self.convert_btn.configure(state="normal")
        self.select_btn.configure(state="normal")

if __name__ == "__main__":
    app = App()
    app.mainloop()
