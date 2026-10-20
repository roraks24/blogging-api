from pydantic import BaseModel, ConfigDict

class Post(BaseModel):
    author: str
    title: str
    content: str
    date_posted: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str
