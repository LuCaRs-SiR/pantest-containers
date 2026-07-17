import { api } from '$lib/api';
import type { ToolOutput, ReportsResponse, StatusResponse } from '$lib/types';

export function nmapScan(target: string) {
  return api<ToolOutput>('/api/nmap', 'POST', { target });
}

export function reconScan(domain: string) {
  return api<ToolOutput>('/api/recon', 'POST', { domain });
}

export function hackAgent(target: string) {
  return api<ToolOutput>('/api/hackagent', 'POST', { target });
}

export function autopentestX(target: string) {
  return api<ToolOutput>('/api/autopentestx', 'POST', { target });
}

export function inspector(target: string) {
  return api<ToolOutput>('/api/inspector', 'POST', { target });
}

export function burp(command: string) {
  return api<ToolOutput>('/api/burp', 'POST', { command });
}

export function kali(command: string) {
  return api<ToolOutput>('/api/kali', 'POST', { command });
}

export function getStatus() {
  return api<StatusResponse>('/api/status', 'GET');
}

export function getReports() {
  return api<ReportsResponse>('/api/reports', 'GET');
}
