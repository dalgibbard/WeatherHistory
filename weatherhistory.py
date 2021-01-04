from datetime import datetime
from meteostat import Stations
import xlsxwriter
from meteostat.hourly import Hourly

'''
Get the temperatures for a given location, between two dates, at a certain time
- Example below is 1/1/2020 -> 31/12/2020  at midday.
- Temperatures rounded appropriately to integers, and displayed in Celcius
'''

Hourly.cache_dir = "/tmp/weather_cache"

# Start / End dates
start, end = (datetime(2020, 1, 1), datetime(2020, 12, 31))
# Geographic co-ordinates (Basildon, UK)
lat, lon = (51.5761, 0.4887)

# Get nearest station to location
stations = Stations()
stations = stations.nearby(lat, lon)
stations = stations.inventory('daily', (start, end))
station = stations.fetch(1)

df = Hourly(station, start, end)
df = df.fetch()  # returns a pandas dataframe

# Add columns for hour / minute in the dataframe, from the 'time' index.
df["hour"] = df.index.hour
df["minute"] = df.index.minute

# Create a new dataframe containing only values for midday
newdf = df[(df.hour == 12) & (df.minute == 0)]
# Create a new dataframe of midday timing, containing only the temperature, rounded, as integers.
temps = newdf["temp"].round(decimals=0).astype(int)
# Print it for review
print(temps)

# Output to Excel sheet
temps.to_excel("2020-weather.xlsx", engine='xlsxwriter')
