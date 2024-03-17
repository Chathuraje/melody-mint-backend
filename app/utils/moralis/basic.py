import json
from moralis import evm_api
from app.utils.logging import get_logger
from app.utils import config

logger = get_logger()

def get_wallet_amount(wallet_address: str):
    params = {
        "exclude_spam": True,
        "exclude_unverified_contracts": True,
        "address": "0xc3d3E220EcA81BBb0593191C30b160c99bd32D96",
        "chain": "sepolia"
        }

    result = evm_api.wallets.get_wallet_net_worth(
        api_key=config.MORALIS_API_KEY,
        params=params,
    )

    print(json.dumps(result, indent=4))