from pydantic_settings import BaseSettings

class Settings(BaseSettings): 
    database_hostname : str
    database_port_number : str
    database_password : str
    database_super_password : str
    database_username : str
    database_name : str
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int

    class Config: 
        env_file = ".env"
    

settings = Settings()
