import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path
from pydub import AudioSegment
import threading
import os

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Universal OGG Tuna GUI")
        self.geometry("500(x)400") # 少し高さを調整しました
        ctk.set_appearance_mode("dark")

        # UI要素
        self.label = ctk.CTkLabel(self, text="音声ファイルをOGGに一括変換", font=("Hiragino Sans", 20, "bold"))
        self.label.pack(pady=20)

        self.file_list_label = ctk.CTkLabel(self, text="ファイルを選択してください", text_color="gray", wraplength=400)
        self.file_list_label.pack(pady=5)

        self.select_btn = ctk.CTkButton(self, text="ファイルを選択", command=self.select_files)
        self.select_btn.pack(pady=10)

        self.convert_btn = ctk.CTkButton(self, text="変換開始", command=self.start_conversion, state="disabled", fg_color="green")
        self.convert_btn.pack(pady=10)

        self.progress = ctk.CTkProgressBar(self)
        self.progress.set(0)
        self.progress.pack(pady=20, padx=20, fill="x")

        self.status_label = ctk.CTkLabel(self, text="", font=("Hiragino Sans", 12))
        self.status_label.pack(pady=5)

        self.files = []

    def select_files(self):
        self.files = filedialog.askopenfilenames(
            filetypes=[("Audio Files", "*.mp3 *.webm *.m4a *.wav *.flac")]
        )
        if self.files:
            self.file_list_label.configure(text=f"{len(self.files)} 個のファイルを選択中", text_color="white")
            self.label.configure(text="音声ファイルをOGGに一括変換", text_color="white")
            self.convert_btn.configure(state="normal")
            self.progress.set(0)

    def start_conversion(self):
        self.convert_btn.configure(state="disabled")
        self.select_btn.configure(state="disabled")
        # メインスレッドを止めないよう別スレッドで実行
        threading.Thread(target=self.convert_process, daemon=True).start()

    def convert_process(self):
        total = len(self.files)
        # ユーザーのダウンロードフォルダ内の 'converted_ogg' を指定
        out_dir = Path.home() / "Downloads" / "converted_ogg"
        
        try:
            out_dir.mkdir(exist_ok=True, parents=True)
        except Exception as e:
            self.label.configure(text="フォルダ作成エラー", text_color="red")
            print(f"Error: {e}")
            return

        for i, file_path in enumerate(self.files):
            try:
                p = Path(file_path)
                # 画面上の進捗テキストを更新
                self.status_label.configure(text=f"処理中 ({i+1}/{total}): {p.name}")
                
                audio = AudioSegment.from_file(str(p))
                output_path = out_dir / f"{p.stem}.ogg"
                audio.export(str(output_path), format="ogg", codec="libvorbis")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
            
            self.progress.set((i + 1) / total)
        
        # 完了後の処理
        self.label.configure(text="変換完了！", text_color="cyan")
        self.status_label.configure(text=f"保存先: {out_dir}")
        self.convert_btn.configure(state="normal")
        self.select_btn.configure(state="normal")
        
        # 完了時に保存フォルダを自動で開く（便利機能）
        try:
            os.startfile(out_dir) if os.name == 'nt' else os.system(f'open "{out_dir}"')
        except:
            pass

if __name__ == "__main__":
    app = App()
    app.mainloop()
