#!env python

# You will use this to log in to your Strava account
import webbrowser
from stravalib.client import Client

import json
import os
import requests
import time
import sys

### CONFIG ###
output_style = "detailed"  # options are "summary" or "detailed"
first_activity_date = "2026-01-01"  # format YYYY-MM-DD - this is the date after which you want to pull activities. Change as needed.
FTP = 250 # this is your Functional Threshold Power in watts - change as needed for accurate FTP% calculations. If you don't have an FTP, you can set this to 1 to avoid errors, but the FTP% values will not be meaningful.
strava_api_url = "https://www.strava.com/api/v3" # this is the base URL for the Strava API - it should not need to be changed, but you can change it if you want to use a different version of the API or a different endpoint.
### END OF CONFIG ###

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Open the secrets file and store the client ID and client secret as objects, separated by a comma
# Read below to learn how to set up the app that provides you with the client ID
# and the client secret
client_id, client_secret = open("client_secrets.txt").read().strip().split(",")

# Create a client object
client = Client()

# Define your scope (this is read-only - see below for a "write" example which
# allows you to update activities and publish new activities to your Strava account).
# read_all allows read access for both private and public activities
request_scope = ["read_all", "profile:read_all", "activity:read_all"]

# Create a localhost URL for authorization (for local development)
redirect_url = "http://127.0.0.1:5000/authorization"

# Create authorization url; your app client_id required to authorize
url = client.authorization_url(
    client_id=client_id,
    redirect_uri=redirect_url,
    scope=request_scope,
)

token_path = 'token.json'

if not os.path.exists(token_path):
    # Open the URL in a web browser
    webbrowser.open(url)

    eprint(
        """You will see a url that looks like this. """,
        """http://127.0.0.1:5000/authorization?state=&code=12323423423423423423423550&scope=read,activity:read_all,profile:read_all,read_all")""",
        """Copy the values between code= and & in the url that you see in the
    browser. """,
    )
    # Using input allows you to copy the code into your Python console
    # (or Jupyter Notebook)
    code = input("Please enter the code that you received: ")
    eprint(
        f"Great! Your code is {code}\n"
        "Next, I will exchange that code for a token.\n"
        "I only have to do this once."
    )

    # Exchange the code returned from Strava for an access token
    token_response = client.exchange_code_for_token(
        client_id=client_id, client_secret=client_secret, code=code
    )

    # Save the token response as a JSON file
    with open(token_path, "w") as f:
        json.dump(token_response, f)

    eprint("Token saved - hooray!")
else:
    eprint("Token already saved - loading from file.")
    # Open the token JSON file that you saved earlier
    with open(token_path, "r") as f:
        token_response = json.load(f)
    
    refresh_response = client.refresh_access_token(
        client_id=client_id,  # Stored in the secrets.txt file above
        client_secret=client_secret,
        refresh_token=token_response["refresh_token"],  # Stored in your JSON file
    )

    with open(token_path, "w") as f:
        json.dump(refresh_response, f)

    eprint("Refreshed token saved - hooray!")

    token_response = refresh_response
    
headers = {
    "Authorization": f"Bearer {token_response['access_token']}",
    "Accept": "application/json"
}
activities_json_path = "activities.json"

if not os.path.exists(activities_json_path):
    first_activity_epoch = int(time.mktime(time.strptime(first_activity_date, "%Y-%m-%d")))
    response = requests.get(f"{strava_api_url}/athlete/activities?after={first_activity_epoch}&per_page=200", headers=headers)
    with open(activities_json_path, "w") as f:
        f.write(response.text)
    activities_json = response.json()
else:
    eprint("Activities JSON already saved - loading from file.")
    with open(activities_json_path, "r") as f:
        activities_json = json.load(f)

for i, activity in enumerate(activities_json):
    # Variables for all activities - these will be used in the summary and detailed outputs below. If a variable is not present in the activity data, it will be set to "N/A" to avoid errors.
    ACT_start_date = activity['start_date_local'] if 'start_date_local' in activity else "N/A"
    ACT_name = activity['name'] if 'name' in activity else "N/A"
    ACT_sport = activity['sport_type'] if 'sport_type' in activity else "N/A"
    ACT_distance_m = round(activity['distance']) if 'distance' in activity else "N/A"
    ACT_distance_km = round(activity['distance']/1000, 2) if 'distance' in activity else "N/A"
    ACT_elevation = round(activity['total_elevation_gain']) if 'total_elevation_gain' in activity else "N/A"
    ACT_moving_time = time.strftime('%H:%M:%S', time.gmtime(activity['moving_time'])) if 'moving_time' in activity else "N/A"
    ACT_avg_speed = round(activity['average_speed']*3.6, 2) if 'average_speed' in activity else "N/A"
    ACT_max_speed = round(activity['max_speed']*3.6, 2) if 'max_speed' in activity else "N/A"
    ACT_avg_pace_pkm = time.strftime('%M:%S', time.gmtime((activity['moving_time']/activity['distance'])*1000)) if 'moving_time' in activity and 'distance' in activity and activity['distance'] > 0 else "N/A"
    ACT_avg_pace_p100m = time.strftime('%M:%S', time.gmtime((activity['moving_time']/activity['distance'])*100)) if 'moving_time' in activity and 'distance' in activity and activity['distance'] > 0 else "N/A"
    ACT_avg_hr = activity['average_heartrate'] if 'average_heartrate' in activity else "N/A"
    ACT_max_hr = activity['max_heartrate'] if 'max_heartrate' in activity else "N/A"
    ACT_avg_watts = activity['average_watts'] if 'average_watts' in activity else "N/A"
    ACT_avg_FTP_percent = round((ACT_avg_watts/FTP)*100) if ACT_avg_watts != "N/A" else "N/A"
    ACT_max_watts = activity['max_watts'] if 'max_watts' in activity else "N/A"
    ACT_max_FTP_percent = round((ACT_max_watts/FTP)*100) if ACT_max_watts != "N/A" else "N/A"
    ACT_cadence_rpm = activity['average_cadence'] if 'average_cadence' in activity else "N/A"
    ACT_cadence_spm = activity['average_cadence']*2 if 'average_cadence' in activity else "N/A"
    ACT_kilojoules = activity['kilojoules'] if 'kilojoules' in activity else "N/A"
    ACT_suffer_score = activity['suffer_score'] if 'suffer_score' in activity else "N/A"

    if ACT_sport == "Ride" or ACT_sport == "VirtualRide":
        if output_style == "summary":
            print(f"{ACT_start_date} | \"{ACT_name}\" ({ACT_sport}) | {ACT_moving_time} | {ACT_distance_km}km | {ACT_elevation}m elev gain. Avg speed {ACT_avg_speed}kph, max {ACT_max_speed}kph. Avg HR {ACT_avg_hr}bpm, max {ACT_max_hr}bpm. Avg power {ACT_avg_watts}W ({ACT_avg_FTP_percent}% FTP), max {ACT_max_watts}W ({ACT_max_FTP_percent}% FTP). Avg cadence {ACT_cadence_rpm}rpm. Effort {ACT_kilojoules}kJ. Suffer score {ACT_suffer_score}.")
        else:
            print(f"""🚴 STRAVA ACTIVITY SUMMARY
==========================
                            
📋 ACTIVITY:
Date: {ACT_start_date}
Name: {ACT_name}
Type: {ACT_sport}

📊 DISTANCE & TIME:
Distance: {ACT_distance_km}km
Elevation: {ACT_elevation}m
Moving Time: {ACT_moving_time}

❤️ HEART RATE:
Average: {ACT_avg_hr}bpm
Max: {ACT_max_hr}bpm

⚡ PERFORMANCE:
Avg Speed: {ACT_avg_speed}km/h
Max Speed: {ACT_max_speed}km/h
Avg Watts: {ACT_avg_watts}W ({ACT_avg_FTP_percent}% FTP)
Max Watts: {ACT_max_watts}W ({ACT_max_FTP_percent}% FTP)
Cadence: {ACT_cadence_rpm}rpm
Effort: {ACT_kilojoules}kJ
Suffer Score: {ACT_suffer_score}

🎯 DEVICE & LINK:
Device: {activity['device_name'] if 'device_name' in activity else "N/A"}
URL: https://www.strava.com/activities/{activity['id']}
""")
    if ACT_sport == "Run":
        if output_style == "summary":
            print(f"{ACT_start_date} | \"{ACT_name}\" ({ACT_sport}) | {ACT_moving_time} | {ACT_distance_km}km | {ACT_elevation}m elev gain. Avg speed {ACT_avg_speed}kph, pace {ACT_avg_pace_pkm}/km. Avg HR {ACT_avg_hr}bpm, max {ACT_max_hr}bpm. Avg cadence {ACT_cadence_spm}spm. Effort {ACT_kilojoules}kJ. Suffer score {ACT_suffer_score}.")
        else:
            print(f"""🏃 STRAVA ACTIVITY SUMMARY
==========================
                            
📋 ACTIVITY:
Date: {ACT_start_date}
Name: {ACT_name}
Type: {ACT_sport}

📊 DISTANCE & TIME:
Distance: {ACT_distance_km}km
Elevation: {ACT_elevation}m
Moving Time: {ACT_moving_time}

❤️ HEART RATE:
Average: {ACT_avg_hr}bpm
Max: {ACT_max_hr}bpm

⚡ PERFORMANCE:
Avg Speed: {ACT_avg_speed}km/h
Avg pace: {ACT_avg_pace_pkm}/km
Cadence: {ACT_cadence_spm}spm
Effort: {ACT_kilojoules}kJ
Suffer Score: {ACT_suffer_score}

🎯 DEVICE & LINK:
Device: {activity['device_name'] if 'device_name' in activity else "N/A"}
URL: https://www.strava.com/activities/{activity['id']}
""")
    if ACT_sport == "Swim":
        if output_style == "summary":
            print(f"{ACT_start_date} | \"{ACT_name}\" ({ACT_sport}) | {ACT_moving_time} | {ACT_distance_m}m. Avg pace {ACT_avg_pace_p100m}/100m. Avg HR {ACT_avg_hr}bpm, max {ACT_max_hr}bpm. Suffer score {ACT_suffer_score}.")
        else:
            print(f"""🏊 STRAVA ACTIVITY SUMMARY
==========================
                            
📋 ACTIVITY:
Date: {ACT_start_date}
Name: {ACT_name}
Type: {ACT_sport}

📊 DISTANCE & TIME:
Distance: {ACT_distance_m}m
Moving Time: {ACT_moving_time}

❤️ HEART RATE:
Average: {ACT_avg_hr}bpm
Max: {ACT_max_hr}bpm

⚡ PERFORMANCE:
Avg pace: {ACT_avg_pace_p100m}/100m
Suffer Score: {ACT_suffer_score}

🎯 DEVICE & LINK:
Device: {activity['device_name'] if 'device_name' in activity else "N/A"}
URL: https://www.strava.com/activities/{activity['id']}
""")
    if ACT_sport == "TableTennis":

        if output_style == "summary":
            print(f"{ACT_start_date} | \"{ACT_name}\" ({ACT_sport}) | {ACT_moving_time}. Avg HR {ACT_avg_hr}bpm, max {ACT_max_hr}bpm. Suffer score {ACT_suffer_score}.")
        else:
            print(f"""🏓 STRAVA ACTIVITY SUMMARY
==========================
                            
📋 ACTIVITY:
Date: {ACT_start_date}
Name: {ACT_name}
Type: {ACT_sport}

📊 DISTANCE & TIME:
Moving Time: {ACT_moving_time}

❤️ HEART RATE:
Average: {ACT_avg_hr}bpm
Max: {ACT_max_hr}bpm

⚡ PERFORMANCE:
Suffer Score: {ACT_suffer_score}

🎯 DEVICE & LINK:
Device: {activity['device_name'] if 'device_name' in activity else "N/A"}
URL: https://www.strava.com/activities/{activity['id']}
""")
    if ACT_sport == "WeightTraining":
        if output_style == "summary":
            print(f"{ACT_start_date} | \"{ACT_name}\" ({ACT_sport}) | {ACT_moving_time}. Avg HR {ACT_avg_hr}bpm, max {ACT_max_hr}bpm. Suffer score {ACT_suffer_score}.")
        else:
            print(f"""🏋️ STRAVA ACTIVITY SUMMARY
==========================
                            
📋 ACTIVITY:
Date: {ACT_start_date}
Name: {ACT_name}
Type: {ACT_sport}

📊 DISTANCE & TIME:
Moving Time: {ACT_moving_time}

❤️ HEART RATE:
Average: {ACT_avg_hr}bpm
Max: {ACT_max_hr}bpm

⚡ PERFORMANCE:
Suffer Score: {ACT_suffer_score}

🎯 DEVICE & LINK:
Device: {activity['device_name'] if 'device_name' in activity else "N/A"}
URL: https://www.strava.com/activities/{activity['id']}
""")