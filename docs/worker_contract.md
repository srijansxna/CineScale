# Video Processing Worker Contract

## Input

- job_id: unique job identifier
- input_path: path to source video
- output_dir: base output directory

## Output

{
"qualities": [
{
"resolution": "360p",
"path": "output/360p/video.mp4"
},
{
"resolution": "720p",
"path": "output/720p/video.mp4"
}
],
"thumbnails": [
"storage/thumbnails/thumb.jpg"
],
"metadata": {
"duration": "...",
"codec": "...",
"resolution": "...",
"fps": "..."
}
}
