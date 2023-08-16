from pydantic import BaseModel, validator
from datetime import datetime

class GetFilesRequest(BaseModel):
    
    to_: str 
    start_date: datetime = None
    end_date: datetime = None

    
    