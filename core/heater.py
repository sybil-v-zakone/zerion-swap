import random
from config import (
    polygon_rpc,
    sleep_time,
    matic_deviation,
    usdc_deviation,
    usdt_deviation
)

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

    def warmup(self):
        tokens_available = [USDC_TOKEN, USDT_TOKEN]

        while len(self.data) > 0:
            active_wallet = random.choice(list(self.data))
            matic_multiplier = random.uniform(*matic_deviation)
            to_token = random.choice(tokens_available)
            to_token_multiplier = random.uniform(*usdc_deviation) if to_token.signature == "USDC" else random.uniform(*usdt_deviation)

            client = ZerionClient(rpc=polygon_rpc, private_key=active_wallet)

            logger.debug(f"Wallet: {client.public_key}")

            try:
                tx_res, tx_message = client.swap(from_token=MATIC_TOKEN, to_token=to_token, deviation=matic_multiplier)
                if tx_res:
                    logger.success(tx_message)
                    self.data[active_wallet] -= 1

                    sleep(sleep_time)

                    tx_res, tx_message = client.swap(from_token=to_token, to_token=MATIC_TOKEN,
                                                     deviation=to_token_multiplier)

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
