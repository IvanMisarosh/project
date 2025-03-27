import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
# load_dotenv()

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

class Settings:
    if os.getenv("WEBSITE_HOSTNAME"):
        # Azure PostgreSQL Flexible server connection string but it's in incorrect format
        # DATABASE_URL: str = os.getenv("AZURE_POSTGRESQL_CONNECTIONSTRING")
        DATABASE_URL: str = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}?sslmode={os.getenv('DB_SSLMODE')}"
        if not DATABASE_URL:
            logger.error("Missing environment variable: AZURE_POSTGRESQL_CONNECTIONSTRING")
    else:
        logger.info("Connecting to local PostgreSQL server based on .env file...")
        load_dotenv()
        DATABASE_URL: str = os.getenv("DATABASE_URL")
        DEBUG: bool = os.getenv("DEBUG", "False").lower() in ["true", "1"]

settings = Settings()
