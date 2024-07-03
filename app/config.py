from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    username: str # Example: tonaquint\username
    password: str
    smtp_server: str
    smtp_port: int 
    smtp_user: str # Email address
    smtp_password: str
    sgu_zerto_base_url: str
    boi_zerto_base_url: str
    fb_zerto_base_url: str
    class Config:
        env_file = '.env'
settings = Settings()