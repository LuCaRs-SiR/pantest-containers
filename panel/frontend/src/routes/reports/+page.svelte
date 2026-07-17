<script lang="ts">
  import { onMount } from 'svelte';
  import { getStatus } from '$lib/services';
  import type { StatusResponse } from '$lib/types';

  let status = $state<StatusResponse | null>(null);
  let loading = $state(true);
  let error = $state('');

  const issues = $derived.by(() => {
    if (!status) return [];
    return Object.entries(status.containers)
      .map(([name, item]) => ({ name, item }))
      .filter(
        ({ item }) =>
          !item.exists ||
          !item.running ||
          item.status === 'restarting' ||
          (item.restart_count ?? 0) > 0 ||
          Boolean(item.error)
      );
  });

  const healthy = $derived.by(() => {
    if (!status) return 0;
    return Object.values(status.containers).filter((x) => x.running).length;
  });

  const total = $derived.by(() => {
    if (!status) return 0;
    return Object.keys(status.containers).length;
  });

  async function refresh() {
    loading = true;
    error = '';
    try {
      status = await getStatus();
    } catch (err: any) {
      error = err.message ?? 'Nie udało się pobrać statusu.';
    } finally {
      loading = false;
    }
  }

  onMount(refresh);
</script>

<h1 class="text-3xl font-black text-cockpit-accent mb-6">Status Kontenerów</h1>

<button class="neon-glow mb-4" onclick={refresh} disabled={loading}>
  {loading ? 'Odświeżanie...' : 'Odśwież'}
</button>

{#if error}
  <p class="error">{error}</p>
{/if}

{#if status}
  <div class="summary glass neon-border">
    <div><strong>Backend:</strong> {status.backend}</div>
    <div><strong>Kontenery Running:</strong> {healthy}/{total}</div>
    <div><strong>AI Gateway:</strong> {status.ai_gateway.error ? status.ai_gateway.error : 'ok'}</div>
  </div>

  <div class="summary glass neon-border issues">
    <h2>Diagnostyka</h2>
    {#if issues.length === 0}
      <p>Brak wykrytych problemów z kontenerami.</p>
    {:else}
      {#each issues as row}
        <div class="issue-row">
          <strong>{row.name}</strong>
          <span>status={row.item.status}</span>
          <span>restarty={row.item.restart_count ?? 0}</span>
          {#if row.item.error}
            <span class="issue-error">{row.item.error}</span>
          {/if}
        </div>
      {/each}
    {/if}
  </div>

  <div class="grid">
    {#each Object.entries(status.containers) as [name, item]}
      <div class="card glass neon-border">
        <h3>{name}</h3>
        <p><strong>Status:</strong> {item.status}</p>
        <p><strong>State:</strong> {item.state_status ?? 'n/a'}</p>
        <p><strong>Running:</strong> {item.running ? 'tak' : 'nie'}</p>
        <p><strong>Exists:</strong> {item.exists ? 'tak' : 'nie'}</p>
        <p><strong>Restarts:</strong> {item.restart_count ?? 0}</p>
        <p><strong>Health:</strong> {item.health_status ?? 'n/a'}</p>
      </div>
    {/each}
  </div>
{/if}

<style>
  .summary {
    padding: 16px;
    margin-bottom: 16px;
    display: grid;
    gap: 8px;
  }

  .issues {
    border-color: rgba(255, 140, 0, 0.4);
  }

  .issues h2 {
    margin: 0;
    font-family: 'Orbitron', sans-serif;
    font-size: 16px;
  }

  .issue-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
    font-size: 14px;
  }

  .issue-error {
    color: #ff6b6b;
    max-width: 100%;
    overflow-wrap: anywhere;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 12px;
  }

  .card {
    padding: 14px;
  }

  h3 {
    margin-bottom: 8px;
    font-family: 'Orbitron', sans-serif;
  }

  p {
    margin: 4px 0;
  }

  .error {
    color: #ff6b6b;
    margin-bottom: 12px;
  }
</style>
