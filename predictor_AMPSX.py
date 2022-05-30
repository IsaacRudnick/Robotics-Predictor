import json
import os

from matplotlib import pyplot as plt

def average_previous_scores(team, timestamp, outlier_percent):
    # divide by 100 to get outlier_percent as a decimal
    outlier_percent /= 100 
    
    team_scores = []
    
    # Get all the matches for the team
    
    try: 
        with open(f'data/teams/{team}.json', 'r') as team_file:
            team_event_matches = json.load(team_file)
    except FileNotFoundError: 
        print("No file found for team:", team)
        return "this will cause an error; the match will be skipped"

    # Skip this team if it has no matches
    if bool([a for a in team_event_matches.values() if a == []]): 
        print("No matches found for team:", team)
        return "this will cause an error; the match will be skipped"
    
    for event_key in team_event_matches:
        path = f"data/events/{event_key.replace('2019', '')}.json"
        # Skip this event if there is no file for it
        if not os.path.isfile(path): continue
        
        try:
            with open(f"data/events/{event_key.replace('2019', '')}.json", 'r') as event_file:
                event_data = json.load(event_file)
        except:
            print(f"Error loading event file: {event_key}")
            continue
                
        for match_key in event_data:
            
            match_info = event_data[match_key]
            
            # Skip this match if it happens in the "future"
            if match_info['game_start_time'] > timestamp: continue
            
            if team in match_info['blue']['teams']:
                team_scores.append(match_info['blue']['score'])
            elif team in match_info['red']['teams']:
                team_scores.append(match_info['red']['score'])
                
    average_score = sum(team_scores) / len(team_scores)
    high_outlier_cutoff = average_score + (average_score * outlier_percent)
    low_outlier_cutoff = average_score - (average_score * outlier_percent)
    
    team_scores_sans_outliers = list(filter(lambda x: low_outlier_cutoff <= x <= high_outlier_cutoff, team_scores))

    if len(team_scores_sans_outliers) == 0: #< len(team_scores)*(1/2):
        return sum(team_scores) / len(team_scores)
    else:
        return sum(team_scores_sans_outliers) / len(team_scores_sans_outliers)

 
if __name__ == "__main__":
    
    outlier_percents = list(range(0, 210, 10))
    respective_correct_percents = []
    
    for outlier_percent in outlier_percents:
        
        print(f"Outlier Percent: {outlier_percent} | {outlier_percents.index(outlier_percent) + 1}/{len(outlier_percents)}")
                
        predictions = {"correct": 0, "incorrect": 0}
        total_matches_analyzed = 0
        
        # For each event file, get the matches
        path = 'data/events/'
        dir = os.listdir(path)

        for event_file in dir:
            # print(f"Event: {event_file.replace('.json', '')} | {dir.index(event_file)+1}/{len(dir)}")
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
            # try:
            average_blue_scores = sum([average_previous_scores(team, match_info["game_start_time"], outlier_percent) for team in blue_teams])
            average_red_scores = sum([average_previous_scores(team, match_info["game_start_time"], outlier_percent) for team in red_teams])
            # except: 
            #     print("Error:", match_key)
            #     continue

            if average_blue_scores > average_red_scores:
                predicted_winner = "blue"
            elif average_red_scores > average_blue_scores:
                predicted_winner = "red"
            # Skip if tie!
            else: 
                continue
            
            actual_winner = match_info["result"]

            if predicted_winner == actual_winner:
                
                predictions["correct"] += 1
            elif predicted_winner != actual_winner:
                predictions["incorrect"] += 1
                
            total_matches_analyzed += 1

            # print(f"Match: {match_key} | Predicted Winner: {predicted_winner} | Actual Winner: {actual_winner}")
                
            # print(f"Correct Prediction: {100 * predictions['correct'] / sum(predictions.values())}%")
        correctness = round(100 * predictions['correct'] / sum(predictions.values()), 2)
        print(f"Across {total_matches_analyzed} matches analyzed, {correctness}% of predictions were correct")
        
        respective_correct_percents.append(correctness)

    print(f"{outlier_percents = }")
    print(f"{respective_correct_percents = }")
    plt.scatter(outlier_percents, respective_correct_percents)
    plt.show()
    
    