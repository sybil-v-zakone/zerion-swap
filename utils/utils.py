from loguru import logger
from config import swaps_range, wallets_file
from tqdm import tqdm
import random
import time


def read_file_by_lines(file_path) -> list:
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            return [line.strip() for line in file]
    except FileNotFoundError as e:
        logger.error(f"{str(e)} while try to open \"{file_path}\"")
    except Exception as e:
        logger.error(f"{str(e)} while open txt file: \"{file_path}\"")


def get_swaps_count() -> int:
    random_even_number = random.randint(swaps_range[0], swaps_range[1])
    if random_even_number % 2 != 0:
        random_even_number += 1
    return random_even_number


def generate_pairs() -> dict:
    return {key: get_swaps_count() for key in read_file_by_lines(wallets_file)}


def sleep(sleep_range: list):
    try:
        for _ in tqdm(range(random.randint(*sleep_range)), colour="#ff8e76"):
            time.sleep(1)
    except Exception as e:
        logger.error(f"Sleep error: {str(e)}")