from web3 import Web3, AsyncWeb3
from app.config.file_handle import load_support_blocchain_data
from app.config.settings import get_settings
from app.utils import logging

logger = logging.getLogger()
env = get_settings()


async def connect_web3(chain_id: int) -> Web3:

    try:
        data = load_support_blocchain_data()
        rpc_url = data[str(chain_id)].get("rpc_url")

        web3 = Web3(AsyncWeb3.HTTPProvider(f"{rpc_url}/{env.INFURA_SECRET_KEY}"))

        return web3

    except Exception as e:
        logger.error("An error occurred: %s", e)
        raise e
