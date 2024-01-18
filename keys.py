from CurveTools import Curve, P256
from Point import Point


def get_public_key(d: int, curve: Curve) -> Point:
    """Generate a public key from a private key.

    The public key :math:`Q` is a point on the curve calculated as :math:`Q = dG`, where :math:`d`
    is the private key and :math:`G` is the curve's base point.

    Args:
        |  d (long): An integer representing the private key.
        |  curve (fastecdsa.curve.Curve): The curve over which the key will be calulated.

    Returns:
        fastecdsa.point.Point: The public key, a point on the given curve.
    """
    return d * curve.G
