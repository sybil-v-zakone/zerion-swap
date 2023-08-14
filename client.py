import time

from eth_typing import HexStr
from web3 import Web3
from eth_abi import encode
from constants import *


class ZerionClient:
    def __init__(self, rpc: str, private_key: str):
        self.w3 = Web3(Web3.HTTPProvider(rpc))
        self.private_key = private_key
        self.public_key = Web3.to_checksum_address(self.w3.eth.account.from_key(private_key=private_key).address)
        self.zerion = self.w3.eth.contract(
            abi=ZERION_ROUTER_ABI,
            address=ZERION_ROUTER_ADDRESS
        )
        self.uniswap = self.w3.eth.contract(
            abi=UNISWAP_ABI,
            address=UNISWAP_CONTRACT_ADDRESS
        )

    def swap_matic_usdc(self, value: float):
        value = int(Web3.to_wei(value, 'ether'))

        call_data = self.get_call_data(value)

        data = self.zerion.encodeABI('execute', args=(
            (
                (  # input.tokenAmount
                    ETH_CONTRACT_ADDRESS,
                    value,
                    2
                ),
                (  # input.permit
                    0,
                    '0x'
                )
            ),
            (
                USDC_CONTRACT_ADDRESS,  # output.token
                0  # output.absoluteAmount
            ),
            (
                1,  # swapDescription.swapType
                (  # swapDescription.protocolFee
                    5000000000000000,
                    "0x4a183b7ED67B9E14b3f45Abfb2Cf44ed22c29E54"
                ),
                (  # swapDescription.marketplaceFee
                    0,
                    "0x0000000000000000000000000000000000000000"
                ),
                self.public_key,  # swapDescription.account
                CALLER_CONTRACT_ADDRESS,  # swapDescription.caller
                call_data
            ),
            (
                0,  # accountSignature.salt
                '0x'  # accountSignature.signature
            ),
            (
                0,  # protocolFeeSignature.deadline
                '0x'  # protocolFeeSignature.signature
            )
        ))

        txn = {
            'chainId': self.w3.eth.chain_id,
            'from': self.public_key,
            'to': ZERION_ROUTER_ADDRESS,
            'value': value,
            'nonce': self.w3.eth.get_transaction_count(self.public_key),
            'gasPrice': self.w3.eth.gas_price,
            'data': data
        }

        try:
            txn['gas'] = int(self.w3.eth.estimate_gas(txn) * 1.05)
        except Exception as ex:
            print(f"Gas error: {ex}")

        sign = self.w3.eth.account.sign_transaction(txn, self.private_key)
        return self.w3.eth.send_raw_transaction(sign.rawTransaction)

    def verify_tx(self, tx_hash) -> bool:
        try:
            data = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=200)
            if "status" in data and data["status"] == 1:
                print(f"Successful swap: https://polygonscan.com/tx/{tx_hash.hex()}")
                return True
            else:
                print(f'Swap failed: {data["transactionHash"].hex()}')
                return False
        except Exception as e:
            print(f"Unexpected error in verify_tx function: {e}")
            return False

    def get_call_data(self, value: int):
        call_data = self.call_uniswap(value)

        return encode(['address', 'address', 'address', 'bytes', 'address'],
                      [ETH_CONTRACT_ADDRESS,
                       UNISWAP_CONTRACT_ADDRESS,
                       UNISWAP_CONTRACT_ADDRESS,
                       bytes.fromhex(call_data[2:]),
                       USDC_CONTRACT_ADDRESS])

    def call_uniswap(self, value: int) -> HexStr:
        call_data = self.uniswap.encodeABI('exactInputSingle', args=[
            (
                WMATIC_CONTRACT_ADDRESS,
                USDC_CONTRACT_ADDRESS,
                500,
                ZERION_ROUTER_ADDRESS,
                int(time.time()) + 30 * 60,
                value,
                0,
                0
            )
        ]
                                           )
        return call_data
