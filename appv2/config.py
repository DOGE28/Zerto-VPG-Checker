from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    keycloak_client_id: str
    keycloak_client_secret: str
    threshold: int = 90
    smtp_port: int = 25
    smtp_address: str
    smtp_sender: str
    smtp_receiver: str


    class Config:
        env_file = '../.env'
settings = Settings()
