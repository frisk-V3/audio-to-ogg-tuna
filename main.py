import os
import sys
from pydub import AudioSegment
from datetime import datetime

def convert_to_ogg(file_path):
    """各種音声フォーマットをOGG(Vorbis)に変換する"""
    supported_extensions = ('.mp3', '.webm', '.m4a', '.wav', '.flac')
    
    if not file_path.lower().endswith(supported_extensions):
        return f"[SKIP] 対応外の形式です: {os.path.basename(file_path)}"

    try:
        # ファイルの読み込み
        ext = os.path.splitext(file_path)[1].replace('.', '')
        audio = AudioSegment.from_file(file_path, format=ext)

        # 出力ファイルパスの作成 (元の場所/output/ファイル名.ogg)
        output_dir = os.path.join(os.path.dirname(file_path), "converted_ogg")
        os.makedirs(output_dir, exist_ok=True)
        
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}.ogg")

        # OGGとして書き出し（ビットレートは標準的な192k）
        audio.export(output_path, format="ogg", codec="libvorbis", bitrate="192k")

        return f"[SUCCESS] 変換完了: {output_path}"

    except Exception as e:
        return f"[ERROR] 失敗 ({os.path.basename(file_path)}): {str(e)}"

if __name__ == "__main__":
    print("="*50)
    print(" Audio to OGG Converter (pydub edition)")
    print("="*50)

    targets = sys.argv[1:]

    if not targets:
        print("\n[!] 使い方: 音声ファイルをこのEXEにドラッグ＆ドロップしてください。")
    else:
        print(f"\n{len(targets)} 個のファイルを処理中...\n")
        for t in targets:
            result = convert_to_ogg(t)
            print(result)

    print("\n" + "="*50)
    print(f"完了時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("何かキーを押すと終了します...")
    input()
