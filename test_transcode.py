#!/usr/bin/env python3
"""
Test script for video transcoding module.
"""
import logging
import sys
import os

# Add Services directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Services'))

from transcoder.transcode import transcode_video, get_available_resolutions

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    # Example usage
    input_video = "input/input.mp4"
    output_directory = "output"
    
    print(f"Available resolutions: {get_available_resolutions()}")
    print(f"\nTranscoding {input_video}...")
    
    try:
        # Transcode to all resolutions
        results = transcode_video(input_video, output_directory)
        
        print("\nTranscoding completed successfully!")
        print("\nOutput files:")
        for resolution, filepath in results.items():
            print(f"  {resolution}: {filepath}")
        
        return 0
        
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
