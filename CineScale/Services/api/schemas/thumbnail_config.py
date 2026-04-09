from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional


VALID_THUMBNAIL_KEYS = {"thumbnail_10", "thumbnail_50", "thumbnail_90"}


class ThumbnailConfigRequest(BaseModel):
    default_thumbnail: Literal["thumbnail_10", "thumbnail_50", "thumbnail_90"]
    video_title: str = Field(..., min_length=1, max_length=30)

    @field_validator("video_title")
    @classmethod
    def strip_title(cls, v: str) -> str:
        return v.strip()


class ThumbnailConfigResponse(BaseModel):
    video_id: str
    video_title: str
    default_thumbnail: str
    final_thumbnail_url: Optional[str] = None
