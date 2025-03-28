from flask import Flask, render_template, request, Response, stream_with_context
import requests
import json
from config import DEEPSEEK_API_KEY

app = Flask(__name__)

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    messages = data.get('messages', [])

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    def generate():
        try:
            response = requests.post(
                DEEPSEEK_API_URL,
                headers=headers,
                json={
                    "model": "deepseek-chat",
                    "messages": messages,
                    "stream": True,
                    "temperature": 0.7
                },
                stream=True
            )

            for line in response.iter_lines():
                if line:
                    try:
                        json_response = json.loads(line.decode('utf-8').replace('data: ', ''))
                        if 'choices' in json_response and len(json_response['choices']) > 0:
                            content = json_response['choices'][0].get('delta', {}).get('content', '')
                            if content:
                                yield f"data: {json.dumps({'content': content})}\n\n"
                    except json.JSONDecodeError:
                        continue

            yield "event: done\ndata: {}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)