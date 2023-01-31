import numba
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
def iter_gradient_generator(num_iter, max_iter) -> [uint8, uint8, uint8]:
    if num_iter == max_iter:
        return [0, 0, 0]
    elif num_iter < max_iter / 3:
        return [
            uint8(255 * (num_iter / (max_iter / 3))),
            0,
            255,
        ]
    elif num_iter < 2 * max_iter / 3:
        return [
            255,
            uint8(255 * (1 - ((num_iter - max_iter / 3) / (max_iter / 3)))),
            255,
        ]
    else:
        return [
            255,
            255,
            uint8(255 * ((num_iter - 2 * max_iter / 3) / (max_iter / 3))),
        ]
