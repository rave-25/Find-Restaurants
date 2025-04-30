from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()


class Settings(BaseSettings):
    GOOGLE_KEY: str
    FOURSQUARE_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

Config = Settings()