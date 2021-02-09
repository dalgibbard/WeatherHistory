# WeatherHistory
Little python UI applet to lookup historical temperatures, at a particular time of day, within a date range.

Uses the Meteostat Python library from [https://dev.meteostat.net/] for weather data.

[WIP] Gooey-based UI
Known Issues:
* Forced UI use with Gooey, not great for testing on command line etc 
* Output file doesn't add/set .xlsx if not set[untested] // no sanitisation on extension
* Doesn't work with Python3.9 (Gooey needs wxpython 4.1.0, and wheels for that only exist for 3.8 in ubuntu + Windows; fails to build otherwise)