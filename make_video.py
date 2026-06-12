import os
import subprocess
import asyncio
import edge_tts
import imageio_ffmpeg

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

# Images directory and files
img_dir = r"C:\Users\Swati\.gemini\antigravity\brain\74e887bb-ce6f-4552-bf61-2a0cf4fec934"
images = [
    "media__1781300891535.png",
    "media__1781300891543.png",
    "media__1781300891560.png",
    "media__1781300891575.png",
    "media__1781300891576.png"
]

scripts = [
    "Welcome to Auto UI, the ultimate autonomous frontend designer for the Microsoft Agents League Hackathon. By combining Microsoft Azure OpenAI and Google Gemini, we turn your ideas into reality.",
    "Simply describe what you want in plain English. Here, we are asking for an e-commerce product grid with filters. Auto UI instantly starts writing production-ready code.",
    "The AI can handle incredibly creative requests too. Take a look at this four-panel comic strip about a robot learning to code, complete with beautiful styling.",
    "And here is the fully functional e-commerce product grid we requested earlier. It features glassmorphism, responsive design, and Microsoft Foundry IQ styling.",
    "From functional dashboards to stunning portfolios, Auto UI empowers anyone to become a frontend designer in seconds. Thank you for watching!"
]

async def make_audio():
    print("Generating AI Voiceover...")
    for i, text in enumerate(scripts):
        communicate = edge_tts.Communicate(text, "en-US-JennyNeural")
        await communicate.save(f"audio_{i}.mp3")
        print(f"Generated audio_{i}.mp3")

asyncio.run(make_audio())

print("Rendering video clips with FFmpeg...")
for i in range(5):
    img_path = os.path.join(img_dir, images[i])
    cmd = [
        ffmpeg_exe, "-y",
        "-loop", "1", "-framerate", "25",
        "-i", img_path,
        "-i", f"audio_{i}.mp3",
        "-c:v", "libx264", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
        f"clip_{i}.mp4"
    ]
    subprocess.run(cmd, check=True)
    print(f"Rendered clip_{i}.mp4")

print("Concatenating clips into final video...")
with open("concat.txt", "w") as f:
    for i in range(5):
        f.write(f"file 'clip_{i}.mp4'\n")

subprocess.run([ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", "concat.txt", "-c", "copy", "AutoUI_Demo.mp4"], check=True)

print("Cleaning up temporary files...")
for i in range(5):
    if os.path.exists(f"audio_{i}.mp3"): os.remove(f"audio_{i}.mp3")
    if os.path.exists(f"clip_{i}.mp4"): os.remove(f"clip_{i}.mp4")
if os.path.exists("concat.txt"): os.remove("concat.txt")

print("Done! Video created as AutoUI_Demo.mp4")
