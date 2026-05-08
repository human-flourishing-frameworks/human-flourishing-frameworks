import os
from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return {
        'status': 'ok',
        'message': 'Impossibility Engine',
        'timestamp': datetime.utcnow().isoformat()
    }

@app.route('/health', methods=['GET'])
def health():
    return {'ok': True}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
