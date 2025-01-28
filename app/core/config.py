import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

class MailConfig(BaseModel):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False

class Settings:
    APP_NAME = "Product Price Board"
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    DATABASE_URL_DEV = "sqlite:///./dev3.db"
    DATABASE_URL_PROD = os.getenv("DATABASE_URL_PROD")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = os.getenv("DEBUG")
    if DEBUG:
        BASE_URL = "localhost"

    BASE_URL = os.getenv("BASE_URL")

    @property
    def DATABASE_URL(self):
        if self.ENVIRONMENT == "production":
            return self.DATABASE_URL_PROD
        return self.DATABASE_URL_DEV

    # Add mail_config
    @property
    def mail_config(self) -> MailConfig:
        return MailConfig(
            MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
            MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
            MAIL_FROM=os.getenv("MAIL_FROM"),
            MAIL_SERVER=os.getenv("MAIL_SERVER"),
            MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
            MAIL_TLS=bool(os.getenv("MAIL_TLS", True)),
            MAIL_SSL=bool(os.getenv("MAIL_SSL", False)),
        )

settings = Settings()

# Accessing the database URL
DATABASE_URL = settings.DATABASE_URL
