from pydantic import BaseModel

## write your serializers

class TwitSerializers(BaseModel):
    title:str
    description:str  
    user_id:int


class ReactSerializers(BaseModel):
    react_emuji:str
    user_id:int
    



class UserOut(BaseModel):
    id: int
    frist_name: str
    last_name: str
    username: str
    username: str

    class Config:
        orm_mode = True



class ReactOut(BaseModel):
    id: int
    react_emuji: str
    user_id: int
    creator: UserOut
    

    class Config:
        orm_mode = True


class TwitOut(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    reacts: list[ReactOut]

    class Config:
        orm_mode = True
