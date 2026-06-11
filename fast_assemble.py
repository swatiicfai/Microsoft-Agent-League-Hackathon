import os
import subprocess
from moviepy import AudioFileClip
import imageio_ffmpeg

OUTPUT_DIR = "demo_assets"
VIDEO_FILE = "AutoUI_Demo.mp4"

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

# Create individual videos with audio for each scene
scenes = []
for i in range(7):
    audio_path = os.path.join(OUTPUT_DIR, f"audio_{i:02d}.mp3")
    img_path = os.path.join(OUTPUT_DIR, f"screen_{i:02d}.png")
    out_path = os.path.join(OUTPUT_DIR, f"scene_{i:02d}.mp4")
    
    # Get audio duration
    audio = AudioFileClip(audio_path)
    dur = audio.duration + 1.0 # 1s padding
    audio.close()
    
    # FFmpeg command to combine image and audio
    cmd = [
        ffmpeg_exe, "-y",
        "-loop", "1", "-framerate", "24",
        "-i", img_path,
        "-i", audio_path,
        "-c:v", "libx264", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-t", str(dur),
        out_path
    ]
    print(f"Generating scene {i}...")
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    scenes.append(out_path)

# Create concat list
list_file = os.path.join(OUTPUT_DIR, "list.txt")
with open(list_file, "w") as f:
    for scene in scenes:
        f.write(f"file '{os.path.basename(scene)}'\n")

# Concatenate all scenes
concat_cmd = [
    ffmpeg_exe, "-y",
    "-f", "concat", "-safe", "0",
    "-i", list_file,
    "-c", "copy",
    VIDEO_FILE
]
print("Assembling final video...")
subprocess.run(concat_cmd)
print("Done!")
