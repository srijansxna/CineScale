#!/bin/bash
# Start Celery worker for video processing

echo "Starting Celery Worker..."
echo "========================="
echo ""
echo "Make sure Redis is running:"
echo "  docker-compose up redis"
echo ""
echo "Or start everything:"
echo "  docker-compose up"
echo ""
echo "========================="
echo ""

# Set Python path to include Services directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)/Services"

# Start Celery worker
cd Services/worker
celery -A celery_app worker --loglevel=info --concurrency=2
