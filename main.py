# IMPORTS
import hashlib  # for hashing
import secrets  # for entropy
import base58  # for easier debugging
# fastesdca alt
import CurveTools
from Point import Point

# Constants
PATH = r"C:\Users\yaele\PycharmProjects\Wallet\log.txt"
WORDLIST = r"C:\Users\yaele\PycharmProjects\Wallet\english.txt"
ORDER = 115792089237316195423570985008687907852837564279074904382605163141518161494337
# global variables
index = 0

# FUNCTIONS
# 27-11-23 based on BIP39
def generate_entropy():
    """generates entropy and adds a checksum at the end"""  # CORRECT
    ent = secrets.token_bytes(32)
    print(ent.hex())  # for debugging
    hashed = hashlib.sha256(ent)
    checksum = hashed.hexdigest()[0:2]
    print(ent.hex())  # for debugging
    ent = ent.hex() + checksum
    return ent

def binary_slicing(mum):  # CORRECT
    """slices the sentence after  11 bits, generates a mnemonic sentence"""
    str = ''
    sentence = ''
    binary = bin(int(mum, 16))[2:]
    while len(binary) < 264:
        binary = '0' + binary
    binary = binary[len(binary) - 264:]
    for i in range(0, 24):
        start = i * 11
        end = start + 10
        output = binary[start:end + 1]
        sentence = sentence + read_line(int(output, 2), WORDLIST)  # convert to words
        str = str + ' ' + output
    sentence = sentence.replace('\n', ' ')
    print(sentence)
    return str[1:]

def mnemonic_to_seed(sentence):  # CORRECT
    """creates a seed based on a mnemonic phrase"""
    sentence = sentence.encode()
    passphrase = ''
    iterations = 2048
    salt = "mnemonic" + passphrase
    hash_name = 'sha512'
    seed = hashlib.pbkdf2_hmac(hash_name, sentence, salt.encode(), iterations, dklen=None)
    print(seed.hex())
    append(seed.hex(), PATH)
    print("seed:")
    print(base58.b58encode(seed))
    return seed.hex()

#PUBKEY
def get_public_key(d: int, curve: CurveTools.Curve) -> Point:
    return d * curve.G
def generate_public_key(private_key):  # CORRECT
    """generates a compressed public key based on given private key -> str"""
    key = int(private_key.hex(), 16)
    pub_key = get_public_key(key, CurveTools.secp256k1)
    x = hex(getattr(pub_key, 'x'))[2:]
    print(x)
    y = getattr(pub_key, 'y')
    print(y)
    print(hex(y))
    if y % 2 == 0:
        comp = "02" + x
    else:
        comp = "03" + x
    return comp

def master_key(seed):
    master = hashlib.pbkdf2_hmac('sha512', seed.encode(), 'Bitcoin seed'.encode(), 2480, dklen=None)
    print("master hex :" + master.hex())
    private_key = master.hex()[:64]  # IMPORTANT ELEMENT
    print(private_key)
    chain_code = master.hex()[64:]  # IMPORTANT ELEMENT
    print(chain_code)
    return master, chain_code

def derive_child(private_key, chain_code):  # TODO fix
    global index
    public_key = generate_public_key(private_key)
    print("pubkey:" + public_key)
    data = str(int(public_key.encode(), 16) + index).encode()
    print("debbug 1")
    index += 1
    print("debbug 2")
    cc = str(chain_code).encode()
    print("debbug 3")
    inter_key = hashlib.pbkdf2_hmac('sha512', data, cc, 2048, dklen=None)
    print("debbug 4")
    temp = int.from_bytes(inter_key, "big")
    child_chain_code = int(hex(temp)[64:-1], 16)
    high = int(hex(temp)[0:65], 16)
    # if child_chain_code >= ORDER:
    # raise Exception("Chain code is greater than the order of the curve. Try the next index.")
    # derive_child(private_key, chain_code)
    child_private_key = hex(int((high + int(private_key, 16)), 16) % ORDER)[64]
    print(child_private_key)


def read_line(line_number, read_from):
    """reads from a specific line"""
    file = open(read_from)
    content = file.readlines()
    file.close()
    return content[line_number]


def append(data, read_from):
    file = open(read_from, 'a')
    file.write(data)
    file.close()


def export():
    first =master_key(mnemonic_to_seed(binary_slicing(generate_entropy())))
    append(derive_child(first[0],first[1]),PATH)
# LOGIN
def run_wallet():  # NOT READY
    pass
def authentication():  # NOT READY
    mnemonic = input("please enter your mnemonic phrase\n")
    while mnemonic_to_seed(mnemonic) != read_line(0, PATH):  # contains the hashed seed
        response = input('wrong mnemonic phrase. Would you like to try again or generate new one (qm)')
        if response == 'n':
            append(mnemonic_to_seed(binary_slicing(generate_entropy())), PATH)

    run_wallet()

if __name__ == '__main__':
    pass