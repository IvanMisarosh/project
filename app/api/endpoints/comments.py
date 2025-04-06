from fastapi import APIRouter, HTTPException
from app.schemas.comment import Comment
from app.db.mongodb import db
from bson import ObjectId

router = APIRouter()

@router.post("/comments/")
async def add_comment(comment: Comment):
    result = await db.comments.insert_one(comment.model_dump())
    if not result.acknowledged:
        raise HTTPException(status_code=500, detail="Failed to add comment")
    return {"id": str(result.inserted_id)}

@router.get("/comments/{post_id}")
async def get_comments(post_id: int):
    comments = await db.comments.find(
        {"post_id": post_id},
        {"_id": 0}).to_list(length=100)
    # <-- виключає _id
    return comments
