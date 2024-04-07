import os
from dotenv import load_dotenv

load_dotenv()

DB_URL: str = os.getenv("DB_URL")  # type: ignore
DB_USERNAME: str = os.getenv("DB_USERNAME")  # type: ignore
DB_PASSWORD: str = os.getenv("DB_PASSWORD")  # type: ignore
DB_NAME: str = os.getenv("DB_NAME")  # type: ignore

JWT_SECRET: str = os.getenv("JWT_SECRET")  # type: ignore
JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")  # type: ignore
JWT_EXPIRY_MINUTES: int = int(os.getenv("JWT_EXPIRY_MINUTES"))  # type: ignore

MORALIS_API_KEY: str = os.getenv("MORALIS_API_KEY")  # type: ignore
