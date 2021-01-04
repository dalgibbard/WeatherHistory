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
# Time of day
timeofday = 12

# Get nearest station to location
stations = Stations()
stations = stations.nearby(lat, lon)
station = stations.inventory('daily', (start, end)).fetch(1)

df = Hourly(station, start, end).fetch() # returns a pandas dataframe

# Create a new dataframe containing only temperature values for midday, rounded to nearest int
newdf = df["temp"][(df.index.hour == timeofday) & (df.index.minute == 0)].round(decimals=0).astype(int)
# Print it for review
print(newdf)

# Output to Excel sheet
newdf.to_excel("2020-weather.xlsx", engine='xlsxwriter')
