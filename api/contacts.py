from fastapi import Depends, HTTPException

from functions.auth import auth
from models.Users import Users

from db.engine import SessionLocal
db = SessionLocal()

def contacts(data:dict = Depends(auth)):
    err, status = Users.get_all_users(db, domain= data["domain"], jid = data["jid"])
    if not err:
        return status 
    raise HTTPException(503, detail=status)

