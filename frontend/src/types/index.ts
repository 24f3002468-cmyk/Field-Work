export interface Task {
  id: string;
  day_number?: number;
  category: string;
  name: string;
  description?: string;
  planned_start?: string;
  planned_end?: string;
  planned_minutes: number;
  actual_minutes: number;
  status: 'NOT_STARTED' | 'IN_PROGRESS' | 'COMPLETED' | 'PARTIALLY_COMPLETED' | 'SKIPPED' | 'MISSED' | 'BLOCKED';
  completion_percentage: number;
  is_critical: boolean;
  priority: string;
  notes?: string;
}

export interface TodayData {
  today_date: string;
  current_time: string;
  day_number: number;
  part: number;
  phase: string;
  sub_phase: string;
  primary_technology: string;
  total_tasks: number;
  completed_tasks: number;
  total_planned_minutes: number;
  actual_minutes: number;
  tasks: Task[];
  active_task_now: Task | null;
  milestone: string | null;
}

export interface Milestone {
  id: number;
  name: string;
  target_day: number;
  target_date: string;
  description?: string;
  status: 'pending' | 'in-progress' | 'completed' | 'missed';
  critical: boolean;
  part: number;
  phase?: string;
  completed_date?: string;
}

export interface BacklogSummary {
  overdue_count: number;
  overdue_hours: number;
  overdue_tasks: Task[];
  critical_overdue_tasks: Task[];
  backlog_by_category: Record<string, number>;
  catch_up_recommendation: string;
}

export interface ProjectStatus {
  deadline: string;
  current_stage: string;
  current_stage_number: number;
  stages_completed: number;
  total_stages: number;
  checklist_verified: number;
  total_checklist: number;
  ship_status: 'NOT SHIPPED' | 'READY TO SHIP' | 'SHIPPED';
}

export interface DSASummary {
  total_recorded: number;
  easy_solved: number;
  medium_solved: number;
  medium_minimum_target: number;
  medium_stretch_target: number;
  hard_solved: number;
  medium_progress_pct: number;
}

export interface PlacementPointsSummary {
  required_points: number;
  earned_points: number;
  pending_points: number;
  remaining_points: number;
  certificates: number;
  problem_solving: number;
  other_activities: number;
  submission_status: string;
}

export interface VerificationReport {
  status: 'PASS' | 'FAIL';
  days_count: number;
  tasks_count: number;
  milestones_count: number;
  issues_found: number;
  issues: string[];
  timestamp: string;
}

export interface ApplicationResponse {
  id: number;
  company: string;
  role: string;
  application_date: string;
  status: string;
  notes?: string;
  job_url?: string;
  created_at?: string;
  updated_at?: string;
}

export interface ProjectStageResponse {
  id: number;
  stage_number: number;
  name: string;
  description?: string;
  status: string;
}

export interface ProjectChecklistResponse {
  id: number;
  title: string;
  verified: boolean;
  category?: string;
}
