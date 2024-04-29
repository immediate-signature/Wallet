import server
import json


# new wallet

def extract(input):
    return json.dumps(json.loads(input))



def load(name):
    # if you know the name
    call = 'loadwallet "' + name + '"' + ' true'  # true = load_on_startup
    server.rpc_call(call)


# important
def backup(PATH):
    call = 'backupwallet ' + '"' + PATH + '"'
    server.rpc_call(call)


def filter_utxo(amount):
    data = '-named -rpcwallet="wallet" listunspent query_options=' + r'"{\"minimumSumAmount\":' + str(
        amount) + '}"'  # name of the wallet!!
    return server.rpc_call(data)


def transaction(amount: int, destination: str):
    ## Outputs - inputs = transaction fee, so always double-check your math!
    me = json.dumps(json.loads(server.rpc_call(r'getaddressesbylabel ""')))[2:36]
    print(me)
    list = json.loads(filter_utxo(amount))
    if (len(list) == 0 ):
        return "error"
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





def sign(raw_tx, address):
    call = 'signrawtransaction ' + raw_tx + "'[]' " + r'[\"' + address + r'\"]'
    server.rpc_call(call)
