from fastapi import Depends, HTTPException
from schemas.files import GetFilesRequest
from models.Files import Files
from functions.auth import auth

from db.engine import SessionLocal
db = SessionLocal()

def getFiles(request: GetFilesRequest = Depends(GetFilesRequest),data:dict = Depends(auth)):
    err, files = Files.get_files(db, from_=data["jid"], to_=request.to_, start_date=request.start_date, end_date=request.end_date)
    if not err:
        return files 
    raise HTTPException(503, detail="Service Unavailable")
    