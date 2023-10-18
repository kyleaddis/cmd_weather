import argparse
import requests
import zip_lookup
from rich import print
from rich.console import Console
from rich.table import Table


def get_forecast_url(zip_code: str):
    lat, long = zip_lookup.find_zip(zip_code)
    api_url = f"https://api.weather.gov/points/{lat},{long}"
    try:
        response = requests.get(api_url)
        return response.json()["properties"]["forecast"]
    except requests.exceptions.RequestException as e:
        print(f"Error making the API request: {e}")


def get_weather(forecast_url: str):
    try:
        response = requests.get(forecast_url)
        if response.status_code == 200:
            data_to_columns(response.json()["properties"])
        else:
            print(f"API request failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error making the API request: {e}")


def data_to_columns(data):
    table = Table(title="Weather forcast", show_header=True)
    table.add_column("Day", vertical="middle")
    table.add_column("Temperature", vertical="middle")
    table.add_column("Wind Speed", vertical="middle")
    table.add_column("Forecast", max_width=50, vertical="middle")
    for d in data["periods"]:
        table.add_row(
            d["name"], str(d["temperature"]), str(d["windSpeed"]), d["detailedForecast"]
        )
    console = Console()
    console.print(table, justify="center")


def main():
    parser = argparse.ArgumentParser(description="Check the weather by zip code.")
    parser.add_argument("zip_code", type=str, help="zip code")

    args = parser.parse_args()
    url = get_forecast_url(args.zip_code)

    if url:
        (get_weather(url))


if __name__ == "__main__":
    main()
