from pydantic import BaseModel
from typing import Optional


## write your serirlaizers


class UserSerializers(BaseModel):
    frist_name:str
    last_name:str
    username:str
    password:str


class UserSerializersPatch(BaseModel):
    frist_name:Optional[str] = None
    last_name:Optional[str] = None
    username:Optional[str] = None
