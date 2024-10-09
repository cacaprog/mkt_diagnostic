# Marketing Diagnostic App Documentation

Welcome to the **Marketing Diagnostic App** documentation! This guide provides a comprehensive overview of your application, including its purpose, setup instructions, file structure, code explanations, deployment steps, and usage guidelines. Whether you're a developer looking to understand the inner workings or a user wanting to utilize the app, this documentation has you covered.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Installation and Setup](#installation-and-setup)
3. [File Structure](#file-structure)
4. [Detailed Code Explanations](#detailed-code-explanations)
    - [app.py](#apppy)
    - [templates/index.html](#templatesindexhtml)
    - [templates/result.html](#templatesresulthtml)
    - [Procfile](#procfile)
    - [Pipfile](#pipfile)
    - [requirements.txt](#requirementstxt)
5. [Deployment Instructions](#deployment-instructions)
6. [Usage Guidelines](#usage-guidelines)
7. [Contributing Guidelines](#contributing-guidelines)
8. [License Information](#license-information)

---

## Project Overview

The **Marketing Diagnostic App** is a web-based tool designed to assess the effectiveness of a company's digital marketing strategies. Users answer a series of questions related to their marketing practices, and based on their responses, the app provides a score along with personalized recommendations to enhance their marketing efforts. The application leverages Google Sheets for data storage and is built using the Flask framework, making it easy to deploy on platforms like Heroku.

### Key Features

- **Interactive Questionnaire:** Users answer multiple-choice questions to evaluate their marketing strategies.
- **Score Calculation:** Based on responses, the app calculates a total score to gauge marketing effectiveness.
- **Personalized Recommendations:** Provides actionable insights and follow-up steps tailored to the user's score.
- **Data Storage:** Saves user responses and scores to Google Sheets for easy tracking and analysis.
- **Responsive Design:** Ensures a seamless experience across various devices and screen sizes.
- **Deployment Ready:** Configured for deployment on Heroku using a Procfile and Pipfile for dependency management.

---

## Installation and Setup

To set up the **Marketing Diagnostic App** locally or prepare it for deployment, follow these steps:

### Prerequisites

- **Python 3.11**: Ensure you have Python 3.11 installed on your machine.
- **Pipenv**: Used for managing Python dependencies. Install via `pip install pipenv`.
- **Git**: For version control and deployment purposes.
- **Heroku Account**: Required if you plan to deploy the app on Heroku.

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/cacaprog/marketing-diagnostic-app.git
   cd marketing-diagnostic-app
   ```

2. **Set Up a Virtual Environment**

   Using **Pipenv**:

   ```bash
   pipenv install
   pipenv shell
   ```

3. **Install Dependencies**

   If you're not using Pipenv, you can install dependencies using `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   The app requires a Google Sheets credentials JSON. Set it as an environment variable:

   ```bash
   export GOOGLE_SHEETS_CREDENTIALS='{"type": "...", ...}'
   ```

   Replace the placeholder with your actual credentials JSON.

5. **Run the Application Locally**

   ```bash
   python app.py
   ```

   The app should be accessible at `http://localhost:5000`.

---

## File Structure

Here's an overview of the project's file structure:

```
marketing-diagnostic-app/
│
├── app.py
├── Procfile
├── Pipfile
├── requirements.txt
│
├── templates/
│   ├── index.html
│   └── result.html
│
└── README.md
```

- **app.py**: The main Flask application script.
- **Procfile**: Configuration file for Heroku deployment.
- **Pipfile**: Specifies project dependencies and Python version.
- **requirements.txt**: Lists Python packages required by the app.
- **templates/**: Directory containing HTML templates.
  - **index.html**: The homepage with the questionnaire.
  - **result.html**: Displays the user's score and recommendations.
- **README.md**: This documentation file.

---

## Detailed Code Explanations

### app.py

```python
import os
import json
from flask import Flask, render_template, request
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Add enumerate to the Jinja2 environment globals
app.jinja_env.globals.update(enumerate=enumerate)

# Questions
questions = [
    # ... [List of questions with options and scores]
]

# Recommendations
recommendations = [
    # ... [List of recommendation dictionaries based on score ranges]
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
    opt_in = request.form.get('opt_in') == 'on'

    # Save the assessment information to Google Sheets
    data = [timestamp, name, email, company_name, industry, employees, role, score, recommendation, follow_up, opt_in]
    save_to_google_sheets(data)

    return render_template('result.html', score=score, recommendation=recommendation)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
```

**Explanation:**

- **Imports:** Essential libraries for Flask, handling JSON, datetime operations, and Google Sheets integration.
- **Flask App Initialization:** Sets up the Flask application and adds `enumerate` to Jinja2 globals for template usage.
- **Questions & Recommendations:** Defines the questionnaire and the logic for providing recommendations based on the user's score.
- **Google Sheets Setup:** Authenticates and connects to a specified Google Sheet using credentials provided via environment variables.
- **Routes:**
  - `/`: Renders the `index.html` template with the questionnaire.
  - `/submit`: Processes the form submission, calculates the score, determines recommendations, saves data to Google Sheets, and renders the `result.html` template.
- **Main Block:** Runs the Flask app on the specified port, defaulting to `5000`.

### templates/index.html

```html
<!DOCTYPE html>
<html lang="pt">
<head>
    <!-- [Head content including meta tags, styles, and scripts] -->
</head>
<body>
    <div class="progress-bar-container">
        <div class="progress-bar"></div>
    </div>
    <div class="container">
        <h1>Diagnóstico de Marketing Digital</h1>
        <h3>Preencha o formulário abaixo e receba um diagnóstico grátis de marketing digital</h3>
        <form action="/submit" method="post">
            <div class="section personal-info">
                <h3>Informações Pessoais</h3>
                <!-- [Input fields for personal information] -->
            </div>
            <div class="section business-info">
                <h3>Informações de Negócio</h3>
                {% for i, question in enumerate(questions) %}
                    <div class="question">
                        <h3>{{ question.question }}</h3>
                        <div class="question-options">
                            {% for option in question.options %}
                                <label>
                                    <input type="radio" name="question_{{ i }}" value="{{ option.score }}" required> {{ option.text }}
                                </label>
                            {% endfor %}
                        </div>
                    </div>
                {% endfor %}
            </div>
            <div class="section opt-in">
                <label class="opt-in-label">
                    <input type="checkbox" name="opt_in" id="opt_in">
                    <span class="custom-checkbox"></span>
                    <span class="label-text">Estou de acordo <a href="https://www.conectivo.com.br/nossa-politica-privacidade/" target="_blank">política privacidade</a></span>
                 </label>
            </div>
            <button type="submit">Acessar Diagnóstico</button>
        </form>
    </div>
</body>
</html>
```

**Explanation:**

- **Structure:** A responsive form that collects personal and business information along with answers to the marketing diagnostic questions.
- **Progress Bar:** Visual indicator showing the user's progress through the questionnaire.
- **Form Sections:**
  - **Personal Information:** Collects user's name, role, email, company name, industry, and number of employees.
  - **Business Information:** Dynamically generates questions from the `questions` list in `app.py`, allowing users to select answers.
  - **Opt-In:** Checkbox for users to agree to the privacy policy.
- **Styling & Scripts:** Inline CSS for styling and JavaScript for handling the progress bar updates based on user interactions.

### templates/result.html

```html
<!DOCTYPE html>
<html lang="pt">
<head>
    <!-- [Head content including meta tags and styles] -->
</head>
<body>
    <div class="container">
        <h1>Seu Score: {{ score }}</h1>
        <p>{{ recommendation }}</p>
        <h2>Fale com um Consultor</h2>
        <p>E obtenha mais informações de como transformar a estratégia de marketing digital da sua empresa, <a href="https://calendar.app.google/FFGNURK9Ei36bWpT8">agende aqui</a>.</p>
    </div>
</body>
</html>
```

**Explanation:**

- **Display Score and Recommendation:** Shows the user's total score and the corresponding recommendation based on their responses.
- **Call to Action:** Encourages users to schedule a consultation for further assistance, providing a link to a calendar booking page.
- **Styling:** Consistent with `index.html` for a seamless user experience.

### Procfile

```
web: python app.py
```

**Explanation:**

- **Purpose:** Specifies the command that Heroku should execute to start the application.
- **Content:** Tells Heroku to run `app.py` using Python when deploying the web application.

### Pipfile

```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
flask = "*"
gspread = "*"
oauth2client = "*"
secure-smtplib = "*"

[dev-packages]

[requires]
python_version = "3.11"
```

**Explanation:**

- **Source:** Defines the Python Package Index (PyPI) as the source for dependencies.
- **Packages:**
  - **flask:** Web framework used to build the application.
  - **gspread:** Library for interacting with Google Sheets.
  - **oauth2client:** Handles OAuth 2.0 authentication for Google APIs.
  - **secure-smtplib:** Provides secure SMTP client functionality.
- **Requires:** Specifies that the project requires Python version 3.11.

### requirements.txt

```
blinker==1.8.2
click==8.1.7
Flask==3.0.3
itsdangerous==2.2.0
Jinja2==3.1.4
MarkupSafe==2.1.5
Werkzeug==3.0.3
```

**Explanation:**

- **Dependency Versions:** Lists specific versions of packages required for the application to run, ensuring consistency across different environments.
- **Purpose:** Used for installing dependencies in environments where `pipenv` is not used.

---

## Deployment Instructions

Deploying the **Marketing Diagnostic App** to Heroku involves several steps. Below is a step-by-step guide to help you through the process.

### Prerequisites

- **Heroku CLI:** Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) on your machine.
- **Heroku Account:** Sign up for a [Heroku account](https://signup.heroku.com/) if you don't have one.
- **Git:** Ensure Git is installed and initialized in your project directory.

### Steps

1. **Login to Heroku**

   ```bash
   heroku login
   ```

   This command opens a browser window for authentication.

2. **Create a New Heroku App**

   ```bash
   heroku create your-app-name
   ```

   Replace `your-app-name` with your desired app name. If you omit the name, Heroku will generate one for you.

3. **Set Environment Variables**

   The app requires the `GOOGLE_SHEETS_CREDENTIALS` environment variable. Set it using Heroku's `config:set` command:

   ```bash
   heroku config:set GOOGLE_SHEETS_CREDENTIALS='{"type": "...", ...}'
   ```

   Replace the placeholder with your actual Google Sheets credentials JSON.

4. **Push Code to Heroku**

   ```bash
   git add .
   git commit -m "Deploy Marketing Diagnostic App"
   git push heroku main
   ```

   Ensure your main branch is named `main`. If it's `master`, adjust the command accordingly.

5. **Scale the Dynos**

   ```bash
   heroku ps:scale web=1
   ```

6. **Open the App**

   ```bash
   heroku open
   ```

   This command opens your deployed app in the default web browser.

### Additional Configurations

- **Logging:** To view logs for debugging, use:

  ```bash
  heroku logs --tail
  ```

- **Database (Optional):** If you plan to use a database in the future, consider adding Heroku Postgres:

  ```bash
  heroku addons:create heroku-postgresql:hobby-dev
  ```

---

## Usage Guidelines

### For Users

1. **Access the App:**
   - Navigate to the app's URL (e.g., `https://your-app-name.herokuapp.com`).

2. **Fill Out the Questionnaire:**
   - Provide personal and business information in the respective sections.
   - Answer all the marketing diagnostic questions by selecting the appropriate options.

3. **Submit the Form:**
   - After completing the questionnaire and agreeing to the privacy policy, click on the "Acessar Diagnóstico" button.

4. **View Results:**
   - Upon submission, you'll receive a score indicating the effectiveness of your marketing strategies.
   - Read the personalized recommendations to improve your marketing efforts.
   - Optionally, schedule a consultation with a marketing consultant for further assistance.

### For Administrators

- **Accessing Data:**
  - All user responses and scores are saved to the specified Google Sheet ("Marketing Diagnostic App").
  - Use Google Sheets to analyze data, track trends, and gain insights into user responses.

- **Managing Questions and Recommendations:**
  - To update questions or recommendations, modify the respective sections in `app.py` and redeploy the app.

- **Maintaining the App:**
  - Regularly monitor app performance and logs via Heroku.
  - Update dependencies as needed to ensure security and functionality.

---

## Contributing Guidelines

Thank you for considering contributing to the **Marketing Diagnostic App**! Your contributions help improve the application for everyone.

### How to Contribute

1. **Fork the Repository**

   Click the "Fork" button at the top-right corner of the repository page to create a personal copy.

2. **Clone the Forked Repository**

   ```bash
   git clone https://github.com/cacaprog/marketing-diagnostic-app.git
   cd marketing-diagnostic-app
   ```

3. **Create a New Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Changes**

   Implement your feature or fix a bug. Ensure that your code follows the project's coding standards.

5. **Commit Your Changes**

   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

6. **Push to Your Fork**

   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**

   Navigate to the original repository and click "Compare & pull request" for your branch. Provide a clear description of your changes.

### Code of Conduct

Please adhere to the [Code of Conduct](CODE_OF_CONDUCT.md) when contributing to this project.

---

## License Information

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this software as per the terms of the license.

---

## Acknowledgements

- **Flask:** A lightweight WSGI web application framework.
- **Google Sheets API:** For seamless data storage and retrieval.
- **Heroku:** For providing a platform to deploy and host the application.

---

## Contact

For any questions or feedback, please contact [ccananea@yahoo.com.br](mailto:ccananea@yahoo.com.br).

---

*Thank you for using the Marketing Diagnostic App! We hope it helps you enhance your digital marketing strategies effectively.*
