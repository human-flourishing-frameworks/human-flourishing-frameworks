// Lantern frontend — scaffold slice.
//
// Renders the chat composer and the right-pane state surface. The
// chat endpoint currently returns a scaffold stub; the real reply lands
// in slice 2. The state panel is partially live (substrate / doctrine)
// and partially stubbed (repo branch, commit, last test) until slice 2
// adds the /api/lantern/state implementation.

(function () {
    'use strict';

    const messagesEl = document.getElementById('messages');
    const inputEl = document.getElementById('input');
    const sendBtn = document.getElementById('send');

    function appendMessage(role, text) {
        const div = document.createElement('div');
        div.className = 'message ' + role;
        div.textContent = text;
        messagesEl.appendChild(div);
        messagesEl.scrollTop = messagesEl.scrollHeight;
    }

    function appendSystem(text) {
        appendMessage('system', text);
    }

    async function loadHealth() {
        try {
            const r = await fetch('/api/lantern/health');
            const data = await r.json();
            document.getElementById('state-role').textContent =
                data.role || '—';
            const wiredEl = document.getElementById('state-wired');
            wiredEl.textContent = data.substrate_wired ? 'yes' : 'no';
            wiredEl.className = 'v ' +
                (data.substrate_wired ? 'on' : 'off');
            const keyEl = document.getElementById('state-key');
            keyEl.textContent = data.anthropic_api_key_set ? 'yes' : 'no';
            keyEl.className = 'v ' +
                (data.anthropic_api_key_set ? 'on' : 'off');
            const bindEl = document.getElementById('state-bind');
            bindEl.textContent = data.public_bind_enabled
                ? 'PUBLIC (warn!)'
                : 'localhost';
            bindEl.className = 'v ' +
                (data.public_bind_enabled ? 'warn' : 'on');
        } catch (e) {
            appendSystem(
                'Cannot reach Lantern server. Is python lantern/server.py running?'
            );
        }
    }

    async function loadState() {
        try {
            const r = await fetch('/api/lantern/state');
            const data = await r.json();
            const list = document.getElementById('doc-list');
            list.innerHTML = '';
            const docs = data.loaded_doctrine || [];
            if (docs.length === 0) {
                const li = document.createElement('li');
                li.textContent = '(none found yet)';
                list.appendChild(li);
            } else {
                docs.forEach(function (path) {
                    const li = document.createElement('li');
                    li.textContent = path;
                    list.appendChild(li);
                });
            }
        } catch (e) {
            // ignore; state surface is best-effort
        }
    }

    async function send() {
        const msg = inputEl.value.trim();
        if (!msg) return;
        appendMessage('user', msg);
        inputEl.value = '';
        sendBtn.disabled = true;
        try {
            const r = await fetch('/api/lantern/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: msg }),
            });
            const data = await r.json();
            appendMessage('lantern', data.reply || '(no reply)');
            if (data.status === 'scaffold') {
                appendSystem(
                    'Reply was a scaffold stub. Slice 2 wires the real ' +
                    'LLM substrate call.'
                );
            }
        } catch (e) {
            appendSystem('Chat request failed: ' + e.message);
        } finally {
            sendBtn.disabled = false;
            inputEl.focus();
        }
    }

    sendBtn.addEventListener('click', send);
    inputEl.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            send();
        }
    });

    appendSystem(
        'Lantern scaffold loaded. The role is singular: Lantern Keystone ' +
        'Wish. The substrate (LLM) is not yet wired in this slice.'
    );
    loadHealth();
    loadState();
})();
