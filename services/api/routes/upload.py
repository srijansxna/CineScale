from fastapi import APIRouter, UploadFile, File
import uuid
import os
import threading

from services.api.core.jobs import jobs
from services.api.core.states import JobStatus
from services.api.core.worker import process_video

router = APIRouter()

RAW_DIR = "storage/raw"
os.makedirs(RAW_DIR, exist_ok=True)

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())

    # ✅ DEFINE file_path BEFORE using it
    file_path = os.path.join(RAW_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    jobs[job_id] = {
        "status": JobStatus.PENDING,
        "filename": file.filename
    }

    # ✅ file_path now exists
    threading.Thread(
        target=process_video,
        args=(job_id, file_path)
    ).start()

    return {
        "job_id": job_id,
        "status": JobStatus.PENDING
    }
