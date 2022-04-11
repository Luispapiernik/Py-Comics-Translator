from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    TESSERACT_PATH: str = Field(..., env="Path to the tesseract folder")


settings = Settings()
