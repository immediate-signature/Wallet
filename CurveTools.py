class Curve:
    _oid_lookup = {}  # a lookup table for getting curve instances by their object identifier

    def __init__(self, name: str, p: int, a: int, b: int, q: int, gx: int, gy: int, oid: bytes = None):
        self.name = name
        self.p = p
        self.a = a
        self.b = b
        self.q = q
        self.gx = gx
        self.gy = gy
        self.oid = oid

        if oid is not None:
            self._oid_lookup[oid] = self

    @classmethod
    def is_point_on_curve(self, point: (int, int)) -> bool:
        x, y, = point
        left = y * y
        right = (x * x * x) + (self.a * x) + self.b
        return (left - right) % self.p == 0

    @property
    def G(self):
        from Point import Point
        return Point(self.gx, self.gy, self)


P256 = Curve(
    'P256',
    115792089210356248762697446949407573530086143415290314195533631308867097853951,
    -3,
    41058363725152142129326129780047268409114441015993725554835256314039467401291,
    115792089210356248762697446949407573529996955224135760342422259061068512044369,
    48439561293906451759052585252797914202762949526041747995844080717082404635286,
    36134250956749795798585127919587881956611106672985015071877198253568414405109,
    b'\x2A\x86\x48\xCE\x3D\x03\x01\x07'
)

secp256k1 = Curve(
    'secp256k1',
    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
    0x0,
    0x7,
    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
    0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
    b'\x2B\x81\x04\x00\x0A'
)