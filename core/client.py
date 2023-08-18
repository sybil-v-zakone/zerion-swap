import time

from eth_typing import HexStr
from web3 import Web3
from eth_abi import encode

from utils.constants import *
from models.client_base import ClientBase


class ZerionClient(ClientBase):
    def __init__(self, rpc: str, private_key: str):
        super().__init__(rpc, private_key)

        self.zerion = self.w3.eth.contract(
            abi=ZERION_ROUTER_ABI,
            address=ZERION_ROUTER_ADDRESS
        )
        self.uniswap = self.w3.eth.contract(
            abi=UNISWAP_ABI,
            address=UNISWAP_CONTRACT_ADDRESS
        )

    def swap(self, from_token: Token, to_token: Token, amount=None, deviation: float = 1.0) -> tuple[bool, str]:
        if not amount:
            amount = int(self.balance_of(from_token) * deviation)
        else:
            amount = from_token.to_wei(amount)

        innative_amount = amount

        is_approved = self.approve(ZERION_ROUTER_ADDRESS, from_token, amount)
        if not is_approved:
            return False, f"Failed to approve transaction"
        time.sleep(5)

        caller_call_data = self.get_call_data(amount, from_token=from_token, to_token=to_token)
        # TODO: absoluteAmount

        data = self.zerion.encodeABI('execute', args=(
            ((from_token.contract_address, amount, 2), (0, '0x')),
            (to_token.contract_address, 0),
            (
                PARAM_SWAP_TYPE,
                (PARAM_FEE_SHARE_PF, ZERION_MULTISIG_ADDRESS),
                (PARAM_FEE_SHARE_MF, NULL_ADDRESS),
                self.public_key,
                CALLER_CONTRACT_ADDRESS,
                caller_call_data
            ),
            PARAM_ACC_SIGNATURE,
            PARAM_FEE_SIGNATURE
        ))

        if not from_token.is_native:
            amount = None

        tx = self.send_tx(to_adr=ZERION_ROUTER_ADDRESS, data=data, value=amount)
        if self.verify_tx(tx):
            return (True, (f"Successful swap: {from_token.from_wei(innative_amount)} {from_token.signature} -> {to_token.signature}. "
                    f"Hash: https://polygonscan.com/tx/{tx.hex()}"))
        return False, f"Failed swap: {from_token.from_wei(innative_amount)} {from_token.signature} -> {to_token.signature}. "

    def get_call_data(self, value: int, from_token: Token, to_token: Token):
        call_data = self.call_uniswap(value, from_token=from_token, to_token=to_token) \
            if from_token.is_native \
            else self.multicall_uniswap(value, from_token=from_token, to_token=to_token)

        return encode(['address', 'address', 'address', 'bytes', 'address'],
                      [from_token.contract_address,
                       UNISWAP_CONTRACT_ADDRESS,
                       UNISWAP_CONTRACT_ADDRESS,
                       Web3.to_bytes(hexstr=call_data),
                       to_token.contract_address])

    def multicall_uniswap(self, value: int, from_token: Token, to_token: Token) -> HexStr:
        if to_token.signature == "MATIC":
            to_token = WMATIC_TOKEN

        first_param = self.call_uniswap(value, from_token=from_token, to_token=to_token)
        second_param = self.unwrap_weth9()
        call_data = self.uniswap.encodeABI('multicall', args=[
            [
                Web3.to_bytes(hexstr=first_param),
                Web3.to_bytes(hexstr=second_param)
            ]
        ])
        return call_data

    def unwrap_weth9(self) -> HexStr:
        hex_str = self.uniswap.encodeABI('unwrapWETH9', args=(
            PARAM_AMOUNT_MINIMUM,
            ZERION_ROUTER_ADDRESS
        ))
        return hex_str

    def call_uniswap(self, value: int, from_token: Token, to_token: Token) -> HexStr:
        recipient = ZERION_ROUTER_ADDRESS if from_token.is_native else NULL_ADDRESS
        if from_token.signature == "MATIC":
            from_token = WMATIC_TOKEN
        call_data = self.uniswap.encodeABI('exactInputSingle', args=[
            (
                from_token.contract_address,
                to_token.contract_address,
                PARAM_SWAP_FEE,
                recipient,
                int(time.time()) + THIRTY_MINUTES,
                value,
                0,
                0
            )
        ])
        return call_data
