<script lang="ts">
  import { askAI } from '$lib/services';

  let prompt = $state('');
  let messages = $state<{ user: string; ai: string }[]>([]);
  let loading = $state(false);

  async function send() {
    if (!prompt.trim() || loading) return;
    const userPrompt = prompt;
    prompt = '';
    loading = true;
    try {
      const res = await askAI(userPrompt);
      messages = [...messages, { user: userPrompt, ai: res.response ?? '' }];
    } catch (err: any) {
      messages = [...messages, { user: userPrompt, ai: `Error: ${err.message}` }];
    } finally {
      loading = false;
    }
  }
</script>

<div class="chat neon-card glass">
  {#each messages as m}
    <div class="bubble user neon-border">{m.user}</div>
    <div class="bubble ai neon-border">{m.ai}</div>
  {/each}

  <textarea bind:value={prompt} placeholder="Zadaj pytanie AI..."></textarea>
  <button class="neon-glow" onclick={send} disabled={loading}>
    {loading ? '...' : 'Wyślij'}
  </button>
</div>

<style>
  .chat {
    display: flex;
    flex-direction: column;
    gap: 15px;
    font-family: 'Orbitron', sans-serif;
  }

  .bubble {
    padding: 12px;
    border-radius: var(--radius);
    max-width: 80%;
  }

  .user {
    align-self: flex-end;
    background: #00AFFF22;
  }

  .ai {
    background: #222;
    border-left: 3px solid var(--accent-cyan);
  }

  textarea {
    background: var(--bg-panel);
    color: var(--text-main);
    border: 1px solid var(--accent-cyan);
    border-radius: var(--radius);
    padding: 12px;
    font-family: 'Share Tech Mono', monospace;
    min-height: 80px;
  }
</style>
