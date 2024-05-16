from web3 import Web3, AsyncWeb3
from config.file_handle import load_support_blocchain_data
from config.settings import get_settings
from app.utils import logging
import json

logger = logging.getLogger()
env = get_settings()


async def connect_web3(chain_id: int) -> Web3:

    try:
        data = load_support_blocchain_data()
        rpc_url = data[str(chain_id)].get("rpc_url")

        web3 = Web3(AsyncWeb3.HTTPProvider(f"{rpc_url}/{env.ALCHEMY_SECRET_KEY}"))

        if web3.is_connected():
            logger.info("Connected to the blockchain.")
            return web3
        else:
            logger.error("Failed to connect to the blockchain.")
            raise Exception("Failed to connect to the blockchain.")

    except Exception as e:
        logger.error("An error occurred: %s", e)
        raise e


async def web3_get_contract(chain_id: int):
    with open("config/abi.json", "r") as f:
        abi = json.load(f)

    try:
        web3 = await connect_web3(chain_id)
        contract_address = web3.to_checksum_address(env.MELODY_MINT_CONTRACT_ADDRESS)
        contract = web3.eth.contract(address=contract_address, abi=abi)
        return contract

    except Exception as e:
        logger.error("An error occurred: %s", e)
        raise e
