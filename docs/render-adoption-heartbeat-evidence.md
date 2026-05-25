# Render adoption heartbeat evidence

Date: 2026-05-16

Render starts the service with:

```text
gunicorn safe_app:app --bind 0.0.0.0:$PORT --log-file -
```

The previous adoption startup path lived only inside `app.py`'s
`if __name__ == "__main__"` block. That block runs for `python app.py`, but it
does not run when Gunicorn imports `safe_app:app`.

The fix exposes `bootstrap_adoption_heartbeat()` in `app.py` and calls it from
`safe_app.py`, so the Render/Gunicorn path now registers the local node and
starts the existing adoption heartbeat helper exactly once per WSGI process.

Validation:

```text
python -m unittest tests.test_app_runtime_safety
```

The targeted test proves:

- importing `app` alone does not call `register_node` or `start_heartbeat`;
- importing `safe_app`, the Gunicorn entrypoint, calls both with the configured
  Render node identity.
