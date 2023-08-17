import os

# абсолютный путь до файла с приватниками
wallets_file = os.path.abspath("data/wallets.txt")

# количество свапов [от, до] (выбирается рандомное четное число из промежутка, [до] - обязательно четное число)
swaps_range = [1, 4]

# время между свапами (выбирается рандомное число из промежутка)
sleep_time = [10, 20]

polygon_rpc = "https://rpc.ankr.com/polygon"

