from .metadata import extract_metadata
from .thumbnails import generate_thumbnails
from .transcode import transcode_video


def run_pipeline(video_path: str, output_dir: str, include_transcoding: bool = False) -> dict:
    """
    Deterministic processing pipeline.
    Order is strict:
    1. Metadata
    2. Thumbnails
    3. Transcoding (optional)
    """

    metadata = extract_metadata(video_path)
    thumbnails = generate_thumbnails(video_path, output_dir)
    
    result = {
        "metadata": metadata,
        "thumbnails": thumbnails
    }
    
    if include_transcoding:
        transcoded_files = transcode_video(video_path, output_dir)
        result["transcoded_files"] = transcoded_files

    return result
