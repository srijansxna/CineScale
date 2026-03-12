# GET /api/videos/{video_id} - Implementation

## ✅ Endpoint Complete

**URL:** `GET /api/videos/{video_id}`  
**Purpose:** Get complete video information including metadata, variants, thumbnails, and processing status

## Features

✅ Video metadata (duration, resolution, codec, bitrate, fps)  
✅ Available variants/resolutions  
✅ Thumbnail URLs  
✅ Processing status and progress  
✅ Original file information  
✅ Timestamps  

## Request

```bash
GET /api/videos/{video_id}
```

**Path Parameters:**
- `video_id` (string, required) - Unique video identifier (UUID)

## Response

```json
{
  "video_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "filename": "demo.mp4",
  "file_size": 15728640,
  "content_type": "video/mp4",
  "metadata": {
    "duration": 120.5,
    "width": 1920,
    "height": 1080,
    "codec": "h264",
    "bitrate": 5000,
    "fps": 30.0
  },
  "variants": [
    {
      "resolution": "1080p",
      "width": 1920,
      "height": 1080,
      "file_size": 15728640,
      "url": "/api/videos/6ba7b810/stream/1080p",
      "status": "ready"
    },
    {
      "resolution": "720p",
      "width": 1280,
      "height": 720,
      "file_size": 8388608,
      "url": "/api/videos/6ba7b810/stream/720p",
      "status": "ready"
    }
  ],
  "thumbnails": [
    "/api/videos/6ba7b810/thumbnails/thumb_1.jpg",
    "/api/videos/6ba7b810/thumbnails/thumb_2.jpg"
  ],
  "processing": {
    "status": "DONE",
    "progress": 100,
    "job_id": "550e8400-e29b-41d4-a716-446655440000",
    "started_at": "2024-03-12T10:30:00Z",
    "completed_at": "2024-03-12T10:32:00Z",
    "error": null
  },
  "created_at": "2024-03-12T10:30:00Z",
  "updated_at": "2024-03-12T10:32:00Z"
}
```

## Response Fields

### Video Information
- `video_id` - Unique video identifier
- `filename` - Original filename
- `file_size` - Original file size in bytes
- `content_type` - MIME type
- `created_at` - Upload timestamp
- `updated_at` - Last update timestamp

### Metadata (when processing complete)
- `duration` - Video duration in seconds
- `width` - Video width in pixels
- `height` - Video height in pixels
- `codec` - Video codec (h264, h265, vp9, etc.)
- `bitrate` - Bitrate in kbps
- `fps` - Frames per second

### Variants (available resolutions)
- `resolution` - Resolution name (720p, 1080p, etc.)
- `width` - Width in pixels
- `height` - Height in pixels
- `file_size` - Variant file size
- `url` - Streaming URL
- `status` - Variant status (pending, processing, ready, failed)

### Thumbnails
- Array of thumbnail URLs
- Can be used for video preview

### Processing Status
- `status` - Overall status (PENDING/PROCESSING/DONE/FAILED)
- `progress` - Progress percentage (0-100)
- `job_id` - Associated processing job ID
- `started_at` - When processing started
- `completed_at` - When processing completed
- `error` - Error message if failed

## Examples

### 1. Pending Video (Just Uploaded)
```bash
curl http://localhost:8000/api/videos/6ba7b810-9dad-11d1-80b4-00c04fd430c8
```

Response:
```json
{
  "video_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "filename": "demo.mp4",
  "file_size": 1570024,
  "content_type": "video/mp4",
  "metadata": null,
  "variants": [],
  "thumbnails": [],
  "processing": {
    "status": "PENDING",
    "progress": 0,
    "job_id": "550e8400-...",
    "started_at": null,
    "completed_at": null,
    "error": null
  },
  "created_at": "2024-03-12T10:30:00Z",
  "updated_at": null
}
```

### 2. Processing Video
```json
{
  "processing": {
    "status": "PROCESSING",
    "progress": 45,
    "started_at": "2024-03-12T10:30:05Z"
  }
}
```

### 3. Completed Video (Full Details)
```json
{
  "metadata": {
    "duration": 120.5,
    "width": 1920,
    "height": 1080,
    "codec": "h264",
    "bitrate": 5000,
    "fps": 30.0
  },
  "variants": [
    {
      "resolution": "1080p",
      "url": "/api/videos/6ba7b810/stream/1080p",
      "status": "ready"
    },
    {
      "resolution": "720p",
      "url": "/api/videos/6ba7b810/stream/720p",
      "status": "ready"
    }
  ],
  "thumbnails": [
    "/api/videos/6ba7b810/thumbnails/thumb_1.jpg"
  ],
  "processing": {
    "status": "DONE",
    "progress": 100,
    "completed_at": "2024-03-12T10:32:00Z"
  }
}
```

### 4. Failed Video
```json
{
  "processing": {
    "status": "FAILED",
    "progress": 30,
    "error": "Unsupported video codec"
  }
}
```

## Related Endpoints

### Stream Video Variant
```bash
GET /api/videos/{video_id}/stream/{resolution}
```

Example:
```bash
curl http://localhost:8000/api/videos/6ba7b810/stream/720p
```

### Get Thumbnail
```bash
GET /api/videos/{video_id}/thumbnails/{thumbnail_name}
```

Example:
```bash
curl http://localhost:8000/api/videos/6ba7b810/thumbnails/thumb_1.jpg
```

## Testing

### Automated Test
```bash
chmod +x test_video_detail.sh
./test_video_detail.sh
```

### Manual Test
```bash
# 1. Upload video
RESPONSE=$(curl -s -X POST http://localhost:8000/api/upload \
  -F "file=@video.mp4")

# 2. Get video_id
VIDEO_ID=$(echo $RESPONSE | jq -r '.video_id')

# 3. Get video details
curl http://localhost:8000/api/videos/$VIDEO_ID | jq
```

### Interactive Docs
Visit: http://localhost:8000/docs

## Use Cases

### 1. Video Player UI
```javascript
// Fetch video details
const response = await fetch(`/api/videos/${videoId}`);
const video = await response.json();

// Display metadata
console.log(`Duration: ${video.metadata.duration}s`);
console.log(`Resolution: ${video.metadata.width}x${video.metadata.height}`);

// Show thumbnails
video.thumbnails.forEach(thumb => {
  displayThumbnail(thumb);
});

// Select quality
video.variants.forEach(variant => {
  addQualityOption(variant.resolution, variant.url);
});
```

### 2. Processing Status Monitor
```javascript
// Poll for processing status
const checkStatus = async () => {
  const response = await fetch(`/api/videos/${videoId}`);
  const video = await response.json();
  
  updateProgressBar(video.processing.progress);
  
  if (video.processing.status === 'DONE') {
    showVideoPlayer(video);
  } else if (video.processing.status === 'FAILED') {
    showError(video.processing.error);
  } else {
    setTimeout(checkStatus, 2000); // Poll every 2 seconds
  }
};
```

### 3. Video Gallery
```javascript
// Display video card
const displayVideoCard = (video) => {
  return `
    <div class="video-card">
      <img src="${video.thumbnails[0]}" />
      <h3>${video.filename}</h3>
      <p>${formatDuration(video.metadata.duration)}</p>
      <p>${video.metadata.width}x${video.metadata.height}</p>
      <span class="status">${video.processing.status}</span>
    </div>
  `;
};
```

## Implementation Files

```
services/api/
├── routes/
│   └── videos.py                  # GET /api/videos/{video_id}
├── schemas/
│   └── video_detail.py            # Response models
└── services/
    └── video_service.py           # get_video_by_id, get_job_by_video_id
```

## Data Flow

```
Client Request
  ↓
GET /api/videos/{video_id}
  ↓
VideoService.get_video_by_id()
  ↓
PostgreSQL: SELECT FROM videos
  ↓
VideoService.get_job_by_video_id()
  ↓
PostgreSQL: SELECT FROM processing_jobs
  ↓
Build Response:
  - Video info
  - Metadata (from job.result)
  - Variants (from job.result)
  - Thumbnails (from job.result)
  - Processing status
  ↓
Return VideoDetailResponse
```

## Next Steps

1. ✅ Video detail endpoint
2. Implement worker to populate metadata
3. Add video transcoding for variants
4. Generate thumbnails
5. Add video listing endpoint
6. Add search and filtering
7. Add pagination
