import pandas as pd
import os
from web3 import Web3
from time import time
from time import sleep
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor
import plotly.express as px



chainstack_rpc = os.environ['chainstack_rpc']
alchemy_rpc = os.environ['alchemy_rpc']
ankr_rpc = os.environ['ankr_rpc']
quicknode_rpc = os.environ['quicknode_rpc']
infura_rpc = os.environ['infura_rpc']
getblock_rpc = os.environ['getblock_rpc']


df_block = []
df_balance = []
df_call = []


def get_balance(provider,token):
    
    w3 = Web3(Web3.HTTPProvider(token))
    t_start = time()
    block = w3.eth.get_balance('0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045')
    t_end = time()
    return [datetime.utcfromtimestamp(t_start).strftime('%Y-%m-%d %H:%M:%S'),provider,round(t_end-t_start,2),block]

def main_getbalance():
    # URLs to make requests to
    providers_dict = {
        'chainstack':chainstack_rpc,
        'alchemy':alchemy_rpc,
        'ankr':ankr_rpc,
        'quicknode':quicknode_rpc,
        'infura':infura_rpc,
        'getblock':getblock_rpc
    }

    # Using ThreadPoolExecutor to run requests in parallel
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda args: get_balance(*args), providers_dict.items()))

    
    for i in results:
        df_balance.append(i)






def latest_block(provider,token):
    
    w3 = Web3(Web3.HTTPProvider(token))
    t_start = time()
    block = w3.eth.get_block('latest')
    t_end = time()
    return [datetime.utcfromtimestamp(t_start).strftime('%Y-%m-%d %H:%M:%S'),provider,round(t_end-t_start,2),datetime.utcfromtimestamp(block['timestamp']).strftime('%Y-%m-%d %H:%M:%S'),block['number']]

def main_latestblock():
    # URLs to make requests to
    providers_dict = {
        'chainstack':chainstack_rpc,
        'alchemy':alchemy_rpc,
        'ankr':ankr_rpc,
        'quicknode':quicknode_rpc,
        'infura':infura_rpc,
        'getblock':getblock_rpc
    }

    # Using ThreadPoolExecutor to run requests in parallel
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda args: latest_block(*args), providers_dict.items()))

    
    for i in results:
        df_block.append(i)
def call(provider,token):
    
    w3 = Web3(Web3.HTTPProvider(token))
    t_start = time()
    block = w3.eth.call({'value': 0, 'gas': 13374112304499493, 'maxFeePerGas': 13374112304499493, 'maxPriorityFeePerGas': 13374112304499493, 'to': '0xc305c901078781C232A2a521C2aF7980f8385ee9', 'data': '0x477a5c98'})
    t_end = time()
    return [datetime.utcfromtimestamp(t_start).strftime('%Y-%m-%d %H:%M:%S'),provider,round(t_end-t_start,2),block]








def main_call():
    # URLs to make requests to
    providers_dict = {
        'chainstack':chainstack_rpc,
        'alchemy':alchemy_rpc,
        'ankr':ankr_rpc,
        'quicknode':quicknode_rpc,
        'infura':infura_rpc,
        'getblock':getblock_rpc
    }

    # Using ThreadPoolExecutor to run requests in parallel
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda args: call(*args), providers_dict.items()))

    
    for i in results:
        df_call.append(i)
    





for i in range(0,50):
    sleep(1)
    main_latestblock()

for i in range(0,50):
    sleep(1)
    main_getbalance()

for i in range(0,50):
    sleep(1)
    main_call()



columns_block = ['batch_time_id', 'provider', 'time_to_execute','block_timestamp','block_number']
columns_balance = ['batch_time_id', 'provider', 'time_to_execute','balance']
columns_call = ['batch_time_id', 'provider', 'time_to_execute','output']


block_results = pd.DataFrame(df_block, columns=columns_block)
balance_results = pd.DataFrame(df_balance, columns=columns_balance)
call_results = pd.DataFrame(df_call, columns=columns_call)


block_results.to_csv('csv/block_results.csv',index=False)
balance_results.to_csv('csv/balance_results.csv',index=False)
call_results.to_csv('csv/call_results.csv',index=False)
