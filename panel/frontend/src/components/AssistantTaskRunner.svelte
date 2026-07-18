<script lang="ts">
  import { runAssistantTask } from '$lib/services';
  import type { AssistantRunResponse } from '$lib/types';

  let task = $state('');
  let target = $state('');
  let domain = $state('');
  let loading = $state(false);
  let error = $state('');
  let result = $state<AssistantRunResponse | null>(null);

  async function run() {
    if (!task.trim() || loading) return;

    loading = true;
    error = '';
    result = null;

    try {
      result = await runAssistantTask(task.trim(), target.trim(), domain.trim());
    } catch (err: any) {
      error = err.message ?? 'Nie udało się uruchomić orkiestracji.';
    } finally {
      loading = false;
    }
  }
</script>

<section class="assistant glass neon-border">
  <h2>Asystent Orkiestracji Pentestu</h2>
  <p class="desc">
    Opisz cel zadania, a asystent dobierze narzędzia, uruchomi je we właściwej kolejności
    i zapisze raport w zakładce Status i Raporty.
  </p>

  <div class="form">
    <textarea
      bind:value={task}
      placeholder="Np. Zrób szybki rekonesans domeny example.com i zweryfikuj usługi na 192.168.1.20"
    />
    <div class="row">
      <input bind:value={target} placeholder="Target (opcjonalnie), np. 192.168.1.20" />
      <input bind:value={domain} placeholder="Domain (opcjonalnie), np. example.com" />
    </div>
    <button class="neon-glow" onclick={run} disabled={loading || !task.trim()}>
      {loading ? 'Uruchamianie...' : 'Uruchom zadanie'}
    </button>
  </div>

  {#if error}
    <p class="error">{error}</p>
  {/if}

  {#if result}
    <div class="result">
      <h3>Wynik wykonania</h3>
      <p><strong>Status:</strong> {result.report.summary.status}</p>
      <p>
        <strong>Profile:</strong>
        {(result.report.selected_profiles ?? []).join(', ') || 'brak'}
      </p>
      <p><strong>Kroki:</strong> {result.report.summary.total_steps}</p>
      <p><strong>Błędy:</strong> {result.report.summary.failed_steps}</p>
      <p>
        <strong>Dane wejściowe (resolved):</strong>
        target={result.report.input_resolved?.target ?? '-'},
        domain={result.report.input_resolved?.domain ?? '-'}
      </p>
      <p><strong>Wniosek:</strong> {result.report.summary.conclusion}</p>
      <p>
        <strong>Raport:</strong>
        <a href="/reports">otwórz zakładkę raportów</a>
      </p>

      <div class="steps">
        {#each result.report.steps as step}
          <div class="step">
            <div class="step-head">
              <strong>{step.order}. {step.label}</strong>
              <span class={step.status === 'ok' ? 'ok' : 'bad'}>{step.status}</span>
            </div>
            <div class="meta">tool={step.tool} exit_code={step.exit_code}</div>
          </div>
        {/each}
      </div>
    </div>
  {/if}
</section>

<style>
  .assistant {
    padding: 16px;
    margin-bottom: 20px;
  }

  h2 {
    margin: 0 0 8px;
    font-family: 'Orbitron', sans-serif;
  }

  .desc {
    margin: 0 0 12px;
    color: var(--text-secondary);
  }

  .form {
    display: grid;
    gap: 10px;
  }

  textarea {
    min-height: 90px;
  }

  .row {
    display: grid;
    gap: 10px;
    grid-template-columns: 1fr 1fr;
  }

  .error {
    color: #ff6b6b;
    margin-top: 10px;
  }

  .result {
    margin-top: 14px;
    padding-top: 10px;
    border-top: 1px solid rgba(0, 229, 255, 0.2);
  }

  .steps {
    margin-top: 10px;
    display: grid;
    gap: 8px;
  }

  .step {
    padding: 10px;
    border: 1px solid rgba(0, 229, 255, 0.15);
    border-radius: 8px;
  }

  .step-head {
    display: flex;
    justify-content: space-between;
    gap: 10px;
  }

  .meta {
    font-family: 'Share Tech Mono', monospace;
    color: var(--text-secondary);
    margin-top: 4px;
    font-size: 12px;
  }

  .ok {
    color: #45d483;
  }

  .bad {
    color: #ff6b6b;
  }

  @media (max-width: 900px) {
    .row {
      grid-template-columns: 1fr;
    }
  }
</style>
