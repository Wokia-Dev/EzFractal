import numba
import numpy
from numpy import uint8


def is_float(element: any) -> bool:
    if element is None:
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min(value, max_value), min_value)


@numba.njit(fastmath=True)
def iter_gradient_generator(num_iter: int, max_iter: int, saturation: float = 0.8, lightness: float = 0.5) -> [uint8,
                                                                                                               uint8,
                                                                                                               uint8]:
    if num_iter == max_iter:
        return [0, 0, 0]
    else:
        h = num_iter / max_iter
        c = (1 - numpy.abs(2 * lightness - 1)) * saturation
        x = c * (1 - numpy.abs((h * 6) % 2 - 1))
        m = lightness - c / 2
        if 0 <= h < 1 / 6:
            r, g, b = c + m, x + m, m
        elif 1 / 6 <= h < 1 / 3:
            r, g, b = x + m, c + m, m
        elif 1 / 3 <= h < 1 / 2:
            r, g, b = m, c + m, x + m
        elif 1 / 2 <= h < 2 / 3:
            r, g, b = m, x + m, c + m
        elif 2 / 3 <= h < 5 / 6:
            r, g, b = x + m, m, c + m
        else:
            r, g, b = c + m, m, x + m
    return [int(r * 255), int(g * 255), int(b * 255)]
