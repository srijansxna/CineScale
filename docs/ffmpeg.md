# FFmpeg Verification

Verified FFmpeg and FFprobe installation.

## Transcoding Commands

```bash
ffmpeg -i input.mp4 -vf scale=640:360 output_360p.mp4
ffmpeg -i input.mp4 -vf scale=1280:720 output_720p.mp4
