from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    google_auth: bool = False

class UserCreate(UserBase):
    password: str = None

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True
