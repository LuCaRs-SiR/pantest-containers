import { api } from '$lib/api';
import { DEFAULT_AI_MODEL } from '$lib/config';
import type { AIResponse } from '$lib/types';

export function askAI(prompt: string, model: string = DEFAULT_AI_MODEL) {
  return api<AIResponse>('/api/ai', 'POST', { model, prompt });
}
