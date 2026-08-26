import os
from uuid import UUID

import boto3
from botocore.client import Config
from fastapi import UploadFile
from app import config

class ObjectStorage:

    def __init__(self):
        self.endpoint_url = config.S3_ENDPOINT_URL
        self.access_key = config.S3_ACCESS_KEY
        self.secret_key = config.S3_SECRET_KEY
        self.bucket = config.S3_BUCKET

        self.client = boto3.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name="us-east-1",
            config=Config(
                signature_version="s3v4"
            ),
        )

    def ensure_bucket(self):
        buckets = self.client.list_buckets()

        exists = any(
            bucket["Name"] == self.bucket
            for bucket in buckets["Buckets"]
        )

        if not exists:
            self.client.create_bucket(
                Bucket=self.bucket
            )

    async def upload(
        self,
        file: UploadFile,
        document_id: UUID,
    ) -> str:

        object_key = f"documents/{document_id}.pdf"

        self.client.upload_fileobj(
            file.file,
            self.bucket,
            object_key,
            ExtraArgs={
                "ContentType": file.content_type
                or "application/pdf"
            },
        )

        return object_key
    
    def download(
        self,
        object_key: str,
    ) -> bytes:

        response = self.client.get_object(
            Bucket=self.bucket,
            Key=object_key,
        )

        try:
            return response["Body"].read()
        finally:
            response["Body"].close()