import random
from config import (polygon_rpc, sleep_time)
from core.client import ZerionClient
from loguru import logger

from utils.utils import (generate_pairs, sleep)
from utils.constants import (
    MATIC_TOKEN,
    USDT_TOKEN,
    USDC_TOKEN
)

# типа warmup == прогрев => нагреватель == heater xddddd
class Heater:
    def __init__(self):
        self.data = generate_pairs()
        #self.clients = [ZerionClient(rpc=polygon_rpc, private_key=key) for key in self.data.keys()]

    def warmup(self):
        tokens_available = [MATIC_TOKEN, USDC_TOKEN, USDT_TOKEN]

        while len(self.data) > 0:
            active_wallet = random.choice(list(self.data))
            client = ZerionClient(rpc=polygon_rpc, private_key=active_wallet)

            logger.debug(f"Wallet: {client.public_key}")

            try:
                from_token, to_token = client.determine_balances(tokens_available)
            except StopIteration as ex:
                logger.error(f"Error while determining tokens to swap from/to: {ex}")
                continue

            try:
                tx_res, tx_message = client.swap(from_token, to_token)
                if tx_res:
                    logger.success(tx_message)
                    self.data[active_wallet] -= 1

                    if self.data[active_wallet] == 0:
                        self.data.pop(active_wallet)

                    sleep(sleep_time)
                else:
                    logger.error(tx_message)

            except Exception as ex:
                logger.error(ex)

        logger.success("Script has ended its work. Wallets are now on fire.")
