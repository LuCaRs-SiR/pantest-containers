import { browser } from '$app/environment';

const API_URL = import.meta.env.VITE_PUBLIC_API_URL ?? 'http://localhost:8001';

export async function api<T = unknown>(
	path: string,
	method: 'GET' | 'POST' = 'GET',
	body?: Record<string, unknown>
): Promise<T> {
	if (!browser) {
		throw new Error('api() powinno być wołane tylko w przeglądarce');
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
