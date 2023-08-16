from fastapi import File,UploadFile
from pydantic import BaseModel
from .helpers import as_form

@as_form
class UploadRequest(BaseModel):
    to_: str 
    message_id: str
    file: UploadFile = File(...) 

    