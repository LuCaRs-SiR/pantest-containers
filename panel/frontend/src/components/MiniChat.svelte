<script lang="ts">
  import { api } from '$lib/api';
  import Button from './Button.svelte';
  import Input from './Input.svelte';

  let prompt = $state('');
  let messages = $state<{ user: string; ai: string }[]>([
    {
      user: 'Analyze scan results for vulnerabilities...',
      ai: 'Critical findings detected:\n• Open SSH port 22 on target.com\n• Outdated Apache 2.4.41 with known CVEs'
    }
  ]);
  let loading = $state(false);

  async function send() {
    if (!prompt.trim() || loading) return;
    const userPrompt = prompt;
    prompt = '';
    loading = true;
    try {
      const res = await api<{ response: string }>('/api/ai', 'POST', { model: 'qwen2.5:14b-instruct', prompt: userPrompt });
      messages = [...messages, { user: userPrompt, ai: res.response ?? '(brak odpowiedzi)' }];
    } catch (err: any) {
      messages = [...messages, { user: userPrompt, ai: `Error: ${err.message}` }];
    } finally {
      loading = false;
    }
  }
</script>

<div class="mini-chat glow-card">
  <h3 class="section-title">AI Assistant</h3>
  <div class="messages cockpit-scrollbar">
    {#each messages as m}
      <div class="bubble user">{m.user}</div>
      <div class="bubble ai">{m.ai}</div>
    {/each}
  </div>
  <div class="flex gap-2 mt-3">
    <Input bind:value={prompt} placeholder="Zadaj pytanie AI" />
    <Button onclick={send} disabled={loading}>{loading ? '…' : 'Wyślij'}</Button>
  </div>
</div>

<style>
  .mini-chat {
    @apply p-4 h-full flex flex-col;
  }
  .section-title {
    @apply text-lg font-bold text-cockpit-text mb-3;
  }
  .messages {
    @apply flex-1 overflow-y-auto bg-cockpit-terminal/50 rounded-lg p-3 text-sm;
  }
  .bubble {
    @apply p-2 rounded-lg mb-2;
  }
  .user {
    @apply bg-cockpit-accent/10 text-cockpit-accent border-r-2 border-cockpit-accent;
  }
  .ai {
    @apply bg-cockpit-panel-light text-cockpit-text border-l-2 border-cockpit-pink whitespace-pre-wrap;
  }
</style>
