from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ALPHAVANTAGE_APIKEY: str
    ALPHAVANTAGE_URL: str = "https://www.alphavantage.co/"

    class Config:
        env_file = "../.env"  # Specifies the path to the .env file
        env_file_encoding = "utf-8"


# Create a global instance of Settings to be used throughout the app
settings = Settings()