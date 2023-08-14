import os
from client import ZerionClient
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
polygon_rpc = "https://rpc.ankr.com/polygon"
private_key = os.environ.get("MAIN_WALLET_PRIVATE_KEY")


def main():
    client = ZerionClient(rpc=polygon_rpc, private_key=private_key)
    swap_hash = client.swap_matic_usdc(0.01)
    client.verify_tx(swap_hash)


if __name__ == "__main__":
    main()
