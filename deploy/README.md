# Multi-Platform Deploy — HFF Dashboard

Zero single points of failure. 10 free hosts for the HFF public surface.

## Live Surfaces

| # | Platform | Type | URL | Status |
|---|----------|------|-----|--------|
| 1 | Render | Flask API + Dashboard | https://human-flourishing-frameworks.onrender.com/ | PRIMARY |
| 2 | Netlify | Static (docs hub) | TBD | PENDING |
| 3 | Surge.sh | Static (art + OS) | TBD | PENDING |
| 4 | Vercel | Static | TBD | PENDING |
| 5 | Cloudflare Pages | Static | TBD | PENDING |
| 6 | Heroku | Flask API | TBD | PENDING |
| 7 | Railway | Flask API | TBD | PENDING |
| 8 | GitHub Pages | Static docs | BLOCKED (private repo) | N/A |
| 9 | Fly.io | Flask container | TBD | PENDING |
| 10 | Hugging Face Spaces | Flask app | TBD | PENDING |

## Strategy

- **Flask API hosts** (Render, Heroku, Railway, Fly.io, HF Spaces): full API + dashboard
- **Static hosts** (Netlify, Surge, Vercel, Cloudflare): art panels, OS dashboard, docs hub
- Static hosts serve the HTML pages that can point to any live API backend
