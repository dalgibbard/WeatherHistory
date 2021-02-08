from datetime import datetime, timedelta
from meteostat import Stations
import xlsxwriter
from meteostat.hourly import Hourly
import sys

'''
Get the temperatures for a given location, between two dates, at a certain time
- Example below is 1/1/2020 -> 31/12/2020  at midday.
- Temperatures rounded appropriately to integers, and displayed in Celcius
'''

#Hourly.cache_dir = "/tmp/weather_cache"

# Start / End dates
start = datetime(2021, 1, 15)
end = datetime(2021, 2, 8)
# Geographic co-ordinates (Basildon, UK)
lat, lon = (51.5761, 0.4887)
# Time of day
timeofday = 12

# Get nearest station to location
# If no data received, shorten end date until data is available
def getStation(start, end):
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

df = getStation(start, end)

print(df)

# Create a new dataframe containing only temperature values for midday, rounded to nearest int
newdf = df["temp"][(df.index.hour == timeofday) & (df.index.minute == 0)].round(decimals=0).astype(int)
# Print it for review
print(newdf)

# Output to Excel sheet
newdf.to_excel("2020-weather.xlsx", engine='xlsxwriter')
