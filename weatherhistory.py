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
    print(f"Location Lookup: {location}\n Result -- lat: {lat} | lon: {lon}")
    return float(lat), float(lon)


def run(location, start, end, outputfile, timeofday):
    Hourly.cache_dir = ".weather_cache"
    lat, lon = lookup_location(location)

    df = getStation(lat, lon, start, end)
    # print(df)

    # Create a new dataframe containing only temperature values for midday, rounded to nearest int
    newdf = df["temp"][(df.index.hour == timeofday) & (df.index.minute == 0)].round(decimals=0).astype(int)
    # Print it for review
    print(newdf)

    # Output to Excel sheet
    print(f"Creating Output File: {outputfile}")
    newdf.to_excel(outputfile, engine='xlsxwriter')


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
        return getStation(lat, lon, start, end)
    else:
        return df


@Gooey(target="weatherhistory.exe")
def main():
    # TODO: Write to file what our script name is, so we can set the decorator target accordingly
    if "linux" in sys.platform and os.environ.get("DISPLAY") is None:
        print("Need a valid DISPLAY set!")
        sys.exit(1)

    parser = GooeyParser(description="Historical temperature finder, for a certain time of day")
    parser.add_argument('start', type=str, widget="DateChooser", help="Start Date")
    parser.add_argument('end', type=str, widget="DateChooser", help="End Date")
    parser.add_argument('outputfile', widget="FileSaver", default="output.xlsx", gooey_options=dict(wildcard="Excel Spreadsheet (*.xlsx)|*.xlsx"), type=str, help="Output File Name")
    parser.add_argument('location', default="Basildon, UK", type=str, help="Location to weather search")
    parser.add_argument('timeofday', default=12, type=int, help="Time of day (hour) to report time for")
    args = parser.parse_args()
    sl = args.start.split("-")
    start = datetime(int(sl[0]), int(sl[1]), int(sl[2]))
    el = args.end.split("-")
    end = datetime(int(el[0]), int(el[1]), int(el[2]))
    run(args.location, start, end, args.outputfile, args.timeofday)


if __name__ == "__main__":
    main()
