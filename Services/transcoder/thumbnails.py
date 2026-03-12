import subprocess
import logging
import os
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)

THUMBNAIL_TIMESTAMPS = [1, 5, 10]  # seconds (fixed, deterministic)
THUMBNAIL_PERCENTAGES = [10, 50, 90]  # percentage positions


def generate_thumbnails(video_path: str, output_dir: str) -> list[str]:
    """
    Generate thumbnails at fixed timestamps.
    
    DEPRECATED: Use generate_thumbnails_by_percentage for better flexibility.
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


def generate_thumbnails_by_percentage(
    video_path: str,
    output_dir: str,
    percentages: List[int] = None
) -> List[str]:
    """
    Generate thumbnails at percentage positions in the video.
    
    Args:
        video_path: Path to input video file
        output_dir: Directory to save thumbnail images
        percentages: List of percentage positions (e.g., [10, 50, 90])
                    Defaults to [10, 50, 90]
    
    Returns:
        List of paths to generated thumbnail files
    
    Raises:
        FileNotFoundError: If input video doesn't exist
        RuntimeError: If FFmpeg fails or video duration cannot be determined
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    # Default to 10%, 50%, 90% if not specified
    if percentages is None:
        percentages = THUMBNAIL_PERCENTAGES
    
    # Validate percentages
    for pct in percentages:
        if not 0 <= pct <= 100:
            raise ValueError(f"Invalid percentage: {pct}. Must be between 0 and 100")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Get video duration
    duration = _get_video_duration(video_path)
    logger.info(f"Video duration: {duration:.2f} seconds")
    
    generated = []
    input_filename = Path(video_path).stem
    
    for pct in percentages:
        timestamp = (pct / 100.0) * duration
        output_path = _extract_frame_at_timestamp(
            video_path,
            output_dir,
            input_filename,
            timestamp,
            pct
        )
        generated.append(output_path)
    
    logger.info(f"Generated {len(generated)} thumbnails from {video_path}")
    return generated


def _get_video_duration(video_path: str) -> float:
    """
    Get video duration in seconds using ffprobe.
    
    Args:
        video_path: Path to video file
    
    Returns:
        Duration in seconds
    
    Raises:
        RuntimeError: If ffprobe fails or duration cannot be determined
    """
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]
    
    logger.debug(f"Getting duration: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            logger.error(f"ffprobe failed: {result.stderr}")
            raise RuntimeError(f"Failed to get video duration: {result.stderr}")
        
        duration = float(result.stdout.strip())
        return duration
        
    except ValueError as e:
        logger.error(f"Invalid duration value: {result.stdout}")
        raise RuntimeError(f"Could not parse video duration: {e}")


def _extract_frame_at_timestamp(
    video_path: str,
    output_dir: str,
    input_filename: str,
    timestamp: float,
    percentage: int
) -> str:
    """
    Extract a single frame at the specified timestamp.
    
    Args:
        video_path: Path to input video
        output_dir: Output directory
        input_filename: Base filename without extension
        timestamp: Time in seconds to extract frame
        percentage: Percentage position (for filename)
    
    Returns:
        Path to generated thumbnail
    """
    output_filename = f"{input_filename}_thumb_{percentage}pct.jpg"
    output_path = os.path.join(output_dir, output_filename)
    
    logger.info(f"Extracting frame at {timestamp:.2f}s ({percentage}%): {output_filename}")
    
    cmd = [
        "ffmpeg",
        "-y",  # Overwrite output file
        "-ss", str(timestamp),
        "-i", video_path,
        "-frames:v", "1",  # Extract single frame
        "-q:v", "2",  # High quality (2-5 is good, lower is better)
        output_path
    ]
    
    logger.debug(f"FFmpeg command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            logger.error(f"FFmpeg failed: {result.stderr}")
            raise RuntimeError(f"Failed to extract frame at {timestamp}s: {result.stderr}")
        
        if not os.path.exists(output_path):
            raise RuntimeError(f"Thumbnail was not created: {output_path}")
        
        logger.info(f"Successfully created thumbnail: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error extracting frame: {str(e)}")
        raise
