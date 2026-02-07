import subprocess
import json

def extract_metadata(video_path: str) -> dict:
    """
    Extract metadata using ffprobe.
    This MUST always run first.
    """
    cmd = [
        "ffprobe",
        "-v", "error",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        video_path
    ]

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError("ffprobe failed")

    data = json.loads(result.stdout)

    video_stream = next(
        (s for s in data["streams"] if s["codec_type"] == "video"),
        None
    )

    if not video_stream:
        raise RuntimeError("No video stream found")

    return {
        "duration": float(data["format"]["duration"]),
        "width": int(video_stream["width"]),
        "height": int(video_stream["height"]),
        "codec": video_stream["codec_name"]
    }
