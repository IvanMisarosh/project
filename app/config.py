import os
import logging
from dotenv import load_dotenv

load_dotenv()  # Завантажує .env лише локально

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

class Settings:
    def __init__(self):
        # Загальні налаштування
        self.DEBUG = os.getenv("DEBUG", "False").lower() in ["true", "1"]
        self.IS_AZURE = bool(os.getenv("WEBSITE_HOSTNAME"))

        if self.IS_AZURE:
            logger.info("Running in Azure environment.")

            # PostgreSQL
            self.DATABASE_URL = (
                f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
                f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
                f"?sslmode={os.getenv('DB_SSLMODE', 'require')}"
            )

            self.MONGODB_URL = os.getenv("MONGODB_URL", "")
            self.MONGODB_NAME = os.getenv("MONGODB_NAME", "")
            self.MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "")

            # Azure Blob Storage
            self.STORAGE_BACKEND = "azure"
            self.AZURE_STORAGE_CONN_STR = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
            self.AZURE_STORAGE_CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
            self.AZURE_STORAGE_SAS_TOKEN = os.getenv("AZURE_STORAGE_SAS_TOKEN")

            if not self.AZURE_STORAGE_CONN_STR:
                logger.warning("AZURE_STORAGE_CONNECTION_STRING not set!")

        else:
            logger.info("Running in local environment.")

            # PostgreSQL
            self.DATABASE_URL = os.getenv("DATABASE_URL")

            # MongoDB
            self.MONGODB_URL = os.getenv("MONGODB_URL")
            self.MONGODB_NAME = os.getenv("MONGODB_NAME")
            self.MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION")

            # Локальне зберігання файлів
            self.STORAGE_BACKEND = "local"
            self.UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
            os.makedirs(self.UPLOAD_DIR, exist_ok=True) 

settings = Settings()
