from fastapi import HTTPException, Header
from functions.jwt import verify

def auth(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(401,detail=f'Unauthorized')
    token = authorization.split(" ")[1]
    valid, data = verify(token)
    if not valid:
        raise HTTPException(401,detail=f'Invalid Token')
    return data