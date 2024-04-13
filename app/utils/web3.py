from eth_account import Account
from eth_account.messages import encode_defunct
from app.config.web3 import connect_web3
from app.utils import logging

logger = logging.getLogger()


async def web3_check_is_valid_address(wallet_address: str, chain_id: int) -> bool:
    try:
        web3 = await connect_web3(chain_id)
        return web3.is_address(wallet_address)

    except Exception as e:
        logger.error("An error occurred: %s", e)
        raise e


def web3_is_valid_signature_format(signature: str) -> bool:
    if not signature.startswith("0x") or len(signature) != 132:
        return False

    try:
        int(signature[2:], 16)
    except ValueError:
        return False

    return True


async def web3_verify_signature(
    message: str, signature: str, wallet_address: str, chain_id: int
) -> bool:

    signable_message = encode_defunct(text=message)

    recovered_address = Account.recover_message(
        signable_message=signable_message, signature=signature
    )

    valid = await web3_check_is_valid_address(
        wallet_address, chain_id
    ) and web3_is_valid_signature_format(signature)

    return recovered_address.lower() == wallet_address.lower() and valid
