import subprocess

import main
import server
import json
import jsonrpc

# new wallet

me = 'bcrt1q93wmp98xzlaf2lka6xudn4rychmhtwracnxdph'  # the users address!!


def generate_wallet():
    call = '-named createwallet "empty" blank=true '
    server.rpc_call(call)
    call = 'sethdseed ' + '"' + main.toWIF(main.master_key(main.generate_entropy())) + '"'
    server.rpc_call(call)


# existing wallet

def load(name):
    # if you know the name
    call = 'loadwallet "' + name + '"' + ' true'  # true = load_on_startup
    server.rpc_call(call)


# important
def backup(PATH):
    call = 'backupwallet ' + '"' + PATH + '"'
    server.rpc_call(call)


def filter_utxo(amount):
    data = '-named -rpcwallet="trial" listunspent  query_options=' + r'"{\"minimumSumAmount\":' + str(
        amount) + '}"'  # name of the wallet!!
    return server.rpc_call(data)


def transaction(amount: int, destination: str):
    ## Outputs - inputs = transaction fee, so always double-check your math!
    list = json.loads(filter_utxo(amount))
    UTXOs = '['
    sum = 0
    for i in range(len(list)):
        UT = list[i]
        sum += UT["amount"]
        UTXOs = UTXOs + r'{\"txid\":\"' + UT["txid"] + r'\",\"vout\":' + str(UT["vout"]) + r'},'
    UTXOs = UTXOs[:-1] + ']'  # list of inputs for the transaction

    # OUTPUT
    output = r'{\"' + destination + r'\":' + str(amount) + "," + r'\"' + me + r'\":' + str(sum - amount) + "}"

    return server.rpc_call("createrawtransaction " + '"' + UTXOs + '" ' + output)

def sign(raw_tx):
    call = 'signrawtransaction ' + raw_tx + "'[]' " + r'[\"' + me + r'\"]'

print(transaction(100, 'bcrt1qvcrs8hlkclcje970j9ak3lzyrakl5tk8edf4h5'))

