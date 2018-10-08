from flask import Flask, jsonify
from collections import Counter
import itertools
import requests

app = Flask(__name__)


@app.route("/leaderboards")
def get_leaderboards():
    auth_token = '75c8c67777c2483cefe219c07ab7f46b4fda3d79'
    headers = {'Authorization': 'Bearer ' + auth_token}

    bounds = [40.811404, 28.595554, 41.199239, 29.428805]
    activity_type = 'cycling'
    min_cat = 56
    max_cat = 56

    segments_response = requests.get(
        'https://www.strava.com/api/v3/segments/explore?bounds=%s&activity_type=%s&min_cat%s=&max_cat=%s' % (bounds, activity_type, min_cat, max_cat), headers=headers)

    leaderboards = []
    for i in segments_response.json()['segments']:
        segment_leaderboards_response = requests.get(
            'https://www.strava.com/api/v3/segments/%s/leaderboard' % (i['id']), headers=headers)
        leaderboards.append(segment_leaderboards_response.json()['entries'])

    athletes = Counter(k['athlete_name']
                       for k in list(itertools.chain(*leaderboards)) if k.get('athlete_name'))

    for key, count in itertools.dropwhile(lambda key_count: key_count[1] >= 2, athletes.most_common()):
        del athletes[key]

    return jsonify(athletes)
