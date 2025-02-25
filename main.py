from pydub import AudioSegment
import os
import whisper
from pathlib import Path
import json


output_folder = ""
def split_audio(input_file_audio, output_folder, chunk_length_ms=30000 ):
    """ Chia nhỏ file audio thành các đoạn 30 giây """
    input_file_audio = Path(input_file_audio)
    output_folder = Path(output_folder)
    audio = AudioSegment.from_file(input_file_audio)
    total_length = len(audio)
    audio = audio.set_frame_rate(16000)

    os.makedirs(output_folder, exist_ok=True)
    file_name = input_file_audio.stem
    output_subfolder = output_folder / file_name
    output_subfolder.mkdir(parents=True, exist_ok=True)
    for i, start in enumerate(range(0, total_length, chunk_length_ms)):
        chunk = audio[start: start + chunk_length_ms]    
        chunk_path = output_subfolder/f"chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")

    print(f"Đã chia nhỏ audio thành {i+1} đoạn.")

def transcript(input_folder, output_file):
    input_folder = Path(input_folder) 
    model = whisper.load_model("small", device="cpu")
    file_paths = sorted(input_folder.glob("*.wav"), key=lambda x: int(x.stem.split('_')[-1]))

        

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("[\n")  # Mở đầu danh sách JSON
        
        
        first_entry = True
        for file_path in file_paths:  # Duyệt file .wav trong thư mục
            print(f"Đang xử lý: {file_path}")
            result = model.transcribe(str(file_path))  # Chuyển đổi file âm thanh

            entry = {
                "audio": str(file_path),
                "text": result["text"]
            }

            if not first_entry:
                f.write(",\n")
            json.dump(entry, f, ensure_ascii=False, indent=4)
            first_entry = False

        f.write("\n]")  # Đóng danh sách JSON
def split_audio_final(folder_path):
    folder_path = Path(folder_path)
    file_list = list(folder_path.glob("*.mp3"))
    for file_path in file_list:
        split_audio(file_path, r"D:\data_training\data_output")

split_audio_final(r"D:\data_training\data_input")
# output(r"D:\data_training\data_output\toeic19", r"D:\data_training\output_final.txt" )