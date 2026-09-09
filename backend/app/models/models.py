from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class PlannerDay(Base):
    __tablename__ = "planner_days"

    id = Column(Integer, primary_key=True, index=True)
    day_number = Column(Integer, unique=True, index=True, nullable=False)
    date = Column(String, unique=True, index=True, nullable=False)  # YYYY-MM-DD
    weekday = Column(String, nullable=False)
    part = Column(Integer, nullable=False)  # 1 or 2
    phase = Column(String, nullable=False)
    sub_phase = Column(String, nullable=True)
    primary_technology = Column(String, nullable=True)
    total_planned_minutes = Column(Integer, default=0)
    milestone_name = Column(String, nullable=True)

    tasks = relationship("PlannerTask", back_populates="day", cascade="all, delete-orphan")

class PlannerTask(Base):
    __tablename__ = "planner_tasks"

    id = Column(String, primary_key=True, index=True)  # e.g., D1-T1
    day_number = Column(Integer, ForeignKey("planner_days.day_number"), nullable=False)
    category = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    planned_start = Column(String, nullable=True)  # HH:MM
    planned_end = Column(String, nullable=True)    # HH:MM
    planned_minutes = Column(Integer, nullable=False, default=0)
    priority = Column(String, default="MEDIUM")
    is_critical = Column(Boolean, default=False)

    day = relationship("PlannerDay", back_populates="tasks")
    completions = relationship("TaskCompletion", back_populates="task", cascade="all, delete-orphan")

class TaskCompletion(Base):
    __tablename__ = "task_completions"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, ForeignKey("planner_tasks.id"), nullable=False)
    date = Column(String, index=True, nullable=False)  # YYYY-MM-DD
    actual_minutes = Column(Integer, default=0)
    status = Column(String, default="NOT_STARTED")  # NOT_STARTED, IN_PROGRESS, COMPLETED, PARTIALLY_COMPLETED, SKIPPED, MISSED, BLOCKED
    completion_percentage = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    task = relationship("PlannerTask", back_populates="completions")

class DailyLog(Base):
    __tablename__ = "daily_logs"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, unique=True, index=True, nullable=False)  # YYYY-MM-DD
    day_number = Column(Integer, nullable=False)
    score = Column(Float, default=0.0)
    workout_completed = Column(Boolean, default=False)
    sleep_hours = Column(Float, default=0.0)
    focus_hours = Column(Float, default=0.0)
    blockers = Column(Text, nullable=True)
    tomorrow_priority = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class WeeklyScorecard(Base):
    __tablename__ = "weekly_scorecards"

    id = Column(Integer, primary_key=True, index=True)
    week_number = Column(Integer, unique=True, index=True, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    target_hours = Column(Float, default=0.0)
    actual_hours = Column(Float, default=0.0)
    completion_percentage = Column(Float, default=0.0)
    dsa_count = Column(Integer, default=0)
    ml_hours = Column(Float, default=0.0)
    project_hours = Column(Float, default=0.0)
    sql_hours = Column(Float, default=0.0)
    iitm_hours = Column(Float, default=0.0)
    status = Column(String, default="ON TRACK")  # ON TRACK, BEHIND, CRITICAL
    notes = Column(Text, nullable=True)

class Milestone(Base):
    __tablename__ = "milestones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    target_day = Column(Integer, nullable=False)
    target_date = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="pending")  # pending, in-progress, completed, missed
    critical = Column(Boolean, default=False)
    part = Column(Integer, default=1)
    phase = Column(String, nullable=True)
    completed_date = Column(String, nullable=True)

class DSAProblem(Base):
    __tablename__ = "dsa_problems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)  # Easy, Medium, Hard
    topic = Column(String, nullable=False)
    platform = Column(String, default="LeetCode")
    status = Column(String, default="solved")  # planned, attempted, solved, reviewed, mastered
    solve_time_minutes = Column(Integer, default=0)
    first_attempt_success = Column(Boolean, default=True)
    needed_hints = Column(Boolean, default=False)
    repeated_problem = Column(Boolean, default=False)
    review_completed = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    solved_date = Column(String, nullable=False)

class ProjectStage(Base):
    __tablename__ = "project_stages"

    id = Column(Integer, primary_key=True, index=True)
    stage_number = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="NOT_STARTED")  # NOT_STARTED, IN_PROGRESS, COMPLETED
    completed_date = Column(String, nullable=True)

class ProjectChecklist(Base):
    __tablename__ = "project_checklist"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    verified = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)

class SQLSession(Base):
    __tablename__ = "sql_sessions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    minutes = Column(Integer, default=0)
    problems_solved = Column(Integer, default=0)
    notes = Column(Text, nullable=True)

class IITMCourse(Base):
    __tablename__ = "iitm_courses"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    term = Column(String, nullable=False)

class IITMTask(Base):
    __tablename__ = "iitm_tasks"

    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, nullable=False)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)  # assignment, quiz, exam, academic_task
    due_date = Column(String, nullable=False)
    submission_status = Column(String, default="Pending")  # Pending, Submitted, Graded
    score = Column(Float, nullable=True)
    completed = Column(Boolean, default=False)

class PlacementPoint(Base):
    __tablename__ = "placement_points"

    id = Column(Integer, primary_key=True, index=True)
    activity_name = Column(String, nullable=False)
    category = Column(String, nullable=False)  # Certificate, Problem Solving, Other
    points = Column(Integer, default=1)
    status = Column(String, default="Pending")  # Pending, Submitted, Verified
    date = Column(String, nullable=False)
    notes = Column(Text, nullable=True)

class SystemDesignTopic(Base):
    __tablename__ = "system_design_topics"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=False)
    category = Column(String, nullable=False)
    confidence = Column(String, default="Medium")  # Low, Medium, High
    mock_completed = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    location = Column(String, nullable=True)
    application_date = Column(String, nullable=False)
    source = Column(String, nullable=True)
    referral = Column(Boolean, default=False)
    status = Column(String, default="TO_APPLY")  # TARGET, TO_APPLY, APPLIED, OA, PHONE_SCREEN, TECHNICAL, SYSTEM_DESIGN, BEHAVIORAL, FINAL, OFFER, REJECTED, WITHDRAWN
    resume_version = Column(String, nullable=True)
    interview_stage = Column(String, nullable=True)
    next_action = Column(String, nullable=True)
    next_action_date = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

class NetworkingContact(Base):
    __tablename__ = "networking_contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    company = Column(String, nullable=False)
    role = Column(String, nullable=True)
    contact_date = Column(String, nullable=False)
    channel = Column(String, nullable=True)
    response = Column(Boolean, default=False)
    follow_up_date = Column(String, nullable=True)
    referral_offered = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)

class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    base_salary = Column(Float, nullable=True)
    total_compensation = Column(Float, nullable=True)
    location = Column(String, nullable=True)
    offer_date = Column(String, nullable=False)
    deadline = Column(String, nullable=True)
    status = Column(String, default="RECEIVED")  # RECEIVED, ACCEPTED, DECLINED, EXPIRED
    notes = Column(Text, nullable=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, nullable=True)
    action = Column(String, nullable=False)
    entity = Column(String, nullable=False)
    entity_id = Column(String, nullable=True)
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class BackupRecord(Base):
    __tablename__ = "backups"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="CREATED")  # CREATED, VERIFIED, FAILED
    checksum = Column(String, nullable=True)
