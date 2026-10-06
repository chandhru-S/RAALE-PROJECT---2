export type ReadinessStatus = 'READY' | 'AT_RISK' | 'NOT_READY' | 'DATA_INCOMPLETE';

export interface TheatreSchedule {
  id: number;
  session_id: string;
  surgery_id: string;
  theatre_id: string;
  department: string;
  procedure_type: string;
  scheduled_start: string;
  scheduled_end: string;
  actual_start?: string;
  actual_end?: string;
  priority: string;
  previous_session_overrun: string;
}

export interface TheatreSummary {
  theatre_id: string;
  current_surgery_id: string | null;
  department: string;
  procedure: string;
  status: ReadinessStatus;
  readiness_score: number;
  confidence_score: number;
  active_alert: string | null;
}

export interface SystemSummary {
  total_theatres: number;
  ready: number;
  at_risk: number;
  not_ready: number;
  data_incomplete: number;
  avg_idle_minutes: number;
}

export interface ReadinessAssessment {
  surgery_id: string;
  checkpoint: string;
  overall_status: ReadinessStatus;
  readiness_score: number;
  confidence_score: number;
  patient_score: number;
  staff_score: number;
  equipment_score: number;
  supply_score: number;
  theatre_score: number;
  blocking_issues: string;
  recommended_actions: string;
  assessed_at: string;
  theatre_id?: string;
  department?: string;
  procedure?: string;
  patient_status?: string;
  staff_status?: string;
  equipment_status?: string;
  supply_status?: string;
}

export interface AlertItem {
  id: number;
  alert_id: string;
  severity: 'HIGH' | 'MEDIUM' | 'LOW';
  theatre_id: string;
  surgery_id: string;
  issue: string;
  confidence_score: number;
  recommended_action: string;
  status: 'ACTIVE' | 'ACKNOWLEDGED' | 'RESOLVED';
  created_at: string;
}

export interface ExperimentMetrics {
  total_sessions: number;
  baseline_avg_idle_mins: number;
  baseline_median_idle_mins: number;
  baseline_total_idle_mins: number;
  prototype_avg_idle_mins: number;
  prototype_median_idle_mins: number;
  prototype_total_idle_mins: number;
  idle_time_reduction_pct: number;
  early_detection_rate: number;
  alert_precision: number;
  false_positive_rate: number;
  false_negative_rate: number;
  target_achieved: boolean;
}

export interface SimulationResult {
  success: boolean;
  test_name: string;
  surgery_id: string;
  theatre_id: string;
  overall_status: ReadinessStatus;
  readiness_score: number;
  confidence_score: number;
  blocking_issues: string;
  recommended_actions: string;
  alert_created: string | null;
}
