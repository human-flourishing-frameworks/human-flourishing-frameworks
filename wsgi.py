"""
WSGI entry point for the Autonomous Agent System.
Used by gunicorn in production: gunicorn wsgi:app
"""
from app_autonomous import app

if __name__ == "__main__":
    app.run()
