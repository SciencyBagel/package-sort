from typing import Literal
import math


Stack = Literal['STANDARD', 'SPECIAL', 'REJECTED']
IsBulky = bool
IsHeavy = bool


CATEGORIES: dict[tuple[IsBulky, IsHeavy], Stack] = {
    (False, False): 'STANDARD',
    (True, False): 'SPECIAL',
    (False, True): 'SPECIAL',
    (True, True): 'REJECTED'
}

THRESHOLD_BULKY_VOLUME = 1_000_000  # cm^3
THRESHOLD_BULKY_DIMENSION = 150  # cm
THRESHOLD_HEAVY_MASS = 20  # kg


def _validate_nonnegative_finite(*vals: float):
    """All values must be finite and >= 0."""

    if any(val < 0 for val in vals) or not all(math.isfinite(val) for val in vals):
        raise ValueError(f'invalid measurements: {vals}')


def _check_bulky(width: float, height: float, length: float) -> IsBulky:
    """Checks if a package is bulky."""

    dimensions = width, height, length

    is_bulky_from_dimensions = any(dim >= THRESHOLD_BULKY_DIMENSION for dim in dimensions)
    is_bulky_from_volume = math.prod(dimensions) >= THRESHOLD_BULKY_VOLUME

    return is_bulky_from_dimensions or is_bulky_from_volume


def _check_heavy(mass: float) -> IsHeavy:
    """Checks whether package is heavy"""

    return mass >= THRESHOLD_HEAVY_MASS


def sort(width: float, height: float, length: float, mass: float) -> Stack:
    """Returns stack cateogry based on package measurements.

    Examples:
        >>> sort(149, 20, 30, 10)
        'STANDARD'
        >>> sort(150, 20, 20, 20)
        'REJECTED'
        >>> sort(149, 149, 149, 19)
        'SPECIAL'
        >>> sort(150, 1, 1, 19)
        'SPECIAL'
        >>> sort(150, 1, 1, 20)
        'REJECTED'
        >>> sort(149, float('inf'), 149, 1)
        Traceback (most recent call last):
        ...
        ValueError: invalid measurements: (149, inf, 149, 1)
        >>> sort(149, 1, 149, -1)
        Traceback (most recent call last):
        ...
        ValueError: invalid measurements: (149, 1, 149, -1)
    """
    _validate_nonnegative_finite(width, height, length, mass)

    is_bulky = _check_bulky(width, height, length)
    is_heavy = _check_heavy(mass)

    return CATEGORIES[(is_bulky, is_heavy)]


if __name__ == '__main__':
    # keeping the testing simple
    import doctest
    doctest.testmod()
