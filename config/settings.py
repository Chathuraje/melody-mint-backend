from functools import lru_cache
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import configparser

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = os.getenv("APP_NAME", "")
    FRONTEND_APP_DOMAIN: str = os.getenv("FRONTEND_APP_DOMAIN", "")
    FRONTEND_APP_URI: str = os.getenv("FRONTEND_APP_URI", "")
    APP_ORGINS_LIST: list[str] = [
        urls.strip() for urls in os.getenv("APP_ORGINS", "").split(",")
    ]

    APP_SECRET_KEY: str = os.getenv("APP_SECRET_KEY", "")

    # Blcochain settings
    SUPPORTED_BLOCKCHAINS_LIST: list[str] = [
        blockchains.strip() for blockchains in os.getenv("APP_ORGINS", "").split(",")
    ]

    # MongoDB settings
    DB_URL: str = os.getenv("DB_URL", "")
    DB_USERNAME: str = os.getenv("DB_USERNAME", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "")
    DB_APP_NAME: str = os.getenv("DB_APP_NAME", "")
    DB_URI: str = (
        f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_URL}/?retryWrites=true&w=majority&appName={DB_APP_NAME}"
    )

    # JWT settings
    JWT_SECRET_ACCESS: str = os.getenv("JWT_SECRET_ACCESS", "")
    JWT_EXPIRY_MINUTES_ACCESS: int = int(os.getenv("JWT_EXPIRY_MINUTES_ACCESS", 5))
    JWT_SECRET_REFRESH: str = os.getenv("JWT_SECRET_REFRESH", "")
    JWT_EXPIRY_MINUTES_REFRESH: int = int(os.getenv("JWT_EXPIRY_MINUTES_REFRESH", 3600))
    JWT_REFRESH_COOKIE_NAME: str = os.getenv(
        "JWT_REFRESH_COOKIE_NAME", "mmweb3_ref_token"
    )
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "")

    # Moralis settings
    MORALIS_API_KEY: str = os.getenv("MORALIS_API_KEY", "")

    # Alchemy settings
    ALCHEMY_SECRET_KEY: str = os.getenv("ALCHEMY_SECRET_KEY", "")

    # Pinata settings
    PINATA_API_KEY: str = os.getenv("PINATA_API_KEY", "")
    PINATA_SECRET_KEY: str = os.getenv("PINATA_SECRET_KEY", "")
    PINATA_JWT_TOKEN: str = os.getenv("PINATA_JWT_TOKEN", "")
    PINATA_URI: str = os.getenv("PINATA_URI", "")
    PINATA_IPFS_URI: str = os.getenv("PINATA_IPFS_URI", "")

    # Melody Mint Contract Details
    MELODY_MINT_CONTRACT_ADDRESS: str = os.getenv("MELODY_MINT_CONTRACT_ADDRESS", "")


@lru_cache()  # Cache the settings to avoid reading the .env file multiple times
def get_settings() -> Settings:
    return Settings()
