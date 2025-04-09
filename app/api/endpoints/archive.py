from azure.storage.queue import QueueClient, BinaryBase64EncodePolicy
from fastapi import APIRouter, HTTPException
from app.config import settings
import json
import os
import logging

router = APIRouter()
logger = logging.getLogger("app")

@router.post("/{post_id}")
async def archive_post(post_id: int):
    # Data to send to the queue
    archive_data = {
        "post_id": post_id,
        "action": "archive"
    }

    # Get the queue connection string and queue name from settings
    queue_conn_str = settings.QUEUE_CONNECTION_STRING
    logger.info(f"queue_conn_str: {queue_conn_str}")

    queue_conn_str_getenv = os.getenv("QUEUE_CONNECTION_STRING")
    logger.info(f"queue_conn_str_getenv: {queue_conn_str_getenv}")
    
    queue_name = settings.QUEUE_NAME

    if not queue_conn_str_getenv:
        raise HTTPException(status_code=500, detail=f"Queue connection string is missing or malformed." \
        f" queue_conn_str_getenv: {queue_conn_str_getenv}, queue_conn_str: {queue_conn_str}")

    # Create the QueueClient using the connection string and queue name
    try:
        queue_client = QueueClient.from_connection_string(queue_conn_str_getenv, queue_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to Azure Queue: {e}")
    
    queue_client.message_encode_policy = BinaryBase64EncodePolicy()
    # Add message to the queue
    try:
        message_bytes = json.dumps(archive_data).encode('utf-8')
        queue_client.send_message(queue_client.message_encode_policy.encode(message_bytes))
        return {"message": "Archiving request has been added to the queue"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add message to the queue: {e}")
