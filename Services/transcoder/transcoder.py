import os
import subprocess
import json


def transcode_video(input_video):
    """
    Generate 360p and 720p versions of the input video.
    """

    # Create output directories
    os.makedirs("output/360p", exist_ok=True)
    os.makedirs("output/720p", exist_ok=True)

    output_360p = "output/360p/video_360p.mp4"
    output_720p = "output/720p/video_720p.mp4"

    cmd_360p = [
        "ffmpeg",
        "-i", input_video,
        "-vf", "scale=640:360",
        output_360p
    ]

    cmd_720p = [
        "ffmpeg",
        "-i", input_video,
        "-vf", "scale=1280:720",
        output_720p
    ]

    subprocess.run(cmd_360p)
    subprocess.run(cmd_720p)

    return [
        {"resolution": "360p", "path": output_360p},
        {"resolution": "720p", "path": output_720p},
    ]


def generate_thumbnail(input_video):
    """
    Generate a thumbnail at 5 seconds into the video.
    """

    os.makedirs("storage/thumbnails", exist_ok=True)

    thumbnail_path = "storage/thumbnails/thumb.jpg"

    cmd = [
        "ffmpeg",
        "-i", input_video,
        "-ss", "00:00:05",
        "-vframes", "1",
        thumbnail_path
    ]

    subprocess.run(cmd)

    return [thumbnail_path]


def extract_metadata(input_video):
    """
    Extract metadata using ffprobe and return parsed JSON.
    """

    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        input_video
    ]

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    metadata = json.loads(result.stdout)

    return metadata


def process_video(job_id, input_path, output_dir):
    """
    Final worker entry point (Day 5 contract-ready).
    """

    print(f"Processing job: {job_id}")

    qualities = transcode_video(input_path)
    thumbnails = generate_thumbnail(input_path)
    metadata = extract_metadata(input_path)

    return {
        "job_id": job_id,
        "qualities": qualities,
        "thumbnails": thumbnails,
        "metadata": metadata
    }


if __name__ == "__main__":
    # Temporary manual test
    result = process_video(
        job_id="test-job-001",
        input_path="input/input.mp4",
        output_dir="output"
    )

    print(json.dumps(result, indent=2))
