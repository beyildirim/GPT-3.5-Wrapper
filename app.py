from flask import Flask, render_template, request, session
from datetime import datetime
import openai

app = Flask(__name__)

app.secret_key = 'my-secret-key'

openai.api_key = 'OpenAI API Key'

@app.route('/')
def home():
    if 'chat_history' not in session:
        session['chat_history'] = []

    return render_template('index.html', messages=session['chat_history'])

@app.route('/submit', methods=['POST'])
def submit():
    query = request.form['query']

    chat_history = session['chat_history']
    chat_history.append(('user', query))

    messages_formatted = [{'role': role, 'content': content} for role, content in chat_history]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages_formatted,
        max_tokens=256,
        temperature=0.7,
        n=1,
        stop=None
    )

    generated_text = response.choices[0].message['content']

    chat_history.append(('assistant', generated_text))

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query_message = f'<div class="message"><div class="text query">{query}<span class="timestamp">{timestamp}</span></div></div>'
    response_message = f'<div class="message"><div class="text response">{generated_text}<span class="timestamp">{timestamp}</span></div></div>'

    return query_message + response_message

if __name__ == '__main__':
    app.run(debug=True)
