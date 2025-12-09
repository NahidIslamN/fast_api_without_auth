from pydantic import BaseModel

## write your serializers

class TwitSerializers(BaseModel):
    title:str
    description:str  
    user_id:int


class ReactSerializers(BaseModel):
    react_emuji:str
    user_id:int
    
