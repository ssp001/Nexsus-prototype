from typing import BinaryIO
from minio import Minio
from minio.error import S3Error
from config import settings
from utils import StorageBucketExcetion
import logfire


class DocumentStorageManager:
    def __init__(self):
        self.client = Minio(
            endpoint=settings.minio_localhost,
            access_key=settings.minio_username,
            secret_key=settings.minio_secretkey,
            secure=False
        )
        self.logging = logfire.configure(service_name=__name__)

    def post_document(self, document_name: str, document_length: int, document_data: BinaryIO):
        """
        Upload a document to the storage bucket.

        """
        try:
            bucket = self.client.bucket_exists(
                bucket_name=settings.minio_bucket_name)
            if bucket is not True:
                self.logging.warning("storage Bucket doesn't exist")
                return None
            respones = self.client.put_object(
                bucket_name=settings.minio_bucket_name, object_name=document_name, data=document_data, length=document_length)
            print(respones)
            self.logging.info("object has been stroed sucessfully")
        except Exception as e:
            self.logging.exception(
                "an excetion ocured can't upload the object in s3", e)
            raise StorageBucketExcetion(
                "an excetion ocured can't upload the object in s3")

    def get_document(self, document_name: str, document_length: BinaryIO):
        """
        Retrieve a document from the storage bucket.

        """
        try:
            bucket = self.client.bucket_exists(
                bucket_name=settings.minio_bucket_name)
            if bucket is not True:
                self.logging.warning("storage Bucket doesn't exist")
                return None
            respones = self.client.get_object(
                bucket_name=settings.minio_bucket_name, object_name=document_name, length=document_length)
            self.logging.debug(f"get_object storage respones")
            with open(f"./tmp/{document_name}.pdf", "wb") as pdf:
                pdf.write(respones.read())
            self.logging.info(
                f"object has been retrieved sucessfully")
            return respones
        except Exception as e:
            self.logging.exception(
                "an excetion ocured can't retrieve the object in s3")
            raise StorageBucketExcetion(
                "an excetion ocured can't retrieve the object in s3") from e
