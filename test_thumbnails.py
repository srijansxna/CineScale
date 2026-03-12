#!/usr/bin/env python3
"""
Test script for thumbnail generation module.
"""
import logging
import sys
import os

# Add Services directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Services'))

from transcoder.thumbnails import generate_thumbnails_by_percentage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    # Example usage
    input_video = "input/input.mp4"
    output_directory = "output/thumbnails"
    
    print(f"Generating thumbnails from {input_video}...")
    print(f"Extracting frames at 10%, 50%, and 90% positions\n")
    
    try:
        # Generate thumbnails at 10%, 50%, 90%
        thumbnail_paths = generate_thumbnails_by_percentage(
            input_video,
            output_directory,
            percentages=[10, 50, 90]
        )
        
        print("\nThumbnail generation completed successfully!")
        print(f"\nGenerated {len(thumbnail_paths)} thumbnails:")
        for i, path in enumerate(thumbnail_paths, 1):
            print(f"  {i}. {path}")
        
        return 0
        
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
