# IMPORTS
import hashlib  # for hashing
import json
import secrets  # for entropy
import tkinter
import winreg  # for registry management
import server
from pathlib import Path

# ec
import CurveTools
import keys
from gui import Signup,Login,Phrase

# Constants
PATH = str(Path.home()) + r'\PycharmProjects\Wallet'
REGPATH = r"HKEY_CURRENT_USER\Software\BitWallet\1\PATH"
WORDLIST = PATH + r"english.txt"
ORDER = 115792089237316195423570985008687907852837564279074904382605163141518161494337
# global variables
index = 2 ** 31

def getmyaddress():
    me = json.dumps(json.loads(server.rpc_call(r'-rpcwallet="wallet" getaddressesbylabel ""')))[2:36]
    return me

def extend(ppk, pcc):
    """derives child keys from the master key"""
    global index
    data = bytes.fromhex(ppk + hex(index)[2:])
    key = bytes.fromhex(pcc)

    index += 1
    inter_key = hashlib.pbkdf2_hmac('sha512', data, key, 2048).hex()

    il = inter_key[:64]
    ir = inter_key[64:]

    if int(ir, 16) >= ORDER:
        raise "chain code is greater than the curve, try again with another index"

    cpk = (int(il, 16) + int(ppk, 16)) % ORDER
    cpk = hex(cpk)

    return cpk[2:]


def toWIF(raw):
    """gets private key and turns it into a WIF private key"""
    key = 'ef' + raw + '01'  # prefix for testnet
    key = key + hash256(key)[:8]  # we only need the first 4 bytes
    key = base58(key)
    return key


def generate_entropy():
    """generates entropy and adds a checksum at the end"""  # CORRECT
    ent = secrets.token_bytes(32)
    hashed = hashlib.sha256(ent)
    checksum = hashed.hexdigest()[0:2]
    ent = ent.hex() + checksum
    return ent


def binary_slicing(mum):  # CORRECT
    """slices the sentence after  11 bits, generates a mnemonic sentence"""
    string = ''
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
        string = string + ' ' + output
    sentence = sentence.replace('\n', ' ')
    print(sentence)
    return string[1:]


def mnemonic_to_seed(sentence):
    """creates a seed based on a mnemonic phrase"""
    sentence = sentence.encode()
    passphrase = ''
    iterations = 2048
    salt = "mnemonic" + passphrase
    hash_name = 'sha512'
    seed = hashlib.pbkdf2_hmac(hash_name, sentence, salt.encode(), iterations, dklen=None)
    return seed.hex()



def generate_uncompressed_pubkey(private_key):
    """generates an uncompressed public key based on given private key -> str"""
    key = int(private_key.encode(), 16)
    pub_key = keys.get_public_key(key, CurveTools.secp256k1)
    x = hex(getattr(pub_key, 'x'))[2:]
    y = hex(getattr(pub_key, 'y'))[2:]
    string = "04" + x + y
    return string


def generate_address(pubkey):
    """gets string of pubkey and returns the base 58 representation of the bitcoin address of this pubkey on the
    testnet"""
    hash_object = hashlib.new('ripemd160')
    data = hashlib.sha256(pubkey.encode()).hexdigest().encode()
    hash_object.update(data)
    hash_value = hash_object.hexdigest()
    print(hash_value)  # first step ripemd160(sha256(uncompressed key))
    hash_value = "6f" + hash_value  # 0x6f testnet
    checksum = hashlib.sha256(hashlib.sha256(hash_value.encode()).hexdigest().encode()).hexdigest()
    address = hash_value + checksum
    # to base 58
    return base58(address)


def generate_public_key(private_key):
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


def master_key(seed):
    # generates the master private key + 32 bytes of data
    master = hashlib.pbkdf2_hmac('sha512', seed.encode(), 'Bitcoin seed'.encode(), 2480, dklen=None)
    private_key = master.hex()[:64]  # IMPORTANT ELEMENT
    chain_code = master.hex()[64:]  # IMPORTANT ELEMENT
    return private_key, chain_code


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




# REG
def save():
    """creates the handle for saving in the reg"""
    h = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 'bitWallet')
    return h


def save_on_reg(data: str):
    """inserts whatever data into the reg file"""
    backup = winreg.QueryValue(winreg.HKEY_CURRENT_USER, 'bitWallet')
    print(backup)
    string = backup + '\n' + data
    print(winreg.QueryValue(winreg.HKEY_CURRENT_USER, 'bitWallet'))
    winreg.SetValue(winreg.HKEY_CURRENT_USER, 'bitWallet', winreg.REG_SZ, string)


# LOGIN
def detectuse():
    try:
        folder = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'bitWallet')
    except:
        signup()
    else:
        login()  # change to username and password
        folder.Close()



def signup():
    '''opens the gui signup window'''

    root = tkinter.Tk()
    obj = Signup(root)
    root.mainloop()
    mnemonic=generate_wallet() #starts to run after the signup quits- which means succsessful registration
    root = tkinter.Tk()
    obj = Phrase(root,mnemonic)
    root.mainloop()




def login():
    '''opens the gui log in window'''
    root = tkinter.Tk()
    obj = Login(root)
    root.mainloop()


# USEFUL
def base58(num: str):  # CORRECT
    """converts a string of hex into a string encoded in base58"""
    num = int(num, 16)
    if num == 0:
        return '1'
    output = ''
    characters = ('1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K',
                  'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e',
                  'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                  'z')
    while num != 0:
        output = characters[num % 58] + output
        num = num // 58

    return output


def hash256(data: str):
    """implementation of the HASH256 function (doing sha256 twice on the same string)
    data : a string of the data in hexadecimal
    """
    h1 = hashlib.sha256(bytes.fromhex(data)).hexdigest()
    h2 = hashlib.sha256(bytes.fromhex(h1)).hexdigest()
    return h2


# new wallet with bitcoin rpc
def generate_wallet():
    call = '-named createwallet "wallet" blank=true descriptors=false load_on_startup=true '
    server.rpc_call(call)
    # for import muli - calls the other functions I made.
    mnemonic = binary_slicing(generate_entropy())
    master = master_key(mnemonic_to_seed(mnemonic))
    key = extend(master[0], master[1])
    privkey = toWIF(key)
    pubkey = generate_public_key(key)
    address = generate_address(pubkey)
    call = (r'-rpcwallet="legacy" importmulti "[{\"scriptPubKey\":{\"address\":\"' + address + (r'\"},\"timestamp'
                                                                                                r'\":\"now\",'
                                                                                                r'\"pubkeys\":[\"') +
            pubkey + r'\"],\"keys\":[\"' + privkey + r'\"]}]" "{\"rescan\":false}"')
    server.rpc_call(call)
    return mnemonic

if __name__ == '__main__':
    detectuse()