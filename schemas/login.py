from pydantic import BaseModel, validator, root_validator

class LoginRequest(BaseModel):
    
    password: str 
    domain: str
    email_id: str = None
    mobile_no: str = None

    @validator('email_id')
    def validate_email_id(cls, v, values):
        if v:
            if '@' not in v:
                raise ValueError('Invalid email address')
            _ , domain = v.split('@')
            if domain:
                if not domain or domain != values["domain"]:
                    raise ValueError('Invalid email address')
            else:
                raise ValueError('Invalid Request')
            subdomains = domain.split('.')
            if not subdomains[-1]:
                raise ValueError('Invalid email address')
        return v
    
    @root_validator
    def validate_email_or_mobile(cls, values):
        if ( "email_id" or "mobile_no" ) in values and not ( values["email_id"] or values["mobile_no"] ):
            raise ValueError("Invalid Request")
        if values["mobile_no"] and ( len(values["mobile_no"]) != 10 or not values["mobile_no"].isdigit() ):
            raise ValueError("Invalid Mobile Number")
        return values