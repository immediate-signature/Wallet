from CurveTools import P256

class Point:
    """Representation of a point on an elliptic curve.

    Attributes:
        |  x (int): The x coordinate of the point.
        |  y (int): The y coordinate of the point.
        |  curve (:class:`Curve`): The curve that the point lies on.
    """

    def __init__(self, x: int, y: int, curve = P256):
        # Reduce numbers before computation to avoid errors and limit computations.
        if curve is not None:
            x = x % curve.p
            y = y % curve.p

        if not (x == 0 and y == 0 and curve is None) and not curve.is_point_on_curve((x, y)):
            raise ValueError(
                'coordinates are not on curve <{}>\n\tx={:x}\n\ty={:x}'.format(curve.name, x, y))
        else:
            self.x = x
            self.y = y
            self.curve = curve