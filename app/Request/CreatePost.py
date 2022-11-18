from pydantic import  BaseModel

class UserPost(BaseModel):
    title:str
    content: str 
    published: bool = True 
