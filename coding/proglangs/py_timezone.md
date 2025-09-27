# Turn a time-zone string into local system time, Python

Suppose you, based in the US, are going to join an online meeting in Beijing. You are given a specific Beijing time in advance, and you would like your computer to notify you one hour before the scheduled meeting time. In this case, you need a utility to **convert the Beijing meeting time to your local computer time**, so that you will receive notifications at the correct local time.

With PowerShell, it is pretty easy to use the built-in function `ConvertTime()` as follows:
```
$timeZoneData = @"
Beijing=China Standard Time
LA=Pacific Standard Time
local=Pacific Standard Time
"@

$timeZoneMap = ConvertFrom-StringData $timeZoneData

# timezone time ["9/27/2025 9:30 AM"] to local system (computer) time
function tzTime2LocalTime() 
{
	param (
		[string]$time_str,
		[string]$tz_city
    ) 
	
	[DateTime]$tzTime = New-Object DateTime
	[DateTime]::TryParse($time_str, [ref]$tzTime)
	"$tzTime [timezone time]`n"
	
	$srcTZone = [System.TimeZoneInfo]::FindSystemTimeZoneById($timeZoneMap[$tz_city])
	$localTZone = [System.TimeZoneInfo]::FindSystemTimeZoneById($timeZoneMap["local"])

	$localTime = [System.TimeZoneInfo]::ConvertTime($tzTime, $srcTZone, $localTZone)

	return $localTime
}
```

Unfortunately, it is not straightforward with Python, as there are no built-in methods to achieve this.

After searching online and researching with coding, I came up with a solution with a very simple idea, namely, **computing the hours difference between the local time zone and the source time zone and adding it to the naive source `datetime`**, which is easy to parse from a time string.

The method `hoursBtwLocal_tz2()` is as follows:
```
from datetime import datetime, timedelta

def hoursBtwLocal_tz2(timezone_city):
    """hours difference btw local and [zone2]"""   
    timezoneMap = {    # city to timezone name
        "New York": "America/New_York",
        "Los Angeles": "America/Los_Angeles",
        "London": "Europe/London",
        "Beijing": "Asia/Shanghai",
        "Tokyo": "Asia/Tokyo",
        "Sydney": "Australia/Sydney",
        "Paris": "Europe/Paris",
        "Dubai": "Asia/Dubai",
        "Mumbai": "Asia/Kolkata"
    }
    
    dtNow = datetime.now()  
    dtLocal = datetime.now(dtNow.astimezone().tzinfo)
    import pytz
    tzName = timezoneMap.get(timezone_city)
    tZone2 = pytz.timezone(tzName)       
    time2 = tZone2.localize(dtNow)

    hoursBtw = (dtLocal.utcoffset() - time2.utcoffset()).total_seconds() / 3600
    return hoursBtw
```
Then, the conversion becomes trivial:
```
def tzTime2LocalTime(date_i, tz_city) -> datetime:
    """timezone time to local system (computer) time
    Args:
        date-string [date_i="9/27/2025 9:30 AM"]
        zone-city [tz_city='Beijing']
    return: local computer datetime
    """
    from dateutil import parser
    dtIn = parser.parse(date_i)
    hoursBtw = hoursBtwLocal_tz2(tz_city)
    dtLocal = dtIn + timedelta(hours=hoursBtw)
    
    return dtLocal
```
I utilize `tzTime2LocalTime()` in my [personal daily event organizer](coming soon ...).

Feel free to copy my code for your own use.
