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

from utils.database import Database
from utils.utils import (sleep)
from utils.constants import (
    MATIC_TOKEN,
    USDT_TOKEN,
    USDC_TOKEN
)


class Heater:
    def __init__(self):
        self.db = Database()

    def warmup(self):
        tokens_available = [USDC_TOKEN, USDT_TOKEN]
        clients = {}

        for item in self.db.data:
            client = ZerionClient(rpc=polygon_rpc, private_key=item.private_key)
            clients[item.private_key] = client

        while self.db.accounts_remaining > 0:
            active_wallet = random.choice(self.db.data)
            matic_multiplier = random.uniform(*matic_deviation)
            to_token = random.choice(tokens_available)
            to_token_multiplier = random.uniform(*usdc_deviation) if to_token.signature == "USDC" else random.uniform(*usdt_deviation)

            client = clients[active_wallet.private_key]

            logger.debug(f"Wallet: {client.public_key}")

            try:
                tx_res, tx_message = client.swap(from_token=MATIC_TOKEN, to_token=to_token, deviation=matic_multiplier)
                if tx_res:
                    logger.success(tx_message)
                    active_wallet.to_stables_swaps -= 1

                    sleep(sleep_time)

                    tx_res, tx_message = client.swap(from_token=to_token, to_token=MATIC_TOKEN,
                                                     deviation=to_token_multiplier)

                    if tx_res:
                        logger.success(tx_message)
                        active_wallet.to_matic_swaps -= 1
                    else:
                        logger.error(tx_message)
                        self.db.move_as_failed(active_wallet)

                    self.db.update()

                    sleep(sleep_time)
                else:
                    logger.error(tx_message)
                    self.db.move_as_failed(active_wallet)
                    self.db.update()

            except Exception as ex:
                logger.error(ex)

        logger.success("Script has ended its work. Wallets are now on fire.")
