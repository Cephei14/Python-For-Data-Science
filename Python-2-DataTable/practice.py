import pandas as pd

def try_read(path: str)-> pd.DataFrame | None:
    """Return the DataFrame, or None if the file cannot be read."""
    try:
        f = pd.read_csv(path)
        return pd.DataFrame(f)
    except (OSError, ValueError, TypeError) as error:
        print(f"Error: {error}")
        return None

print(type(try_read("empty.csv")))
