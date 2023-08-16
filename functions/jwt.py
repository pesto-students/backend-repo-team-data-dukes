import jwt
import time
from datetime import datetime

from env.jwt import JwtSettings

settings = JwtSettings()

def generate(payload, expire_seconds = None):
    current_time = time.time()
    if not expire_seconds :
        expire_time = current_time + settings.JWT_EXPIRE
    else:
        expire_time = current_time + expire_seconds
    issued_time = current_time 

    payload['exp'] = int(expire_time)
    payload["iat"] = int(issued_time)
    payload["iss"] = settings.JWT_ISSUER

    jwt_token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
    return jwt_token

def verify(token):
    try:
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'], issuer=settings.JWT_ISSUER)
        return True, decoded_token    
    except jwt.exceptions.ExpiredSignatureError as e :
        err_msg = f"Expired Token : {e}"
        return False, err_msg
    except jwt.exceptions.InvalidTokenError as e :
        err_msg = f"Invalid Token : {e}"
        return False, err_msg
    except Exception as e:
        err_msg = f"JWT: Error : {e}"
        return False, 