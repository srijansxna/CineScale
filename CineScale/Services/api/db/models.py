from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime


class JobStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    DONE = "DONE"
    FAILED = "FAILED"


class VideoResolution(str, Enum):
    RES_240P = "240p"
    RES_360P = "360p"
    RES_720P = "720p"
    RES_1080P = "1080p"
