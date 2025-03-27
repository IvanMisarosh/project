import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
# load_dotenv()

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

class Settings:
    if os.getenv("WEBSITE_HOSTNAME"):
        DATABASE_URL: str = os.getenv("AZURE_POSTGRESQL_CONNECTIONSTRING")
        if not DATABASE_URL:
            logger.error("Missing environment variable: AZURE_POSTGRESQL_CONNECTIONSTRING")
    else:
        logger.info("Connecting to local PostgreSQL server based on .env file...")
        load_dotenv()
        DATABASE_URL: str = os.getenv("DATABASE_URL")
        DEBUG: bool = os.getenv("DEBUG", "False").lower() in ["true", "1"]

settings = Settings()
