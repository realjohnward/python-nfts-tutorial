from web3 import Web3, middleware
from web3.exceptions import ContractLogicError
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import *
import os
import json

addr = '0x87aC8fB7F9847A6D76Eb217B40A2A91bADd3bbD6'
PRIVATE_KEY = 'e052b603f3795407be51f1e6c50dae0c826100b4a80f7de9ea62dc26105cba86'

bytecode = json.load(open("bytecode.json"))['object']
abi = json.load(open('abi.json'))

w3 = Web3(Web3.HTTPProvider('https://rinkeby.infura.io/v3/84b5c3ce44e04b8aa347a5c4dd247bc7'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.middleware_onion.add(middleware.latest_block_based_cache_middleware)
w3.middleware_onion.add(middleware.simple_cache_middleware)

strategy = construct_time_based_gas_price_strategy(15)

w3.eth.setGasPriceStrategy(strategy)


ColoredPet = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = Web3.toHex(w3.eth.getTransactionCount(addr))
gasprice = w3.eth.generateGasPrice()
print("gasprice: ", gasprice)

tr = {'to': None, 
        'from': addr,
        'value': Web3.toHex(0), 
        'gasPrice': Web3.toHex(gasprice), 
        'nonce': nonce,
        'data': "0x" + bytecode,
        'gas': 5000000,
        }

signed = w3.eth.account.sign_transaction(tr, PRIVATE_KEY)
tx = w3.eth.sendRawTransaction(signed.rawTransaction)    
tx_receipt = w3.eth.waitForTransactionReceipt(tx)

ColoredPet = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

print("----")
print("Done.")