from fastapi import Depends, HTTPException

from schemas.password import PasswordRequest
from functions.auth import auth
from functions.hash import verified
from models.Users import Users

from db.engine import SessionLocal
db = SessionLocal()

def reset_password(request: PasswordRequest, data:dict = Depends(auth)):
    email_id, mobile_no = (data["email_id"],None) if data["key"] == "email_id" else (None,data["mobile_no"])
    err, exist, user = Users.exist(db, email_id=email_id, mobile_no= mobile_no)
    if not err:
        if exist:
            if verified(request.old_password, user.password):
                err, success = Users.update(db, user.id, password = request.new_password)
                if not err:
                    if success :
                        return { "message" : "OK" }
                raise HTTPException(503, detail="Service Unavailable")
            raise HTTPException(403, detail="Incorrect Password")
        raise HTTPException(404, detail= f'User Not Found')
    raise HTTPException(503, detail="Service Unavailable")