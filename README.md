# strava_activities
Get Strava activities through API and summarize

# Example
## output style "summary"
```
2026-02-13T12:04:14Z | "Course à pied le midi" (Run) | 00:50:02 | 7.92km | 5m elev gain. Avg speed 9.49kph, pace 06:19/km. Avg HR 130.1bpm, max 145.0bpm. Avg cadence 174.4spm. Effort 740.8kJ. Suffer score 11.0.
2026-02-14T07:12:04Z | "Entraînement aux poids le matin" (WeightTraining) | 00:07:22. Avg HR 109.6bpm, max 148.0bpm. Suffer score 1.0.
2026-02-14T08:00:31Z | "Natation club 🟡⚫️" (Swim) | 00:30:15 | 1725m. Avg pace 01:45/100m. Avg HR 117.4bpm, max 146.0bpm. Suffer score 9.0.
```
## output style "detailed"
```
🏃 STRAVA ACTIVITY SUMMARY
==========================
                            
📋 ACTIVITY:
Date: 2026-02-13T12:04:14Z
Name: Course à pied le midi
Type: Run

📊 DISTANCE & TIME:
Distance: 7.92km
Elevation: 5m
Moving Time: 00:50:02

❤️ HEART RATE:
Average: 130.1bpm
Max: 145.0bpm

⚡ PERFORMANCE:
Avg Speed: 9.49km/h
Avg pace: 06:19/km
Cadence: 174.4spm
Effort: 740.8kJ
Suffer Score: 11.0

🎯 DEVICE & LINK:
Device: Garmin Forerunner 965
URL: https://www.strava.com/activities/17383130286

🏋️ STRAVA ACTIVITY SUMMARY
==========================
                            
📋 ACTIVITY:
Date: 2026-02-14T07:12:04Z
Name: Entraînement aux poids le matin
Type: WeightTraining

📊 DISTANCE & TIME:
Moving Time: 00:07:22

❤️ HEART RATE:
Average: 109.6bpm
Max: 148.0bpm

⚡ PERFORMANCE:
Suffer Score: 1.0

🎯 DEVICE & LINK:
Device: Garmin Forerunner 965
URL: https://www.strava.com/activities/17390764214

🏊 STRAVA ACTIVITY SUMMARY
==========================
                            
📋 ACTIVITY:
Date: 2026-02-14T08:00:31Z
Name: Natation club 🟡⚫️
Type: Swim

📊 DISTANCE & TIME:
Distance: 1725m
Moving Time: 00:30:15

❤️ HEART RATE:
Average: 117.4bpm
Max: 146.0bpm

⚡ PERFORMANCE:
Avg pace: 01:45/100m
Suffer Score: 9.0

🎯 DEVICE & LINK:
Device: Garmin Forerunner 965
URL: https://www.strava.com/activities/17391086739
```

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