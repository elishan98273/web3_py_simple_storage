from solcx import compile_standard, install_solc
import json
from web3 import Web3


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
chain_id = 5777
my_address = "0x323C81e50EdBCA292f285f97d2C9b017eBD7532b"
#python always looks for hexadecimal in a key you have to add '0x'
private_key = "0xe0325bbd13d7a06948f20db1b5908e1076320bb3d3477107c4cf136474961eef"

#create the contract in python
SimpleStorage - w3.eth.contract(abi-abi, bytecode=bytecode)
print(SimpleStorage)
