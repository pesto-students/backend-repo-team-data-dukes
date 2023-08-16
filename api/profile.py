from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from functions.auth import auth
from models.Users import Users
from schemas.profile import ProfileRequest
from functions.common import remove_unused_keys

from db.engine import SessionLocal

db = SessionLocal()

def update(profileData:ProfileRequest, data:dict = Depends(auth)):
    print(data)
    email_id, mobile_no = (data["email_id"],None) if data["key"] == "email_id" else (None,data["mobile_no"])
    err, exist, user = Users.exist(db, email_id=email_id, mobile_no= mobile_no)
    if not err:
        if exist:
            filtered_update_data = remove_unused_keys(jsonable_encoder(profileData))
            err, success = Users.update_profile(db, user.id, data=filtered_update_data)
            print(success)
            if not err:
                if success :
                    return { "message" : "OK" }
            raise HTTPException(503, detail="Service Unavailable")
        raise HTTPException(404, detail= f'User Not Found')
    raise HTTPException(503, detail="Service Unavailable")
