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

<div class="mini-chat glow-card glow-card-pink">
  <div class="header">
    <div class="header-line header-line-pink"></div>
    <h3 class="section-title font-display">AI Assistant</h3>
  </div>
  <div class="messages cockpit-scrollbar">
    {#each messages as m}
      <div class="bubble user animate-fade-in-up">{m.user}</div>
      <div class="bubble ai animate-fade-in-up font-mono">{m.ai}</div>
    {/each}
  </div>
  <div class="flex gap-2 mt-3">
    <Input bind:value={prompt} placeholder="Zadaj pytanie AI" />
    <Button variant="primary" onclick={send} disabled={loading}>{loading ? '…' : 'Wyślij'}</Button>
  </div>
</div>

<style>
  .mini-chat {
    @apply p-4 h-full flex flex-col;
  }
  .header {
    @apply flex items-center gap-3 mb-3;
  }
  .header-line {
    @apply w-1 h-5 rounded-full;
  }
  .header-line-pink {
    @apply bg-cockpit-pink;
    box-shadow: 0 0 8px var(--cockpit-pink-glow);
  }
  .section-title {
    @apply text-lg font-bold text-cockpit-text tracking-wide;
  }
  .messages {
    @apply flex-1 overflow-y-auto p-3 rounded-lg text-sm;
    background: rgba(0, 0, 0, 0.45);
    border: 1px solid rgba(255, 0, 160, 0.15);
  }
  .bubble {
    @apply p-2.5 rounded-lg mb-2;
  }
  .user {
    @apply bg-cockpit-accent/10 text-cockpit-accent border-r-2 border-cockpit-accent ml-4;
  }
  .ai {
    @apply bg-cockpit-panel-light/80 text-cockpit-text border-l-2 border-cockpit-pink whitespace-pre-wrap mr-4;
  }
</style>
