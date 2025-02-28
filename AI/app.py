from flask import Flask, render_template, request, jsonify, Response
import requests
import json
import re

app = Flask(__name__)

# Ollama API endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"

def format_response(text):
    # 处理代码块：将```包裹的内容转换为HTML代码块
    text = re.sub(
        r'```(.*?)```',
        lambda m: f'<pre><code>{m.group(1)}</code></pre>',
        text,
        flags=re.DOTALL
    )
    # 将普通换行转换为<br>标签
    text = text.replace('\n', '<br>')
    return text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['GET'])
def chat():
    user_message = request.args.get('message', '')
    
    def generate():
        try:
            # 调用Ollama API，启用流式输出
            response = requests.post(
                OLLAMA_API_URL,
                json={
                    "model": "deepseek-r1:1.5b",
                    "prompt": user_message,
                    "stream": True
                },
                stream=True
            )
            
            if response.status_code != 200:
                yield f"data: {json.dumps({'response': '服务器错误：无法连接到Ollama服务'})}\n\n"
                return

            for line in response.iter_lines():
                if line:
                    json_response = json.loads(line)
                    if 'response' in json_response:
                        formatted_response = format_response(json_response['response'])
                        yield f"data: {json.dumps({'response': formatted_response})}\n\n"
            
            # 发送完成事件
            yield "event: done\ndata: {}\n\n"
                    
        except Exception as e:
            yield f"data: {json.dumps({'response': f'发生错误：{str(e)}'})}\n\n"
            
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True) 