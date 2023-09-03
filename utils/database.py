import json

from loguru import logger

from config import (database_autocreate,
                    database_file, wallets_file)
from models.data_item import DataItem
from utils.utils import read_file_by_lines, read_from_json, get_swaps_count


class Database:
    def __init__(self, create_once=False):
        self.data: list[DataItem] = list[DataItem]()
        self.failed_wallets: list[str] = list[str]()
        if database_autocreate or create_once:
            self.create()
        else:
            try:
                dumped_data = read_from_json(database_file)
                self.parse_data_items(dumped_data["data"])
                self.accounts_remaining = dumped_data['accounts_remaining']
                logger.success(f"Database has been loaded")
            except Exception as ex:
                logger.error(f"Seems like database file is wrongly formatted: {ex}")

    def dump(self):
        try:
            with open(database_file, 'w') as fp:
                json.dump(self, fp=fp, default=lambda o: o.__dict__)
        except Exception as ex:
            logger.error(f"Database to json object error: {str(ex)}")

    def parse_data_items(self, wallets: dict):
        for item in wallets:
            wallet = DataItem(
                private_key=item['private_key'],
                to_matic_swaps=item['to_matic_swaps'],
                to_stables_swaps=item['to_stable_swaps']
            )
            self.data.append(wallet)

    def create(self):
        try:
            private_keys = read_file_by_lines(wallets_file)

            try:
                for key in private_keys:
                    swaps_count = int(get_swaps_count() / 2)
                    data_item = DataItem(
                        private_key=key,
                        to_matic_swaps=swaps_count,
                        to_stables_swaps=swaps_count
                    )
                    self.data.append(data_item)
            except Exception as ex:
                logger.error(f"Error while reading data when creating database: {str(ex)}")

            self.accounts_remaining = len(self.data)
            self.dump()
            logger.success(f"Database has been created")
        except Exception as ex:
            logger.error(f"Database creation failed: {str(ex)}")

    def update(self):
        for item in self.data:
            if item.to_stables_swaps == 0 and item.to_matic_swaps == 0:
                self.data.remove(item)
                self.accounts_remaining -= 1
        self.dump()
        logger.success("Database has been updated")

    def move_as_failed(self, val: DataItem):
        self.data.remove(val)
        self.failed_wallets.append(val.private_key)
        self.accounts_remaining -= 1
