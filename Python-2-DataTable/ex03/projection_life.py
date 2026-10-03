from load_csv import load
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter


def decode(text: str | float) -> float:
    """Convert values like '1.2k', '3M', '2B' to float. Invalid -> nan."""
    formats = {"k": 1e3, "M": 1e6}
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
    """The one"""
    income = load("income_per_person_gdppercapita_ppp_inflation_adjusted.csv")
    life = load("life_expectancy_years.csv")
    if income is None or life is None:
        print("Error: could not load the data")
        return

    try:
        data = income[["country", "1900"]].merge(
            life[["country", "1900"]],
            on="country",
            suffixes=("_income", "_life"),
        )
    except KeyError as e:
        print(f"Error: missing column {e}")
        return

    data["x"] = data["1900_income"].map(decode)
    data["y"] = data["1900_life"].map(decode)
    data = data.dropna(subset=["x", "y"])
    data = data[data["x"] > 0]
    if data.empty:
        print("Error: no valid data for 1900")
        return

    plt.scatter(data["x"], data["y"])
    plt.xscale("log")
    plt.xlabel("Gross domestic product")
    plt.ylabel("Life expectancy")
    plt.title("1900")
    plt.gca().xaxis.set_major_formatter(EngFormatter(sep=""))
    plt.show()


if __name__ == "__main__":
    main()
