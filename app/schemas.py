from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str | None = None
    
class UsrInDB(BaseModel):
    hashed_password: str
