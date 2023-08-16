import json
from fastapi.responses import PlainTextResponse
from fastapi import Request
from functions.jwt import verify

async def oauth(request:Request):
    d = await request.body()
    d = json.loads(d.decode("utf-8").replace("'",'"'))
    
    username = d["username"]
    token = d["password"]
    valid, data = verify(token=token)

    if valid:
        if username == data["jid"]:
            return PlainTextResponse("true",status_code=200)
    return PlainTextResponse("false",status_code=401)