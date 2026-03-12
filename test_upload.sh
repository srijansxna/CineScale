#!/bin/bash

echo "🧪 Testing POST /api/upload endpoint"
echo "===================================="
echo ""

# Check if API is running
echo "1. Checking API health..."
HEALTH=$(curl -s http://localhost:8000/health)
if [ $? -eq 0 ]; then
    echo "✅ API is running"
    echo "$HEALTH" | jq
else
    echo "❌ API is not running. Start it with: python run.py"
    exit 1
fi

echo ""
echo "2. Uploading test video..."

# Check if test video exists
if [ ! -f "Services/worker/samples/demo.mp4" ]; then
    echo "❌ Test video not found: Services/worker/samples/demo.mp4"
    exit 1
fi

# Upload video
RESPONSE=$(curl -s -X POST http://localhost:8000/api/upload \
  -F "file=@Services/worker/samples/demo.mp4")

if [ $? -eq 0 ]; then
    echo "✅ Upload successful!"
    echo ""
    echo "Response:"
    echo "$RESPONSE" | jq
    
    # Extract job_id and video_id
    JOB_ID=$(echo "$RESPONSE" | jq -r '.job_id')
    VIDEO_ID=$(echo "$RESPONSE" | jq -r '.video_id')
    
    echo ""
    echo "📋 Summary:"
    echo "  Job ID:   $JOB_ID"
    echo "  Video ID: $VIDEO_ID"
    echo ""
    echo "Next steps:"
    echo "  - Check job status: curl http://localhost:8000/api/jobs/$JOB_ID"
    echo "  - View in database: psql -d cinescale -c 'SELECT * FROM videos;'"
else
    echo "❌ Upload failed"
    echo "$RESPONSE"
    exit 1
fi
