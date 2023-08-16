from pydantic import BaseSettings

env_file = ".env"

class CloudFrontSettings(BaseSettings):

    CLOUDFRONT_URL:str = None

    class Config:
        env_file = env_file