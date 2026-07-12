import { browser } from '$app/environment';
import { API_URL } from './config';

export async function api<T = unknown>(
  path: string,
  method: 'GET' | 'POST' = 'GET',
  body?: Record<string, unknown>
): Promise<T> {
  if (!browser) {
    throw new Error('api() should only be called in the browser');
  }

  const init: RequestInit = {
    method,
    headers: { 'Content-Type': 'application/json' }
  };

  if (body && method === 'POST') {
    init.body = JSON.stringify(body);
  }

  const res = await fetch(`${API_URL}${path}`, init);

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API ${method} ${path} failed: ${res.status} ${res.statusText} ${text}`);
  }

  return res.json();
}
