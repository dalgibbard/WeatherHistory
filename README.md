# WeatherHistory
Little python script to pull midday temperature for a given year, for every day in that year.

Uses the Meteostat Python library from [https://dev.meteostat.net/]

Edit the script to set co-ordinates, time of day, and start/end dates.


[WIP] Gooey-based UI
Issues:
* Output file doesn't add/set .xlsx if not set//no sanitisation on extension
* File picker wants to pick an existing file
* Building with nuitka (standalone) results in error calling python.exe [Gooey bug?]
* Doesn't work with Python3.9 (Gooey needs wxpython 4.1.0, and wheels for that only exist for 3.8 in ubuntu + Windows)