import json
import requests
import os
API_KEY = os.getenv('TBA_API_KEY')
from get_events import get_api_data

def save_team_details(team_key, team_matches):
    path = f'data/teams/{team_key}.json'
    
    # Make sure the directory exists (create if it doesn't)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Overwrite file with new data
    with open(path, 'w') as file:
        json.dump(team_matches, file)  
        
def get_team_matches(team_key):        
    team_matches = {}
    
    event_keys = get_api_data(f"/team/{team_key}/events/2022/keys")
    
    for event_key in event_keys:
        # Create empty list in team_matches for this event
        team_matches[event_key] = []
        
        # read correspondent event file
        path = f'data/events/{event_key}.json'.replace('2022', '')
        with open(path, 'r') as file:
            # Read the current file data. If there is no file (week0), skip this event 
            try:
                event_matches = json.load(file)
            except json.decoder.JSONDecodeError as e:
                continue
            
        # for each match in the event
        for match_key in event_matches:
            match = event_matches[match_key]
            match_key = match_key.replace(f"{event_key}_", '')
            
            # If the team was in this match, save it to their list of matches
            if team_key in match['blue']['teams'] or team_key in match['red']['teams']:
                team_matches[event_key].append(match_key)
    
    return team_matches

    
if __name__ == "__main__":
    print("Getting all teams from this year...")
    teams = []
    for i in range(30):
        teams += get_api_data(f"/teams/2022/{i}/keys")

    print(f"Got {len(teams)} teams")

    # For each team, get their match data by event
    for team_key in teams:
        print(f"Getting matches for {team_key} | {teams.index(team_key)+1}/{len(teams)}")
        team_matches = get_team_matches(team_key)
        total_match_count = sum([len(event) for event in team_matches.values()])
        print(f"Team {team_key} had {total_match_count} matches")
        
        save_team_details(team_key, team_matches)