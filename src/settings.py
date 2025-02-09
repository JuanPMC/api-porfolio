from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ALPHAVANTAGE_APIKEY: str
    ALPHAVANTAGE_URL: str = "https://www.alphavantage.co/"
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    ACCESS_TOKEN_URL: str = "https://oauth2.googleapis.com/token"
    AUTHORIZE_URL : str = "https://accounts.google.com/o/oauth2/auth"
    SECRET_KEY : str
    METADATA_URL: str = "https://accounts.google.com/.well-known/openid-configuration"
    SUPABASE_URL: str
    SUPABASE_KEY: str
    model_config = SettingsConfigDict(
        env_file="../.env",  # Specifies the path to the .env file
        env_file_encoding="utf-8"
    )



# Create a global instance of Settings to be used throughout the app
settings = Settings()