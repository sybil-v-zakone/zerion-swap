class Token:
    def __init__(
            self,
            contract_address: str,
            abi: list | None,
            signature: str,
            decimals: int,
            is_native: bool
    ):
        self.contract_address = contract_address
        self.abi = abi
        self.signature = signature
        self.decimals = decimals
        self.is_native = is_native

    def to_wei(self, value: float) -> int:
        return int(value * 10 ** self.decimals)

    def from_wei(self, value: float) -> int:
        return value / 10 ** self.decimals
