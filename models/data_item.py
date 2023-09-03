from web3 import Web3


class DataItem:
    def __init__(
            self,
            private_key: str,
            to_matic_swaps: int,
            to_stables_swaps: int
    ):
        self.private_key = private_key
        self.address = Web3.to_checksum_address(Web3().eth.account.from_key(private_key=private_key).address)
        self.to_matic_swaps = to_matic_swaps
        self.to_stables_swaps = to_stables_swaps
