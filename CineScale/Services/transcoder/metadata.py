import subprocess
import json
import logging
import os
from typing import Dict, Optional

logger = logging.getLogger(__name__)


def extract_metadata(video_path: str) -> dict:
    """
    Extract comprehensive video metadata using ffprobe.
    
    Args:
        video_path: Path to video file
    
    Returns:
        Dictionary containing:
        - duration: Video duration in seconds (float)
        - codec: Video codec name (str)
        - fps: Frames per second (float)
        - resolution: Resolution as "WIDTHxHEIGHT" (str)
        - width: Video width in pixels (int)
        - height: Video height in pixels (int)
        - bitrate: Video bitrate in bits/second (int)
        - audio_codec: Audio codec name (str, optional)
        - file_size: File size in bytes (int)
    
    Raises:
        FileNotFoundError: If video file doesn't exist
        RuntimeError: If ffprobe fails or no video stream found
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    logger.info(f"Extracting metadata from: {video_path}")
    
    cmd = [
        "ffprobe",
        "-v", "error",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        video_path
    ]
    
    logger.debug(f"FFprobe command: {' '.join(cmd)}")
    
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
            raise RuntimeError(f"ffprobe failed: {result.stderr}")
        
        data = json.loads(result.stdout)
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse ffprobe output: {e}")
        raise RuntimeError(f"Invalid JSON from ffprobe: {e}")
    
    # Find video stream
    video_stream = next(
        (s for s in data["streams"] if s["codec_type"] == "video"),
        None
    )
    
    if not video_stream:
        raise RuntimeError("No video stream found")
    
    # Find audio stream (optional)
    audio_stream = next(
        (s for s in data["streams"] if s["codec_type"] == "audio"),
        None
    )
    
    # Extract format information
    format_info = data.get("format", {})
    
    # Parse FPS from r_frame_rate (e.g., "30/1" or "30000/1001")
    fps = _parse_frame_rate(video_stream.get("r_frame_rate", "0/1"))
    
    # Get bitrate (prefer stream bitrate, fallback to format bitrate)
    bitrate = int(video_stream.get("bit_rate", 0))
    if bitrate == 0:
        bitrate = int(format_info.get("bit_rate", 0))
    
    # Build metadata dictionary
    metadata = {
        "duration": float(format_info.get("duration", 0)),
        "codec": video_stream.get("codec_name", "unknown"),
        "fps": fps,
        "resolution": f"{video_stream['width']}x{video_stream['height']}",
        "width": int(video_stream["width"]),
        "height": int(video_stream["height"]),
        "bitrate": bitrate,
        "file_size": int(format_info.get("size", 0))
    }
    
    # Add audio codec if available
    if audio_stream:
        metadata["audio_codec"] = audio_stream.get("codec_name", "unknown")
    
    logger.info(f"Metadata extracted: {metadata['resolution']} @ {metadata['fps']:.2f}fps, "
                f"{metadata['codec']}, {metadata['duration']:.2f}s")
    
    return metadata


def _parse_frame_rate(frame_rate_str: str) -> float:
    """
    Parse frame rate from FFprobe format (e.g., "30/1" or "30000/1001").
    
    Args:
        frame_rate_str: Frame rate string in "numerator/denominator" format
    
    Returns:
        Frame rate as float (frames per second)
    """
    try:
        if "/" in frame_rate_str:
            num, den = frame_rate_str.split("/")
            return float(num) / float(den)
        return float(frame_rate_str)
    except (ValueError, ZeroDivisionError):
        logger.warning(f"Could not parse frame rate: {frame_rate_str}")
        return 0.0


def get_video_info_summary(video_path: str) -> str:
    """
    Get a human-readable summary of video metadata.
    
    Args:
        video_path: Path to video file
    
    Returns:
        Formatted string with video information
    """
    metadata = extract_metadata(video_path)
    
    duration_min = int(metadata["duration"] // 60)
    duration_sec = int(metadata["duration"] % 60)
    bitrate_mbps = metadata["bitrate"] / 1_000_000
    file_size_mb = metadata["file_size"] / (1024 * 1024)
    
    summary = f"""Video Information:
  File: {os.path.basename(video_path)}
  Duration: {duration_min}m {duration_sec}s
  Resolution: {metadata['resolution']}
  FPS: {metadata['fps']:.2f}
  Codec: {metadata['codec']}
  Bitrate: {bitrate_mbps:.2f} Mbps
  File Size: {file_size_mb:.2f} MB"""
    
    if "audio_codec" in metadata:
        summary += f"\n  Audio Codec: {metadata['audio_codec']}"
    
    return summary
