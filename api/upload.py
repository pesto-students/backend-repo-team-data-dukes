import uuid
from fastapi import Depends, HTTPException

from schemas.upload import UploadRequest
from functions.helpers import get_extension, get_file_type
from functions.s3 import S3
from functions.auth import auth
from models.Files import Files
from models.helpers import file_profiler

from db.engine import SessionLocal
db = SessionLocal()
s3 = S3()

def upload(request: UploadRequest = Depends(UploadRequest.as_form),data:dict = Depends(auth)):
    
    ext,content_type = get_extension(request.file.filename)
    type = get_file_type(ext)
    id = uuid.uuid4()

    err, url, uploaded_at = s3.upload(request.file.file,file_name=f'{id}.{ext}',content_type=content_type,username=data["username"])
    if err:
        raise HTTPException(503, detail='Service Unavailable')
    
    err, file = Files.create(db, id=id ,from_=data[data["key"]], to_= request.to_, domain= data["domain"], type=type, url=url, message_id= request.message_id, ext=ext, uploaded_at=uploaded_at)
    if err:
        raise HTTPException(503, detail='Service Unavailable')

    return file_profiler([file])[0]



    
