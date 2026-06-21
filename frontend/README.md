Frontend static prototype

This folder contains a lightweight static Single-Page App (SPA) prototype that calls the backend API endpoints.

Files:
- `static/index.html` — main UI
- `static/app.js` — minimal frontend logic (login, employees, prediction)
- `static/styles.css` — basic styles

Run locally:

1. Serve the `frontend/static` folder with a simple static server, for example:

```bash
# Python 3
python -m http.server 4200 --directory frontend/static

# Or using Node (if installed):
npx http-server frontend/static -p 4200
```

2. Open http://localhost:4200 in your browser. Update `API_BASE` in `app.js` to point to the backend if different.

This is a prototype — if you want a full Angular scaffold, I can generate an `ng` project next.
