from web3 import Web3, middleware
from web3.exceptions import ContractLogicError
from web3.gas_strategies.time_based import *
from web3.middleware import geth_poa_middleware
import json
import sys 

link_to_img = sys.argv[1]
if not link_to_img.startswith("./"):
    link_to_img = "./" + link_to_img

metadata_hashes = json.load(open('metadata_hashes.json'))[link_to_img]

w3 = Web3(provider=Web3.HTTPProvider("https://rinkeby.infura.io/v3/84b5c3ce44e04b8aa347a5c4dd247bc7"))

from_addr = '0x87aC8fB7F9847A6D76Eb217B40A2A91bADd3bbD6'
contract_addr = '0x7651487ca5dE4685C91973533099C043191D993A'
ABI = json.load(open('abi.json'))
PRIVATE_KEY = 'e052b603f3795407be51f1e6c50dae0c826100b4a80f7de9ea62dc26105cba86'

contract = w3.eth.contract(contract_addr, abi=ABI)

w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.middleware_onion.add(middleware.latest_block_based_cache_middleware)
w3.middleware_onion.add(middleware.simple_cache_middleware)

strategy = construct_time_based_gas_price_strategy(10)

w3.eth.setGasPriceStrategy(strategy)

def handle_transaction(fn_name, args):
    addr = Web3.toChecksumAddress(from_addr)
    
    def calculate_nonce():
        return Web3.toHex(w3.eth.getTransactionCount(addr))
        
    data = contract.encodeABI(fn_name, args=args)
    
    while True:
        try:
            gas = getattr(contract.functions, fn_name)(*args).estimateGas({'from': addr})
            break 
        except ContractLogicError as e:
            print(f"A contract error occurred while calculating gas: {e}")
            print("S=skip, R=retry, Q=quit")
            answer = input("> ")
            if "q" in answer.lower():
                quit()
            elif "s" in answer.lower():
                return
        except Exception as e:
            print(f"A misc. error occurred while calculating gas: {e}")
            print("Resolve bug. Quitting now.")
            quit()

    gasprice = w3.eth.generateGasPrice()

    txn_fee = gas * gasprice
    
    tr = {'to': contract.address, 
            'from': from_addr,
            'value': Web3.toHex(0), 
            'gasPrice': Web3.toHex(gasprice), 
            'nonce': calculate_nonce(),
            'data': data,
            'gas': gas,
            }

    print(f"Transaction:\n{tr}\n\nFunction: {fn_name}\nArguments:{args}\n\nEstimated Gas: {gas} * Gasprice: {gasprice} = {txn_fee} Txn Fee\n\nY=Yes I want to make the txn with calculated gasprice. <ANY #>=Yes I want to make the txn with a custom gasprice. N=No I'd like to skip this txn. Q=Quit")
    answer1 = input("> ")
    if "y" in answer1.lower():
        while True:
            try:
                signed = w3.eth.account.sign_transaction(tr, PRIVATE_KEY)
                tx = w3.eth.sendRawTransaction(signed.rawTransaction)    
                tx_receipt = w3.eth.waitForTransactionReceipt(tx)
                print("TXN RECEIPT: ", tx_receipt)
                break 
            except Exception as e:
                print(f"{fn_name} Error: ", e)
                print("\nC=continue, R=retry, Q=quit")
                answer = input("> ")
                if "q" in answer.lower():
                    quit()
                elif answer.lower() == 'c':
                    break
                else:
                    tr['nonce'] = calculate_nonce()
    elif "q" in answer1.lower():
        quit()

checksum_from_addr = Web3.toChecksumAddress(from_addr)

for i, metadata_hash in enumerate(metadata_hashes):
    token_uri = f'ipfs://{metadata_hash}'
    handle_transaction("createNFT", [token_uri])