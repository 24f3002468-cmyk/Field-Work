import json
from datetime import datetime, timedelta
import os

START_DATE = datetime(2026, 9, 10)
TOTAL_DAYS = 200

MILESTONES = [
    {
        "id": 1,
        "name": "DSA Arrays & Hashing Mastery",
        "target_day": 14,
        "target_date": (START_DATE + timedelta(days=13)).strftime("%Y-%m-%d"),
        "description": "Complete core array manipulation and hashing patterns.",
        "critical": False,
        "part": 1,
        "phase": "DSA Foundation"
    },
    {
        "id": 2,
        "name": "Python & NumPy/Pandas Baseline",
        "target_day": 30,
        "target_date": (START_DATE + timedelta(days=29)).strftime("%Y-%m-%d"),
        "description": "Solid understanding of vectorized operations and Pandas DataFrames.",
        "critical": False,
        "part": 1,
        "phase": "ML Foundation"
    },
    {
        "id": 3,
        "name": "SQL Milestone 1 (20 Hours)",
        "target_day": 45,
        "target_date": (START_DATE + timedelta(days=44)).strftime("%Y-%m-%d"),
        "description": "Complete 20 hours of focused SQL practice (Part 1 target: 40-50h).",
        "critical": True,
        "part": 1,
        "phase": "SQL Focus"
    },
    {
        "id": 4,
        "name": "Project 1 Baseline Model Complete",
        "target_day": 60,
        "target_date": (START_DATE + timedelta(days=59)).strftime("%Y-%m-%d"),
        "description": "TF-IDF + Cosine similarity baseline functional.",
        "critical": True,
        "part": 1,
        "phase": "Project 1"
    },
    {
        "id": 5,
        "name": "Project 1 API & SHAP Integration",
        "target_day": 85,
        "target_date": (START_DATE + timedelta(days=84)).strftime("%Y-%m-%d"),
        "description": "FastAPI backend with model explainability ready.",
        "critical": True,
        "part": 1,
        "phase": "Project 1"
    },
    {
        "id": 6,
        "name": "PROJECT 1 SHIPPING DEADLINE",
        "target_day": 104,
        "target_date": "2026-12-22",
        "description": "Resume Intelligence Platform live, deployed, documented, and clean GitHub.",
        "critical": True,
        "part": 1,
        "phase": "Project 1"
    },
    {
        "id": 7,
        "name": "Part 1 Foundation Complete & SQL Target Achieved",
        "target_day": 113,
        "target_date": "2026-12-31",
        "description": "40-50h SQL complete, DSA foundation built, IITM term requirements fulfilled.",
        "critical": True,
        "part": 1,
        "phase": "Part 1 Review"
    },
    {
        "id": 8,
        "name": "LeetCode Medium 25 Problems Milestone",
        "target_day": 140,
        "target_date": (START_DATE + timedelta(days=139)).strftime("%Y-%m-%d"),
        "description": "25 Medium-level problems mastered with review notes.",
        "critical": False,
        "part": 2,
        "phase": "LeetCode Medium"
    },
    {
        "id": 9,
        "name": "System Design Fundamentals Core",
        "target_day": 160,
        "target_date": (START_DATE + timedelta(days=159)).strftime("%Y-%m-%d"),
        "description": "Functional mastery of distributed storage, caching, load balancing, and API design.",
        "critical": True,
        "part": 2,
        "phase": "System Design"
    },
    {
        "id": 10,
        "name": "LeetCode Medium Target (50-60 Solved)",
        "target_day": 180,
        "target_date": (START_DATE + timedelta(days=179)).strftime("%Y-%m-%d"),
        "description": "Reach 50-60 solid Medium-level problems target.",
        "critical": True,
        "part": 2,
        "phase": "Interview Execution"
    },
    {
        "id": 11,
        "name": "FINAL GOAL: Offer Conversion & Plan Completion",
        "target_day": 200,
        "target_date": "2027-04-30",
        "description": "Complete 200-day execution plan and secure ML / Software Engineering offer.",
        "critical": True,
        "part": 2,
        "phase": "Offer Conversion"
    }
]

PROJECT_STAGES = [
    {"id": 1, "name": "Data collection", "description": "Gather resume and job description datasets."},
    {"id": 2, "name": "EDA", "description": "Exploratory Data Analysis and text cleaning."},
    {"id": 3, "name": "TF-IDF + cosine baseline", "description": "Implement baseline text matching score."},
    {"id": 4, "name": "ML model", "description": "Train scikit-learn / XGBoost ranking models."},
    {"id": 5, "name": "Evaluation", "description": "Evaluate precision, recall, and ranking metrics."},
    {"id": 6, "name": "Feature engineering", "description": "Extract skill embeddings and experience features."},
    {"id": 7, "name": "NER", "description": "Named Entity Recognition for entities like skills and titles."},
    {"id": 8, "name": "Explainability / SHAP", "description": "SHAP feature importance visualization."},
    {"id": 9, "name": "API", "description": "FastAPI service for resume scoring."},
    {"id": 10, "name": "Deployment", "description": "Deploy API to cloud / Docker container."},
    {"id": 11, "name": "Streamlit/demo", "description": "Build interactive Streamlit / React web UI demo."},
    {"id": 12, "name": "Documentation", "description": "Comprehensive README, architecture diagrams, and API docs."},
    {"id": 13, "name": "GitHub cleanup", "description": "Clean commit history, remove secrets, format code."},
    {"id": 14, "name": "Final testing", "description": "End-to-end integration and API load testing."},
    {"id": 15, "name": "Shipping", "description": "Mark project as officially shipped by Dec 22, 2026."}
]

PROJECT_CHECKLIST_ITEMS = [
    {"id": 1, "title": "Live API exists", "verified": False},
    {"id": 2, "title": "GitHub repository exists & clean", "verified": False},
    {"id": 3, "title": "Code is complete & clean", "verified": False},
    {"id": 4, "title": "README complete with architecture diagram", "verified": False},
    {"id": 5, "title": "Demo UI (Streamlit/React) functional", "verified": False},
    {"id": 6, "title": "Deployment confirmed (cloud/Docker)", "verified": False},
    {"id": 7, "title": "API load & integration tested", "verified": False},
    {"id": 8, "title": "Final verification passed", "verified": False},
    {"id": 9, "title": "Baseline model vs ML model comparison documented", "verified": False},
    {"id": 10, "title": "Explainability (SHAP) endpoint working", "verified": False},
    {"id": 11, "title": "No hardcoded secret keys or mock credentials", "verified": False}
]

def generate_planner():
    days = []
    current_date = START_DATE
    
    for day_num in range(1, TOTAL_DAYS + 1):
        date_str = current_date.strftime("%Y-%m-%d")
        weekday_str = current_date.strftime("%A")
        
        is_part1 = current_date <= datetime(2026, 12, 31)
        part = 1 if is_part1 else 2
        
        if part == 1:
            if day_num <= 25:
                phase = "DSA & Foundations"
                sub_phase = "Arrays, Strings, Python Basics"
                primary_tech = "Python / DSA"
            elif day_num <= 50:
                phase = "ML Math & SQL Focus"
                sub_phase = "Linear Algebra, Calculus, SQL Joins & Aggregations"
                primary_tech = "SQL / ML Math"
            elif day_num <= 85:
                phase = "ML Core & PyTorch / Project 1"
                sub_phase = "Scikit-Learn, PyTorch Tensors, Project Baseline & API"
                primary_tech = "PyTorch / Project 1"
            else:
                phase = "Project Shipping & Part 1 Consolidation"
                sub_phase = "Project 1 Shipping (Dec 22 Deadline), SQL 40-50h Target, IITM"
                primary_tech = "Project 1 / SQL"
        else:
            if day_num <= 140:
                phase = "LeetCode Medium & System Design"
                sub_phase = "Trees, Graphs, System Design Building Blocks"
                primary_tech = "DSA / System Design"
            elif day_num <= 175:
                phase = "Interview Execution & Behavioral"
                sub_phase = "Mock Interviews, Resume Stories, Networking"
                primary_tech = "Interview Prep / Applications"
            else:
                phase = "Applications & Offer Conversion"
                sub_phase = "Targeted Applications, Final Interviews, Offer Negotiations"
                primary_tech = "Offer Conversion"
                
        day_tasks = [
            {
                "id": f"D{day_num}-T1",
                "day_number": day_num,
                "category": "DSA",
                "name": "Morning DSA / LeetCode",
                "description": f"Solve & review 1 DSA problem (Day {day_num}).",
                "planned_start": "07:00",
                "planned_end": "07:45",
                "planned_minutes": 45,
                "priority": "HIGH",
                "is_critical": True
            },
            {
                "id": f"D{day_num}-T2",
                "day_number": day_num,
                "category": "SQL" if (part == 1 and day_num % 2 == 1) else ("System Design" if part == 2 else primary_tech),
                "name": "Rotating Technical Subject",
                "description": "Core concepts and problem solving.",
                "planned_start": "07:45",
                "planned_end": "08:30",
                "planned_minutes": 45,
                "priority": "MEDIUM",
                "is_critical": False
            },
            {
                "id": f"D{day_num}-T3",
                "day_number": day_num,
                "category": "ML" if part == 1 else "Interview Preparation",
                "name": "Study Block 1 — Technical Deep Dive",
                "description": f"Focus area: {phase}.",
                "planned_start": "17:00",
                "planned_end": "18:30",
                "planned_minutes": 90,
                "priority": "HIGH",
                "is_critical": True
            },
            {
                "id": f"D{day_num}-T4",
                "day_number": day_num,
                "category": "IITM",
                "name": "Study Block 2 — IITM Academic Work",
                "description": "Assignments, quizzes, lectures, and Placement Points activities.",
                "planned_start": "18:30",
                "planned_end": "19:30",
                "planned_minutes": 60,
                "priority": "HIGH",
                "is_critical": True
            },
            {
                "id": f"D{day_num}-T5",
                "day_number": day_num,
                "category": "Projects" if (part == 1 or day_num <= 130) else "Applications",
                "name": "Study Block 3 — Project 1 Execution / Applications",
                "description": "Hands-on implementation, coding, and application submission.",
                "planned_start": "20:30",
                "planned_end": "22:00",
                "planned_minutes": 90,
                "priority": "HIGH",
                "is_critical": True
            },
            {
                "id": f"D{day_num}-T6",
                "day_number": day_num,
                "category": "Daily Review",
                "name": "Daily Scorecard & Reflection",
                "description": "Log actual time, complete scorecard, set tomorrow's top priority.",
                "planned_start": "22:00",
                "planned_end": "22:15",
                "planned_minutes": 15,
                "priority": "MEDIUM",
                "is_critical": False
            }
        ]

        matching_milestone = next((m for m in MILESTONES if m["target_day"] == day_num or m["target_date"] == date_str), None)

        day_data = {
            "day_number": day_num,
            "date": date_str,
            "weekday": weekday_str,
            "part": part,
            "phase": phase,
            "sub_phase": sub_phase,
            "primary_technology": primary_tech,
            "total_planned_minutes": sum(t["planned_minutes"] for t in day_tasks),
            "tasks": day_tasks,
            "milestone": matching_milestone["name"] if matching_milestone else None
        }
        days.append(day_data)
        current_date += timedelta(days=1)

    dataset = {
        "start_date": START_DATE.strftime("%Y-%m-%d"),
        "end_date": (START_DATE + timedelta(days=TOTAL_DAYS-1)).strftime("%Y-%m-%d"),
        "total_days": TOTAL_DAYS,
        "milestones": MILESTONES,
        "project_stages": PROJECT_STAGES,
        "project_checklist": PROJECT_CHECKLIST_ITEMS,
        "days": days
    }

    os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "planner_data.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)
        
    print(f"Successfully generated planner_data.json with {len(days)} days and {len(MILESTONES)} milestones.")

if __name__ == "__main__":
    generate_planner()
