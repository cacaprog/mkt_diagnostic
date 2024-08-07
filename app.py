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
    {
        "question": "Você têm um entendimento claro do seu público-alvo?",
        "options": [
            {"text": "Muito claro", "score": 10},  # 5 * 2
            {"text": "Razoavelmente claro", "score": 6},  # 3 * 2
            {"text": "Pouco claro", "score": 4},  # 2 * 2
            {"text": "Nada claro", "score": 0}
        ]
    },
    {
        "question": "Você tem uma proposta de valor única que diferencia seu produto/serviço?",
        "options": [
            {"text": "Sim", "score": 10},  # 5 * 2
            {"text": "Não", "score": 0}
        ]
    },
    {
        "question": "Você têm um processo de vendas definido?",
        "options": [
            {"text": "Muito definido", "score": 10},  # 5 * 2
            {"text": "Moderadamente definido", "score": 6},  # 3 * 2
            {"text": "Pouco definido", "score": 4},  # 2 * 2
            {"text": "Nada definido", "score": 0}
        ]
    },
    {
        "question": "Quão eficazes são suas estratégias de vendas na conversão de leads?",
        "options": [
            {"text": "Muito eficazes", "score": 10},  # 5 * 2
            {"text": "Moderadamente eficazes", "score": 6},  # 3 * 2
            {"text": "Pouco eficazes", "score": 4},  # 2 * 2
            {"text": "Nada eficazes", "score": 0}
        ]
    },
    {
        "question": "Quão diversificados são os seus canais de marketing digital?",
        "options": [
            {"text": "Muito diversificados", "score": 10},  # 5 * 2
            {"text": "Moderadamente diversificados", "score": 6},  # 3 * 2
            {"text": "Pouco diversificados", "score": 4},  # 2 * 2
            {"text": "Nada diversificados", "score": 0}
        ]
    },
    {
        "question": "Você tem uma estratégia documentada para cada canal de marketing digital?",
        "options": [
            {"text": "Sim", "score": 10},  # 5 * 2
            {"text": "Não", "score": 0}
        ]
    },
    {
        "question": "Você analisa os seus KPIs de marketing digital?",
        "options": [
            {"text": "Semanalmente", "score": 10},  # 5 * 2
            {"text": "Mensalmente", "score": 6},  # 3 * 2
            {"text": "Trimestralmente", "score": 4},  # 2 * 2
            {"text": "Raramente/Nunca", "score": 0}
        ]
    },
    {
        "question": "Você tem um sistema centralizado para coletar e analisar dados de marketing?",
        "options": [
            {"text": "Sim", "score": 10},  # 5 * 2
            {"text": "Parcialmente", "score": 6},  # 3 * 2
            {"text": "Não", "score": 0}
        ]
    },
    {
        "question": "Quão confiante você está na precisão e integridade dos seus dados?",
        "options": [
            {"text": "Muito confiante", "score": 10},  # 5 * 2
            {"text": "Moderadamente confiante", "score": 6},  # 3 * 2
            {"text": "Pouco confiante", "score": 4},  # 2 * 2
            {"text": "Nada confiante", "score": 0}
        ]
    },
    {
        "question": "Você usa regularmente insights baseados em dados para otimizar suas campanhas de marketing digital?",
        "options": [
            {"text": "Sim, sempre", "score": 10},  # 5 * 2
            {"text": "Ocasionalmente", "score": 6},  # 3 * 2
            {"text": "Raramente", "score": 4},  # 2 * 2
            {"text": "Nunca", "score": 0}
        ]
    }
]



# Recommendations
recommendations = [
    {
        "min_score": 75,
        "max_score": 100,
        "recommendation": "Sua estratégia de Marketing Digital é forte. Continue refinando sua abordagem e explore táticas avançadas para manter sua vantagem competitiva.",
        "follow_up": "Implemente segmentação avançada de clientes, experimente campanhas inovadoras, colete e analise feedback de clientes, estabeleça parcerias e mantenha-se atualizado com as tendências emergentes."
    },
    {
        "min_score": 50,
        "max_score": 74,
        "recommendation": "Você tem uma base sólida, mas várias áreas precisam de melhorias. Foque na diversificação dos canais, refinamento dos processos de vendas e utilização de análises.",
        "follow_up": "Explore novos canais de marketing, invista em treinamento de vendas, integre ferramentas avançadas de análise, desenvolva uma estratégia de conteúdo abrangente e implemente automação de marketing."
    },
    {
        "min_score": 25,
        "max_score": 49,
        "recommendation": "Sua estratégia de Marketing Digital precisa de melhorias significativas. Priorize a criação de uma estratégia documentada e revisões regulares de desempenho.",
        "follow_up": "Crie um documento detalhado de estratégia, conduza auditorias regulares, defina métricas de desempenho claras, desenvolva um calendário de conteúdo e construa personas detalhadas de clientes."
    },
    {
        "min_score": 0,
        "max_score": 24,
        "recommendation": "Sua estratégia de Marketing Digital está no início ou inexistente. Ação imediata é necessária para estabelecer uma estratégia robusta.",
        "follow_up": "Crie uma estratégia fundamental, inscreva-se em treinamentos de marketing e vendas, invista em ferramentas essenciais de marketing, lance campanhas iniciais e considere contratar um consultor ou agência para orientação."
    }
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