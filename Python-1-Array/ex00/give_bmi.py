import numpy as np


def _check_numbers(values, name: str) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be a list")
    for v in values:
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            raise TypeError(f"{name} must contain only int or float")
        if not np.isfinite(v):
            raise ValueError(f"{name} contains a non-finite value")


def give_bmi(height: list[int | float],
             weight: list[int | float]) -> list[int | float]:
    """Return the BMI (weight / height^2) for each height/weight pair."""
    _check_numbers(height, "height")
    _check_numbers(weight, "weight")
    if len(height) != len(weight):
        raise ValueError("lists must be the same length")
    if any(h < 1 or w < 1 for h, w in zip(height, weight)):
        raise ValueError("Unrealistic value(s)")
    h_arr = np.array(height, dtype=float)
    w_arr = np.array(weight, dtype=float)
    return (w_arr / (h_arr ** 2)).tolist()


def apply_limit(bmi: list[int | float], limit: int) -> list[bool]:
    """Return True for each BMI value strictly above the limit."""
    _check_numbers(bmi, "bmi")
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise TypeError("limit must be an int")
    return [bool(v > limit) for v in bmi]
