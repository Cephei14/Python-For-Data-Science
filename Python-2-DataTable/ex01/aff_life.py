from load_csv import load
import matplotlib.pyplot as plt


def main():
    """Load the dataset and plot the life expectancy of Japan."""
    data = load("life_expectancy_years.csv")
    if data is None:
        return
    try:
        rows = data[data["country"] == "Japan"]
    except KeyError as e:
        print(f"Error: missing column {e}")
        return
    if rows.empty:
        print("Error: country 'Japan' not found.")
        return
    series = rows.iloc[0].drop("country")
    try:
        years = [int(year) for year in series.index]
        values = [float(value) for value in series.values]
    except ValueError as e:
        print(f"Error: bad data format ({e})")
        return
    plt.plot(years, values)
    plt.title("Japan Life expectancy Projections")
    plt.xlabel("Year")
    plt.ylabel("Life expectancy")
    plt.show()


if __name__ == "__main__":
    main()
