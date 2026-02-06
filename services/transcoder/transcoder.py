import subprocess
import os

def transcode():
    input_video = "input.mp4"

    os.makedirs("output/360p", exist_ok=True)
    os.makedirs("output/720p", exist_ok=True)

    cmd_360p = [
        "ffmpeg",
        "-i", input_video,
        "-vf", "scale=640:360",
        "output/360p/video_360p.mp4"
    ]

    cmd_720p = [
        "ffmpeg",
        "-i", input_video,
        "-vf", "scale=1280:720",
        "output/720p/video_720p.mp4"
    ]

    subprocess.run(cmd_360p)
    subprocess.run(cmd_720p)

if __name__ == "__main__":
    transcode()
