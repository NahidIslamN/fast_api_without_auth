from fastapi import APIRouter, HTTPException, Depends, status
from database import get_db
from models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from users.serializers import UserSerializers, UserSerializersPatch


router = APIRouter(
    prefix="/api",
    tags=["Users"]
)


@router.get('/users/', status_code=status.HTTP_200_OK)
async def get_userlist(db:AsyncSession=(Depends(get_db))):
    db_operation = await db.execute(
        select(User)        
    )
    users = db_operation.scalars().all()

    return{
        'success':True,
        "message":"data fatched !",
        "users":users
    }



@router.post('/users/', status_code=status.HTTP_201_CREATED)
async def register_user(user_data:UserSerializers,db:AsyncSession=(Depends(get_db))):
    new_user = User(
        frist_name = user_data.frist_name,
        last_name =  user_data.last_name,
        username =  user_data.username,
        password = user_data.password
    )
    db.add(new_user)

    try:
        await db.commit()
        await db.refresh(new_user)
        return{
            "success":True,
            "message":"user created successfull"
        }
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user already exits with this id!"
        )



@router.get('/users/{pk}', status_code=status.HTTP_200_OK)
async def get_user_details(pk:int,db:AsyncSession=(Depends(get_db))):
    user = await db.get(User, pk)

    if user:
        return{
            "success":True,
            "message":"user data fatched!",
            'users':user
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found with this id!"
        )




@router.patch('/users/{pk}', status_code=status.HTTP_200_OK)
async def update_user_details(pk:int,updated_data:UserSerializersPatch,db:AsyncSession=(Depends(get_db))):
    user = await db.get(User, pk)

    if user:
        if updated_data.frist_name:
            user.frist_name = updated_data.frist_name
        
        if updated_data.last_name:
            user.last_name = updated_data.last_name
        
        if updated_data.username:
            user.username = updated_data.username
        
        try:
            await db.commit()
            await db.refresh(user)
            return{
                "success":True,
                "message":"update user data successfull!"
            }
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="username has already taken!"
            )
            
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found with this id"
        )
    


@router.delete('/users/{pk}', status_code=status.HTTP_200_OK)
async def delete_user_details(pk:int,db:AsyncSession=(Depends(get_db))):
    user = await db.get(User, pk)

    if user:
        await db.delete(user)
        await db.commit()
        return{
            "success":True,
            "message":"delete user data successful !"
        }
       
            
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found with this id!"
        )
    
    

    
    
    

    
