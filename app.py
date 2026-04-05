from flask import Flask, render_template_string, request, redirect, url_for, make_response
import pandas as pd
import os

app = Flask(__name__)

DATA_FILE = 'election_data.csv'
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=['Party'])
    df.to_csv(DATA_FILE, index=False)

# உங்கள் கம்ப்யூட்டரில் உள்ள படங்களின் பெயர்கள்
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
    :root {
        --primary-bg: #f8f9fa;
        --card-bg: rgba(255, 255, 255, 0.9);
        --accent-gradient: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    }

    body { 
        font-family: 'Segoe UI', Roboto, sans-serif; 
        margin: 0; padding: 20px;
        background: linear-gradient(45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite; /* பின்னணி நிறம் மெதுவாக மாறும் */
        min-height: 100vh;
        display: flex; justify-content: center; align-items: center;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .container { 
        max-width: 900px; width: 100%;
        background: var(--card-bg);
        backdrop-filter: blur(10px); /* Glass effect */
        padding: 40px; border-radius: 24px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.3);
        text-align: center;
    }

    .tn-header-logo { width: 70px; filter: drop-shadow(0 2px 5px rgba(0,0,0,0.2)); }

    h1 { color: #1a2a6c; font-size: 28px; margin: 20px 0; text-transform: uppercase; letter-spacing: 1px; }

    .party-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 20px; margin: 30px 0;
    }

    .party-card { 
        background: white; border: 2px solid transparent;
        padding: 20px; border-radius: 18px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer; position: relative;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    .party-card:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 15px 30px rgba(0,0,0,0.15);
        border-color: #3498db;
    }

    .party-card img { width: 90px; height: 90px; object-fit: contain; transition: 0.3s; }
    
    .party-card input[type="radio"] { margin-top: 15px; width: 20px; height: 20px; }

    .vote-btn { 
        background: var(--accent-gradient);
        color: white; border: none; padding: 16px 50px;
        border-radius: 50px; font-size: 20px; font-weight: bold;
        cursor: pointer; transition: 0.3s;
        box-shadow: 0 10px 20px rgba(42, 82, 152, 0.3);
    }

    .vote-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 25px rgba(42, 82, 152, 0.4);
        filter: brightness(1.1);
    }

    /* ரிசல்ட் பார் டிசைன் */
    .results { margin-top: 50px; text-align: left; background: #fff; padding: 25px; border-radius: 20px; }
    
    .bar-item { margin-bottom: 20px; }
    .bar-info { display: flex; justify-content: space-between; margin-bottom: 8px; font-weight: 600; }
    
    .bar-bg { background: #e9ecef; border-radius: 50px; height: 12px; overflow: hidden; }
    .bar-fill { 
        height: 100%; border-radius: 50px;
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        transition: width 1.5s ease-in-out; /* சார்ட் லோட் ஆகும்போது அனிமேஷன் */
    }
</style>
</head>
<body>
    <div class="container">
        <img src="/static/tn_logo.png" class="tn-header-logo">
        <h1>தமிழக சட்டமன்றத் தேர்தல் 2026 - கருத்துக் கணிப்பு</h1>
        <form action="/vote" method="post">
            <div class="party-grid">
                {% for party in parties %}
                <label class="party-card">
                    <img src="{{ party.image }}" alt="{{ party.name }}"><br>
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
                <div style="text-align: left;">
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
    # பயனர் ஏற்கனவே வாக்களித்துள்ளாரா என்று 'Cookie' மூலம் சரிபார்த்தல்
    if request.cookies.get('has_voted'):
        return """
        <div style="text-align:center; padding:50px; font-family:Arial;">
            <h2>நீங்கள் ஏற்கனவே வாக்களித்துவிட்டீர்கள்!</h2>
            <p>ஒரு நபர் ஒரு முறை மட்டுமே வாக்களிக்க முடியும்.</p>
            <a href="/">முகப்புப் பக்கத்திற்குச் செல்ல</a>
        </div>
        """

    party = request.form.get('selected_party')
    if party:
        # வாக்குகளை CSV கோப்பில் சேமித்தல்
        df = pd.read_csv(DATA_FILE)
        new_vote = pd.DataFrame([{'Party': party}])
        df = pd.concat([df, new_vote], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)

        # வெற்றிகரமாக ஓட்டு போட்ட பிறகு, Cookie-ஐ செட் செய்தல்
        resp = make_response(redirect(url_for('index')))
        # 30 நாட்களுக்கு இந்த பிரவுசரில் மீண்டும் ஓட்டு போட முடியாது
        resp.set_cookie('has_voted', 'true', max_age=30*24*60*60)
        return resp
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)