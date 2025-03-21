import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import sys

def get_ffmpeg_path():
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(sys.argv[0])))
    return os.path.join(base_path, "ffmpeg.exe")

def check_video_exists(path):
    if os.path.exists(path):
        return True
    return False
    
def check_foto_path():
    foto_folder = 'foto_result'
    if os.path.isdir(foto_folder):
        print('succes')
    else:
        os.makedirs(foto_folder)
    return foto_folder
    
def run_ffmpeg(input_path):
    
    foto_folder = check_foto_path()
    
    filename = os.path.basename(input_path)
    name, _ = os.path.splitext(filename)
    output_filename = f"{name}_removed.mp4"
    output_path = os.path.join(foto_folder, output_filename)
    exists = check_video_exists(output_path)
    if not exists:
        status_label.config(text=f'status: Хорошо, проверьте \n {output_path}')
        ffmpeg_path = get_ffmpeg_path()
        

        cmd = [
            ffmpeg_path,
            '-i', input_path,
            '-map_metadata', '-1',
            '-map_chapters', '-1',
            '-metadata', 'encoder=',
            '-metadata:s:v', 'handler_name=',
            '-metadata:s:a', 'handler_name=',
            '-metadata:s:v', 'language=',
            '-metadata:s:a', 'language=',
            '-metadata:s:v', 'vendor_id=',
            '-metadata:s:a', 'vendor_id=',
            '-metadata:s:v', 'encoder=',
            '-metadata:s:a', 'encoder=',
            '-fflags', '+bitexact',
            '-flags:v', '+bitexact',
            '-flags:a', '+bitexact',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            '-c:a', 'copy',
            output_path
        ]

        try:
            subprocess.run(cmd, check=True)
            messagebox.showinfo("Успех", f"Готово! Сохранено как:\n{output_path}")
        except subprocess.CalledProcessError:
            messagebox.showerror("Ошибка", "Ошибка при обработке видео.")
    else:
        status_label.config(text='status: Видео уже существует')
        
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    if file_path:
        run_ffmpeg(file_path)

# GUI
root = tk.Tk()
root.title("Видео metadata")
btn = tk.Button(root, text="Выбрать видео", command=select_file, font=("Arial", 14), padx=20, pady=10)
btn.pack(pady=30)

status_label = tk.Label(root, text="status:", font=("Arial", 12))
status_label.pack()
root.geometry("400x200")
root.mainloop()
