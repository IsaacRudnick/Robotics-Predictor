import json
import os
from predictor_HPS import highest_previous_score
from predictor_AMPS import average_previous_scores
import matplotlib.pyplot as plt

# For calculating weighted avg
# [number, average]

team_avg_scores = []
team_high_scores = []

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
    team_avg_score = round(average_previous_scores(team_file.replace('.json', ''), 3053863314), 1)
    # print(f"{team_avg_score = }")
    
    team_avg_scores.append(team_avg_score)
    team_high_scores.append(team_high_score)

fig = plt.figure()
ax = fig.add_subplot(111)

plt.scatter(team_avg_scores, team_high_scores, s=2)
plt.xlabel("Average Score")
plt.ylabel("Highest Score")
# plot y=1.987x + 0
plt.plot(team_avg_scores, [1.987 * x + 0 for x in team_avg_scores], "r-")

# Choose one of these two
plt.plot(team_avg_scores, [1 * x + 0 for x in team_avg_scores], "g-")
# ax.set_aspect('equal')

plt.xlim(-10, max(team_high_scores)*1.2)
plt.ylim(-10, max(team_high_scores)*1.2)

plt.show()