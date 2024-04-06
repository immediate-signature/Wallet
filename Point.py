import CurveTools


# for y^2 = x^3 + 7

def modinv(a: int, n=CurveTools.secp256k1.p):  # Extended Euclidean Algorithm/'division' in elliptic curves
    r"""modulo inverse function
      Args:
            |  a (int): The value which will be calculated.
            |  n (int): The prime number of y^2 = x^3 + 7 curve
    """
    lm, hm = 1, 0
    low, high = a % n, n
    while low > 1:
        ratio = high // low
        nm, new = hm - lm * ratio, high - low * ratio
        lm, low, hm, high = nm, new, lm, low
    return lm % n


class Point:
    """Representation of a point on an elliptic curve.

    Attributes:
        |  x (int): The x coordinate of the point.
        |  y (int): The y coordinate of the point.
        |  curve (:class:`Curve`): The curve that the point lies on.
    """

    def __init__(self, x: int, y: int, curve=CurveTools.secp256k1):
        r"""Initialize a point on an elliptic curve.

        The x and y parameters must satisfy the equation :math:`y^2 \equiv x^3 + ax + b \pmod{p}`,
        where a, b, and p are attributes of the curve parameter.

        Args:
            |  x (int): The x coordinate of the point.
            |  y (int): The y coordinate of the point.
            |  curve (:class:`Curve`): The curve that the point lies on.
        """

        # Reduce numbers before computation to avoid errors and limit computations.
        if curve is not None:
            x = x % curve.p
            y = y % curve.p

        #if not (x == 0 and y == 0 and curve is None) and not curve.is_point_on_curve((x, y)):
        #    raise ValueError(
        #        'coordinates are not on curve <{}>\n\tx={:x}\n\ty={:x}'.format(curve.name, x, y))
        #else:
            self.x = x
            self.y = y
            self.curve = curve

    def addition(self, other, n=CurveTools.secp256k1.p):
        lam = ((other.y - self.y) * modinv(other.x - self.x)) % n
        xr = (lam ** 2 - self.x - other.x) % n
        yr = (lam * (self.x - xr) - self.y) % n
        return Point(xr, yr)

    def double(self, n = CurveTools.secp256k1.p):
        slope = ((3 * self.x ** 2) * modinv((2 * self.y))) % n # using modular inverse to perform "division"
        x = (slope ** 2 - (2 * self.x)) % n
        y = (slope * (self.x - x) - self.y) % n
        return Point(x,y)


    def multiply(self, scalar):  # Double & add. EC Multiplication, Not true multiplication
        if scalar == 0 or scalar >= CurveTools.secp256k1.q:
            raise Exception("Invalid Scalar/Private Key")
        scalar_bin = str(bin(scalar))[2:]
        p = Point(self.x, self.y)
        for i in range(1, len(scalar_bin)):  # This is invented EC multiplication.
            p = p.double()
            if scalar_bin[i] == "1":
                p = p.addition(self)
        return p