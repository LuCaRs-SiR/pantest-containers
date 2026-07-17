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
}

export interface StatusResponse {
  ai_gateway: Record<string, unknown>;
  backend: string;
  containers: Record<string, ContainerStatus>;
}

export interface ReportsResponse {
  reports: Array<Record<string, unknown>>;
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
