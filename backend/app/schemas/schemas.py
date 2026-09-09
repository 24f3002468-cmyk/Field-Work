from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from datetime import datetime

# Auth Schemas
class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool

    class Config:
        from_attributes = True

# Task & Planner Schemas
class PlannerTaskSchema(BaseModel):
    id: str
    day_number: int
    category: str
    name: str
    description: Optional[str] = None
    planned_start: Optional[str] = None
    planned_end: Optional[str] = None
    planned_minutes: int
    priority: str
    is_critical: bool

    class Config:
        from_attributes = True

class TaskCompletionCreate(BaseModel):
    task_id: str
    date: str
    actual_minutes: int = Field(ge=0)
    status: str
    completion_percentage: float = Field(ge=0.0, le=100.0)
    notes: Optional[str] = None

class TaskCompletionResponse(BaseModel):
    id: int
    task_id: str
    date: str
    actual_minutes: int
    status: str
    completion_percentage: float
    notes: Optional[str] = None
    updated_at: datetime

    class Config:
        from_attributes = True

class PlannerDaySchema(BaseModel):
    day_number: int
    date: str
    weekday: str
    part: int
    phase: str
    sub_phase: Optional[str] = None
    primary_technology: Optional[str] = None
    total_planned_minutes: int
    milestone_name: Optional[str] = None
    tasks: List[PlannerTaskSchema] = []

    class Config:
        from_attributes = True

# Daily Log Schemas
class DailyLogCreate(BaseModel):
    date: str
    day_number: int
    score: float = Field(ge=0.0, le=10.0)
    workout_completed: bool = False
    sleep_hours: float = 0.0
    focus_hours: float = 0.0
    blockers: Optional[str] = None
    tomorrow_priority: Optional[str] = None
    notes: Optional[str] = None

class DailyLogResponse(DailyLogCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Milestone Schemas
class MilestoneResponse(BaseModel):
    id: int
    name: str
    target_day: int
    target_date: str
    description: Optional[str] = None
    status: str
    critical: bool
    part: int
    phase: Optional[str] = None
    completed_date: Optional[str] = None

    class Config:
        from_attributes = True

class MilestoneStatusUpdate(BaseModel):
    status: str
    completed_date: Optional[str] = None

# DSA Schemas
class DSAProblemCreate(BaseModel):
    title: str
    difficulty: str
    topic: str
    platform: str = "LeetCode"
    status: str = "solved"
    solve_time_minutes: int = 0
    first_attempt_success: bool = True
    needed_hints: bool = False
    repeated_problem: bool = False
    review_completed: bool = False
    notes: Optional[str] = None
    solved_date: str

class DSAProblemResponse(DSAProblemCreate):
    id: int

    class Config:
        from_attributes = True

# Project Schemas
class ProjectStageResponse(BaseModel):
    id: int
    stage_number: int
    name: str
    description: Optional[str] = None
    status: str
    completed_date: Optional[str] = None

    class Config:
        from_attributes = True

class ProjectChecklistResponse(BaseModel):
    id: int
    title: str
    verified: bool
    notes: Optional[str] = None

    class Config:
        from_attributes = True

# IITM Schemas
class IITMTaskCreate(BaseModel):
    course_code: str
    title: str
    type: str
    due_date: str
    submission_status: str = "Pending"
    score: Optional[float] = None
    completed: bool = False

class IITMTaskResponse(IITMTaskCreate):
    id: int

    class Config:
        from_attributes = True

class PlacementPointCreate(BaseModel):
    activity_name: str
    category: str
    points: int = 1
    status: str = "Pending"
    date: str
    notes: Optional[str] = None

class PlacementPointResponse(PlacementPointCreate):
    id: int

    class Config:
        from_attributes = True

# System Design Schemas
class SystemDesignTopicCreate(BaseModel):
    topic: str
    category: str
    confidence: str = "Medium"
    mock_completed: bool = False
    notes: Optional[str] = None

class SystemDesignTopicResponse(SystemDesignTopicCreate):
    id: int

    class Config:
        from_attributes = True

# Application & Networking Schemas
class ApplicationCreate(BaseModel):
    company: str
    role: str
    location: Optional[str] = None
    application_date: str
    source: Optional[str] = None
    referral: bool = False
    status: str = "TO_APPLY"
    resume_version: Optional[str] = None
    interview_stage: Optional[str] = None
    next_action: Optional[str] = None
    next_action_date: Optional[str] = None
    notes: Optional[str] = None

class ApplicationResponse(ApplicationCreate):
    id: int

    class Config:
        from_attributes = True

class NetworkingContactCreate(BaseModel):
    name: str
    company: str
    role: Optional[str] = None
    contact_date: str
    channel: Optional[str] = None
    response: bool = False
    follow_up_date: Optional[str] = None
    referral_offered: bool = False
    notes: Optional[str] = None

class NetworkingContactResponse(NetworkingContactCreate):
    id: int

    class Config:
        from_attributes = True

class OfferCreate(BaseModel):
    company: str
    role: str
    base_salary: Optional[float] = None
    total_compensation: Optional[float] = None
    location: Optional[str] = None
    offer_date: str
    deadline: Optional[str] = None
    status: str = "RECEIVED"
    notes: Optional[str] = None

class OfferResponse(OfferCreate):
    id: int

    class Config:
        from_attributes = True

class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None

class StandardErrorResponse(BaseModel):
    error: ErrorDetail
