from fastapi import APIRouter, HTTPException, Depends, status
from database import get_db
from models import Twit, User, React
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import selectinload, defer
from posts.serializers import TwitSerializers, ReactSerializers



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


@post_router.post('/posts/', status_code=status.HTTP_200_OK)
async def create_twit(twit_data:TwitSerializers, db:AsyncSession = Depends(get_db)):
    user = await db.get(User, twit_data.user_id)
    if user:
        new_twit = Twit(
            title = twit_data.title,
            description = twit_data.description,            
            user_id = twit_data.user_id
        )
        db.add(new_twit)
        try:
            await db.commit()
            await db.refresh(new_twit)
            return {
                "success":True,
                "message":'twit created successful!',
                "twit":new_twit
            }
        except:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user not found with this id!"
            )
        
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user not found with this id!"
        )




@post_router.get('/posts/{pk}', status_code=status.HTTP_200_OK)
async def create_twit(pk:int, db:AsyncSession = Depends(get_db)):
    db_operations = await db.execute(
        select(Twit).where(Twit.id == pk).options(
            defer(
                Twit.user_id
            )
        ).options(selectinload(Twit.reacts).options(selectinload(React.creator).options(
            defer(User.password),
        )))
    )
    twit = db_operations.scalar_one_or_none()
    if twit:        
        return {
            "success":True,
            "message":'twit created successful!',
            "twit":twit
        }
                
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="twit not found with this id!"
        )


@post_router.put('/posts/{pk}',  status_code=status.HTTP_200_OK)
async def create_twit(pk:int, react_data:ReactSerializers, db:AsyncSession = Depends(get_db)):
    db_operations = await db.execute(
        select(Twit).where(Twit.id == pk).options(selectinload(Twit.reacts))
    )
    twit = db_operations.scalar_one_or_none()
    
    if twit:
        user = await db.get(User, react_data.user_id)
        if user:
            new_react = React(
                react_emuji=react_data.react_emuji,
                user_id=react_data.user_id
            )
            db.add(new_react)
            await db.flush()

            twit.reacts.append(new_react)

            await db.commit()
            await db.refresh(new_react)

            return {"new_react": new_react}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user not found with this id!"
            )

                
    else:
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="twit not found with this id!"
        )


