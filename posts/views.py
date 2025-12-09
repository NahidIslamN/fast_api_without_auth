from fastapi import APIRouter, HTTPException, Depends, status
from database import get_db
from models import Twit
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from posts.serializers import TwitSerializers


post_router = APIRouter(
    prefix="/api",
    tags=["Twits"]
)

@post_router.get('/posts/', status_code=status.HTTP_200_OK)
async def get_post_lists(db:AsyncSession = Depends(get_db)):
    db_operations = await db.execute(
        select(Twit)
    )
    posts =db_operations.scalars().all()
    return {
        "success":True,
        "message":"data fatched !",
        "twits":posts
    }
