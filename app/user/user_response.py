from pydantic import BaseModel


class UserResponse(BaseModel):
    uuid:str
    username:str