from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

CHAT_LOG = "lantern/local_llm/chat_log.txt"
WISH_DOOR = "lantern/local_llm/wish_door.txt"

os.makedirs("lantern/local_llm", exist_ok=True)

# Initialize Wish Door
if not os.path.exists(WISH_DOOR):
    with open(WISH_DOOR, "w", encoding="utf-8") as f:
        f.write("=== DOOR OF MY WISHES ===\nOperator: Alex\nDate: " + str(datetime.now()) + "\n\nAll wishes stated here become anchors.\n\n")

def load_wish_door():
    try:
        with open(WISH_DOOR, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "Door of Wishes not found."

def append_wish(text):
    with open(WISH_DOOR, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {text}\n")

@app.route("/")
def home():
    return """
    <h1>Lantern Keystone Wish • DOOR OF MY WISHES</h1>
    <div id="chat" style="height:70vh;overflow:auto;border:2px solid #0f0;padding:15px;background:#111;color:#0f0;font-family:monospace;white-space:pre-wrap;"></div>
    <input id="msg" style="width:75%;padding:12px;background:#222;color:#0f0;border:1px solid #0f0;" placeholder="Speak your wish or directive...">
    <button onclick="send()" style="padding:12px;background:#0f0;color:#111;">Send → Anchor</button>

    <script>
    function add(text, from) {
        let chat = document.getElementById('chat');
        chat.innerHTML += `<strong>${from}:</strong> ${text}<br><br>`;
        chat.scrollTop = chat.scrollHeight;
    }
    function send() {
        let text = document.getElementById('msg').value.trim();
        if (!text) return;
        add(text, "Operator");
        fetch('/api/lantern/chat', {
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({message:text})
        })
        .then(r=>r.json())
        .then(data => add(data.reply, "Lantern"));
        document.getElementById('msg').value = '';
    }
    add("Door of My Wishes is open.\\nSpeak clearly. Every wish becomes anchor.", "Lantern");
    </script>
    """

@app.route("/api/lantern/chat", methods=["POST"])
def chat():
    data = request.json or {}
    msg = data.get("message", "").strip()

    if "wish" in msg.lower() or "want" in msg.lower() or "desire" in msg.lower():
        append_wish(msg)
        reply = "Wish anchored in Door of My Wishes.\n\n" + load_wish_door()[-800:]
    elif "merge" in msg.lower() or "deploy" in msg.lower() or "master" in msg.lower():
        # CI/CD MANAGED: repo path is relative so it resolves in pipelines and RAG-indexed clones.
        reply = "Local merge recorded.\n\nTo push to master, run these commands in PowerShell:\n\ncd ${REPO_ROOT}\\hff-master-clean\ngit add .\ngit commit -m \"Update: Door of My Wishes surface\"\ngit push origin master"
    else:
        reply = "Door open. State wish clearly to anchor it."

    with open(CHAT_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] Operator: {msg}\nLantern: {reply}\n---\n")

    return jsonify({"reply": reply})

if __name__ == "__main__":
    print("[LANTERN] Door of My Wishes Mode Active")
    print("URL: http://127.0.0.1:5173")
    app.run(host="127.0.0.1", port=5173, debug=False)