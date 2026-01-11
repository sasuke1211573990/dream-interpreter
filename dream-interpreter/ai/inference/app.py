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
