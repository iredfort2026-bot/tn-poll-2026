import os
from flask import Flask, render_template_string, request, redirect, url_for, make_response
import pandas as pd
import requests

app = Flask(__name__)

# உங்கள் Google Web App URL (சரியானது)
GSHEET_URL = "https://script.google.com/macros/s/AKfycbw35JGXlrqo0I5fcfQzpN_vbmfN9m44eLCaZz5PwDBvv5fH2h9r5Jy8f15Qm6OsciBC/exec"

# டேட்டா ஃபைல் செட்டிங்ஸ்
DATA_FILE = 'election_data.csv'
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=['Party'])
    df.to_csv(DATA_FILE, index=False)

PARTIES = [
    {'id': 'DMK', 'name': 'திமுக', 'image': '/static/dmk.png'},
    {'id': 'AIADMK', 'name': 'அதிமுக', 'image': '/static/admk.png'},
    {'id': 'TVK', 'name': 'தவெக', 'image': '/static/tvk.png'},
    {'id': 'NTK', 'name': 'நாம் தமிழர்', 'image': '/static/ntk.png'},
    {'id': 'BJP', 'name': 'பாஜக', 'image': '/static/bjp.png'}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ta">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TN Opinion Poll 2026</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background: #f4f7f6; display: flex; justify-content: center; align-items: flex-start; padding: 20px; min-height: 100vh; margin: 0; }
        .container { width: 100%; max-width: 500px; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center; margin-top: 20px; }
        .party-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 20px 0; }
        .party-card { border: 2px solid #eee; padding: 15px; border-radius: 15px; cursor: pointer; transition: 0.3s; display: flex; flex-direction: column; align-items: center; }
        .party-card:hover { border-color: #1a2a6c; background: #f9f9f9; }
        .party-card img { width: 70px; height: 70px; object-fit: contain; margin-bottom: 10px; }
        .vote-btn { background: #1a2a6c; color: white; border: none; padding: 15px 50px; border-radius: 30px; font-size: 18px; cursor: pointer; width: 100%; margin-top: 10px; }
        .results { margin-top: 30px; text-align: left; background: #fdfdfd; padding: 15px; border-radius: 10px; }
        .bar-bg { background: #eee; height: 10px; border-radius: 5px; margin: 5px 0 15px 0; overflow: hidden; }
        .bar-fill { background: linear-gradient(90deg, #1a2a6c, #b21f1f); height: 100%; border-radius: 5px; }
        .disclaimer { font-size: 11px; color: #888; margin-top: 30px; line-height: 1.4; border-top: 1px solid #eee; padding-top: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <div style="font-size: 50px;">🗳️</div>
        <h2 style="margin: 10px 0; font-size: 20px;">தமிழக சட்டமன்றத் தேர்தல் 2026 - கருத்துக் கணிப்பு</h2>
        <form action="/vote" method="post">
            <div class="party-grid">
                {% for party in parties %}
                <label class="party-card">
                    <img src="{{ party.image }}">
                    <span style="font-weight: bold; font-size: 14px;">{{ party.name }}</span>
                    <input type="radio" name="selected_party" value="{{ party.id }}" required style="margin-top: 8px;">
                </label>
                {% endfor %}
            </div>
            <button type="submit" class="vote-btn">வாக்களிக்கிறேன்</button>
        </form>
        <div class="results">
            <h3 style="border-bottom: 2px solid #1a2a6c; padding-bottom: 5px;">தற்போதைய நிலவரம்</h3>
            {% set total_votes = counts.values()|sum %}
            {% for party in parties %}
                {% set vote_count = counts.get(party.id, 0) %}
                {% set percentage = (vote_count / total_votes * 100)|round(1) if total_votes > 0 else 0 %}
                <div style="margin-bottom: 5px; font-size: 14px;">
                    <strong>{{ party.name }}</strong>: {{ vote_count }} வாக்குகள் ({{ percentage }}%)
                    <div class="bar-bg"><div class="bar-fill" style="width: {{ percentage }}%"></div></div>
                </div>
            {% endfor %}
        </div>
        <div style="margin-top: 30px; padding: 20px; border-top: 2px dashed #ddd; background: #fff9e6; border-radius: 15px; text-align: center;">
    <h2 style="color: #1a2a6c; font-size: 20px; margin-bottom: 5px;">iRedfort E-Solutions Pvt Ltd</h2>
    <h3 style="color: #d35400; font-size: 16px; margin-top: 0;">🛡️ அங்கீகரிக்கப்பட்ட டிஜிட்டல் சிக்னேச்சர் (DSC) மையம்</h3>
    
    <p style="font-size: 13px; color: #555; line-height: 1.5; margin: 15px 0;">
        நாங்கள் <strong>Capricorn</strong> மற்றும் <strong>XtraTrust</strong> நிறுவனங்களின் அதிகாரப்பூர்வ பார்ட்னர். <br>
        Class 3 DSC, இ-டெண்டர், மற்றும் வருமான வரித் தாக்கல் செய்யத் தேவையான டிஜிட்டல் கையொப்பங்கள் மற்றும் 
        <strong>PROXKey</strong> டோக்கன்கள் எங்களிடம் கிடைக்கும்.
    </p>
    
    <div style="display: flex; justify-content: center; gap: 15px; margin: 15px 0; align-items: center;">
        <img src="https://www.certificate.digital/images/logo.png" alt="Capricorn" style="height: 30px;">
        <img src="https://www.xtratrust.com/assets/images/logo.png" alt="XtraTrust" style="height: 30px;">
        <span style="font-weight: bold; color: #555; font-size: 12px;">PROXKey Authorized</span>
    </div>

    <a href="https://wa.me/919942245217?text=I%20need%20DSC%20Service%20from%20iRedfort" 
       style="display: inline-block; background: #25D366; color: white; padding: 12px 25px; border-radius: 50px; text-decoration: none; font-weight: bold; font-size: 14px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
        💬 தொடர்புக்கு: 99422 45217
    </a>

    
</div>
        <div class="disclaimer">
            <strong>பொறுப்புத் துறப்பு (Disclaimer):</strong> இது ஒரு தனிப்பட்ட நபரால் நடத்தப்படும் கருத்துக் கணிப்பு. இதற்கும் இந்திய தேர்தல் ஆணையத்திற்கும் அல்லது தமிழ்நாடு அரசுக்கும் எந்தத் தொடர்பும் இல்லை.
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
    
    # Google Sheet-க்கு அனுப்புதல்
    if party:
        try:
            # .post-ஐ இப்படி மாற்றுவது நல்லது
            requests.post(GSHEET_URL, params={'party': party}, timeout=5)
        except:
            pass

    # CSV-யில் சேமித்தல் (Backup)
    df = pd.read_csv(DATA_FILE)
    new_vote = pd.DataFrame([{'Party': party}])
    df = pd.concat([df, new_vote], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('has_voted', 'true', max_age=30*24*60*60)
    return resp

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
