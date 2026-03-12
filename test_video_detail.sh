#!/bin/bash

echo "🧪 Testing GET /api/videos/{video_id} endpoint"
echo "==============================================="
echo ""

# Upload a video first
echo "1. Uploading test video..."
UPLOAD_RESPONSE=$(curl -s -X POST http://localhost:8000/api/upload \
  -F "file=@Services/worker/samples/demo.mp4")

VIDEO_ID=$(echo "$UPLOAD_RESPONSE" | jq -r '.video_id')
JOB_ID=$(echo "$UPLOAD_RESPONSE" | jq -r '.job_id')

echo "✅ Upload complete"
echo "   Video ID: $VIDEO_ID"
echo "   Job ID:   $JOB_ID"
echo ""

# Get video details
echo "2. Getting video details..."
VIDEO_RESPONSE=$(curl -s "http://localhost:8000/api/videos/$VIDEO_ID")

echo "$VIDEO_RESPONSE" | jq
echo ""

# Extract key information
STATUS=$(echo "$VIDEO_RESPONSE" | jq -r '.processing.status')
PROGRESS=$(echo "$VIDEO_RESPONSE" | jq -r '.processing.progress')
FILENAME=$(echo "$VIDEO_RESPONSE" | jq -r '.filename')
FILE_SIZE=$(echo "$VIDEO_RESPONSE" | jq -r '.file_size')

echo "📊 Video Summary:"
echo "   Filename:  $FILENAME"
echo "   Size:      $FILE_SIZE bytes"
echo "   Status:    $STATUS"
echo "   Progress:  $PROGRESS%"
echo ""

# Test non-existent video
echo "3. Testing non-existent video..."
curl -s "http://localhost:8000/api/videos/invalid-video-id" | jq
echo ""

echo "✅ All tests complete!"
echo ""
echo "💡 To simulate processed video with metadata, update the job result:"
echo "   docker compose -f docker-compose.postgres.yml exec postgres psql -U postgres -d cinescale"
echo "   UPDATE processing_jobs SET status='DONE', progress=100, result='{\"metadata\":{\"duration\":120,\"width\":1920,\"height\":1080}}' WHERE job_id='$JOB_ID';"
