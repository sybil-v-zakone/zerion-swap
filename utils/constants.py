import os
import json

from models.token import Token

NULL_ADDRESS = "0x0000000000000000000000000000000000000000"

# Contracts

POLYGON_MATIC_ADDRESS = "0x0000000000000000000000000000000000001010"

ZERION_ROUTER_ADDRESS = "0xd7F1Dd5D49206349CaE8b585fcB0Ce3D96f1696F"
ZERION_ROUTER_ABI = json.load(open(os.path.abspath("abis/zerion_router.json")))

ZERION_MULTISIG_ADDRESS = "0x4a183b7ED67B9E14b3f45Abfb2Cf44ed22c29E54"

CALLER_CONTRACT_ADDRESS = "0xC629Bf86f02ef13E8F1f5F75adE8a8165587998F"
CALLER_ABI = json.load(open(os.path.abspath("abis/simple_caller.json")))

UNISWAP_CONTRACT_ADDRESS = "0xE592427A0AEce92De3Edee1F18E0157C05861564"
UNISWAP_ABI = json.load(open(os.path.abspath("abis/uniswap.json")))

# Zerion transaction parameters-related constants

PARAM_SWAP_TYPE = 1

PARAM_FEE_SHARE_PF = 5000000000000000

PARAM_FEE_SHARE_MF = 0

PARAM_ACC_SIGNATURE = (0, '0x')

PARAM_FEE_SIGNATURE = (0, '0x')

PARAM_AMOUNT_MINIMUM = 0

PARAM_SWAP_FEE = 500

THIRTY_MINUTES = 1800


# Tokens

USDC_TOKEN = Token(
    contract_address="0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
    abi=json.load(open(os.path.abspath("abis/usdc.json"))),
    decimals=6,
    signature="USDC",
    is_native=False
)

USDT_TOKEN = Token(
    contract_address="0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
    abi=json.load(open(os.path.abspath("abis/usdt.json"))),
    decimals=6,
    signature="USDT",
    is_native=False
)

MATIC_TOKEN = Token(
    contract_address="0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
    abi=json.load(open(os.path.abspath("abis/matic.json"))),
    decimals=18,
    signature="MATIC",
    is_native=True
)

POLYGON_MATIC_TOKEN = Token(
    contract_address=POLYGON_MATIC_ADDRESS,
    abi=json.load(open(os.path.abspath("abis/matic.json"))),
    decimals=18,
    signature="MATIC",
    is_native=True
)

WMATIC_TOKEN = Token(
    contract_address="0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
    abi=json.load(open(os.path.abspath("abis/wmatic.json"))),
    decimals=18,
    signature="WMATIC",
    is_native=False
)
