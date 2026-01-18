from flask import Flask, request, jsonify
from service import DreamInterpreter
import os
import sys

# Ensure we can import from current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

# Lazy loading or global loading? Global is better for responsiveness.
print("Initializing AI Model...")
# Initialize interpreter. 
# Note: In production, this might take time and memory.
try:
    interpreter = DreamInterpreter()
    print("AI Model Initialized successfully.")
except Exception as e:
    print(f"Error initializing AI model: {e}")
    interpreter = None

@app.route('/', methods=['GET'])
def index():
    return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8" />
    <title>梦境解析 AI 助手</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 0 16px;
            background-color: #f5f5f5;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        .card {
            background: #fff;
            border-radius: 8px;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        textarea {
            width: 100%;
            min-height: 120px;
            padding: 12px;
            border-radius: 6px;
            border: 1px solid #ccc;
            resize: vertical;
            font-size: 14px;
        }
        button {
            margin-top: 12px;
            padding: 10px 18px;
            border-radius: 6px;
            border: none;
            background-color: #4f46e5;
            color: #fff;
            font-size: 14px;
            cursor: pointer;
        }
        button:disabled {
            background-color: #a5b4fc;
            cursor: not-allowed;
        }
        #status {
            margin-top: 8px;
            font-size: 13px;
            color: #666;
        }
        #result {
            margin-top: 16px;
            padding: 16px;
            background-color: #111827;
            color: #e5e7eb;
            border-radius: 8px;
            white-space: pre-wrap;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <h1>梦境解析 AI 助手</h1>
    <div class="card">
        <p>在下面输入你的梦境描述，点击“开始解析”即可查看 AI 的解析结果。</p>
        <textarea id="dream-input" placeholder="例如：昨晚我梦见自己在飞，但怎么也飞不高……"></textarea>
        <button id="submit-btn" onclick="interpretDream()">开始解析</button>
        <div id="status"></div>
        <div id="result"></div>
    </div>
    <script>
        async function interpretDream() {
            const textarea = document.getElementById('dream-input');
            const resultEl = document.getElementById('result');
            const statusEl = document.getElementById('status');
            const button = document.getElementById('submit-btn');

            const text = textarea.value.trim();
            if (!text) {
                alert('请先输入你的梦境内容');
                return;
            }

            button.disabled = true;
            statusEl.textContent = '🔮 正在解析中，这可能需要一段时间，请稍候…';
            resultEl.textContent = '';

            try {
                const response = await fetch('/interpret', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ text })
                });

                const data = await response.json();

                if (response.ok && data.interpretation) {
                    statusEl.textContent = '✅ 解析完成';
                    resultEl.textContent = data.interpretation;
                } else {
                    statusEl.textContent = '❌ 解析失败';
                    resultEl.textContent = data.error || '未知错误';
                }
            } catch (e) {
                statusEl.textContent = '❌ 请求失败，请确认 AI 服务正在运行';
                resultEl.textContent = e.toString();
            } finally {
                button.disabled = false;
            }
        }
    </script>
</body>
</html>
    """

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'model_loaded': interpreter is not None})

@app.route('/interpret', methods=['POST'])
def interpret():
    if not interpreter:
        return jsonify({'error': 'AI Model not initialized'}), 503

    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        result = interpreter.interpret(text)
        return jsonify({'interpretation': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
