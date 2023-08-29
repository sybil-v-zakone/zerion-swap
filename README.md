# Zerion Swap
Софт для набивания транзакций через Zerion Swap (**MATIC** -> **USDC** / **USDT** и обратно)

### Установка

В папке с проектом в терминале прописать `pip install -r requirements.txt`

### Настройка

Настройки находятся в `config.py`:
* `swaps_range` — количество свапов [от, до] (выбирается рандомное четное число из промежутка, [до] - обязательно четное число)
* `sleep_time` — время ожидания между свапами (выбирается рандомное число из промежутка)
* `matic_deviation` / `usdc_deviation` / `usdt_deviation` — множитель баланса: случайно выбранное число из промежутка умножается на баланс и свапается (для каждого токена указывается отдельно)
* `polygon_rpc` — используемая rpc

### Запуск

Для запуска скрипта в консоль нужно написать: `python main.py`

1 строка = 1 приватный ключ
