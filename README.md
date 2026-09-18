# HowBusyToday

Multi-tenant crowd prediction app for regional theme parks, waterparks, and zoos.

**Stack:** Django + Django REST Framework (backend) · React + Vite + Tailwind CSS (frontend)

## Project layout

```
backend/          Django project (howbusytoday) + parks app
frontend/         Vite React SPA
```

## Backend setup

Requires Python 3.11+.

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

API base: `http://127.0.0.1:8000/api/`

| Endpoint | Description |
|---|---|
| `GET /api/parks/` | List parks (`?category=waterpark\|theme_park\|zoo`, `?search=`) |
| `GET /api/parks/<slug>/forecast/` | Park + next 7 days crowd & weather |
| `/admin/` | Django admin |

CORS is enabled for `http://localhost:5173`.

## Frontend setup

```bash
cd frontend
npm install
npm run dev
```

If `npm install` fails with `UNABLE_TO_VERIFY_LEAF_SIGNATURE`, the repo includes `frontend/.npmrc` (`strict-ssl=false`) to work around local SSL inspection (antivirus / proxy). Prefer fixing your system CA trust when you can.

App: `http://localhost:5173`

Vite proxies `/api` to the Django server, so no extra env vars are required for local development.

## Prediction heuristic

`parks/services/prediction.py` scores crowds 1–10 from:

- Weekend / statutory holiday calendar factors (raises score)
- Temperature and rain chance, weighted by park category (waterparks are most weather-sensitive)

`seed_demo_data` generates sample parks and 14 days of weather/predictions using that service.
