| # | Where | What it checks | Code | Raises |
|---|---|---|---|---|
| 1 | `_check_numbers` | Argument is a list | `if not isinstance(values, list):` | `TypeError` |
| 2 | `_check_numbers` | Every element is an `int` or `float` (bools rejected) | `if isinstance(v, bool) or not isinstance(v, (int, float)):` | `TypeError` |
| 3 | `_check_numbers` | No `nan` or `inf` values | `if not np.isfinite(v):` | `ValueError` |
| 4 | `give_bmi` | Height and weight lists have the same length | `if len(height) != len(weight):` | `ValueError` |
| 5 | `give_bmi` | No unrealistic values (height or weight below 1) | `if any(h < 1 or w < 1 for h, w in zip(height, weight)):` | `ValueError` |
| 6 | `apply_limit` | `limit` is an `int` (bools rejected) | `if isinstance(limit, bool) or not isinstance(limit, int):` | `TypeError` |

Checks 1 to 3 run inside `_check_numbers`, which is called in three places:

| Call | Validates |
|---|---|
| `_check_numbers(height, "height")` | the `height` list (in `give_bmi`) |
| `_check_numbers(weight, "weight")` | the `weight` list (in `give_bmi`) |
| `_check_numbers(bmi, "bmi")` | the `bmi` list (in `apply_limit`) |

The order in `give_bmi` matters: types are checked first (checks 1 to 3 for both lists), then the length (4), then the value range (5). This way a string in the list gives a clear `TypeError` instead of crashing on a comparison like `"a" < 1`.