import hashlib
import json

import CurveTools
import keys
import main
import script
import server


def generate_public_key(private_key):  # CORRECT
    """generates a compressed public key based on given private key -> str"""
    key = int(private_key.encode(), 16)
    pub_key = keys.get_public_key(key, CurveTools.secp256k1)
    x = hex(getattr(pub_key, 'x'))[2:]
    y = getattr(pub_key, 'y')
    if y % 2 == 0:
        comp = "02" + x
    else:
        comp = "03" + x
    return comp


def generate_address(pubkey):  # CORRECT
    """gets string of pubkey and returns the base 58 representation of the bitcoin address of this pubkey on the
    testnet"""
    hash_object = hashlib.new('ripemd160')
    data = hashlib.sha256(bytes.fromhex(pubkey)).hexdigest()
    hash_object.update(bytes.fromhex(data))
    hash_value = hash_object.hexdigest()  # first step ripemd160(sha256(uncompressed key))
    hash_value = "6f" + hash_value  # 0x6f testnet
    sha = hashlib.sha256(bytes.fromhex(hash_value)).hexdigest()  # first hashing for the checksum
    checksum = hashlib.sha256(bytes.fromhex(sha)).hexdigest()[:8]
    address = hash_value + checksum
    # to base 58
    return main.base58(address)


# generate public key = comppresed already

def bech32(pubkey): #not used
    # making of the ScriptPubKey
    data = hashlib.sha256(bytes.fromhex(pubkey)).hexdigest()
    hash_object = hashlib.new('ripemd160')
    hash_object.update(bytes.fromhex(data))
    script_public_key = '0014' + hash_object.hexdigest()  # Witness
    return script_public_key


# for import muli - calls the other functions I made.
'''
mnemonic = main.binary_slicing(main.generate_entropy())
master = main.master_key(main.mnemonic_to_seed(mnemonic))
key = main.extend(master[0], master[1])
privkey = main.toWIF(key)
pubkey = generate_public_key(key)
address = generate_address(pubkey)

print(privkey)
print(pubkey)
print(address)

list = json.dumps(json.loads(server.rpc_call(r'getaddressesbylabel ""')))
print(type(list))
print(list[2:36])
print(list[1])

print("new:")
data = server.rpc_call(r'decoderawtransaction \"02000000014e08a48d95c8f4c03d8cb33c21ab35bc7d7acbcdf30274d8d93a094a6296b66d0000000000fdffffff0200e1f505000000001600144122612ba846ce849edb984c7edd701ecac8d9c198978b44000000001976a9146a6402eef465f58a16810d5c2313a3be1de7093788ac00000000\"')
hex = json.loads(data)["hex"]
print(hex)



data = server.rpc_call(r'-rpcwallet="wallet" listunspent 0')
data = json.loads(data)[0]["txid"]

print(data)
'''
#reciever
def filter_utxo(amount):
    data = '-named -rpcwallet="reciever" listunspent 0 query_options=' + r'"{\"minimumSumAmount\":' + str(
        amount) + '}"'  # name of the wallet!!
    return server.rpc_call(data)

def transaction(amount: int, destination: str):
    ## Outputs - inputs = transaction fee, so always double-check your math!
    me = json.dumps(json.loads(server.rpc_call(r'-rpcwallet="reciever" getaddressesbylabel ""')))[2:36]
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
    output = r'{\"' + destination + r'\":' + str(amount) + "," + r'\"' + me + r'\":' + str(sum - amount - FEE) + "}"

    return server.rpc_call("createrawtransaction " + '"' + UTXOs + '" ' + output)

print(transaction(0.5, server.rpc_call(r'-rpcwallet-"wallet" getaddressesbylabel ""') ))