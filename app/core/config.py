from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Project"
    
    # Database
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "fastapi_db"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: str = "5432"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # Webhook
    WEBHOOK_SECRET: str = "default_secret_please_change"

    # OpenAI
    OPENAI_API_KEY: str = ""

    @property
    def DATABASE_URL(self) -> str:
        # We are using asyncpg for asynchronous database access
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
