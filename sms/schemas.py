from pydantic import BaseModel
from typing import Optional

class Staff(BaseModel):
    # request
    firstname : str
    lastname : str
    email : str
    password: str
    class Config():
        orm_mode = True

class User(BaseModel):
    # response
    firstname: str
    lastname: str 
    class Config():
        orm_mode = True


class updateUser(BaseModel):
    id: int
    lastname: str

class user_login(BaseModel):
    # check user login
    firstname: str
    password: str 
    class Config():
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    token_schemas: Optional[str] = None
