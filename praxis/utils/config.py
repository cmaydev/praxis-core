"""PRAXIS-1 global settings via .env file"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str = ""
    user_role: str = "user"  # can be 'user', 'admin', or 'developer'

    class Config:
        env_file = ".env"

# Global settings object
settings = Settings()
