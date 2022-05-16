import json

def save_match_details(match_id, match_details):
    with open('./matches.json', 'w') as f:
        data = json.load(f)
        data[match_id] = match_details
        json.dump(data, f)
        

        