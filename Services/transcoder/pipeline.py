from transcoder.metadata import extract_metadata
from transcoder.thumbnails import generate_thumbnails


def run_pipeline(video_path: str, output_dir: str) -> dict:
    """
    Deterministic processing pipeline.
    Order is strict:
    1. Metadata
    2. Thumbnails
    """

    metadata = extract_metadata(video_path)
    thumbnails = generate_thumbnails(video_path, output_dir)

    return {
        "metadata": metadata,
        "thumbnails": thumbnails
    }
