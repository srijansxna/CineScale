"""
MinIO storage service using the boto3-compatible API (via boto3 + endpoint_url).

Buckets:
  - raw-videos      : original uploads
  - video-variants  : transcoded renditions (360p, 720p, 1080p …)
  - thumbnails      : generated thumbnail images

All public-facing URLs are pre-signed with a configurable TTL.
"""

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from pathlib import Path
from typing import Optional
import logging

from services.api.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class StorageService:
    """MinIO storage via boto3-compatible S3 API."""

    def __init__(self):
        self._client = boto3.client(
            "s3",
            endpoint_url=settings.minio_endpoint,
            aws_access_key_id=settings.minio_access_key,
            aws_secret_access_key=settings.minio_secret_key,
            config=Config(signature_version="s3v4"),
            region_name="us-east-1",  # required by boto3, ignored by MinIO
        )
        self._ensure_buckets()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _ensure_buckets(self) -> None:
        """Create buckets if they don't exist yet."""
        for bucket in (
            settings.minio_bucket_raw,
            settings.minio_bucket_variants,
            settings.minio_bucket_thumbnails,
        ):
            try:
                self._client.head_bucket(Bucket=bucket)
            except ClientError as e:
                if e.response["Error"]["Code"] in ("404", "NoSuchBucket"):
                    self._client.create_bucket(Bucket=bucket)
                    logger.info("Created bucket: %s", bucket)
                else:
                    raise

    def _upload(self, bucket: str, key: str, file_path: str, content_type: Optional[str] = None) -> str:
        """Upload a local file to *bucket* under *key*. Returns the object key."""
        extra = {"ContentType": content_type} if content_type else {}
        self._client.upload_file(
            file_path, bucket, key, ExtraArgs=extra or None)
        logger.info("Uploaded %s → s3://%s/%s", file_path, bucket, key)
        return key

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def upload_file(
        self,
        file_path: str,
        bucket: str,
        object_key: str,
        content_type: Optional[str] = None,
    ) -> str:
        """
        Upload any local file to the specified bucket.

        Args:
            file_path:   Absolute or relative path to the local file.
            bucket:      Target MinIO bucket name.
            object_key:  Destination key inside the bucket.
            content_type: Optional MIME type (e.g. "video/mp4").

        Returns:
            The object key of the uploaded file.
        """
        return self._upload(bucket, object_key, file_path, content_type)

    def get_file_url(
        self,
        bucket: str,
        object_key: str,
        expiry: Optional[int] = None,
    ) -> str:
        """
        Generate a pre-signed URL for an object.

        Args:
            bucket:     Bucket name.
            object_key: Object key inside the bucket.
            expiry:     URL lifetime in seconds (defaults to settings value).

        Returns:
            Pre-signed HTTPS/HTTP URL string.
        """
        url = self._client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": object_key},
            ExpiresIn=expiry or settings.minio_presigned_expiry,
        )
        return url

    def store_video_variant(
        self,
        video_id: str,
        resolution: str,
        file_path: str,
    ) -> str:
        """
        Store a transcoded video variant and return its pre-signed URL.

        Object key pattern: <video_id>/<resolution>/<filename>

        Args:
            video_id:   UUID of the parent video.
            resolution: Label such as "360p", "720p", "1080p".
            file_path:  Local path to the transcoded file.

        Returns:
            Pre-signed URL for the stored variant.
        """
        filename = Path(file_path).name
        key = f"{video_id}/{resolution}/{filename}"
        self._upload(settings.minio_bucket_variants, key,
                     file_path, content_type="video/mp4")
        return self.get_file_url(settings.minio_bucket_variants, key)

    def store_thumbnail(
        self,
        video_id: str,
        thumbnail_name: str,
        file_path: str,
    ) -> str:
        """
        Store a thumbnail image and return its pre-signed URL.

        Object key pattern: <video_id>/<thumbnail_name>

        Args:
            video_id:       UUID of the parent video.
            thumbnail_name: Filename for the thumbnail (e.g. "thumb_50pct.jpg").
            file_path:      Local path to the thumbnail image.

        Returns:
            Pre-signed URL for the stored thumbnail.
        """
        key = f"{video_id}/{thumbnail_name}"
        self._upload(settings.minio_bucket_thumbnails, key,
                     file_path, content_type="image/jpeg")
        return self.get_file_url(settings.minio_bucket_thumbnails, key)


# FastAPI dependency
def get_storage_service() -> StorageService:
    return StorageService()
