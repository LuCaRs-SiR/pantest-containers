export interface AIResponse {
  response: string;
}

export interface ToolOutput {
  output: string;
  exit_code: number;
}

export interface ContainerStatus {
  exists: boolean;
  status: string;
  running: boolean;
  started_at?: string;
  finished_at?: string;
  state_status?: string;
  error?: string;
  restart_count?: number;
  health_status?: string;
}

export interface StatusResponse {
  ai_gateway: Record<string, unknown>;
  backend: string;
  containers: Record<string, ContainerStatus>;
}

export interface ReportsResponse {
  reports: ReportListItem[];
}

export interface ReportListItem {
  id: string;
  task: string;
  created_at: string;
  status: 'ok' | 'partial' | 'failed' | 'unknown';
  steps_total: number;
  steps_failed: number;
}

export interface AssistantStep {
  order: number;
  tool: string;
  label: string;
  container: string;
  command: string[];
  status?: 'ok' | 'error';
  exit_code?: number;
  output?: string;
}

export interface ProfessionalFinding {
  id: string;
  title: string;
  severity: 'critical' | 'high' | 'medium' | 'low' | 'informational';
  category: string;
  affected_asset: string;
  evidence: string;
  impact: string;
  recommendation: string;
}

export interface ProfessionalReport {
  meta: {
    report_type: string;
    version: string;
    prepared_at: string;
    language: string;
    classification: string;
  };
  engagement: {
    objective: string;
    scope: {
      target?: string | null;
      domain?: string | null;
      profiles?: string[];
    };
    authorization_notice: string;
  };
  executive_summary: {
    overall_risk: 'critical' | 'high' | 'medium' | 'low';
    assessment_status: 'ok' | 'partial' | 'failed' | 'unknown';
    key_observations: string[];
    conclusion: string;
  };
  methodology: {
    standard_reference: string[];
    phases: string[];
    tools_used: string[];
  };
  findings: ProfessionalFinding[];
  recommendations: {
    immediate: string[];
    short_term: string[];
    long_term: string[];
  };
  limitations: string[];
  appendix: {
    step_trace: Array<{
      order?: number;
      label?: string;
      tool?: string;
      status?: string;
      exit_code?: number;
      evidence_excerpt?: string;
    }>;
  };
  markdown?: string;
}

export interface AssistantReport {
  id: string;
  created_at: string;
  task: string;
  selected_profiles?: string[];
  input: {
    target?: string | null;
    domain?: string | null;
  };
  input_resolved?: {
    target?: string | null;
    domain?: string | null;
  };
  status: 'ok' | 'partial' | 'failed' | 'unknown';
  summary: {
    status: 'ok' | 'partial' | 'failed' | 'unknown';
    total_steps: number;
    failed_steps: number;
    conclusion: string;
  };
  plan: AssistantStep[];
  steps: AssistantStep[];
  professional_report?: ProfessionalReport;
}

export interface AssistantRunResponse {
  report: AssistantReport;
  report_meta: {
    id: string;
    path: string;
    created_at: string;
    task: string;
    status: string;
  };
}

export interface PriorityTask {
  name: string;
  priority: 'critical' | 'high' | 'medium' | 'low';
}

export interface TeamMember {
  name: string;
  value: number;
}

export interface LogEntry {
  time: string;
  event: string;
}
