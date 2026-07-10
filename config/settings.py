from pydantic_settings import BaseSettings
from pydantic import BaseModel, ConfigDict
from fastapi import File, UploadFile
from typing import *


class SysemSettings(BaseSettings):
    pageindex_api_key: str
    # Bucket storage
    minio_secretkey: str
    minio_username: str
    minio_localhost: str
    minio_bucket_name: str

    model_config = ConfigDict(
        env_file=".env"
    )


class UserClass(BaseModel):
    query: str
    doc_id: str


settings = SysemSettings()
