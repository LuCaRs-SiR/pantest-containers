<script lang="ts">
  import { api } from '$lib/api';

  let prompt = $state('');
  let messages = $state<{ user: string; ai: string }[]>([
    {
      user: 'Analiza projektu...',
      ai: 'Wykryto zagrożenia opóźnienia:\n• Zadanie #12 jest zależne od zasobów zajętych przez zespół B\n• Zalecane: przesunięcie terminu o 2 dni lub przydzielenie dodatkowego dewelopera'
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
      messages = [...messages, { user: userPrompt, ai: res.response ?? '' }];
    } catch (err: any) {
      messages = [...messages, { user: userPrompt, ai: `Error: ${err.message}` }];
    } finally {
      loading = false;
    }
  }
</script>

<div class="assistant neon-card glass">
  <h3 class="assistant-title">Asystent Projektowy AI</h3>
  <div class="messages">
    {#each messages as m}
      <div class="bubble user">{m.user}</div>
      <div class="bubble ai">{m.ai}</div>
    {/each}
  </div>
  <textarea bind:value={prompt} placeholder="Zapytaj asystenta AI..."></textarea>
  <button class="neon-glow" onclick={send} disabled={loading}>
    {loading ? '...' : 'Wyślij'}
  </button>
</div>

<style>
  .assistant {
    display: flex;
    flex-direction: column;
    gap: 15px;
    padding: 20px;
  }

  .assistant-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 16px;
    color: var(--text-main);
  }

  .messages {
    display: flex;
    flex-direction: column;
    gap: 10px;
    max-height: 200px;
    overflow-y: auto;
  }

  .bubble {
    padding: 12px;
    border-radius: var(--radius);
    font-family: 'Rajdhani', sans-serif;
    font-size: 14px;
    white-space: pre-wrap;
  }

  .user {
    align-self: flex-end;
    background: rgba(0, 229, 255, 0.15);
    border-right: 3px solid var(--accent-cyan);
  }

  .ai {
    align-self: flex-start;
    background: rgba(255, 0, 170, 0.1);
    border-left: 3px solid var(--accent-magenta);
  }

  textarea {
    min-height: 60px;
  }
</style>
