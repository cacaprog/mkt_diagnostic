import os
from flask import Flask, render_template, request

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
    # Add the rest of the questions similarly
]

recommendations = [
    {"min_score": 55, "max_score": 60, "recommendation": "Your digital transformation efforts are excellent. Continue to innovate and refine your strategy to stay ahead.", "follow_up": "Offer advanced consulting services for AI integration, advanced analytics, and continuous improvement."},
    {"min_score": 40, "max_score": 54, "recommendation": "You have a solid digital transformation foundation, but there are areas for improvement. Focus on integrating technologies and enhancing digital culture.", "follow_up": "Provide a tailored plan to optimize technology integration, process automation, and employee training."},
    # Add other score ranges similarly
]

@app.route('/')
def index():
    return render_template('index.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    for i, question in enumerate(questions):
        answer = request.form.get(f'question_{i}')
        score += int(answer)

    for rec in recommendations:
        if rec['min_score'] <= score <= rec['max_score']:
            recommendation = rec['recommendation']
            follow_up = rec['follow_up']
            break

    return render_template('result.html', score=score, recommendation=recommendation, follow_up=follow_up)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
