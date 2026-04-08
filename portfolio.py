import os
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ta">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>iRedfort E-Solutions Pvt Ltd | Portfolio</title>
    <style>
        :root { --primary: #1a2a6c; --secondary: #b21f1f; --accent: #d35400; --light: #f4f7f6; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; background: var(--light); }
        .container { max-width: 900px; margin: 0 auto; padding: 20px; }
        header { background: white; padding: 40px 20px; text-align: center; border-bottom: 5px solid var(--primary); border-radius: 0 0 20px 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .hero-title { font-size: 2.5em; color: var(--primary); margin: 0; }
        .hero-tagline { font-size: 1.2em; color: var(--accent); font-weight: bold; margin-top: 10px; }
        
        .section { background: white; padding: 30px; margin-top: 25px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
        h2 { color: var(--primary); border-left: 5px solid var(--secondary); padding-left: 15px; margin-bottom: 20px; }
        
        .services-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
        .service-card { background: #fdfdfd; padding: 20px; border: 1px solid #eee; border-radius: 10px; transition: 0.3s; }
        .service-card:hover { transform: translateY(-5px); border-color: var(--primary); }
        
        .info-table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 0.9em; }
        .info-table th, .info-table td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        .info-table th { background: #f8f9fa; color: var(--primary); }

        .footer-cta { text-align: center; margin-top: 40px; padding: 40px; background: var(--primary); color: white; border-radius: 20px; }
        .btn-whatsapp { background: #25D366; color: white; padding: 15px 30px; text-decoration: none; border-radius: 50px; font-weight: bold; display: inline-block; margin-top: 20px; transition: 0.3s; }
        .btn-whatsapp:hover { background: #128C7E; transform: scale(1.05); }
        
        .badge { display: inline-block; padding: 5px 15px; background: #e8f0fe; color: #1a73e8; border-radius: 20px; font-size: 0.8em; font-weight: bold; margin-top: 10px; }
    </style>
</head>
<body>

<div class="container">
    <header>
        <h1 class="hero-title">iRedfort E-Solutions Pvt Ltd</h1>
        <p class="hero-tagline">Authorized Partner: Capricorn | XtraTrust | PROXKey</p>
        <div class="badge">MSME Registered: UDYAM-TN-37-0021061 [cite: 16, 61]</div>
    </header>

    <div class="section">
        <h2>எங்களைப் பற்றி (About Us)</h2>
        <p>iRedfort E-Solutions Pvt Ltd என்பது தென்காசி மாவட்டம், கடையநல்லூரில் அமைந்துள்ள ஒரு அங்கீகரிக்கப்பட்ட தகவல் தொழில்நுட்ப சேவை நிறுவனமாகும்[cite: 20, 32, 72]. நாங்கள் இந்திய அரசின் MSME அமைச்சகத்தின் கீழ் பதிவு செய்யப்பட்டு, நம்பகமான டிஜிட்டல் தீர்வுகளை வழங்கி வருகிறோம்[cite: 13, 14, 21].</p>
    </div>

    <div class="section">
        <h2>எங்கள் சேவைகள் (Services)</h2>
        <div class="services-grid">
            <div class="service-card">
                <h3>Class 3 DSC</h3>
                <p>Capricorn மற்றும் XtraTrust நிறுவனங்களின் அதிகாரப்பூர்வ பார்ட்னராக, பாதுகாப்பான டிஜிட்டல் கையொப்பங்களை வழங்குகிறோம்.</p>
            </div>
            <div class="service-card">
                <h3>PROXKey Tokens</h3>
                <p>உயர்தரமான மற்றும் நம்பகமான PROXKey USB டோக்கன்களின் அங்கீகரிக்கப்பட்ட விநியோகஸ்தர்[cite: 1, 6, 8].</p>
            </div>
            <div class="service-card">
                <h3>Software Solutions</h3>
                <p>மென்பொருள் நிறுவுதல் (Software Installation) மற்றும் இதர கணினி சார்ந்த தொழில்நுட்ப சேவைகள்[cite: 38, 83].</p>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>அலுவலக முகவரி & வங்கி விபரங்கள்</h2>
        <table class="info-table">
            <tr><th>Address</th><td>18/37, Jawahar Street, Muthukrishnapuram, Kadayanallur, TN-627751 [cite: 32, 74]</td></tr>
            <tr><th>Bank Name</th><td>Tamilnad Mercantile Bank Limit [cite: 66]</td></tr>
            <tr><th>IFSC Code</th><td>TMBL0000318 [cite: 66]</td></tr>
            <tr><th>A/C Number</th><td>318100050304447 [cite: 66]</td></tr>
        </table>
    </div>

    <div class="footer-cta">
        <h2>உங்கள் DSC தேவைகளுக்கு எங்களை அணுகுங்கள்</h2>
        <p>உடனடி சேவை மற்றும் சிறந்த விலையில் டிஜிட்டல் சிக்னேச்சர்கள் பெற:</p>
        <a href="https://wa.me/919363035217?text=Hi%20iRedfort,%20I%20need%20DSC%20service" class="btn-whatsapp">
            💬 WhatsApp: 93630 35217 [cite: 5]
        </a>
    </div>

    <p style="text-align: center; font-size: 0.8em; color: #888; margin-top: 20px;">
        © 2026 iRedfort E-Solutions Pvt Ltd. All Rights Reserved.
    </p>
</div>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
