import json
import os
from app.utils import logging
from pathlib import Path

logger = logging.getLogger()


def load_support_blocchain_data() -> dict:
    file_path = Path("app/data/blockchain_data.json")

    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
            return data
        else:
            raise FileNotFoundError("Blockchain configuration file not found.")

    except Exception as e:
        logger.error("An error occurred: %s", e)
        raise e
