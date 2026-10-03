from load_csv import load
import matplotlib.pyplot as plt


def main():
    """Extract the years and life expectancies of one country,
    then Load the dataset and plot the life expectancy of a country."""
    try:
        data = load("life_expectancy_years.csv")
        assert data is not None, "No data"
        mask = data["country"] == "Qatar"
        rows = data[mask]
    except AssertionError as e:
        print(f"Error: {e}")
    if rows.empty:
        raise ValueError("Country 'Japan' not found.")
    series = rows.iloc[0].drop("country")
    years = [int(year) for year in series.index]
    values = [float(value) for value in series.values]
    plt.plot(years, values)
    plt.title("Japan Life expectancy Projections")
    plt.xlabel("Life expectancy")
    plt.ylabel("Year")
    plt.show()


if __name__ == "__main__":
    main()
