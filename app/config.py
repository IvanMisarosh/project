import os
from dotenv import load_dotenv

# Load environment variables from .env file
# load_dotenv()

class Settings:
    if os.getenv("WEBSITE_HOSTNAME"):
        DATABASE_URL: str = os.getenv("AZURE_POSTGRESQL_CONNECTIONSTRING")
        if not DATABASE_URL:
            print("Missing environment variable: AZURE_POSTGRESQL_CONNECTIONSTRING")
    else:
        load_dotenv()
        DATABASE_URL: str = os.getenv("DATABASE_URL")
        DEBUG: bool = os.getenv("DEBUG", "False").lower() in ["true", "1"]

settings = Settings()
