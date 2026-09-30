def is_rectangular(table):
    """Check that table is a list of lists whose rows have equal length."""
    if not isinstance(table, list):
        return False
    if not all(isinstance(row, list) for row in table):
        return False
    return all(len(row) == len(table[0]) for row in table)


def shape_of(table):
    """shape of table"""
    return (len(table), len(table[0]) if table else 0)


def slice_me(family: list, start: int, end: int) -> list | None:
    """Prints shape and returns the sliced table"""
    try:
        if not is_rectangular(family):
            raise ValueError("input must be a 2D list with equal-sized rows")
        for v in (start, end):
            if isinstance(v, bool) or not isinstance(v, int):
                raise TypeError("start and end must be integers")
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")
        return None
    print(f"My shape is : {shape_of(family)}")
    sliced = family[start:end]
    print(f"My new shape is : {shape_of(sliced)}")
    return sliced
