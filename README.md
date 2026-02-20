# strava_activities
Get Strava activities through API and summarize

# Strava API
Refer to https://stravalib.readthedocs.io/en/v2.2/get-started/how-to-get-strava-data-python.html for setting up authentication

# Configuration
Change configuration in get_activities.py :
```python
### CONFIG ###
output_style = "summary"  # options are "summary" or "detailed"
first_activity_date = "2026-01-01"  # format YYYY-MM-DD - this is the date after which you want to pull activities. Change as needed.
FTP = 250
strava_api_url = "https://www.strava.com/api/v3"
### END OF CONFIG ###
```