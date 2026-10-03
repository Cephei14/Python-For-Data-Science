from load_csv import load
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter


def decode(text: str | float) -> float:
    """"""
    formats = {"k": 1e3, "M": 1e6, "B": 1e9}
    if isinstance(text, (int, float)):
        return float(text)
    text = text.strip()
    try:
        n = float(text)
    except ValueError:
        n = float(text[:-1])
    if text[-1] in formats:
        return n * formats[text[-1]]
    return n

def main():
    """The one"""
    try:
        data = load("population_total.csv")
        assert data is not None, "No data"
        mask = (data["country"] == "Japan") | (data["country"] == "Morocco")
        val = data.loc[mask, "1800":"2050"].values.tolist()
        idx = data.loc[mask, "1800":"2050"].index.tolist()
        x = [[decode(i)] for i in val[0]]
        y = [[decode(j)] for j in val[1]]
    except AssertionError as e:
        print(f"Error: {e}")
    years = list(range(1800, 2051))
    plt.plot(years, x, label="Japan")
    plt.plot(years, y, label="Morocco")
    plt.xlabel("Year")
    plt.ylabel("Population")
    plt.title("Population Projections")
    plt.gca().yaxis.set_major_formatter(EngFormatter(sep=""))
    plt.legend()
    plt.show()


    

if __name__ == "__main__":
    main()
