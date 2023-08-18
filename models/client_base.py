from web3 import Web3
from web3.contract import Contract

from models.token import Token
from loguru import logger
from utils.constants import POLYGON_MATIC_TOKEN
from utils.utils import sleep

class ClientBase:
    def __init__(self, rpc: str, private_key: str):
        self.w3 = Web3(Web3.HTTPProvider(rpc))
        self.private_key = private_key
        self.public_key = Web3.to_checksum_address(self.w3.eth.account.from_key(private_key=private_key).address)

    def send_tx(
        self,
        to_adr: str,
        from_adr: str = None,
        data=None,
        gas_multiplier=1.05,
        value=None
    ):
        if not from_adr:
            from_adr = self.public_key

        txn = {
            "chainId": self.w3.eth.chain_id,
            "nonce": self.w3.eth.get_transaction_count(self.public_key),
            "from": Web3.to_checksum_address(from_adr),
            "to": Web3.to_checksum_address(to_adr),
            "gasPrice": self.w3.eth.gas_price
        }

        if data:
            txn["data"] = data

        if value:
            txn["value"] = value

        try:
            txn["gas"] = int(self.w3.eth.estimate_gas(txn) * gas_multiplier)
        except Exception as e:
            logger.error(f"Transaction failed: {e}")
            return None

        sign = self.w3.eth.account.sign_transaction(txn, self.private_key)
        return self.w3.eth.send_raw_transaction(sign.rawTransaction)

    def verify_tx(self, tx_hash) -> bool:
        try:
            data = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=200)
            if "status" in data and data["status"] == 1:
                return True
            else:
                logger.error(f'Transaction failed: {data["transactionHash"].hex()}')
                return False
        except Exception as e:
            logger.error(f"Unexpected error in verify_tx function: {e}")
            return False

    def get_allowance(self, token_contract: Contract, spender: str, owner: str = None):
        if not owner:
            owner = self.public_key

        return token_contract.functions.allowance(owner, spender).call()

    def balance_of(self, token: Token):
        if token.signature == "MATIC":
            token = POLYGON_MATIC_TOKEN

        return int(self.w3.eth.contract(
            address=token.contract_address,
            abi=token.abi
        ).functions.balanceOf(self.public_key).call())

    def approve(self, spender: str, token: Token, value: int):
        if token.is_native:
            return True

        contract = self.w3.eth.contract(address=token.contract_address, abi=token.abi)

        allowance = self.get_allowance(token_contract=contract, spender=spender)
        if allowance >= value:
            logger.info(f"Allowance is greater than approve value. {allowance} >= {value}")
            return True

        data = contract.encodeABI("approve", args=(spender, value))
        tx_hash = self.send_tx(contract.address, data=data)
        if self.verify_tx(tx_hash=tx_hash):
            logger.success(f"Successful approve: {allowance} {token.signature}")
            sleep([10, 15])
            return True
        logger.warning("Error while approving transaction")
        return False
