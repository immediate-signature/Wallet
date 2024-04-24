import hashlib
import CurveTools
import keys
import main


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

def bech32(pubkey):
    # making of the ScriptPubKey
    data = hashlib.sha256(bytes.fromhex(pubkey)).hexdigest()
    hash_object = hashlib.new('ripemd160')
    hash_object.update(bytes.fromhex(data))
    script_public_key = '0014' + hash_object.hexdigest()  # Witness
    return script_public_key


master = main.master_key(main.mnemonic_to_seed(main.binary_slicing(main.generate_entropy())))
key = main.extend(master[0], master[1])
wif = main.toWIF(key)
print(wif)
print(generate_address(generate_public_key(key)))
print(bech32(generate_public_key(key)))
print(generate_public_key(key))
