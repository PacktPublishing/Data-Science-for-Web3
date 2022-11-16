import asyncio
import json
from web3 import Web3
from websockets import connect
import winsound

#set up the alarm
frequency = 2500
duration = 1000

#connect to the node
infura_ws_url = 'wss://mainnet.infura.io/ws/v3/[YOUR API KEY]'
infura_http_url = 'https://mainnet.infura.io/v3/[YOUR API KEY]'
web3 = Web3(Web3.HTTPProvider(infura_http_url))

#details of the smart contract we are tracking
tether_account = web3.toChecksumAddress('0xdAC17F958D2ee523a2206206994597C13D831ec7')
with open ("./tether_abi.json") as f:
    tether_abi= json.load (f)
tetherContract = web3.eth.contract(address=tether_account, abi=tether_abi)

async def get_event():
    async with connect(infura_ws_url) as ws:
        await ws.send('{"jsonrpc": "2.0", "id": 1, "method": "eth_subscribe", "params": ["newPendingTransactions"]}')
        subscription_response = await ws.recv()
        print(subscription_response)

        while True:
            try:
                message = await asyncio.wait_for(ws.recv(), timeout=15)
                response = json.loads(message)
                txHash = response['params']['result']
                tx = web3.eth.get_transaction(txHash)
                if tx.to == tether_account:
                    winsound.Beep(frequency, duration)
                    print({
                        "hash": txHash,
                        "from": tx["from"],
                        "value_eth": web3.fromWei(tx["value"], 'ether'),
                        "function": tetherContract.decode_function_input(tx["input"])[0],
                        "value_usdt": (tetherContract.decode_function_input(tx["input"])[1]['_value'])*10**-6
                    })
                pass
            except:
                pass

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    while True:
        loop.run_until_complete(get_event())
