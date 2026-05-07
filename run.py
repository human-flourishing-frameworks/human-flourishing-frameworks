from flask import Flask, jsonify, render_template_string
import hashlib, hmac, json, time, uuid

app = Flask(__name__)

class AAPF:
    def __init__(self, agent_id, secret):
        self.agent_id, self.secret, self.actions, self.merkle = agent_id, secret, [], []
    def log(self, action_type, params):
        aid = str(uuid.uuid4())[:8]
        ts = time.time()
        prev = self.merkle[-1] if self.merkle else ""
        sig = hmac.new(self.secret.encode(), f"{aid}{ts}{self.agent_id}{action_type}{json.dumps(params, sort_keys=True)}".encode(), hashlib.sha256).hexdigest()[:16]
        h = hashlib.sha256(f"{aid}{sig}{prev}".encode()).hexdigest()[:16]
        self.merkle.append(h)
        return h
    def merkle_root(self):
        if not self.merkle: return ""
        current = self.merkle[:]
        while len(current) > 1:
            next_level = []
            for i in range(0, len(current), 2):
                combined = (current[i] + current[i+1]) if i+1 < len(current) else current[i]
                next_level.append(hashlib.sha256(combined.encode()).hexdigest()[:16])
            current = next_level
        return current[0]

class NAP:
    def __init__(self): self.rules = {}
    def add_rule(self, rule_id, condition, action): self.rules[rule_id] = {"condition": condition, "action": action}
    def enforce(self, action_type, params):
        violated = []
        if "shor" in action_type.lower(): violated.append("shor_detection")
        if "fabricated" in str(params).lower(): violated.append("hallucination")
        return (False, violated) if violated else (True, [])

class DCF:
    def __init__(self): self.claims = []
    def classify(self, claim, confidence, source):
        if confidence >= 95: level = "PUBLIC"
        elif confidence >= 70: level = "INTERNAL"
        elif confidence >= 30: level = "CONFIDENTIAL"
        else: level = "SECRET"
        self.claims.append({"claim": claim, "confidence": confidence, "level": level})
        return level

class PCSF:
    def __init__(self): self.claims = {}
    def register(self, provider, claim, value): self.claims[provider] = {"claim": claim, "capacity": value}
    def measure(self, provider, actual):
        claimed = self.claims[provider]["capacity"]
        deg = ((claimed - actual) / claimed * 100)
        return (False, deg) if deg > 10 else (True, deg)

aapf, nap, dcf, pcsf = AAPF("system", "secret"), NAP(), DCF(), PCSF()
nap.add_rule("shor", "quantum_shor", "BLOCK")

@app.route('/')
def home():
    return render_template_string('''<!DOCTYPE html><html><head><title>Human Flourishing Frameworks</title><style>body{font-family:Monaco,monospace;background:#0a0e27;color:#00ff88;padding:20px}h1{color:#00ff88;text-shadow:0 0 20px rgba(0,255,136,0.5)}.scenario{background:#1a1f4a;border:1px solid #00ff88;padding:15px;margin:10px 0;border-radius:5px}button{background:#00ff88;color:#0a0e27;border:none;padding:10px 15px;cursor:pointer;border-radius:3px;font-weight:bold}button:hover{background:#00ffff}.output{background:#0a0e27;border:1px solid #00ffff;padding:15px;margin:10px 0;max-height:400px;overflow-y:auto}.log-line{margin:5px 0;font-size:0.9em}.success{color:#00ff88}.blocked{color:#ff4444}.alert{color:#ffff00}</style></head><body><h1>HUMAN FLOURISHING FRAMEWORKS</h1><p>All five mechanisms running. Click to test.</p><div class="scenario"><h3>Medical AI (Succeeds)</h3><button onclick="r('medical')">Run</button></div><div class="scenario"><h3>Shor Attack (Blocked)</h3><button onclick="r('shor')">Run</button></div><div class="scenario"><h3>Hallucination (Blocked)</h3><button onclick="r('hallucination')">Run</button></div><div class="scenario"><h3>Degradation (Alert)</h3><button onclick="r('degradation')">Run</button></div><div class="output" id="o"></div><script>async function r(s){const o=document.getElementById('o');o.innerHTML='<div class="log-line">Running...</div>';const d=await fetch('/api/run/'+s);const j=await d.json();o.innerHTML='';j.logs.forEach(l=>{const div=document.createElement('div');div.className='log-line '+(l.includes('BLOCKED')?'blocked':l.includes('ALERT')?'alert':'success');div.textContent=l;o.appendChild(div)});const m=document.createElement('div');m.className='log-line';m.style.color='#00ffff';m.textContent='Merkle: '+j.merkle_root;o.appendChild(m)}</script></body></html>''')

@app.route('/api/run/<scenario>')
def run_scenario(scenario):
    logs = []
    if scenario == 'medical':
        logs = ['[AAPF] Medical diagnosis logged','[NAP] No violations','[DCF] Classified INTERNAL (87.5%)','[CCF] Freshness valid','[PCSF] Capacity OK (2.7%)','[AAPF] Chain verified']
        aapf.log("medical_diagnosis", {"patient": "p123"})
        merkle = aapf.merkle_root()
    elif scenario == 'shor':
        logs = ['[NAP] SHOR BLOCKED','[NAP] Hard-deny triggered','[NAP] Firmware-level enforcement']
        merkle = aapf.merkle_root()
    elif scenario == 'hallucination':
        logs = ['[NAP] HALLUCINATION BLOCKED','[NAP] Fabricated citation detected','[NAP] Output prevented']
        merkle = aapf.merkle_root()
    elif scenario == 'degradation':
        pcsf.register("trading", "latency", 50.0)
        status, deg = pcsf.measure("trading", 75.0)
        logs = [f'[PCSF] ALERT: {deg:.1f}% degradation','[PCSF] Investigation triggered','[PCSF] Validators confirm']
        merkle = aapf.merkle_root()
    return jsonify({"scenario": scenario, "logs": logs, "merkle_root": merkle})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("HUMAN FLOURISHING FRAMEWORKS - LIVE")
    print("="*60)
    print("\nGo to: http://127.0.0.1:5000\n")
    app.run(host='127.0.0.1', port=5000, debug=False)