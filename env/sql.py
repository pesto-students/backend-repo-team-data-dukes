from pydantic import BaseSettings

env_file = ".env"

class SQLSettings(BaseSettings):

    SQL_USER: str = None
    SQL_PASS: str = None
    SQL_HOST: str = 'localhost'
    SQL_PORT: str = 3306
    SQL_DB: str = 'prosody'

    class Config:
        env_file = env_file