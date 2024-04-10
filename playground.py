import hashlib


def base58(num: str):
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


def toWIF(raw):  # TODO: FIX!
    key = 'ef' + raw + '01'  # prefix for testnet
    h = hashlib.new('sha256')
    h.update(bin(int(key,16)).encode())
    print(h.hexdigest())
    #hex_num = int(key,16)
    #bi_num = bin(hex_num)
    #hashlib.sha256(bi_num)
    #checksum = hashlib.sha256(sh).hexdigest()[:8]
    #key = key + checksum
    enc = base58(key)
   # print(checksum)
    return enc


print(toWIF('bdf83ecc5c09f495aa671d370f46eef8d3caadf3bdf5c285736f7aa4b880e609'))

print('ab56'.encode('hex'))