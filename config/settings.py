from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    GOOGLE_API_KEY: str
    TAVILY_API_KEY: str

    MODEL: str = "gemini-2.5-flash"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()