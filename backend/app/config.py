from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    database_url: str = "sqlite:///./blog.db"
    admin_username: str = "admin"
    admin_password: str = "changeme123"
    access_token_expire_minutes: int = 60

    class Config:
        env_file = ".env"

settings = Settings()
