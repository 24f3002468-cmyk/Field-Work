# 200-Day ML Systems Execution Dashboard

A production-quality personal execution operating system built to operationalize the **200-Day ML Systems Execution Plan** (September 10, 2026 → April 30, 2027).

---

## 1. Overview & Architecture

The dashboard serves as an immutable execution manager, daily operating system, data integrity validator, and progress tracker without altering the planner's original structure, deadlines, or objectives.

### Key Components
- **Immutable Source-of-Truth Engine**: Deterministically seeds 200 execution days mapped to calendar dates, schedule time-blocks, and milestones (Project 1 shipping on Dec 22, 2026, Offer Goal on Apr 30, 2027).
- **Today Engine & Schedule Guard**: Respects fixed daily schedule (Morning routine 5-6 AM, Workout 6-7 AM, Morning DSA 7-7:45 AM, Technical 7:45-8:30 AM, **College 9 AM - 4 PM Non-Study Window**, Post-college Study Blocks 5:00-6:30 PM, 6:30-7:30 PM, 8:30-10:00 PM, Nightly Scorecard 10:00-10:15 PM).
- **Backlog & Non-Destructive Catch-Up Engine**: Detects overdue tasks and hours, presenting recovery recommendations without modifying original planner tasks.
- **Trackers**:
  - **DSA**: 50–60 Medium problem target tracking + problem log.
  - **SQL**: Part 1 40–50h focus tracker.
  - **Project 1**: 15 stages of Resume Intelligence Platform + 11-item ship checklist.
  - **IITM & Placement Points**: Dedicated academic & eligible points tracker.
  - **Applications**: Interview pipeline & offer converter.
- **Automated Verification**: `python verify.py` runs database checks, 200-day date math verification, Pytest test suite, and direct DB integrity audit.

---

## 2. Technology Stack

- **Backend**: FastAPI (Python 3.11+), SQLAlchemy ORM, Pydantic v2, Pytest, JWT security.
- **Database**: PostgreSQL / SQLite (`sqlite:///./ml_dashboard.db` default zero-config).
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Zustand state store, Axios API client with local offline queue & autosave sync.
- **Orchestration**: Docker & Docker Compose.

---

## 3. Quick Start & Setup

### Option A: Local Development

1. **Install Backend Dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. **Generate Seed Planner Data**:
   ```bash
   python planner/seed_planner.py
   ```

3. **Run Verification Suite**:
   ```bash
   python verify.py
   ```

4. **Start Backend API Server**:
   ```bash
   python -m uvicorn app.main:app --app-dir backend --reload --port 8000
   ```
   *FastAPI Swagger documentation will be live at `http://127.0.0.1:8000/docs`.*

5. **Start Frontend Dev Server**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

---

### Option B: Docker Compose

```bash
docker compose up --build
```
- Frontend: `http://localhost:3000`
- Backend API & Swagger: `http://localhost:8000/docs`

---

## 4. Verification Suite (`python verify.py`)

Run the full verification suite anytime:
```bash
python verify.py
```

Output:
```text
========================================
200-DAY DASHBOARD VERIFICATION SUITE
========================================

Planner Data             : PASS
Backend & API Tests      : PASS
Database Integrity       : PASS
----------------------------------------
RESULT: SYSTEM VERIFIED (ALL TESTS PASSED)
========================================
```

---

## 5. Directory Structure

```text
ml-execution-dashboard/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routers (v1)
│   │   ├── core/         # Config, security, DB session, Asia/Kolkata timezone
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Today, Backlog, Scoring, Verification, Backup services
│   │   └── main.py       # FastAPI app & startup seeder
│   └── tests/            # Pytest test suite
├── frontend/
│   ├── src/
│   │   ├── components/   # Navbar, WhatShouldIDoNow widget
│   │   ├── pages/        # Dashboard, Today, Planner, DSA, Project, SQL, IITM, Applications, Verification
│   │   ├── store/        # Zustand state store with offline sync
│   │   └── types/        # TypeScript interfaces
├── planner/
│   ├── seed_planner.py   # Seed engine
│   └── planner_data.json # 200-day execution calendar JSON
├── verify.py             # System verification runner
├── docker-compose.yml
├── Dockerfile
└── README.md
```
