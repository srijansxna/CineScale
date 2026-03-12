@echo off
REM Start Celery worker for video processing

echo Starting Celery Worker...
echo =========================
echo.
echo Make sure Redis is running:
echo   docker-compose up redis
echo.
echo Or start everything:
echo   docker-compose up
echo.
echo =========================
echo.

REM Check if celery is installed
python -c "import celery" 2>nul
if errorlevel 1 (
    echo ERROR: Celery is not installed!
    echo.
    echo Please install dependencies:
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Start Celery worker using Python module
python -m celery -A Services.worker.celery_app worker --loglevel=info --concurrency=2 --pool=solo
