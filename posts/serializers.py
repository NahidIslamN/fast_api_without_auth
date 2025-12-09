from pydantic import BaseModel

## write your serializers

class TwitSerializers(BaseModel):
    title:str
    description:str  
    user_id:int