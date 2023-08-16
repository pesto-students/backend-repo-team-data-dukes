from pydantic import BaseModel, validator
from functions.hash import hash_password

class PasswordRequest(BaseModel):
    
    old_password: str 
    new_password: str

    @validator('new_password')
    def hash_password(cls, v):
        return hash_password(v)
    