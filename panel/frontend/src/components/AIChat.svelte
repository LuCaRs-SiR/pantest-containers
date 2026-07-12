<script lang="ts">
  import { api } from '$lib/api';
  import Button from './Button.svelte';
  import Input from './Input.svelte';

  let prompt = $state('');
  let messages = $state<{ user: string; ai: string }[]>([]);
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

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  }
</script>

<div class="chat">
  <div class="messages cockpit-scrollbar">
    {#each messages as m}
      <div class="bubble user">{m.user}</div>
      <div class="bubble ai">{m.ai}</div>
    {/each}
  </div>

  <div class="flex gap-2">
    <Input bind:value={prompt} placeholder="Zadaj pytanie AI" onkeydown={handleKeydown} />
    <Button onclick={send} disabled={loading}>{loading ? '…' : 'Wyślij'}</Button>
  </div>
</div>

<style>
  .chat {
    @apply flex flex-col gap-4 h-full;
  }
  .messages {
    @apply flex-1 overflow-y-auto bg-cockpit-panel rounded-xl p-4 border border-white/5;
  }
  .bubble {
    @apply p-3 rounded-lg mb-2 max-w-3xl;
  }
  .user {
    @apply bg-cockpit-accent/10 self-end text-right border-r-4 border-cockpit-accent;
  }
  .ai {
    @apply bg-cockpit-terminal border-l-4 border-cockpit-accent text-cockpit-text whitespace-pre-wrap;
  }
</style>
