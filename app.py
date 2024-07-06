import os
import json
from flask import Flask, render_template, request
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials


app = Flask(__name__)

# Add enumerate to the Jinja2 environment globals
app.jinja_env.globals.update(enumerate=enumerate)


questions = [
    {
        "question": "Do you have a clear digital transformation strategy documented?",
        "options": [
            {"text": "Yes, fully documented and communicated", "score": 5},
            {"text": "Partially documented", "score": 3},
            {"text": "No, not documented", "score": 0}
        ]
    },
    
    {
        "question": "How committed is your leadership team to driving digital transformation?",
        "options": [
            {"text": "Highly committed", "score": 5},
            {"text": "Moderately committed", "score": 3},
            {"text": "Slightly committed", "score": 2},
            {"text": "Not committed", "score": 0}
        ]
    },

    {
        "question": "Do you have a dedicated team or leader responsible for digital transformation?",
        "options": [
            {"text": "Yes, a dedicated team/leader", "score": 50},
            {"text": "Partially, shared responsibilities", "score": 10},
            {"text": "No, no dedicated team/leader", "score": 25}
        ]
    },
    
    # Add the rest of the questions similarly
]

recommendations = [
    {"min_score": 55, "max_score": 60, "recommendation": "Your digital transformation efforts are excellent. Continue to innovate and refine your strategy to stay ahead.", "follow_up": "Offer advanced consulting services for AI integration, advanced analytics, and continuous improvement."},
    {"min_score": 40, "max_score": 54, "recommendation": "You have a solid digital transformation foundation, but there are areas for improvement. Focus on integrating technologies and enhancing digital culture.", "follow_up": "Provide a tailored plan to optimize technology integration, process automation, and employee training."},
    {"min_score": 25, "max_score": 39, "recommendation": "Your digital transformation efforts are in progress but need significant improvement. Prioritize strategy documentation, leadership commitment, and technology adoption.", "follow_up": "Provide a tailored plan to optimize technology integration, process automation, and employee training."},
    {"min_score": 0, "max_score": 24, "recommendation": "You are at the early stages of digital transformation. Immediate action is needed to develop a strategy and start adopting digital technologies.", "follow_up":"Propose foundational digital transformation services, starting with strategic planning and basic technology implementation."},
    # Add other score ranges similarly
]

# Google Sheets setup
try:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials_json = os.environ.get('GOOGLE_SHEETS_CREDENTIALS')
    if not credentials_json:
        raise ValueError("GOOGLE_SHEETS_CREDENTIALS environment variable is not set.")
    credentials_dict = json.loads(credentials_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    client = gspread.authorize(creds)
    # Open the Google Sheet by name
    sheet = client.open("Marketing Diagnostic App").sheet1
    print("Google Sheets client initialized successfully.")
except Exception as e:
    print(f"Error initializing Google Sheets client: {e}")
    raise

def save_to_google_sheets(data):
    try:
        sheet.append_row(data)
        print("Data saved to Google Sheets.")
    except Exception as e:
        print(f"Error saving data to Google Sheets: {e}")
        raise

@app.route('/')
def index():
    return render_template('index.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    for i, question in enumerate(questions):
        answer = request.form.get(f'question_{i}')
        score += int(answer)

    # Initialize recommendation and follow_up with default values
    recommendation = "No recommendation found."
    follow_up = "No follow-up actions available."

    for rec in recommendations:
        if rec['min_score'] <= score <= rec['max_score']:
            recommendation = rec['recommendation']
            follow_up = rec['follow_up']
            break

    # Collect additional information
    name = request.form.get('name')
    email = request.form.get('email')
    company_name = request.form.get('company_name')
    industry = request.form.get('industry')
    employees = request.form.get('employees')
    role = request.form.get('role')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Save the assessment information to Google Sheets
    data = [timestamp, name, email, company_name, industry, employees, role, score, recommendation, follow_up]
    save_to_google_sheets(data)

    return render_template('result.html', score=score, recommendation=recommendation)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)