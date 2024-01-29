import os
from web3 import Web3, AsyncWeb3


secret_key = os.environ.get('CHAINSTACK')
print(secret_key)
#w3 = Web3(Web3.HTTPProvider(secret_key))

#print(w3.eth.get_block('latest'))