import os
from uuid import uuid4
from fastapi import UploadFile
from app.config import settings

# Azure
from azure.storage.blob import BlobServiceClient

async def save_file(file: UploadFile) -> str:
    filename = f"{uuid4().hex}_{file.filename}"

    if settings.STORAGE_BACKEND == "local":
        file_path = os.path.join(settings.UPLOAD_DIR, filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        return file_path

    elif settings.STORAGE_BACKEND == "azure":
        blob_service = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONN_STR)
        container_client = blob_service.get_container_client(settings.AZURE_STORAGE_CONTAINER_NAME)
        sas_token = settings.AZURE_STORAGE_SAS_TOKEN

        blob_client = container_client.get_blob_client(filename)
        await blob_client.upload_blob(await file.read(), overwrite=True)

        blob_url = f"https://{blob_service.account_name}.blob.core.windows.net/{settings.AZURE_STORAGE_CONTAINER_NAME}/{filename}?{sas_token}"
        return blob_url

    raise RuntimeError("Unsupported storage backend")


async def delete_file(file_url: str) -> None:
    if settings.STORAGE_BACKEND == "local":
        file_path = os.path.join(settings.UPLOAD_DIR, os.path.basename(file_url))
        if os.path.exists(file_path):
            os.remove(file_path)

    elif settings.STORAGE_BACKEND == "azure":
        blob_service = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONN_STR)
        container_client = blob_service.get_container_client(settings.AZURE_STORAGE_CONTAINER_NAME)

        blob_name = os.path.basename(file_url)
        blob_client = container_client.get_blob_client(blob_name)
        await blob_client.delete_blob()

    else:
        raise RuntimeError("Unsupported storage backend")
