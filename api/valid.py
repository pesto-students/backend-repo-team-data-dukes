from fastapi import Depends
from fastapi.exceptions import HTTPException
from schemas.valid import ValidRequest
from models.Users import Users

from db.engine import SessionLocal
db = SessionLocal()

def valid(request:ValidRequest = Depends()): 
    err, exist, _ = Users.exist(db, email_id=request.email_id, mobile_no=request.mobile_no)
    if not err:
        if exist:
            return { "message" : "OK" }
        raise HTTPException(404, detail=f'Users does not exist')
    raise HTTPException(503, detail= f'Service Unavailable')
