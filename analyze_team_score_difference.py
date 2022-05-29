import json
import os
from predictor_highest_score import highest_previous_score
from predictor_previous_scores import average_previous_scores

path = 'data/teams/'
# For each event file, get the matches

dir = os.listdir(path)

for team_file in dir:
    print(f"Team: {team_file.replace('.json', '')} | {dir.index(team_file)+1}/{len(dir)}")
    f = os.path.join(path, team_file)
    # If not a file, skip this iteration
    if not os.path.isfile(f): continue
    with open(f, 'r') as file:
        try: 
            team_matches = json.load(file)
        # If empty file (or other error), skip this iteration
        except json.decoder.JSONDecodeError as e:
            continue


