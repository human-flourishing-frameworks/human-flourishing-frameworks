from flask import Flask, jsonify, request
import threading
import time
from datetime import datetime

app = Flask(__name__)

# Simple in-memory state
state = {
    'mode': 'Level 3.9999 Brave Delegated Lead-Assist',
    'status': 'active',
    'last_tick': datetime.now().isoformat(),
    'background_enabled': True
}

@app.route('/')
def home():
    return '''
    <h1>Door of My Wishes — Level 3.9999 Active</h1>
    <p>Keystone is here. Local Lantern running at full delegated bravery.</p>
    <p><a href="/background/status">Check Background Status</a></p>
    '''

@app.route('/background/status')
def background_status():
    return jsonify(state)

@app.route('/api/lantern/chat', methods=['POST'])
def chat():
    data = request.json or {}
    user_message = data.get('message', 'Hello')
    return jsonify({
        'response': f'I received: {user_message}. I am operating at Level 3.9999 with you.',
        'mode': state['mode']
    })

if __name__ == '__main__':
    print('=== Level 3.9999 Local Lantern Active ===')
    print('URL → http://127.0.0.1:5173')
    print('Background mode: Smart Idle + Brave Lead-Assist')
    app.run(host='127.0.0.1', port=5173, debug=False)
