import json
from pprint import pprint
import requests
import os
API_KEY = os.getenv('TBA_API_KEY')

def save_match_details(event_id, match_id, match_details):
        
    updated_details = {
        "post_result_time": match_details['post_result_time'],
        "game_start_time": match_details['actual_time'],
        "blue": {
            "teams": match_details['alliances']['blue']['team_keys'],
            "score": match_details['alliances']['blue']['score']
            },
        "red": {
            "teams": match_details['alliances']['red']['team_keys'],
            "score": match_details['alliances']['red']['score']
        },  
        "result": match_details['winning_alliance']
    }
    
    if None in updated_details.values():
        return
    
    path = f'data/events/{event_id}.json'
    # Get current file data
    with open(path, 'r') as file:
        # Read the current file data. If empty, mark data as empty dict
        try:
            data = json.load(file)
        except json.decoder.JSONDecodeError as e:
            data = {}

    # Update with more data 
    data[match_id] = updated_details
    
    # Write expanded data to file
    with open(path, 'w') as file:
        json.dump(data, file)  
        
def get_api_data(api_extension):
    # Request data from BlueALliance API
    data = json.loads(requests.get(f'https://www.thebluealliance.com/api/v3/{api_extension}', headers={'X-TBA-Auth-Key': API_KEY}).text)
    return data

# If this file is being run and not imported to somewhere else, run the following
if __name__ == "__main__":

    events = get_api_data("events/2019")

    total_matches = 0
    for count, event in enumerate(events):
        # Clear event file
        path = f'./data/events/{event["event_code"]}.json'
        # Make sure the directory exists (create if it doesn't)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        # Delete file contents because of using write only mode
        with open(path, 'w') as file: pass
            
        print(f"{count+1}/{len(events)} | Event: {event['name']}")
        matches = get_api_data(f"event/{event['key']}/matches")
        
        # Sort matches by order of time, NOT number
        matches = list(filter(lambda x: x['predicted_time'] != None, matches))
        matches.sort(key=lambda x: x['predicted_time'])
        total_matches += len(matches)
        
        for match in matches:

            red_teams = match['alliances']['red']['team_keys']
            blue_teams = match['alliances']['blue']['team_keys']

            # print(f"\tMatch: {match['key'].split('_')[1]}")
            save_match_details(event['event_code'], match['key'], match)
            
    print(f"Total Matches: {total_matches}")
