import json
from pathlib import Path
import uuid
from fastapi import UploadFile
import requests
from app.api.v1.model.Campaign import CampaignOffChain
from app.utils import logging
from config import settings

logger = logging.getLogger()
env = settings.get_settings()


async def pinFiletoIPFS(file: UploadFile) -> str:
    url = f"{env.PINATA_URI}/pinning/pinFileToIPFS"
    headers = {"Authorization": f"Bearer {env.PINATA_JWT_TOKEN}"}

    file_name = f"{uuid.uuid4()}{Path(file.filename).suffix}" if file.filename else ""

    files = {
        "file": file.file,
        "pinataMetadata": (None, '{"name": "' + file_name + '"}'),
        "pinataOptions": (None, '{"cidVersion": 1}'),
    }

    response = requests.post(url, headers=headers, files=files)
    if response.status_code != 200:
        raise Exception("Failed to pin file to IPFS")

    return response.json()["IpfsHash"]


async def pinFiletoJSON(data: dict) -> str:
    url = f"{env.PINATA_URI}/pinning/pinJSONToIPFS"
    headers = {
        "Authorization": f"Bearer {env.PINATA_JWT_TOKEN}",
        "Content-Type": "application/json",
    }

    file_name = f"{uuid.uuid4()}.json"
    payload = {
        "pinataContent": data,
        "pinataMetadata": {"name": file_name},
        "pinataOptions": {"cidVersion": 1},
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception("Failed to pin json to IPFS")

    return response.json()["IpfsHash"]


async def readFromIPFS(ipfs_hash: str) -> dict:
    url = f"{env.PINATA_IPFS_URI}/{ipfs_hash}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to read from IPFS")

    return response.json()
