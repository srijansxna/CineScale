import subprocess
import logging
import os
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)

# Resolution configurations
RESOLUTIONS = {
    "360p": {"width": 640, "height": 360, "bitrate": "800k"},
    "720p": {"width": 1280, "height": 720, "bitrate": "2500k"},
    "1080p": {"width": 1920, "height": 1080, "bitrate": "5000k"}
}


def transcode_video(
    input_path: str,
    output_dir: str,
    resolutions: List[str] = None
) -> Dict[str, str]:
    """
    Transcode video to multiple resolutions using FFmpeg.
    
    Args:
        input_path: Path to input video file
        output_dir: Directory to save transcoded videos
        resolutions: List of resolution keys (e.g., ["360p", "720p", "1080p"])
                    Defaults to all available resolutions
    
    Returns:
        Dictionary mapping resolution to output file path
    
    Raises:
        RuntimeError: If FFmpeg transcoding fails
        FileNotFoundError: If input file doesn't exist
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input video not found: {input_path}")
    
    # Default to all resolutions if not specified
    if resolutions is None:
        resolutions = list(RESOLUTIONS.keys())
    
    # Validate resolutions
    for res in resolutions:
        if res not in RESOLUTIONS:
            raise ValueError(f"Invalid resolution: {res}. Must be one of {list(RESOLUTIONS.keys())}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Get input filename without extension
    input_filename = Path(input_path).stem
    
    output_files = {}
    
    for resolution in resolutions:
        output_path = _transcode_single_resolution(
            input_path,
            output_dir,
            input_filename,
            resolution
        )
        output_files[resolution] = output_path
    
    logger.info(f"Successfully transcoded {input_path} to {len(output_files)} resolutions")
    return output_files


def _transcode_single_resolution(
    input_path: str,
    output_dir: str,
    input_filename: str,
    resolution: str
) -> str:
    """
    Transcode video to a single resolution.
    
    Args:
        input_path: Path to input video
        output_dir: Output directory
        input_filename: Base filename without extension
        resolution: Resolution key (e.g., "720p")
    
    Returns:
        Path to transcoded output file
    """
    config = RESOLUTIONS[resolution]
    output_filename = f"{input_filename}_{resolution}.mp4"
    output_path = os.path.join(output_dir, output_filename)
    
    logger.info(f"Transcoding to {resolution}: {output_filename}")
    
    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-vf", f"scale={config['width']}:{config['height']}",
        "-c:v", "libx264",
        "-b:v", config["bitrate"],
        "-c:a", "aac",
        "-b:a", "128k",
        "-y",  # Overwrite output file if exists
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
            logger.error(f"FFmpeg failed for {resolution}: {result.stderr}")
            raise RuntimeError(f"FFmpeg transcoding failed for {resolution}: {result.stderr}")
        
        logger.info(f"Successfully created {resolution} output: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error transcoding to {resolution}: {str(e)}")
        raise


def get_available_resolutions() -> List[str]:
    """Get list of available resolution presets."""
    return list(RESOLUTIONS.keys())
