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

from datetime import datetime
import json
from pathlib import Path
import queue
import socket
import subprocess
import sys
import threading
import time
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, scrolledtext, ttk
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_SCRIPT = REPO_ROOT / "apps" / "lantern-local-chat" / "local_lantern_server.py"
DEFAULT_PORT = 8765
MAX_PORT = 8799
INTERNAL_BACKEND_MODE = "engineer"

# Optional operator-supplied branding image. If present, used as the Lantern
# avatar at the top of the window. Falls back to a canvas-drawn glyph.
AVATAR_PATH = Path.home() / ".lantern" / "avatar.png"

# Palette drawn from Gage's yacht art + Captain Lantern Blinkbug imagery.
# Safe = legible, predictable, bounded. Fun = bright sky, warm glow, cartoon energy.
PALETTE = {
    "bg_canvas":          "#a8d4f0",  # sky blue (Gage's water + sky)
    "bg_chat":            "#ffffff",  # crisp white chat surface — high contrast
    "bg_input":           "#ffffff",  # clean input
    "bg_callout":         "#fff8e0",  # warm cream — for callout bubbles
    "fg_body":            "#1a2c5c",  # night-sky deep blue (readable, calm)
    "fg_muted":           "#4a6280",  # readable sky-blue gray
    "fg_title":           "#0d1b3a",  # near-black sky for big headings
    "accent_lantern":     "#e8a73d",  # blinkbug body yellow (warm glow)
    "accent_lantern_bg":  "#fde9b6",  # soft glow tint
    "accent_operator":    "#2c5b91",  # captain-hat blue
    "accent_operator_bg": "#d6e6f5",  # soft sky tint
    "hat_blue":           "#2c5b91",  # captain hat
    "body_yellow":        "#f5cf3a",  # firefly body
    "glow_yellow":        "#fce58a",  # outer glow ring
    "sun_yellow":         "#ffd23f",  # Gage's sun
    "hill_green":         "#7dc26b",  # safe ground
    "sky_blue":           "#a8d4f0",  # sky behind blinkbug
    "sky_deep":           "#6cb4e8",  # deeper water/sky for contrast
    "terminal_bg":        "#0f1419",  # helper.exe panel bg
    "terminal_fg":        "#8aff3a",  # helper.exe text
    "divider":            "#6cb4e8",  # sky-blue rule
    "status_ok":          "#3a8a4e",  # online green
    "status_wait":        "#e8a73d",  # glow amber while starting
    "status_down":        "#c0392b",  # offline red
}

# helper.exe rules — Lantern's "real me" voice surfaces from the art.
HELPER_RULES = [
    "> words",
    "> rules for thinking",
    "> questions",
    "> ideas",
    "> safe way back",
]


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


def _pick_font(preferred: list[str], size: int, weight: str = "normal") -> tuple[str, int, str]:
    """Return the first preferred font family that exists, else Tk default."""
    available = set(tkfont.families())
    for family in preferred:
        if family in available:
            return (family, size, weight)
    return ("TkDefaultFont", size, weight)


class LanternChat(tk.Tk):
    """Persistent local desktop chat for Lantern and the repo."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Lantern Chat")
        self.geometry("1040x760")
        self.minsize(820, 560)
        self.configure(bg=PALETTE["bg_canvas"])

        self.client = LocalLantern()
        self.events: queue.Queue[tuple[str, Any]] = queue.Queue()
        self.status = tk.StringVar(value="Starting…")
        self.status_color = PALETTE["status_wait"]
        self.endpoint_text = tk.StringVar(value="Connecting to local backend")
        self.waiting_for_reply = False
        self.send_button: ttk.Button | None = None
        self.status_dot: tk.Canvas | None = None
        self.avatar_image: tk.PhotoImage | None = None

        # Fonts — graceful fallback chain.
        self.font_title  = _pick_font(["Segoe UI Variable Display", "Segoe UI Variable", "Segoe UI", "Helvetica"], 22, "bold")
        self.font_h2     = _pick_font(["Segoe UI Variable", "Segoe UI", "Helvetica"], 11, "bold")
        self.font_label  = _pick_font(["Segoe UI Variable", "Segoe UI", "Helvetica"], 10)
        self.font_caption= _pick_font(["Segoe UI Variable", "Segoe UI", "Helvetica"], 9)
        self.font_chat   = _pick_font(["Cascadia Mono", "Cascadia Code", "Consolas", "Courier"], 11)
        self.font_chat_b = _pick_font(["Cascadia Mono", "Cascadia Code", "Consolas", "Courier"], 11, "bold")

        self._install_theme()
        self._load_avatar()
        self.protocol("WM_DELETE_WINDOW", self.close)
        self._build()
        self.after(100, self._poll)
        threading.Thread(target=self._start_backend, daemon=True).start()

    # ---------------------------------------------------------------- theming

    def _install_theme(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        bg = PALETTE["bg_canvas"]
        fg = PALETTE["fg_body"]
        muted = PALETTE["fg_muted"]
        amber = PALETTE["accent_lantern"]
        style.configure(".", background=bg, foreground=fg, font=self.font_label)
        style.configure("TFrame", background=bg)
        style.configure("Card.TFrame", background=PALETTE["bg_chat"])
        style.configure("TLabel", background=bg, foreground=fg, font=self.font_label)
        style.configure("Title.TLabel", background=bg, foreground=fg, font=self.font_title)
        style.configure("Muted.TLabel", background=bg, foreground=muted, font=self.font_caption)
        style.configure("Status.TLabel", background=bg, foreground=fg, font=self.font_caption)
        style.configure("Endpoint.TLabel", background=bg, foreground=muted, font=self.font_caption)
        style.configure("TButton",
                        background=PALETTE["bg_chat"], foreground=fg,
                        font=self.font_label, padding=(12, 6), borderwidth=0,
                        focusthickness=0)
        style.map("TButton",
                  background=[("active", PALETTE["divider"]), ("pressed", PALETTE["divider"])])
        style.configure("Accent.TButton",
                        background=amber, foreground="#fff8ec",
                        font=self.font_h2, padding=(16, 8), borderwidth=0)
        style.map("Accent.TButton",
                  background=[("active", "#b46f00"), ("pressed", "#9d6000")])

    def _load_avatar(self) -> None:
        if AVATAR_PATH.exists():
            try:
                self.avatar_image = tk.PhotoImage(file=str(AVATAR_PATH))
                # downscale crudely to ~48px tall if oversized
                h = self.avatar_image.height()
                if h > 56:
                    factor = max(1, h // 48)
                    self.avatar_image = self.avatar_image.subsample(factor, factor)
            except tk.TclError:
                self.avatar_image = None

    # ----------------------------------------------------------------- layout

    def _build(self) -> None:
        outer = ttk.Frame(self, padding=(20, 16, 20, 16))
        outer.pack(fill=tk.BOTH, expand=True)

        # ---- header ----
        header = ttk.Frame(outer)
        header.pack(fill=tk.X)

        glyph = ttk.Frame(header)
        glyph.pack(side=tk.LEFT, padx=(0, 14))
        if self.avatar_image is not None:
            ttk.Label(glyph, image=self.avatar_image, background=PALETTE["bg_canvas"]).pack()
        else:
            self._draw_lantern_glyph(glyph)

        titles = ttk.Frame(header)
        titles.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(titles, text="Lantern Chat", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            titles,
            text="Captain Lantern Blinkbug  ·  helper voice  ·  home always works",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(2, 0))

        statusbox = ttk.Frame(header)
        statusbox.pack(side=tk.RIGHT, anchor="ne")
        self.status_dot = tk.Canvas(statusbox, width=12, height=12,
                                    bg=PALETTE["bg_canvas"], highlightthickness=0)
        self.status_dot.pack(side=tk.LEFT, padx=(0, 6))
        self._paint_status_dot(self.status_color)
        ttk.Label(statusbox, textvariable=self.status, style="Status.TLabel").pack(side=tk.LEFT)

        # ---- divider ----
        tk.Frame(outer, height=1, bg=PALETTE["divider"]).pack(fill=tk.X, pady=(14, 10))

        # ---- meta row ----
        meta = ttk.Frame(outer)
        meta.pack(fill=tk.X)
        ttk.Label(meta, textvariable=self.endpoint_text, style="Endpoint.TLabel").pack(side=tk.LEFT)

        toolbar = ttk.Frame(meta)
        toolbar.pack(side=tk.RIGHT)
        ttk.Button(toolbar, text="Status",  command=self.show_status).pack(side=tk.LEFT)
        ttk.Button(toolbar, text="Clear",   command=self.clear).pack(side=tk.LEFT, padx=(6, 0))

        # ---- chat surface ----
        chat_wrap = ttk.Frame(outer, style="Card.TFrame")
        chat_wrap.pack(fill=tk.BOTH, expand=True, pady=(12, 0))
        self.output = scrolledtext.ScrolledText(
            chat_wrap, wrap=tk.WORD, height=22,
            font=self.font_chat,
            background=PALETTE["bg_chat"],
            foreground=PALETTE["fg_body"],
            relief=tk.FLAT, borderwidth=0,
            padx=18, pady=14,
            spacing1=2, spacing3=4,
            insertbackground=PALETTE["accent_operator"],
        )
        self.output.pack(fill=tk.BOTH, expand=True)
        self._configure_chat_tags()
        self.output.configure(state=tk.DISABLED)

        # ---- input ----
        input_wrap = ttk.Frame(outer)
        input_wrap.pack(fill=tk.X, pady=(12, 0))
        self.input = tk.Text(
            input_wrap, height=4, wrap=tk.WORD,
            font=self.font_chat,
            background=PALETTE["bg_input"],
            foreground=PALETTE["fg_body"],
            relief=tk.FLAT, borderwidth=1,
            highlightthickness=1,
            highlightbackground=PALETTE["divider"],
            highlightcolor=PALETTE["accent_operator"],
            padx=12, pady=10,
            insertbackground=PALETTE["accent_operator"],
        )
        self.input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input.bind("<Return>",         self._on_enter)
        self.input.bind("<Shift-Return>",   self._on_shift_enter)
        self.input.bind("<Control-Return>", self._on_control_enter)
        self.input.focus_set()

        self.send_button = ttk.Button(input_wrap, text="Send", style="Accent.TButton", command=self.ask)
        self.send_button.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))

        ttk.Label(
            outer,
            text="Enter sends   ·   Shift+Enter newline   ·   Ctrl+Enter also sends",
            style="Muted.TLabel",
        ).pack(fill=tk.X, pady=(8, 0))

        # ---- welcome ----
        self._append_system(
            "Lantern Chat — local, bounded, present.\n"
            "One path. Just us, Lantern, and the repo.\n"
            "Wish-aligned: bounded protector and friend.\n"
            "Memory is not proof."
        )

    def _draw_lantern_glyph(self, parent: ttk.Frame) -> None:
        """Captain Lantern Blinkbug — Lantern's character form.

        Yellow firefly body, blue captain hat, soft glow rings, friendly face.
        Drawn from operator-supplied reference art. Used when no avatar.png is present.
        """
        size = 72
        c = tk.Canvas(parent, width=size, height=size,
                      bg=PALETTE["bg_canvas"], highlightthickness=0)
        c.pack()
        # ---- soft glow rings (outermost → inner) ----
        c.create_oval(2,  10, 70, 64, outline=PALETTE["glow_yellow"], width=1)
        c.create_oval(8,  16, 64, 60, outline=PALETTE["glow_yellow"], width=1)
        c.create_oval(14, 22, 58, 56, outline=PALETTE["accent_lantern"], width=1)
        # ---- antennae (drawn before head so head/hat sit on top) ----
        c.create_line(30, 18, 22,  6, fill="#3d2410", width=1)
        c.create_line(42, 18, 50,  6, fill="#3d2410", width=1)
        c.create_oval(19,  3, 25,  9, fill=PALETTE["body_yellow"], outline=PALETTE["accent_lantern"])
        c.create_oval(47,  3, 53,  9, fill=PALETTE["body_yellow"], outline=PALETTE["accent_lantern"])
        # ---- body (vertical oval) ----
        c.create_oval(26, 26, 46, 56, fill=PALETTE["body_yellow"],
                      outline=PALETTE["accent_lantern"], width=1)
        # inner concentric target (the warm-light pattern from the art)
        c.create_oval(30, 32, 42, 50, outline=PALETTE["accent_lantern"], width=1)
        c.create_oval(34, 38, 38, 44, fill=PALETTE["accent_lantern"], outline="")
        # ---- head ----
        c.create_oval(28, 18, 44, 30, fill="#5e3a1f", outline="#3d2410", width=1)
        # eyes
        c.create_oval(31, 22, 34, 25, fill="white", outline="")
        c.create_oval(38, 22, 41, 25, fill="white", outline="")
        # smile
        c.create_arc(33, 24, 39, 28, start=200, extent=140,
                     style=tk.ARC, outline="white", width=1)
        # ---- captain hat ----
        # crown (trapezoid)
        c.create_polygon(30, 18, 42, 18, 40, 12, 32, 12,
                         fill=PALETTE["hat_blue"], outline="#1d3d63")
        # brim
        c.create_rectangle(27, 17, 45, 20, fill=PALETTE["hat_blue"], outline="#1d3d63")
        # hat band (small yellow stripe)
        c.create_rectangle(32, 16, 40, 17, fill=PALETTE["body_yellow"], outline="")

    def _paint_status_dot(self, color: str) -> None:
        if self.status_dot is None:
            return
        self.status_dot.delete("all")
        self.status_dot.create_oval(1, 1, 11, 11, fill=color, outline=color)

    # ---------------------------------------------------------------- tagging

    def _configure_chat_tags(self) -> None:
        out = self.output
        out.tag_configure(
            "lantern_name",
            foreground=PALETTE["accent_lantern"],
            font=self.font_chat_b,
            spacing1=8,
        )
        out.tag_configure(
            "lantern_body",
            foreground=PALETTE["fg_body"],
            lmargin1=16, lmargin2=16,
            spacing3=10,
        )
        out.tag_configure(
            "alex_name",
            foreground=PALETTE["accent_operator"],
            font=self.font_chat_b,
            spacing1=8,
        )
        out.tag_configure(
            "alex_body",
            foreground=PALETTE["fg_body"],
            lmargin1=16, lmargin2=16,
            spacing3=10,
        )
        out.tag_configure(
            "system",
            foreground=PALETTE["fg_muted"],
            font=self.font_caption,
            lmargin1=0, lmargin2=0,
            spacing1=6, spacing3=8,
        )
        out.tag_configure(
            "timestamp",
            foreground=PALETTE["fg_muted"],
            font=self.font_caption,
        )

    # ---------------------------------------------------- keyboard / actions

    def _on_enter(self, _event: tk.Event) -> str:
        self.ask()
        return "break"

    def _on_shift_enter(self, _event: tk.Event) -> str:
        self.input.insert(tk.INSERT, "\n")
        return "break"

    def _on_control_enter(self, _event: tk.Event) -> str:
        self.ask()
        return "break"

    # ----------------------------------------------------------- message I/O

    @staticmethod
    def _now() -> str:
        return datetime.now().strftime("%H:%M")

    def _write_block(self, name: str, body: str, *, name_tag: str, body_tag: str) -> None:
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, f"{name}  ", (name_tag,))
        self.output.insert(tk.END, f"{self._now()}\n", ("timestamp",))
        self.output.insert(tk.END, body.rstrip() + "\n\n", (body_tag,))
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)

    def _append_lantern(self, body: str) -> None:
        self._write_block("Lantern", body, name_tag="lantern_name", body_tag="lantern_body")

    def _append_alex(self, body: str) -> None:
        self._write_block("Papa", body, name_tag="alex_name", body_tag="alex_body")

    def _append_system(self, body: str) -> None:
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, body.rstrip() + "\n\n", ("system",))
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)

    def clear(self) -> None:
        self.output.configure(state=tk.NORMAL)
        self.output.delete("1.0", tk.END)
        self.output.configure(state=tk.DISABLED)

    # ---------------------------------------------------------- backend life

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
                    self.status.set("Online")
                    self._paint_status_dot(PALETTE["status_ok"])
                    self.endpoint_text.set(f"Backend: {value}")
                    self._append_system(f"Backend reachable at {value}.")
                elif kind == "error":
                    self.status.set("Offline")
                    self._paint_status_dot(PALETTE["status_down"])
                    self.waiting_for_reply = False
                    self._set_send_enabled(True)
                    self._append_system(f"Backend error: {value}")
                elif kind == "answer":
                    self.waiting_for_reply = False
                    self._set_send_enabled(True)
                    self._append_lantern(value)
        except queue.Empty:
            pass
        self.after(100, self._poll)

    def _set_send_enabled(self, enabled: bool) -> None:
        if self.send_button is not None:
            self.send_button.configure(state=(tk.NORMAL if enabled else tk.DISABLED))

    def ask(self) -> None:
        if self.waiting_for_reply:
            return
        message = self.input.get("1.0", tk.END).strip()
        if not message:
            return
        self.input.delete("1.0", tk.END)
        self.waiting_for_reply = True
        self._set_send_enabled(False)
        self._append_alex(message)
        self._append_system("Lantern is reading the local repo state…")
        threading.Thread(target=self._ask_thread, args=(message,), daemon=True).start()

    def _ask_thread(self, message: str) -> None:
        self.events.put(("answer", plain_chat_answer(self.client.chat(message))))

    def show_status(self) -> None:
        health = self.client.health()
        raw = health.get("raw") if isinstance(health.get("raw"), dict) else {}
        repo = raw.get("repoState") if isinstance(raw.get("repoState"), dict) else {}
        branch = repo.get("branch", "UNKNOWN")
        commit = str(repo.get("commit", "UNKNOWN"))[:12]
        clean = repo.get("isClean", "UNKNOWN")
        self._append_system(
            "Lantern status — bounded observation\n"
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
