#!/usr/bin/env python3
"""
Test script for video metadata extraction module.
"""
import logging
import sys
import os
import json

# Add Services directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Services'))

from transcoder.metadata import extract_metadata, get_video_info_summary

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    # Example usage
    input_video = "input/input.mp4"
    
    print(f"Extracting metadata from {input_video}...\n")
    
    try:
        # Extract metadata
        metadata = extract_metadata(input_video)
        
        print("=" * 60)
        print("METADATA EXTRACTION SUCCESSFUL")
        print("=" * 60)
        
        # Display as formatted JSON
        print("\nRaw Metadata (JSON):")
        print(json.dumps(metadata, indent=2))
        
        # Display human-readable summary
        print("\n" + "=" * 60)
        print(get_video_info_summary(input_video))
        print("=" * 60)
        
        # Display individual fields
        print("\nKey Fields:")
        print(f"  Duration: {metadata['duration']:.2f} seconds")
        print(f"  Codec: {metadata['codec']}")
        print(f"  FPS: {metadata['fps']:.2f}")
        print(f"  Resolution: {metadata['resolution']}")
        print(f"  Bitrate: {metadata['bitrate']:,} bits/sec ({metadata['bitrate']/1_000_000:.2f} Mbps)")
        
        return 0
        
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
