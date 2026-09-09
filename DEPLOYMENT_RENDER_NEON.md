# Deploying ML Systems Execution Dashboard on Render & Neon

This step-by-step guide explains how to deploy your **200-Day ML Systems Execution Dashboard** with **Neon Serverless PostgreSQL** and **Render**.

---

## 1. Setup Neon PostgreSQL Database

1. Go to [Neon.tech](https://neon.tech) and log in.
2. Click **New Project** and name it `ml-execution-dashboard`.
3. Copy your **Connection String** from the Neon dashboard. It looks like:
   ```text
   postgresql://user:password@ep-xyz.singapore.aws.neon.tech/neondb?sslmode=require
   ```
4. Save this string — you will set it as `DATABASE_URL` in Render.

---

## 2. Deploy on Render (Using `render.yaml` Blueprint)

### Option A: One-Click Blueprint Deployment (Recommended)

1. Push your repository to GitHub / GitLab.
2. Log in to [Render.com](https://render.com).
3. Click **New +** → **Blueprint**.
4. Select your repository. Render will automatically detect `render.yaml`.
5. Enter the `DATABASE_URL` environment variable when prompted, pasting your Neon connection string.
6. Click **Apply**. Render will automatically provision and deploy:
   - `ml-dashboard-backend` (FastAPI Web Service)
   - `ml-dashboard-frontend` (React Static Site)

---

### Option B: Manual Web Service Setup on Render

#### 1. Backend Web Service (`ml-dashboard-backend`)
- **Type**: Web Service
- **Environment**: Python 3
- **Build Command**: `pip install -r backend/requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Environment Variables**:
  - `DATABASE_URL`: *your Neon PostgreSQL connection string*
  - `PYTHONPATH`: `./backend`
  - `TIMEZONE`: `Asia/Kolkata`
  - `SECRET_KEY`: *generate a secure random string*

#### 2. Frontend Static Site (`ml-dashboard-frontend`)
- **Type**: Static Site
- **Build Command**: `cd frontend && npm install && npm run build`
- **Publish Directory**: `frontend/dist`
- **Redirects/Rewrites**: Add a rewrite rule:
  - Source: `/*`
  - Destination: `/index.html`
  - Action: `Rewrite`
- **Environment Variables**:
  - `VITE_API_BASE_URL`: `https://ml-dashboard-backend.onrender.com/api/v1` (replace with your actual backend URL)

---

## 3. Database Seeding & Verification

When the backend service starts on Render for the first time, `app/main.py` automatically detects if the database is empty and populates all **200 execution days**, milestones, project stages, and default tasks into your Neon PostgreSQL database.

To manually test database integrity on Neon, run the verification script pointing to your Neon database:

```bash
DATABASE_URL="postgresql://user:password@ep-xyz.singapore.aws.neon.tech/neondb?sslmode=require" python verify.py
```

Expected Output:
```text
========================================
VERIFICATION RESULTS SUMMARY
========================================
Planner Data             : PASS
Backend & API Tests      : PASS
Database Integrity       : PASS
----------------------------------------
RESULT: SYSTEM VERIFIED (ALL TESTS PASSED)
========================================
```
