import json
import os
from predictor_highest_score import highest_previous_score
from predictor_previous_scores import average_previous_scores

# For calculating weighted avg
# [number, average]
score_difference_sum = {"count": 0, "total": 0}

path = 'data/teams/'
dir = os.listdir(path)

for team_file in dir:
    # print(f"Team: {team_file.replace('.json', '')} | {dir.index(team_file)+1}/{len(dir)}")
    f = os.path.join(path, team_file)
    # If not a file, skip this iteration
    if not os.path.isfile(f): continue
    with open(f, 'r') as file:
        try: 
            team_matches = json.load(file)
        # If empty file (or other error), skip this iteration
        except json.decoder.JSONDecodeError as e:
            continue
        
    # Skip this team if it has no matches
    if bool([a for a in team_matches.values() if a == []]): continue
    
    # Feed fake timestamp of years in future to get all matches
    team_high_score = highest_previous_score(team_file.replace('.json', ''), 3053863314)
    # print(f"{team_high_score = }")
    team_avg_score = average_previous_scores(team_file.replace('.json', ''), 3053863314)
    # print(f"{team_avg_score = }")
    
    try: 
        difference = (team_high_score / team_avg_score) - 1
    except: continue
    
    score_difference_sum["count"] += 1
    score_difference_sum["total"] += difference

print(f"On average, the highest score for any team was {round(100 * score_difference_sum['total'] / score_difference_sum['count'], 1)}% higher than the average score for that team")
