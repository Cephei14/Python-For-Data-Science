def render_bar(x: int, width: int = 64) -> str:
    """Build the progress bar string for percentage x."""
    p = ""
    if x == 0:
        return p
    for n in range(0, width - 1, 1):
        if ((n / (width - 1)) * 100) > x:
            break
        p += "="
    if p:
        p += ">"
    return p


def ft_tqdm(lst: range):
    """Decorate an iterable with a visual progress bar."""
    total = len(lst)
    if total == 0:
        return
    for n, elem in enumerate(lst, 1):
        x = int((n / total) * 100)
        p = render_bar(x, 64)
        print(f"\r{x:3d}%|[{p:64}]| {n}/{total}", end="", flush=True)
        yield elem
