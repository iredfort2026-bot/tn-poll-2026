import os
from flask import Flask, render_template_string, request, redirect, url_for, make_response
import pandas as pd

app = Flask(__name__)

# டேட்டா ஃபைல் செட்டிங்ஸ்
DATA_FILE = 'election_data.csv'
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=['Party'])
    df.to_csv(DATA_FILE, index=False)

PARTIES = [
    {'id': 'DMK', 'name': 'திமுக', 'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/DMK_logo.svg/512px-DMK_logo.svg.png'},
    {'id': 'AIADMK', 'name': 'அதிமுக', 'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/AIADMK_logo.svg/512px-AIADMK_logo.svg.png'},
    {'id': 'TVK', 'name': 'தவெக', 'image': 'https://upload.wikimedia.org/wikipedia/en/thumb/f/f6/Tamilaga_Vettri_Kazhagam_logo.png/220px-Tamilaga_Vettri_Kazhagam_logo.png'},
    {'id': 'NTK', 'name': 'நாம் தமிழர்', 'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Naam_Tamilar_Katchi_Logo.png/512px-Naam_Tamilar_Katchi_Logo.png'},
    {'id': 'BJP', 'name': 'பாஜக', 'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Bharatiya_Janata_Party_logo.svg/512px-Bharatiya_Janata_Party_logo.svg.png'}
]

# உங்கள் அழகான UI டிசைன்
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ta">
<head>
    <meta charset="UTF-8">
    <meta name="referrer" content="no-referrer">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TN Opinion Poll 2026</title>
    <style>
        body { font-family: sans-serif; background: #f0f2f5; display: flex; justify-content: center; padding: 20px; }
        .container { max-width: 800px; background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center; }
        .party-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 15px; margin: 20px 0; }
        .party-card { border: 1px solid #ddd; padding: 15px; border-radius: 15px; cursor: pointer; }
        .party-card img { width: 80px; height: 80px; object-fit: contain; }
        .vote-btn { background: #1a2a6c; color: white; border: none; padding: 15px 40px; border-radius: 30px; font-size: 18px; cursor: pointer; }
        .results { margin-top: 30px; text-align: left; }
        .bar-bg { background: #eee; height: 10px; border-radius: 5px; margin: 5px 0 15px 0; }
        .bar-fill { background: #3498db; height: 100%; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>தமிழக சட்டமன்றத் தேர்தல் 2026 - கருத்துக் கணிப்பு</h1>
        <form action="/vote" method="post">
            <div class="party-grid">
                {% for party in parties %}
                <label class="party-card">
                    <img src="{{ party.image }}"><br>
                    <strong>{{ party.name }}</strong><br>
                    <input type="radio" name="selected_party" value="{{ party.id }}" required>
                </label>
                {% endfor %}
            </div>
            <button type="submit" class="vote-btn">வாக்களிக்கிறேன்</button>
        </form>
        <div class="results">
            <h2>தற்போதைய நிலவரம்</h2>
            {% set total_votes = counts.values()|sum %}
            {% for party in parties %}
                {% set vote_count = counts.get(party.id, 0) %}
                {% set percentage = (vote_count / total_votes * 100)|round(1) if total_votes > 0 else 0 %}
                <div>
                    {{ party.name }}: {{ vote_count }} வாக்குகள் ({{ percentage }}%)
                    <div class="bar-bg"><div class="bar-fill" style="width: {{ percentage }}%"></div></div>
                </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    df = pd.read_csv(DATA_FILE)
    counts = df['Party'].value_counts().to_dict()
    return render_template_string(HTML_TEMPLATE, parties=PARTIES, counts=counts)

@app.route('/vote', methods=['POST'])
def vote():
    if request.cookies.get('has_voted'):
        return "ஏற்கனவே வாக்களித்துவிட்டீர்கள்! <a href='/'>திரும்பச் செல்ல</a>"
    
    party = request.form.get('selected_party')
    df = pd.read_csv(DATA_FILE)
    new_vote = pd.DataFrame([{'Party': party}])
    df = pd.concat([df, new_vote], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('has_voted', 'true', max_age=30*24*60*60)
    return resp

if __name__ == '__main__':
    # Render-க்கு மிக முக்கியமானது இந்த வரிகள்:
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
