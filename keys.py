import hashlib
import secrets
import CurveTools
from Point import Point, modinv


def get_public_key(d: int, curve=CurveTools.secp256k1) -> Point:
    """Generate a public key from a private key.

    The public key :math:`Q` is a point on the curve calculated as :math:`Q = dG`, where :math:`d`
    is the private key and :math:`G` is the curve's base point.

    Args:
        |  d (long): An integer representing the private key.
        |  curve (fastecdsa.curve.Curve): The curve over which the key will be calculated.

    Returns:
        fastecdsa.point.Point: The public key, a point on the given curve.
    """
    return curve.G.multiply(d)


def sign(data, private_key):
    ent = secrets.token_bytes(32)
    hashed = hashlib.sha256(ent)
    random_point = CurveTools.secp256k1.G.multiply(hashed)
    r = random_point.x % CurveTools.secp256k1.p
    hdata = hashlib.sha256(hashlib.sha256(data.encode()).hexdigest().encode()).hexdigest()
    s = ((hdata + r * private_key) * (modinv(int(ent), CurveTools.secp256k1.p))) % CurveTools.secp256k1.p
    return r, s

"""def sign(private_key, data):
    # data = the entire transaction data
    key = int(generate_entropy(), 16)
    pub_key = keys.get_public_key(key, CurveTools.secp256k1)
    r = hex(getattr(pub_key, 'x'))[2:]
    mult = private_key * r
    message = hashlib.sha256(hashlib.sha256(data).digest()).digest()
    s = (mult + message) / key
"""


def verify(data, s, r, pubkey, n=CurveTools.secp256k1.p):
    message = (hashlib.sha256(data.encode).hexdigest()) % CurveTools.secp256k1.p
    gp = (int(message, 16) * modinv(s)) % CurveTools.secp256k1.p
    pub_key = r // s
    # if pubkey is Point
    # def verify (s,r,n=CurveTools.secp256k1.p, pubkey) : #based on https://github.com/wobine/blackboard101/blob/master/EllipticCurvesPart5-TheMagic-SigningAndVerifying.py
    w = modinv(s)
    p1 = CurveTools.secp256k1.G.multiply((r * w) % n)
    p2 = pubkey.multiply((r * w) % n)
    np = p1.addition(p2)
    return np.x == r
