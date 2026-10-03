from load_csv import load
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter


def decode(text: str | float) -> float:
    """Convert values like '1.2k', '3M', '2B' to float. Invalid -> nan."""
    formats = {"k": 1e3, "M": 1e6, "B": 1e9}
    if isinstance(text, (int, float)):
        return float(text)
    text = text.strip()
    try:
        if text and text[-1] in formats:
            return float(text[:-1]) * formats[text[-1]]
        return float(text)
    except ValueError:
        return float("nan")


def main():
    """Plot the population of Japan versus Morocco from 1800 to 2050."""
    data = load("population_total.csv")
    if data is None:
        return
    curves = {}
    years = []
    try:
        for country in ("Japan", "Morocco"):
            row = data.loc[data["country"] == country, "1800":"2050"]
            if row.empty:
                print(f"Error: country '{country}' not found.")
                return
            years = [int(col) for col in row.columns]
            curves[country] = [decode(v) for v in row.iloc[0]]
    except KeyError as e:
        print(f"Error: missing column {e}")
        return
    for country, values in curves.items():
        plt.plot(years, values, label=country)
    plt.xlabel("Year")
    plt.ylabel("Population")
    plt.title("Population Projections")
    plt.gca().yaxis.set_major_formatter(EngFormatter(sep=""))
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
