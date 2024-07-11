from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    username: str # Example: username@tonaquint.local
    password: str
    smtp_server: str
    smtp_port: int 
    smtp_user: str # Email address
    smtp_password: str
    sgu_zerto_base_url: str
    boi_zerto_base_url: str
    fb_zerto_base_url: str
    sgu_ip: str
    boi_ip: str
    fb_ip: str
    class Config:
        env_file = '../.env'
settings = Settings()