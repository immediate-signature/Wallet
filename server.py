import os
import subprocess


# list of rpc calls: https://developer.bitcoin.org/reference/rpc/index.html
#currently runs in regtest mode
def run_server():
    """runs the bitcoind client provided by bitcoin.org"""
    os.chdir('C:\\Program Files\\Bitcoin\\daemon')
    #os.system('bitcoind') for mainnet!
    os.system('bitcoind -regtest -rpcbind=127.0.0.1:18443')



def rpc_call(name: str):
    rpc = "bitcoin-cli -regtest " + name
    # os.chdir('C:\\Program Files\\Bitcoin\\daemon')
    return subprocess.check_output(rpc)

#include!!! name

run_server()
