import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.post_file import PostFile

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/files/{file_id}")
async def get_file(file_id: int, db: Session = Depends(get_db)):
    file = db.query(PostFile).filter(PostFile.id == file_id).first()
    
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")

    file_path = file.file_url  # File path or URL to fetch from (e.g., Azure Blob URL)
    
    return FileResponse(file_path, media_type="application/octet-stream", filename=file.filename)
