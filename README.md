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
FTP = 250 # this is your Functional Threshold Power in watts - change as needed for accurate FTP% calculations. If you don't have an FTP, you can set this to 1 to avoid errors, but the FTP% values will not be meaningful.
strava_api_url = "https://www.strava.com/api/v3" # this is the base URL for the Strava API - it should not need to be changed, but you can change it if you want to use a different version of the API or a different endpoint.
### END OF CONFIG ###
```