from flask import Flask, render_template, request, send_file, url_for
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from gtts import gTTS
import os
from datetime import datetime

app = Flask(__name__)

# ================== Folders ==================
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
REPORT_FOLDER = os.path.join(app.root_path, 'reports')
AUDIO_FOLDER = os.path.join(app.root_path, 'static', 'audio')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# ================== Telugu Font ==================
TELUGU_FONT_PATH = os.path.join(app.root_path, 'NotoSansTelugu-Regular.ttf')
if os.path.exists(TELUGU_FONT_PATH):
    pdfmetrics.registerFont(TTFont('TeluguFont', TELUGU_FONT_PATH))
else:
    print("Telugu font not found. Telugu text may not render properly in PDF.")

# ================== Disease Solutions ==================
DISEASE_SOLUTIONS = {
    "Leaf Blight": {
        "en": [
            "Remove and destroy infected leaves.",
            "Apply fungicide spray every 7-10 days.",
            "Ensure proper spacing between plants for airflow."
        ],
        "te": [
            "చికిత్స పొందిన ఆకులను తీసి దహనం చేయండి.",
            "ప్రతి 7-10 రోజులకు ఫంగిసైడ్ స్ప్రే చేయండి.",
            "గాలికి వీలుగా మొక్కల మధ్య దూరం ఉంచండి."
        ]
    },
    "Powdery Mildew": {
        "en": [
            "Spray neem oil or sulfur-based fungicide.",
            "Avoid overhead irrigation.",
            "Remove infected plant parts."
        ],
        "te": [
            "నిమ్ ఆయిల్ లేదా సల్ఫర్ ఫంగిసైడ్ స్ప్రే చేయండి.",
            "పైన నీరు అందించే విధానాన్ని నివారించండి.",
            "ఇన్ఫెక్ట్ అయిన భాగాలను తొలగించండి."
        ]
    },
    "Healthy": {
        "en": ["No treatment needed. Maintain regular care."],
        "te": ["చికిత్స అవసరం లేదు. సాధారణ যতనం కొనసాగించండి."]
    }
}

# ================== Routes ==================
@app.route('/')
def upload_file():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    uploaded_file = request.files['file']
    if not uploaded_file:
        return "No file uploaded!", 400

    uploaded_file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
    uploaded_file.save(uploaded_file_path)

    # ===== PREDICTION PLACEHOLDER =====
    label = "Leaf Blight"  # Example
    confidence = 0.95
    # =================================

    voice_text = request.form.get('voiceInput', None)

    # ===== PDF Generation =====
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    report_filename = f"disease_report_{timestamp}.pdf"
    report_path = os.path.join(REPORT_FOLDER, report_filename)
    generate_pdf(report_path, label, confidence, uploaded_file_path, voice_text)

    # ===== Remove uploaded image =====
    if os.path.exists(uploaded_file_path):
        os.remove(uploaded_file_path)

    # ===== Audio Generation (English + Telugu) =====
    audio_en_filename = f"report_en_{timestamp}.mp3"
    audio_te_filename = f"report_te_{timestamp}.mp3"
    audio_en_path = os.path.join(AUDIO_FOLDER, audio_en_filename)
    audio_te_path = os.path.join(AUDIO_FOLDER, audio_te_filename)

    generate_audio(label, confidence, audio_en_path, lang='en')
    generate_audio(label, confidence, audio_te_path, lang='te')

    report_url = url_for('download_report', report_filename=report_filename)
    audio_en_url = url_for('static', filename=f"audio/{audio_en_filename}")
    audio_te_url = url_for('static', filename=f"audio/{audio_te_filename}")

    return render_template('result.html',
                           label=label,
                           confidence=confidence,
                           report_filename=report_filename,
                           report_url=report_url,
                           audio_en_url=audio_en_url,
                           audio_te_url=audio_te_url)

# ================== PDF Function ==================
def generate_pdf(path, disease, confidence, image_path, voice_text=None):
    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter

    # ===== Header =====
    c.setFillColorRGB(46/255, 139/255, 87/255)
    c.rect(0, height-120, width, 120, fill=1, stroke=0)
    c.setFillColorRGB(1,1,1)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width/2, height-70, "🌱 Crop Disease Report")

    # ===== Leaf Image =====
    try:
        if os.path.exists(image_path):
            img = ImageReader(image_path)
            c.drawImage(img, 50, height-400, width=200, height=200, preserveAspectRatio=True, mask='auto')
    except Exception as e:
        print("Image not added:", e)

    # ===== Disease Info =====
    info_x = 280
    info_y = height - 250
    c.setFillColorRGB(232/255, 245/255, 233/255)
    c.roundRect(info_x-10, info_y-90, width-320, 100, 10, fill=1, stroke=0)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(info_x, info_y, f"Disease: {disease}")
    c.setFont("Helvetica", 14)
    c.drawString(info_x, info_y-25, f"Confidence: {confidence*100:.2f}%")
    if voice_text:
        c.drawString(info_x, info_y-50, f"Voice Input: {voice_text}")

    # ===== Solutions Box =====
    sol_box_y = height-450
    c.setFillColorRGB(245/255, 255/255, 245/255)
    c.roundRect(50, 50, width-100, sol_box_y-60, 10, fill=1, stroke=0)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(70, sol_box_y-20, "✅ Recommended Solutions:")

    # English solutions
    c.setFont("Helvetica", 12)
    y_pos = sol_box_y-50
    solutions = DISEASE_SOLUTIONS.get(disease, {"en":["No solution available."], "te":[]})
    for sol in solutions["en"]:
        c.drawString(80, y_pos, f"- {sol}")
        y_pos -= 18

    # Telugu solutions
    if solutions.get("te") and os.path.exists(TELUGU_FONT_PATH):
        c.setFont("TeluguFont", 12)
        y_pos -= 10
        for sol in solutions["te"]:
            c.drawString(80, y_pos, f"- {sol}")
            y_pos -= 18

    c.save()

# ================== Audio Function ==================
def generate_audio(disease, confidence, audio_path, lang='en'):
    solutions = DISEASE_SOLUTIONS.get(disease, {"en":["No solution available."], "te":[]})
    if lang == 'en':
        text = f"Disease: {disease}. Confidence: {confidence*100:.2f} percent. Recommended solutions: " + " ".join(solutions["en"])
        tts = gTTS(text=text, lang='en')
    elif lang == 'te':
        text = f"రోగం: {disease}. నమ్మక స్థాయి: {confidence*100:.2f} శాతం. సిఫార్సు చేసిన పరిష్కారాలు: " + " ".join(solutions.get("te", ["చికిత్స అవసరం లేదు."]))
        tts = gTTS(text=text, lang='te')
    tts.save(audio_path)

# ================== Download Route ==================
@app.route('/download/<report_filename>')
def download_report(report_filename):
    report_path = os.path.join(REPORT_FOLDER, report_filename)
    if os.path.exists(report_path):
        return send_file(report_path, as_attachment=True)
    else:
        return "Report not found!", 404

# ================== Main ==================
if __name__ == "__main__":
    app.run(debug=True)
