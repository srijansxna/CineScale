from services.api.core.worker import process_video
import threading
from services.api.core.states import JobStatus
from fastapi import APIRouter, UploadFile, File
import uuid, os
from services.api.core.jobs import jobs

router = APIRouter()
RAW_DIR = "storage/raw"
os.makedirs(RAW_DIR, exist_ok=True)

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())
    path = os.path.join(RAW_DIR, file.filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    jobs[job_id] = {
        "status": JobStatus.PENDING,
        "filename": file.filename
    }
    threading.Thread(target=process_video, args=(job_id,)).start()
    return {
        "job_id": job_id,
        "status": jobs[job_id]["status"]
    }
