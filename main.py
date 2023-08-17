import os
from core.client import ZerionClient
from dotenv import load_dotenv, find_dotenv
from config import polygon_rpc
from core.heater import Heater
from utils.constants import USDT_TOKEN, USDC_TOKEN, MATIC_TOKEN

load_dotenv(find_dotenv())
private_key = os.environ.get("MAIN_WALLET_PRIVATE_KEY")


def main():
    heater = Heater()
    heater.warmup()


if __name__ == "__main__":
    main()
