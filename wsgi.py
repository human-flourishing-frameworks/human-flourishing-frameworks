#!/usr/bin/env python3
"""
WSGI entry point for Heroku
Gunicorn will use this to run the Flask app
"""

from dashboard_app import app

if __name__ == "__main__":
    app.run()
