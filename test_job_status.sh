#!/bin/bash

echo "🧪 Testing GET /api/job/{job_id} endpoint"
echo "=========================================="
echo ""

# Upload a video first
echo "1. Uploading test video..."
UPLOAD_RESPONSE=$(curl -s -X POST http://localhost:8000/api/upload \
  -F "file=@Services/worker/samples/demo.mp4")

JOB_ID=$(echo "$UPLOAD_RESPONSE" | jq -r '.job_id')
VIDEO_ID=$(echo "$UPLOAD_RESPONSE" | jq -r '.video_id')

echo "✅ Upload complete"
echo "   Job ID: $JOB_ID"
echo ""

# Check job status
echo "2. Checking job status..."
STATUS_RESPONSE=$(curl -s "http://localhost:8000/api/job/$JOB_ID")

echo "$STATUS_RESPONSE" | jq
echo ""

# Extract status info
STATUS=$(echo "$STATUS_RESPONSE" | jq -r '.status')
PROGRESS=$(echo "$STATUS_RESPONSE" | jq -r '.progress')

echo "📊 Job Status Summary:"
echo "   Status:   $STATUS"
echo "   Progress: $PROGRESS%"
echo ""

# Test non-existent job
echo "3. Testing non-existent job..."
curl -s "http://localhost:8000/api/job/invalid-job-id" | jq
echo ""

echo "✅ All tests complete!"
