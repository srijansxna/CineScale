import subprocess
from pathlib import Path

THUMBNAIL_TIMESTAMPS = [1, 5, 10]  # seconds (fixed, deterministic)

def generate_thumbnails(video_path: str, output_dir: str) -> list[str]:
    """
    Generate thumbnails at fixed timestamps.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    generated = []

    for t in THUMBNAIL_TIMESTAMPS:
        output_path = Path(output_dir) / f"thumb_{t}.jpg"

        cmd = [
            "ffmpeg",
            "-y",
            "-ss", str(t),
            "-i", video_path,
            "-frames:v", "1",
            "-q:v", "2",
            str(output_path)
        ]

        subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )

        generated.append(str(output_path))

    return generated
