class Curve:
    _oid_lookup = {}  # a lookup table for getting curve instances by their object identifie.r

    def __init__(self, name: str, p: int, a: int, b: int, q: int, gx: int, gy: int, oid: bytes = None):
        self.name = name
        self.p = p #prime number
        self.a = a
        self.b = b
        self.q = q
        self.gx = gx
        self.gy = gy
        self.oid = oid

        if oid is not None:
            self._oid_lookup[oid] = self

    @property
    def G(self):
        from Point import Point
        return Point(self.gx, self.gy, self)

    def is_point_on_curve(self, point: (int, int)) -> bool:
        r""" Check if a point lies on this curve.

        The check is done by evaluating the curve equation :math:`y^2 \equiv x^3 + ax + b \pmod{p}`
        at the given point :math:`(x,y)` with this curve's domain parameters :math:`(a, b, p)`. If
        the congruence holds, then the point lies on this curve.

        Args:
            point (long, long): A tuple representing the point :math:`P` as an :math:`(x, y)` coordinate
            pair.

        Returns:
            bool: :code:`True` if the point lies on this curve, otherwise :code:`False`.
        """
        x, y = point
        left = y * y

        right = (x * x * x) + (self.a * x) + self.b
        return (int(round(left,2)) - int(round(right,2))) % self.p == 0


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


def validate_type(instance: object, expected_type: type):
    """Validate that instance is an instance of the expected_type.

    Args:
        |  instance: The object whose type is being checked
        |  expected_type: The expected type of instance
        |  var_name: The name of the object

    Raises:
         TypeError: If instance is not of type expected_type
    """
    if not isinstance(instance, expected_type):
        raise TypeError('Expected a value of type {}, got a value of type {}'.format(
            expected_type, type(instance)))

