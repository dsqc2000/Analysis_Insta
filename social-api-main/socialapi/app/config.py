from pydantic import BaseSettings



class Settings(BaseSettings):
    DATABASE_URL: str
    MONGO_INITDB_DATABASE: str
    SELENIUM_COOKIE_PATH:str
    # TODO: figure out what these variables are for 
    # CMS_API_URL: str
    # LOGIN: str
    # PASSWORD: str
    # CLIENT_APP_ID: str
    # PRIVATE_LABEL: str
    # CLIENT_VERSION: str

    class Config:
        env_file = './.env'


settings = Settings()