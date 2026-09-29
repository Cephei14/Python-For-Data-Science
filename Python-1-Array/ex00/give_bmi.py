import numpy as np


def give_bmi(height: list[int | float], weight: list[int | float]) -> list[int | float]:
    """here"""
    if len(height) != len(weight):
        raise ValueError("lists must be the same length")
    for w, h in zip(weight, height):
        if h < 1 or w < 1:
            raise ValueError("Unrealistic value(s)")
    h = np.array(height)
    w = np.array(weight)
    return (w / (h ** 2)).tolist()


def apply_limit(bmi: list[int | float], limit: int) -> list[bool]:
    """here"""
    return [v > limit for v in bmi]
