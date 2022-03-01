from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# We add these two lines that we forgot from the video!
print("Installing...")
install_solc("0.6.0")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)
with open("compiled_code.json", "w") as file:
    json.dump(
        compiled_sol, file
    )  # will take compiled_sol json file and dump it here, but will keep it in the json syntax

# have to get bytecode and abi of file before you can deploy to chain
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
][
    "object"
]  # walking down json tree this stuff is being pulled from complied_code.json file--the bytecode is what the etherm machine understands

# get abi from complied_code.json file tree
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# print(abi) make sure it works

# ganache is a simulated BC we can use to deploy, it will allow you to spin up your own BC locally--Remix-which was only one node--ganache is like Javascript VM in Remix--it test things very quickly cause you are only using one node

# connectin to ganache
# you have to have http from RPC SERVER, chainID or NETWORK ID of the blockchain--the http is the mock address from ganache, address is BC addy
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x9872cC117D5e2ef2271C5ee4a561c26e69e6db25"
# python always looks for hexadecimal in a key you have to add '0x'
# NEVER EVER NEVER HARD CODE YOUR PRIVATE KEY IN CONTRACTS--BAD PRACTIC
private_key = os.getenv(
    "PRIVATE_KEY"
)  # "04198d284b8e9056de7622c6b91cff430b461aa491fbad29503136757297e2b8"  # this signs trasactions
print(private_key)
# create the contract in python
# ***BELOW IS CONTRACT OBJECT***
SimpleStorage = w3.eth.contract(
    abi=abi, bytecode=bytecode
)  # you can check web3 docs about contract types
# print(SimpleStorage)
# build transaction, sign transaction, send transaction
# nonce in BC block  is the number that is assigned when the data is  mined in the block on BC
# nonce of your transactions: if you look at a transaction you have done and scrool down to Nonce 'position' this is the number of transactions that has hashed
# in your contract you have to get the lastest transaction count 'NONCE"
nonce = w3.eth.getTransactionCount(my_address)
# print(nonce) when you python deploy.py you will get back your total of  nonce transactions you have done, this addy is zero cause its a mock addy
# REMEBER WHEN YOU MAKE A TRANSACTION  YOU ARE CHANGING STATE ON BC
# SIMPLE_sTORAGE.SOL DOES NOT HAVE A CONTRUCTOR WRITTEN IN IT BUT IT

# transaction object
transaction = SimpleStorage.constructor().buildTransaction(  # this constructor() is a method in web3.py
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)
# print(transaction) this returns a data object that is happening in  simplestorage.sol

# sign transaction  on web3 docs account.sign_transaction('takes two params'transaction_dict, and a private_key)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# setting envirnment varables
