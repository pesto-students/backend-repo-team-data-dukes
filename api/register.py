from fastapi.exceptions import HTTPException
from schemas.register import RegisterRequest
from models.Users import Users

from db.engine import SessionLocal
db = SessionLocal()

def register(request:RegisterRequest): 
    err, exist, _ = Users.exist(db, email_id=request.email_id, mobile_no=request.mobile_no)
    if not err:
        if exist:
            raise HTTPException(403, detail= f'User Already Exist')
        username = request.email_id.split("@")[0] if request.email_id else request.mobile_no
        jid = request.email_id if request.email_id else f'{request.mobile_no}@{request.domain}'
        err, user = Users.create(db, username=username,
                            domain=request.domain,
                            jid= jid,
                            password=request.password, 
                            email_id=request.email_id, 
                            mobile_no=request.mobile_no)
        if not err:
            if user :
                return { "message" : "OK" }
    raise HTTPException(503, detail= f'Service Unavailable')

