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


def save_assessment(score, recommendation):
    with open('assessments.txt', 'a') as file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file.write(f'{timestamp}, Score: {score}, Recommendation: {recommendation}\n')


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

    return render_template('result.html', score=score, recommendation=recommendation, follow_up=follow_up)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
