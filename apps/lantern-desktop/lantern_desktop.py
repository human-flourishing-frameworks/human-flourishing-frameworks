#!/usr/bin/env python3
"""Native Lantern desktop chat app.

Purpose:
A plain local chat interface between Alex/operator, Lantern, and the HFF repo.

Boundary:
- standard-library Tkinter app;
- localhost Lantern backend only;
- one operator chat path;
- no hosted GPT/Claude/API calls from Lantern;
- no agents, tunnels, sensors, deployments, or repo writes from chat;
- stays on until the user closes the window.
"""

from __future__ import annotations

import json
from pathlib import Path
import queue
import socket
import subprocess
import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_SCRIPT = REPO_ROOT / "apps" / "lantern-local-chat" / "local_lantern_server.py"
DEFAULT_PORT = 8765
MAX_PORT = 8799
INTERNAL_BACKEND_MODE = "engineer"


class LocalLantern:
    """Localhost client plus backend process manager."""

    def __init__(self, preferred_port: int = DEFAULT_PORT, max_port: int = MAX_PORT) -> None:
        self.preferred_port = preferred_port
        self.max_port = max_port
        self.endpoint: str | None = None
        self.process: subprocess.Popen[str] | None = None

    @staticmethod
    def endpoint_for(port: int) -> str:
        return f"http://127.0.0.1:{port}"

    @staticmethod
    def _can_bind(port: int) -> bool:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind(("127.0.0.1", port))
            return True
        except OSError:
            return False

    def health(self, endpoint: str | None = None) -> dict[str, Any]:
        target = endpoint or self.endpoint or self.endpoint_for(self.preferred_port)
        url = target.rstrip("/") + "/healthz"
        try:
            with urlopen(Request(url, headers={"accept": "application/json"}), timeout=1.0) as response:  # noqa: S310
                data = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            return {"ok": False, "status": "BACKEND_HTTP_ERROR_OBSERVED", "url": url, "error": f"HTTP {exc.code}"}
        except (URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            return {"ok": False, "status": "BACKEND_UNREACHABLE_OBSERVED", "url": url, "error": type(exc).__name__}
        if not isinstance(data, dict):
            return {"ok": False, "status": "BACKEND_INVALID_RESPONSE_OBSERVED", "url": url}
        return {
            "ok": data.get("ok") is True,
            "status": "BACKEND_REACHABLE_OBSERVED" if data.get("ok") is True else "BACKEND_DEGRADED_OBSERVED",
            "url": url,
            "raw": data,
        }

    def find_running_endpoint(self) -> str | None:
        checked: set[int] = set()
        for port in [self.preferred_port, *range(DEFAULT_PORT, self.max_port + 1)]:
            if port in checked:
                continue
            checked.add(port)
            endpoint = self.endpoint_for(port)
            if self.health(endpoint).get("ok") is True:
                return endpoint
        return None

    def choose_free_endpoint(self) -> str:
        checked: set[int] = set()
        for port in [self.preferred_port, *range(DEFAULT_PORT, self.max_port + 1)]:
            if port in checked:
                continue
            checked.add(port)
            if self._can_bind(port):
                return self.endpoint_for(port)
        return self.endpoint_for(self.preferred_port)

    def ensure_backend(self) -> str:
        running = self.find_running_endpoint()
        if running:
            self.endpoint = running
            return running
        if not BACKEND_SCRIPT.exists():
            raise FileNotFoundError(f"Lantern backend script not found: {BACKEND_SCRIPT}")
        endpoint = self.choose_free_endpoint()
        port = int(endpoint.rsplit(":", 1)[1])
        self.process = subprocess.Popen(
            [sys.executable, str(BACKEND_SCRIPT), "--host", "127.0.0.1", "--port", str(port)],
            cwd=REPO_ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
            creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
        )
        deadline = time.monotonic() + 10.0
        while time.monotonic() < deadline:
            if self.health(endpoint).get("ok") is True:
                self.endpoint = endpoint
                return endpoint
            time.sleep(0.25)
        raise RuntimeError(f"Lantern backend did not become reachable at {endpoint}")

    def chat(self, message: str) -> dict[str, Any]:
        if not self.endpoint:
            self.ensure_backend()
        url = (self.endpoint or self.endpoint_for(self.preferred_port)).rstrip("/") + "/chat"
        payload = json.dumps({"message": message, "mode": INTERNAL_BACKEND_MODE}).encode("utf-8")
        request = Request(url, data=payload, headers={"content-type": "application/json"}, method="POST")
        try:
            with urlopen(request, timeout=20.0) as response:  # noqa: S310
                data = json.loads(response.read().decode("utf-8"))
        except Exception as exc:  # pragma: no cover - UI surface.
            return {"ok": False, "answer": f"Local Lantern backend is not reachable: {type(exc).__name__}"}
        return data if isinstance(data, dict) else {"ok": False, "answer": "Lantern returned a non-object response."}

    def stop_owned_backend(self) -> None:
        if self.process is None:
            return
        if self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.process.kill()
        self.process = None


def plain_chat_answer(data: dict[str, Any]) -> str:
    """Return a plain chat answer without symbolic/game labels or raw source dumps."""

    if data.get("ok") is not True:
        return str(data.get("answer") or data.get("error") or "Lantern could not answer from the local backend.")

    if isinstance(data.get("plainAnswer"), str) and data["plainAnswer"].strip():
        return data["plainAnswer"].strip()

    frame = data.get("minimalFrame") if isinstance(data.get("minimalFrame"), dict) else {}
    if frame:
        summary = frame.get("Fact", "I read the current repo-backed context.")
        boundary = frame.get("Boundary", "This is local repo-backed output, not an oracle or autonomous action.")
        next_step = frame.get("Next", "Choose one bounded next step.")
        return f"Answer: {summary}\n\nBoundary: {boundary}\n\nNext step: {next_step}"

    answer = str(data.get("answer") or "Lantern local answer was empty.")
    blocked_headings = ("Sources:", "Limits:", "Minimal convergence frame:")
    kept: list[str] = []
    for line in answer.splitlines():
        if any(line.strip().startswith(heading) for heading in blocked_headings):
            break
        kept.append(line)
    cleaned = "\n".join(line for line in kept if not line.startswith("Lantern local answer")).strip()
    return cleaned or answer


class LanternChat(tk.Tk):
    """Persistent local desktop chat for Lantern and the repo."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Lantern Chat")
        self.geometry("980x720")
        self.minsize(760, 520)
        self.client = LocalLantern()
        self.events: queue.Queue[tuple[str, Any]] = queue.Queue()
        self.status = tk.StringVar(value="STARTING_OBSERVED")
        self.endpoint = tk.StringVar(value="Endpoint: unknown")
        self.protocol("WM_DELETE_WINDOW", self.close)
        self._build()
        self.after(100, self._poll)
        threading.Thread(target=self._start_backend, daemon=True).start()

    def _build(self) -> None:
        main = ttk.Frame(self, padding=12)
        main.pack(fill=tk.BOTH, expand=True)

        top = ttk.Frame(main)
        top.pack(fill=tk.X)
        ttk.Label(top, text="Lantern Chat", font=("Segoe UI", 20, "bold")).pack(side=tk.LEFT)
        ttk.Label(top, textvariable=self.status).pack(side=tk.RIGHT)

        description = (
            "Local chat between Alex/operator, Lantern, and the HFF repo. "
            "One operator path. No mode picker. No command execution, repo edits, deployments, browsing, or hosted GPT/Claude calls from this path."
        )
        ttk.Label(main, text=description, wraplength=920).pack(fill=tk.X, pady=(8, 4))
        ttk.Label(main, textvariable=self.endpoint).pack(fill=tk.X, pady=(0, 8))

        toolbar = ttk.Frame(main)
        toolbar.pack(fill=tk.X, pady=(0, 8))
        ttk.Button(toolbar, text="Status", command=self.show_status).pack(side=tk.LEFT)
        ttk.Button(toolbar, text="Clear", command=self.clear).pack(side=tk.LEFT, padx=(6, 0))

        self.output = scrolledtext.ScrolledText(main, wrap=tk.WORD, height=24, font=("Consolas", 10))
        self.output.pack(fill=tk.BOTH, expand=True)
        self.output.insert(tk.END, "Lantern Chat is starting. It stays on until you close this window.\n\n")
        self.output.configure(state=tk.DISABLED)

        bottom = ttk.Frame(main)
        bottom.pack(fill=tk.X, pady=(8, 0))
        self.input = tk.Text(bottom, height=4, wrap=tk.WORD)
        self.input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input.bind("<Control-Return>", lambda _event: self.ask())
        ttk.Button(bottom, text="Send", command=self.ask).pack(side=tk.RIGHT, fill=tk.Y, padx=(8, 0))

    def append(self, text: str) -> None:
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, text + "\n\n")
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)

    def clear(self) -> None:
        self.output.configure(state=tk.NORMAL)
        self.output.delete("1.0", tk.END)
        self.output.configure(state=tk.DISABLED)

    def _start_backend(self) -> None:
        try:
            endpoint = self.client.ensure_backend()
            self.events.put(("ready", endpoint))
        except Exception as exc:  # pragma: no cover - UI surface.
            self.events.put(("error", str(exc)))

    def _poll(self) -> None:
        try:
            while True:
                kind, value = self.events.get_nowait()
                if kind == "ready":
                    self.status.set("BACKEND_REACHABLE_OBSERVED")
                    self.endpoint.set(f"Endpoint: {value}")
                    self.append(f"Status: BACKEND_REACHABLE_OBSERVED at {value}")
                elif kind == "error":
                    self.status.set("BACKEND_UNREACHABLE_OBSERVED")
                    self.append(f"Error: {value}")
                elif kind == "answer":
                    self.append(value)
        except queue.Empty:
            pass
        self.after(100, self._poll)

    def ask(self) -> None:
        message = self.input.get("1.0", tk.END).strip()
        if not message:
            return
        self.input.delete("1.0", tk.END)
        self.append(f"Alex: {message}")
        threading.Thread(target=self._ask_thread, args=(message,), daemon=True).start()

    def _ask_thread(self, message: str) -> None:
        self.events.put(("answer", "Lantern:\n" + plain_chat_answer(self.client.chat(message))))

    def show_status(self) -> None:
        health = self.client.health()
        raw = health.get("raw") if isinstance(health.get("raw"), dict) else {}
        repo = raw.get("repoState") if isinstance(raw.get("repoState"), dict) else {}
        branch = repo.get("branch", "UNKNOWN")
        commit = str(repo.get("commit", "UNKNOWN"))[:12]
        clean = repo.get("isClean", "UNKNOWN")
        self.append(
            "Lantern Chat status — bounded observation\n"
            f"Desktop chat: ONLINE_OBSERVED until closed.\n"
            f"Local backend: {health.get('status', 'UNKNOWN')} at {health.get('url', 'unknown')}.\n"
            f"Repo signal: branch {branch}, commit {commit}, clean {clean}.\n"
            "Edge: This is the current observed local path, not a guarantee of uptime, autonomy, full safety, or no GPT outside Lantern."
        )

    def close(self) -> None:
        if messagebox.askokcancel("Close Lantern Chat", "Close Lantern Chat?"):
            self.client.stop_owned_backend()
            self.destroy()


def main() -> int:
    app = LanternChat()
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
