from fastapi.exceptions import HTTPException
from schemas.login import LoginRequest
from models.Users import Users

from functions.hash import verified
from functions.jwt import generate

from db.engine import SessionLocal
db = SessionLocal()

def login(request: LoginRequest):
    key = "email_id" if request.email_id else "mobile_no"
    err, exist, user = Users.exist(db, email_id=request.email_id, mobile_no=request.mobile_no)
    if not err:
        if exist:
            if verified(request.password, user.password):
                payload = { "id" : user.id, "username" : user.username, "domain" : request.domain, "jid" : user.jid }
                payload[key] = user.__getattribute__(key)
                payload["key"] = key
                token = generate(payload)
                return { "jid" : user.jid ,
                        "token": token,  
                        "email_id" : user.email_id,
                        "mobile_no" : user.mobile_no,
                        "created_at" : user.created_at,
                        "domain" : request.domain,
                        "username" : user.username,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "avatar_url": user.avatar_url }
            else:
                raise HTTPException(401, detail= f'Unauthorized')    
        raise HTTPException(404, detail= f'User Not Found')
    raise HTTPException(503, detail="Service Unavailable")