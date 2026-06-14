from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name : str = "VentaEntradas"
    debug_mode : bool = False
    database_url : str 
    secret_key : str
    algorithm : str = "HS256"
    access_token_expire_minutes : int = 30
    stripe_secret_key : str

    class Config:
        env_file = ".env"

settings = Settings()        