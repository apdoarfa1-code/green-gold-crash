# Green Gold Cloud

An advanced engineering framework designed for monitoring, time-series analysis, and provably fair auditing of crash games (Aviator).

## Local Development & Running

To run the system locally, open **two separate terminal windows (or tabs)** in `/home/apdo/Desktop/كراش`:

### Terminal 1: Start FastAPI Backend
```bash
source .venv/bin/activate
cd backend
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Terminal 2: Start Streamlit Dashboard
```bash
source .venv/bin/activate
streamlit run dashboard/streamlit_app.py --server.port=8501
```

Then open your browser at: `http://localhost:8501`

---

## Deployment Architecture

1. **Database**: Supabase (PostgreSQL with Realtime enabled).
2. **Backend**: Render (FastAPI supporting WebSockets and long-running connections).
3. **Dashboard**: Streamlit Cloud.
4. **Data Collection**: GitHub Actions Cron Job (`collect.yml`).
