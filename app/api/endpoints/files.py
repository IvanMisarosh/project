import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.post_file import PostFile
from app.upload_service import get_file as get_file_url

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{file_id}")
async def get_file(file_id: int, db: Session = Depends(get_db)):
    file = db.query(PostFile).filter(PostFile.id == file_id).first()
    
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")

    file_path = await get_file_url(file.file_url) 
    if file_path.startswith("http://") or file_path.startswith("https://"):
        return {"download_url": file_path}

    if not os.path.exists(file_path):
        print(file_path)
        raise HTTPException(status_code=404, detail="Local file not found")

    return FileResponse(file_path, media_type="application/octet-stream", filename=file.filename)
