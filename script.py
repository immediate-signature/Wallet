import main
import server
import json

# new wallet

def extract(input):
    return json.dumps(json.loads(input))

def generate_wallet():
    call = '-named createwallet "wallet" blank=true descriptors=false load_on_startup=true '
    server.rpc_call(call)
    # for import muli - calls the other functions I made.
    master = main.master_key(main.mnemonic_to_seed(main.binary_slicing(main.generate_entropy())))
    key = main.extend(master[0], master[1])
    privkey = main.toWIF(key)
    pubkey = main.generate_public_key(key)
    address = main.generate_address(pubkey)
    call = (r'-rpcwallet="legacy" importmulti "[{\"scriptPubKey\":{\"address\":\"' + address + (r'\"},\"timestamp'
                                                                                                r'\":\"now\",'
                                                                                                r'\"pubkeys\":[\"') +
            pubkey + r'\"],\"keys\":[\"' + privkey + r'\"]}]" "{\"rescan\":false}"')


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


def getmyaddress():
    me = json.dumps(json.loads(server.rpc_call(r'-rpcwallet="d3" getaddressesbylabel ""')))[2:36]
    return me


def sign(raw_tx, address=getmyaddress()):
    call = 'signrawtransaction ' + raw_tx + "'[]' " + r'[\"' + address + r'\"]'
    server.rpc_call(call)
