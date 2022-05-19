import json
import requests
import os
API_KEY = os.getenv('TBA_API_KEY')
from get_events import get_api_data

def save_team_details(team_number: str, team_details):
    
    updated_details = {}
    
    path = f'data/teams/{team_number}.json'
    # Get current file data
    with open(path, 'r') as file:
        # Read the current file data. If empty, mark data as empty dict
        try:
            data = json.load(file)
        except json.decoder.JSONDecodeError as e:
            data = {}

    # Update with more data 
    data[team_number] = updated_details
    
    # Write expanded data to file
    with open(path, 'w') as file:
        json.dump(data, file)  
    
teams = []
for i in range(30):    
    teams += get_api_data(f"/teams/2022/{i}/keys")
    
if __name__ == "__main__":
    for team in teams:
        event_keys = get_api_data(f"/team/{team}/events/2022/keys")
        print(f"Team: {team}\nEvents: {event_keys}")
        for event_key in event_keys:
            with open(f'./data/events/{event_key}.json', 'r') as file:
                # All matches at that event
                data = json.load(file)
                
            matches = list(filter(lambda x: team in [x['blue']['teams'] + x['red']['teams']], data.values()))
            print(matches)
            input()
            

