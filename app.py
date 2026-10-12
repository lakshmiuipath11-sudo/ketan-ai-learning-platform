import os
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from services.tinyfish import run_tinyfish

load_dotenv()
app = Flask(__name__)

QUESTIONS = [
    {"id": 1, "subject": "Mathematics", "question": "What is 12 × 8?", "options": ["84", "96", "108", "112"], "answer": 1},
    {"id": 2, "subject": "Science", "question": "Which planet is called the Red Planet?", "options": ["Venus", "Mars", "Jupiter", "Mercury"], "answer": 1},
    {"id": 3, "subject": "Mathematics", "question": "What is the square root of 144?", "options": ["10", "11", "12", "14"], "answer": 2},
]

@app.get('/')
def home():
    return render_template('index.html')

@app.get('/api/questions')
def questions():
    return jsonify([{k: v for k, v in q.items() if k != 'answer'} for q in QUESTIONS])

@app.post('/api/grade')
def grade():
    data = request.get_json(silent=True) or {}
    answers = data.get('answers', {})
    if not isinstance(answers, dict):
        return jsonify({'error': 'answers must be an object'}), 400
    score = sum(str(answers.get(str(q['id']))) == str(q['answer']) for q in QUESTIONS)
    return jsonify({'score': score, 'total': len(QUESTIONS)})

@app.get('/health')
def health():
    return jsonify({'status': 'ok'})

@app.get('/api/db-status')
def db_status():
    url = os.getenv('DATABASE_URL')
    if not url:
        return jsonify({'configured': False, 'connected': False})
    try:
        engine = create_engine(url, pool_pre_ping=True, connect_args={'connect_timeout': 3})
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))
        engine.dispose()
        return jsonify({'configured': True, 'connected': True})
    except Exception:
        return jsonify({'configured': True, 'connected': False}), 503

@app.post('/api/tinyfish/run')
def tinyfish_run():
    if not os.getenv('TINYFISH_API_KEY'):
        return jsonify({'error': 'TinyFish API key is not configured'}), 503
    data = request.get_json(silent=True) or {}
    url = data.get('url', '')
    goal = data.get('goal', '')
    if not isinstance(url, str) or not isinstance(goal, str) or not url.startswith('https://') or len(goal) > 1000:
        return jsonify({'error': 'Provide a valid HTTPS URL and goal'}), 400
    # This demo endpoint is deliberately disabled until authentication and
    # outbound URL allowlisting are implemented to prevent public API abuse.
    return jsonify({'error': 'TinyFish execution is disabled until authentication and URL allowlisting are configured'}), 501

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG') == '1', port=int(os.getenv('PORT', '5000')))
