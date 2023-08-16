from pydantic import BaseSettings

env_file = ".env"

class JwtSettings(BaseSettings):

    JWT_SECRET: str = None
    JWT_EXPIRE: int = 3600
    JWT_ISSUER: str 

    class Config:
        env_file = env_file