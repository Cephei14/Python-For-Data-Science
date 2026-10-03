import pandas as pd


def load(path: str) -> pd.DataFrame | None:
    """Load a CSV file, print its dimensions and return the dataset."""
    try:
        data = pd.read_csv(path)
    except (OSError, ValueError, TypeError) as e:
        print(f"Error: {e}")
        return None
    if data.empty:
        print("Error: the dataset is empty.")
        return None
    return data
