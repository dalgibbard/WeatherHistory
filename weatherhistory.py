from datetime import datetime, timedelta
from meteostat import Stations
import xlsxwriter
from meteostat.hourly import Hourly
import sys
from gooey import Gooey, GooeyParser
import requests
import urllib.parse
import os

'''
Get the temperatures for a given location, between two dates, at a certain time
- Example below is 1/1/2020 -> 31/12/2020  at midday.
- Temperatures rounded appropriately to integers, and displayed in Celcius
'''

# Start / End dates
# start = datetime(2021, 1, 15)
# end = datetime(2021, 2, 8)
# # Geographic co-ordinates (Basildon, UK)
# lat, lon = (51.5761, 0.4887)
# # Time of day


def lookup_location(location):
    url = f'https://nominatim.openstreetmap.org/search/{urllib.parse.quote(location)}?format=json'
    response = requests.get(url).json()
    lat = response[0]["lat"]
    lon = response[0]["lon"]
    # Return tuple lat long
    return lat, lon


def run(location, start, end, outputfile, timeofday):
    Hourly.cache_dir = "/tmp/weather_cache"
    lat, lon = lookup_location(location)

    df = getStation(lat, lon, start, end)
    print(df)

    # Create a new dataframe containing only temperature values for midday, rounded to nearest int
    newdf = df["temp"][(df.index.hour == timeofday) & (df.index.minute == 0)].round(decimals=0).astype(int)
    # Print it for review
    print(newdf)

    # Output to Excel sheet
    if outputfile is not None:
        newdf.to_excel("2020-weather.xlsx", engine='xlsxwriter')


# Get nearest station to location
# If no data received, shorten end date until data is available
def getStation(lat, lon, start, end):
    print(f"Start: {start}, End: {end}")
    stations = Stations()
    stations = stations.nearby(lat, lon)
    foundstation = stations.inventory('daily', (start, end)).fetch(1)
    stuff = Hourly(foundstation, start, end)
    df = stuff.fetch()  # returns a pandas dataframe
    if df.empty:
        print("No data in the query, reducing end date until matches show")
        end = end - timedelta(days=1)
        if end <= start:
            print("No matches for time query!")
            sys.exit(1)
        return getStation(start, end)
    else:
        return df


@Gooey
def main():
    if "linux" in sys.platform and os.environ.get("DISPLAY") is None:
        print("Need a valid DISPLAY set!")
        sys.exit(1)

    parser = GooeyParser(description="Historical temperature finder, for a certain time of day")
    parser.add_argument('start', required=True, type=datetime, widget="DateChooser", help="Start Date")
    parser.add_argument('end', required=True, type=datetime, widget="DateChooser", help="End Date")
    parser.add_argument('output_file', required=False, widget="FileChooser", type=str, help="Output File Name")
    parser.add_argument('location', required=True, default="Basildon, UK", type=str, help="Location to weather search")
    parser.add_argument('timeofday', required=True, default=12, type=int)
    args = parser.parse_args()
    run(args.location, args.start, args.end, args.location, args.timeofday)


if __name__ == "__main__":
    main()
