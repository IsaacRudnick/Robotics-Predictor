import json
import os

total_matches_analyzed = 0
predictions = {"correct": 0, "incorrect": 0}
 
def highest_previous_score(team, timestamp):
    
    highest_score = 0
    
    # Get all the matches for the team
    with open(f'data/teams/{team}.json', 'r') as team_file:
        team_event_matches = json.load(team_file)

    for event_key in team_event_matches:
        path = f"data/events/{event_key.replace('2022', '')}.json"
        # Skip this event if there is no file for it
        if not os.path.isfile(path): continue
        
        with open(f"data/events/{event_key.replace('2022', '')}.json", 'r') as event_file:
            try:
                event_data = json.load(event_file)
            except json.decoder.JSONDecodeError as e:
                continue
                
        for match_key in event_data:
            
            match_info = event_data[match_key]
            
            # Skip this match if it happens in the "future"
            if match_info['game_start_time'] > timestamp: continue
            
            if team in match_info['blue']['teams']:
                highest_score = max(highest_score, match_info['blue']['score'])
            elif team in match_info['red']['teams']:
                highest_score = max(highest_score, match_info['red']['score'])
                
    return highest_score

path = 'data/events/'
# For each event file, get the matches

dir = os.listdir(path)

for event_file in dir:
    print(f"Event: {event_file.replace('.json', '')} | {dir.index(event_file)+1}/{len(dir)}")
    f = os.path.join(path, event_file)
    # If not a file, skip this iteration
    if not os.path.isfile(f): continue
    with open(f, 'r') as file:
        try: 
            event_matches = json.load(file)
        # If empty file (or other error), skip this iteration
        except json.decoder.JSONDecodeError as e:
            continue
        
    # For each match in each iterated event
    for match_key in event_matches:

        match_info = event_matches[match_key]

        # the blue teams and the red teams
        blue_teams = match_info['blue']['teams']
        red_teams = match_info['red']['teams']
    
        # Get the average score for each alliance in the past
        average_blue_scores = sum([highest_previous_score(team, match_info["game_start_time"]) for team in blue_teams])/3 
        average_red_scores = sum([highest_previous_score(team, match_info["game_start_time"]) for team in red_teams])/3
        
        predicted_winner = "blue" if average_blue_scores > average_red_scores else "red"
        actual_winner = match_info["result"]

        if predicted_winner == actual_winner:
            predictions["correct"] += 1
        elif predicted_winner != actual_winner:
            predictions["incorrect"] += 1
            
        total_matches_analyzed += 1

        # print(f"Match: {match_key} | Predicted Winner: {predicted_winner} | Actual Winner: {actual_winner}")
        
    # print(f"Correct Prediction: {100 * predictions['correct'] / sum(predictions.values())}%")

print(f"Across {total_matches_analyzed} matches analyzed, {round(100 * predictions['correct'] / sum(predictions.values()))}% of predictions were correct")