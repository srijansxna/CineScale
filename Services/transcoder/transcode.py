import subprocess
from pathlib import Path

RENDITIONS = {
    "360p": "640x360",
    "720p": "1280x720",
}


def transcode(video_path: str, output_dir: str) -> dict:
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    outputs = {}

    for label, scale in RENDITIONS.items():
        output_file = Path(output_dir) / f"{label}.mp4"

        cmd = [
            "ffmpeg",
            "-y",
            "-i", video_path,
            "-vf", f"scale={scale}",
            "-c:a", "copy",
            str(output_file),
        ]

        subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )

        outputs[label] = str(output_file)

    return outputs
