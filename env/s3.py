from pydantic import BaseSettings

env_file = ".env"

class S3Settings(BaseSettings):

    S3_BUCKET: str = None
    S3_REGION: str = None
    S3_AWS_ACCESS_KEY: str = None
    S3_AWS_SECRET_KEY: str = None
    S3_REPO: str = None

    class Config:
        env_file = env_file