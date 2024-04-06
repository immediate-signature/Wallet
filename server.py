import os


# list of rpc calls: https://developer.bitcoin.org/reference/rpc/index.html
def run_server():
    """runs the bitcoind client provided by bitcoin.org"""
    os.chdir('C:\\Program Files\\Bitcoin\\daemon')
    #os.system('bitcoind') for mainnet!
    os.system('bitcoind -testnet -rpcbind=127.0.0.1:18322')



def rpc_call(name: str):
    rpc = "bitcoin-cli -testnet " + name
    # os.chdir('C:\\Program Files\\Bitcoin\\daemon')
    os.system(rpc)


run_server()
