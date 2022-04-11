from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    TESSERACT_PATH: str = Field(..., env="TESSERACT_PATH")


settings = Settings()
